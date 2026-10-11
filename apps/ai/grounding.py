"""A closed publication grammar: models select prepared wording, never write it."""


class GroundingValidationError(ValueError):
    """Safe failure codes without source data or provider output."""


def selection_context(analysis, finding):
    """Build the selectable catalogue solely from immutable local evidence."""
    from .narrative import finding_context
    from .presentation import grounded_wording

    try:
        wording = grounded_wording(analysis, finding)
        return {**finding_context(analysis, finding),
                'paragraph_variants': wording['paragraphs'],
                'check_variants': wording['checks']}
    except (ValueError, KeyError, TypeError, IndexError):
        raise GroundingValidationError('output_finding_unsupported') from None


def _choices(items, ids, by_id, variants_key, *, complete=False):
    if not isinstance(items, list) or not (len(items) == len(ids) if complete else 1 <= len(items) <= 2):
        raise GroundingValidationError('output_findings_invalid' if complete else 'output_narrative_length_invalid')
    seen = set()
    for item in items:
        if not isinstance(item, dict) or set(item) != {'finding_id', 'variant'}:
            raise GroundingValidationError('output_schema_invalid')
        identifier, variant = item['finding_id'], item['variant']
        if not isinstance(identifier, str) or identifier not in by_id or identifier not in ids or identifier in seen:
            raise GroundingValidationError('output_evidence_invalid')
        variants = by_id[identifier].get(variants_key, [])
        if (type(variant) is not int or not 0 <= variant < len(variants)
                or not isinstance(variants[variant], str) or not variants[variant].strip()):
            raise GroundingValidationError('output_variant_invalid')
        seen.add(identifier)
    if complete and seen != set(ids):
        raise GroundingValidationError('output_findings_invalid')
    return seen


def validate_grounded_plan(value, ids, context, experimental=False):
    """Reject invented claims structurally, including ostensibly benign prose."""
    if not isinstance(value, dict) or set(value) != {'sections', 'narrative', 'risk_estimate', 'risk_evidence'}:
        raise GroundingValidationError('output_schema_invalid')
    if (not isinstance(ids, list) or not 1 <= len(ids) <= 6
            or any(not isinstance(identifier, str) for identifier in ids)
            or len(set(ids)) != len(ids)):
        raise GroundingValidationError('output_findings_invalid')
    by_id = {item['finding_id']: item for item in context}
    if set(ids) != set(by_id) or len(by_id) != len(context):
        raise GroundingValidationError('output_evidence_invalid')
    _choices(value['sections'], ids, by_id, 'variants', complete=True)
    narrative = value['narrative']
    if not isinstance(narrative, dict) or set(narrative) != {'paragraphs', 'checks'}:
        raise GroundingValidationError('output_schema_invalid')
    paragraphs = _choices(narrative['paragraphs'], ids, by_id, 'paragraph_variants')
    checks = _choices(narrative['checks'], ids, by_id, 'check_variants')
    if narrative['paragraphs'][0]['finding_id'] != ids[0]:
        raise GroundingValidationError('output_narrative_primary_missing')
    if not paragraphs <= checks:
        raise GroundingValidationError('output_narrative_check_missing')
    score, evidence = value['risk_estimate'], value['risk_evidence']
    if (not isinstance(evidence, list) or any(not isinstance(item, str) or item not in ids for item in evidence)
            or len(set(evidence)) != len(evidence)):
        raise GroundingValidationError('output_evidence_invalid')
    if score is not None and (not experimental or type(score) is not int or not 0 <= score <= 100 or not evidence):
        raise GroundingValidationError('output_score_invalid')
    if score is None and evidence:
        raise GroundingValidationError('output_score_invalid')
    return value


def render_grounded_narrative(analysis, plan):
    """Recheck the persisted choice plan against facts before rendering any text.

    This is also called at the document boundary. A mocked provider or another
    internal caller cannot bypass the grammar by supplying already-rendered prose.
    """
    if not isinstance(plan, dict) or not isinstance(plan.get('sections'), list):
        raise GroundingValidationError('output_schema_invalid')
    sections = plan['sections']
    if not 1 <= len(sections) <= 6:
        raise GroundingValidationError('output_findings_invalid')
    findings = sorted((item for item in analysis.findings if item.get('code') != 'company_check_unknown'),
                      key=lambda item: (-item.get('contribution', 0), item['id']))
    selected = findings[:len(sections)]
    ids = [item['id'] for item in selected]
    context = [selection_context(analysis, finding) for finding in selected]
    # An optional blinded estimate is kept separately by the caller and never
    # affects the wording catalogue, rule points, or rendered public document.
    validate_grounded_plan(plan, ids, context, experimental=True)
    by_id = {item['finding_id']: item for item in context}
    return {key: [{'text': by_id[item['finding_id']][variant_key][item['variant']],
                   'finding_ids': [item['finding_id']]} for item in plan['narrative'][key]]
            for key, variant_key in [('paragraphs', 'paragraph_variants'), ('checks', 'check_variants')]}
