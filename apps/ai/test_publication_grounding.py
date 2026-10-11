"""New publication and cache reuse recheck saved output without changing history."""
from copy import deepcopy
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse

from .grounding import GroundingValidationError
from .jobs import analyse_cluster_task, request_analysis
from .models import AnalysisJob, AnalysisState, Explanation
from .presentation import document_text
from .providers import configuration, reuse_key, PROMPT_VERSION
from .services import (explanation_content, prepare_analysis, publish_explanation,
                       validate_saved_explanation, TEMPLATE_VERSION)
from .tests import AnalysisFixtures


@override_settings(AI_PROVIDER='ollama', AI_MODEL='qwen3:4b', AI_BASE_URL='http://127.0.0.1:11434')
class PublicationGroundingTests(AnalysisFixtures, TestCase):
    def setUp(self):
        self.cluster, _ = self.group()
        self.analysis, _ = prepare_analysis(self.cluster.pk)
        self.initial = AnalysisState.objects.get(cluster=self.cluster).explanation

    def choices(self):
        plan = self.plan(self.analysis)
        identifier = plan['sections'][0]['finding_id']
        plan['narrative'] = {
            'paragraphs': [{'finding_id': identifier, 'variant': 0}],
            'checks': [{'finding_id': identifier, 'variant': 0}],
        }
        return plan

    def saved(self, key, content=None, **fields):
        fields.setdefault('status', 'ready')
        return Explanation.objects.create(analysis=self.analysis, reuse_key=key,
            provider='ollama', model='qwen3:4b', prompt_version=PROMPT_VERSION,
            **(content or explanation_content(self.analysis, self.choices())), **fields)

    def test_current_model_and_sections_only_documents_revalidate_exactly(self):
        for index, plan in enumerate((self.choices(), self.plan(self.analysis))):
            with self.subTest(narrative='narrative' in plan):
                saved = self.saved(f'valid-{index}', explanation_content(self.analysis, plan))
                self.assertEqual(validate_saved_explanation(self.analysis, saved), saved)
                self.assertTrue(publish_explanation(self.analysis, saved))
                self.assertEqual(saved.presentation['document']['score']['value'], 2)
        self.assertEqual(Explanation.objects.get(pk=self.initial.pk).text, self.initial.text)

    def test_publication_rejects_text_document_choice_and_policy_tampering(self):
        original = explanation_content(self.analysis, self.choices())
        cases = []
        text = deepcopy(original)
        text['text'] += '\nThe companies secretly divide procurement markets.'
        cases.append(text)
        narrative = deepcopy(original)
        document = narrative['presentation']['document']
        document['narrative']['paragraphs'][0]['text'] = 'The companies use separate purchasing teams.'
        document['summary'] = document['narrative']['paragraphs'][0]['text']
        narrative['text'] = document_text(document)
        cases.append(narrative)
        choice = deepcopy(original)
        choice['presentation']['narrative']['paragraphs'][0]['variant'] = 99
        cases.append(choice)
        policy = deepcopy(original)
        del policy['presentation']['document']['grounding_policy']
        cases.append(policy)
        for index, content in enumerate(cases):
            with self.subTest(case=index):
                saved = self.saved(f'bad-publication-{index}', content)
                with self.assertRaises(GroundingValidationError):
                    publish_explanation(self.analysis, saved)
                self.assertEqual(AnalysisState.objects.get(cluster=self.cluster).explanation_id, self.initial.pk)

    def test_fallback_requires_exact_template_without_model_narrative(self):
        good = self.saved('valid-fallback', explanation_content(self.analysis), status='fallback')
        self.assertTrue(publish_explanation(self.analysis, good))
        bad = self.saved('invalid-fallback', status='fallback')
        with self.assertRaisesRegex(GroundingValidationError, 'output_saved_template_invalid'):
            publish_explanation(self.analysis, bad)
        content = explanation_content(self.analysis)
        content['text'] += '\nAn invented fallback assertion.'
        bad_text = self.saved('invalid-fallback-text', content, status='fallback')
        with self.assertRaisesRegex(GroundingValidationError, 'output_saved_content_mismatch'):
            publish_explanation(self.analysis, bad_text)

    def test_cached_ready_row_cannot_bypass_generation_guard(self):
        content = explanation_content(self.analysis, self.choices())
        content['text'] += '\nUnsupported cached assertion.'
        cached = self.saved(reuse_key(self.analysis, configuration()), content)
        job = self.request(self.cluster)
        with patch('apps.ai.jobs.generate', side_effect=AssertionError('Cache rejection needs no inference')):
            result = analyse_cluster_task.run(job.pk)
        job.refresh_from_db()
        self.assertEqual(result['status'], 'fallback')
        self.assertEqual(job.error_code, 'output_saved_content_mismatch')
        self.assertNotEqual(job.explanation_id, cached.pk)
        self.assertEqual(job.explanation.text, explanation_content(self.analysis)['text'])
        self.assertEqual(Explanation.objects.get(pk=cached.pk).text, content['text'])

    def test_completed_malformed_cache_creates_new_job_then_reuses_safe_fallback(self):
        content = explanation_content(self.analysis, self.choices())
        content['text'] += '\nUnsupported previously cached assertion.'
        cached = self.saved(reuse_key(self.analysis, configuration()), content)
        old_job = self.request(self.cluster)
        AnalysisJob.objects.filter(pk=old_job.pk).update(
            status='succeeded', analysis=self.analysis, explanation=cached)
        AnalysisState.objects.filter(cluster=self.cluster).update(explanation=cached)
        with self.captureOnCommitCallbacks(execute=False):
            new_job, created = request_analysis(None, self.cluster.pk)
        self.assertTrue(created)
        self.assertNotEqual(new_job.pk, old_job.pk)
        self.assertEqual(AnalysisState.objects.get(cluster=self.cluster).explanation_id, cached.pk)
        with patch('apps.ai.jobs.generate', side_effect=AssertionError('Unsafe cache must fall back')):
            self.assertEqual(analyse_cluster_task.run(new_job.pk)['status'], 'fallback')
        with self.captureOnCommitCallbacks(execute=False):
            reused, created = request_analysis(None, self.cluster.pk)
        self.assertFalse(created)
        self.assertEqual(reused.pk, new_job.pk)
        old_job.refresh_from_db()
        self.assertEqual(old_job.status, 'succeeded')
        self.assertEqual(Explanation.objects.get(pk=cached.pk).text, content['text'])

    def test_cached_wrong_prompt_version_is_not_republished(self):
        cached = Explanation.objects.create(analysis=self.analysis,
            reuse_key=reuse_key(self.analysis, configuration()), provider='ollama', model='qwen3:4b',
            prompt_version='evidence-presentation-5.3', status='ready', text='Preserved historical prose.')
        job = self.request(self.cluster)
        with patch('apps.ai.jobs.generate', side_effect=AssertionError('Wrong cache version needs no inference')):
            result = analyse_cluster_task.run(job.pk)
        job.refresh_from_db()
        self.assertEqual(result['status'], 'fallback')
        self.assertEqual(job.error_code, 'output_saved_version_mismatch')
        self.assertEqual(Explanation.objects.get(pk=cached.pk).text, 'Preserved historical prose.')

    def test_bad_template_cache_falls_back_once_and_reuses_the_safe_result(self):
        content = explanation_content(self.analysis)
        content['text'] += '\nAn unsupported cached template assertion.'
        cached = Explanation.objects.create(analysis=self.analysis, reuse_key='bad-template-cache',
            provider='template', prompt_version=TEMPLATE_VERSION, status='ready', **content)
        job = self.request(self.cluster, use_model=False)
        with patch('apps.ai.jobs.template_for', return_value=cached), patch(
                'apps.ai.jobs.generate', side_effect=AssertionError('Template recovery must not call a model')):
            self.assertEqual(analyse_cluster_task.run(job.pk)['status'], 'fallback')
        with self.captureOnCommitCallbacks(execute=False):
            reused, created = request_analysis(None, self.cluster.pk, use_model=False)
        self.assertFalse(created)
        self.assertEqual(reused.pk, job.pk)
        self.assertEqual(reused.explanation.text, explanation_content(self.analysis)['text'])

    def test_saved_estimate_is_separate_and_matches_its_validated_plan(self):
        plan = self.choices()
        plan['risk_estimate'] = 77
        plan['risk_evidence'] = [plan['sections'][0]['finding_id']]
        content = explanation_content(self.analysis, plan)
        bad = self.saved('estimate-mismatch', content, experimental_score=78,
                         experimental_evidence=plan['risk_evidence'])
        with self.assertRaisesRegex(GroundingValidationError, 'output_saved_estimate_mismatch'):
            publish_explanation(self.analysis, bad)
        good = self.saved('estimate-consistent', content, experimental_score=77,
                          experimental_evidence=plan['risk_evidence'])
        self.assertTrue(publish_explanation(self.analysis, good))
        self.assertEqual(good.presentation['document']['score']['value'], 2)

    def test_legacy_get_preserves_saved_text_without_invoking_publication_guard(self):
        legacy = Explanation.objects.create(analysis=self.analysis, reuse_key='legacy-unchanged',
            provider='ollama', model='historical-synthetic', prompt_version='evidence-presentation-5.3',
            text='Original immutable historical explanation.')
        AnalysisState.objects.filter(cluster=self.cluster).update(explanation=legacy)
        with patch('apps.ai.services.validate_saved_explanation', side_effect=AssertionError('GET must only read saved text')):
            page = self.client.get(reverse('graph:cluster_detail', args=[self.cluster.uuid]))
        self.assertContains(page, legacy.text)
        self.assertEqual(Explanation.objects.get(pk=legacy.pk).text, legacy.text)
