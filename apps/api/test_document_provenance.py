"""Saved wording provenance stays explicit without reconstructing old documents."""
from copy import deepcopy

from django.template.loader import render_to_string
from django.test import SimpleTestCase

from .saved import DocumentSerializer


class DocumentProvenanceTests(SimpleTestCase):
    def document(self):
        return {
            'version': 'readable-explanation-5.2',
            'summary': 'Synthetic saved summary.',
            'findings': [], 'additional_findings': 0,
            'checks': ['Check the recorded source.'],
            'coverage': ['No current arrears check is saved.'],
            'score': {'value': 0, 'items': [], 'meaning': 'Manual review only.'},
            'conclusion': 'The saved data does not establish a violation.',
            'narrative': {
                'paragraphs': [{'text': '<b>Synthetic saved passage.</b>', 'finding_ids': []}],
                'checks': [{'text': 'Check the recorded source.', 'finding_ids': []}],
            },
        }

    def test_serializer_preserves_explicit_saved_grounding_but_never_adds_it_to_legacy(self):
        legacy = self.document()
        original = deepcopy(legacy)
        projected = DocumentSerializer(legacy).data
        self.assertNotIn('grounding_policy', projected)
        self.assertEqual(projected, legacy)
        grounded = deepcopy(legacy)
        grounded.update(version='readable-explanation-5.3', grounding_policy='prepared-claims-1')
        self.assertEqual(DocumentSerializer(grounded).data, grounded)
        self.assertEqual(legacy, original)

    def test_legacy_template_distinguishes_methods_and_escapes_saved_text(self):
        document = self.document()
        original = deepcopy(document)
        legacy = render_to_string('ai/explanation_document.html', {'explanation_document': document})
        self.assertIn('uses an earlier generation method', legacy)
        self.assertNotIn('AI selected and ordered prepared statements', legacy)
        self.assertIn('&lt;b&gt;Synthetic saved passage.&lt;/b&gt;', legacy)
        document.update(version='readable-explanation-5.3', grounding_policy='prepared-claims-1')
        grounded = render_to_string('ai/explanation_document.html', {'explanation_document': document})
        self.assertIn('AI selected and ordered prepared statements', grounded)
        self.assertNotIn('uses an earlier generation method', grounded)
        self.assertIn('&lt;b&gt;Synthetic saved passage.&lt;/b&gt;', grounded)
        self.assertEqual(document['narrative'], original['narrative'])

    def test_template_summary_does_not_claim_ai_selection(self):
        document = self.document()
        del document['narrative']
        result = render_to_string('ai/explanation_document.html', {'explanation_document': document})
        self.assertIn('Synthetic saved summary.', result)
        self.assertNotIn('AI selected and ordered', result)
        self.assertNotIn('earlier generation method', result)
