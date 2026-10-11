"""Readable, evidence-bound documents saved alongside immutable explanation text."""
from collections import Counter
from datetime import date
from decimal import Decimal, InvalidOperation
import re


DOCUMENT_VERSION = 'readable-explanation-5.3'
GROUNDING_POLICY = 'prepared-claims-1'
TITLES = {
    'shared_director': 'Shared director', 'shared_owner': 'Shared owner',
    'mixed_person_roles': 'Ownership and management connection',
    'shared_address': 'Shared address', 'shared_phone': 'Shared phone number',
    'shared_email': 'Shared email address', 'company_arrears': 'Reported company arrears',
    'company_zero_arrears': 'Dated zero-arrears result',
    'stored_contract_summary': 'Available procurement records',
}


def wording_variants(analysis, finding):
    """Only prepared facts reach the model; company labels are inserted locally."""
    code = finding.get('code', '')
    count = len(finding.get('company_ids', []))
    if code in {'shared_director', 'shared_owner'}:
        role = code.removeprefix('shared_')
        edge_ids = {item['id'] for item in finding['evidence'] if item['kind'] == 'graph_edge'}
        edges = [edge for edge in analysis.inputs['graph']['links'] if edge['id'] in edge_ids]
        period = 'The role dates are incomplete, so simultaneous roles still need confirmation.'
        if edges and all(edge.get('valid_from') and edge.get('valid_until') for edge in edges):
            try:
                as_of = date.fromisoformat(analysis.inputs['graph_as_of'])
                applicable = all(date.fromisoformat(edge['valid_from']) <= as_of <
                                 date.fromisoformat(edge['valid_until']) for edge in edges)
            except (TypeError, ValueError):
                applicable = False
            period = (f"Recorded role dates cover {analysis.inputs['graph_as_of']}." if applicable else
                      'The recorded periods do not confirm simultaneous roles on the evidence date.')
        return [f'{count} companies list the same {role}, matched by a verified identifier. {period}',
                f'A person matched by a verified identifier is listed as {role} of {count} companies. {period}']
    if code == 'mixed_person_roles':
        return [f'Saved records list one person, matched by a verified identifier, in ownership and management roles across {count} companies. Role dates need checking in the evidence.',
                f'{count} companies have recorded ownership and management roles linked to the same verified person. Check the recorded role dates.']
    if code in {'shared_address', 'shared_phone', 'shared_email'}:
        label = {'shared_address': 'address', 'shared_phone': 'phone number', 'shared_email': 'email address'}[code]
        return [f'{count} companies have the same recorded {label}.',
                f'The saved records show a matching {label} for {count} companies.']
    if code in {'company_arrears', 'company_zero_arrears'}:
        fact = next(item for item in analysis.inputs['company_checks'] if item['company_id'] == finding['company_ids'][0])
        values = fact['values']
        dates = ', '.join(values['kgd_reporting_dates']) or 'not supplied'
        amount = values['kgd_total_arrears']
        return [f'The saved KGD result reports {amount} KZT in aggregate company arrears. Reporting dates: {dates}.',
                f'KGD recorded aggregate company arrears of {amount} KZT. Reporting dates: {dates}.']
    if code == 'stored_contract_summary':
        metrics = analysis.metrics
        return [f"Saved records contain {metrics['stored_contract_count']} contracts totalling {metrics['stored_contract_amount']} KZT. This is contract volume, not a loss estimate.",
                f"The available {metrics['stored_contract_count']} contracts total {metrics['stored_contract_amount']} KZT; this is not evidence of losses."]
    # Older/custom finding types remain readable through their saved wording.
    return finding['statements']


def grounded_wording(analysis, finding):
    """A closed wording catalogue: model choices cannot introduce factual prose."""
    code = finding.get('code')
    if code not in TITLES:
        raise ValueError('grounding_finding_unsupported')
    nodes = sorted((node for node in analysis.inputs['graph']['nodes']
                    if node['kind'] == 'company'), key=lambda node: node['company_id'])
    aliases = {node['company_id']: '{{C' + str(index) + '}}'
               for index, node in enumerate(nodes, 1)}
    ids = finding.get('company_ids', [])
    if not ids or len(set(ids)) != len(ids) or any(pk not in aliases for pk in ids):
        raise ValueError('grounding_company_scope_invalid')
    names = [aliases[pk] for pk in ids]
    subject = (names[0] if len(names) == 1 else ' and '.join(names) if len(names) == 2
               else ', '.join(names[:-1]) + ' and ' + names[-1] if len(names) == 3
               else f'The {len(names)} companies')
    object_subject = subject[0].lower() + subject[1:] if len(names) > 3 else subject
    if code.startswith('shared_') or code == 'mixed_person_roles':
        if len(ids) < 2:
            raise ValueError('grounding_company_scope_invalid')
    if code in {'shared_address', 'shared_phone', 'shared_email'}:
        label, ordinary, action = {
            'shared_address': ('address', 'a shared office or registration service',
                               'whether the address is a shared office or registration service'),
            'shared_phone': ('phone number', 'a shared administrator or service provider',
                             'who maintains the phone number and whether it belongs to a shared service'),
            'shared_email': ('email address', 'a shared administrator or service provider',
                             'who maintains the email address and whether it belongs to a shared service'),
        }[code]
        paragraphs = [
            f'{subject} have the same recorded {label}. The match could come from {ordinary}; it does not establish common control.',
            f'A matching {label} connects the saved records for {object_subject}. This is a weak signal because {ordinary} could explain it.',
        ]
        checks = [f'Check {action} before treating the contact match as evidence of a closer company relationship.',
                  f'Find out {action}. Then obtain tender participation records to assess whether the companies competed.']
    elif code in {'shared_director', 'shared_owner', 'mixed_person_roles'}:
        if code == 'mixed_person_roles':
            fact = f'Saved records for {object_subject} list the same verified person in ownership and management roles.'
            alternative = f'The ownership and management records for {object_subject} refer to a person matched by a verified identifier.'
            period = 'The dates and scope of those roles still need checking.'
        else:
            role = code.removeprefix('shared_')
            fact = f'Saved records for {object_subject} list the same {role}, matched by a verified identifier.'
            alternative = f'A person matched by a verified identifier is listed as {role} in the saved records for {object_subject}.'
            period = wording_variants(analysis, finding)[0].split('. ', 1)[1]
        paragraphs = [f'{fact} {period} Tender decision-making authority needs separate evidence.',
                      f'{alternative} {period} This makes the scope of company control worth reviewing.']
        checks = ["Check the recorded role dates and whether this person had authority over tender decisions; then compare the firms' tender participation.",
                  'Obtain records of the role periods and bidding responsibilities. Check whether these companies participated in the same lots.']
    elif code in {'company_arrears', 'company_zero_arrears'}:
        if len(ids) != 1:
            raise ValueError('grounding_company_scope_invalid')
        saved = next((item for item in analysis.inputs['company_checks'] if item['company_id'] == ids[0]), None)
        if not saved or not saved.get('values'):
            raise ValueError('grounding_company_check_missing')
        values = saved['values']
        try:
            amount = Decimal(str(values['kgd_total_arrears']))
            reporting = [date.fromisoformat(value).isoformat() for value in values['kgd_reporting_dates']]
            if not amount.is_finite() or amount < 0 or (code == 'company_zero_arrears') != (amount == 0):
                raise ValueError
        except (KeyError, TypeError, ValueError, InvalidOperation):
            raise ValueError('grounding_company_check_invalid') from None
        dates = ', '.join(reporting) or 'not supplied'
        money = format(amount, 'f')
        fact = f'The saved KGD result for {subject} reports {money} KZT in aggregate company arrears. Reporting dates: {dates}.'
        alternative = f'KGD recorded aggregate company arrears of {money} KZT for {subject}. Reporting dates: {dates}.'
        if saved['status'] in {'stale', 'undated'} or not reporting:
            qualification = 'This older or undated result does not establish the present balance.'
        elif saved['status'] == 'retained_fresh' or saved.get('latest_status', 'success') != 'success':
            qualification = 'The latest attempt was unsuccessful; this earlier result is retained.'
        else:
            qualification = 'This is a dated company result, not a finding about a person.'
        if code == 'company_zero_arrears':
            qualification += ' Zero does not establish overall reliability.'
        paragraphs = [f'{fact} {qualification}', f'{alternative} {qualification}']
        checks = [f'Obtain a newer dated arrears result for {subject} if a present-balance assessment is needed. Keep checks about people separate.',
                  f'Check the reporting dates and any later KGD result for {subject}; do not assign company arrears to a director or owner.']
    else:
        if set(ids) != set(aliases):
            raise ValueError('grounding_company_scope_invalid')
        paragraphs = [f'For {object_subject}, {wording_variants(analysis, finding)[0][0].lower() + wording_variants(analysis, finding)[0][1:]}',
                      f'For {object_subject}, {wording_variants(analysis, finding)[1][0].lower() + wording_variants(analysis, finding)[1][1:]}']
        checks = ['Obtain the lot participants, bids and outcomes before assessing whether these companies competed and how their bids compare.',
                  'Compare dated tender participation and bid records. Contract totals alone cannot establish coordinated bidding.']
    return {'paragraphs': paragraphs, 'checks': checks}


def build_document(analysis, plan=None):
    from .grounding import GroundingValidationError
    plan = {} if plan is None else plan
    if not isinstance(plan, dict) or set(plan) - {'sections', 'narrative', 'risk_estimate', 'risk_evidence'}:
        raise GroundingValidationError('output_schema_invalid')
    # Recheck at the persistence boundary, even if a caller bypassed the provider.
    grounded = None
    if 'narrative' in plan:
        from .grounding import render_grounded_narrative
        grounded = render_grounded_narrative(analysis, plan)
    else:
        # Existing safe section-only callers may choose prepared fact variants.
        # Negative indexes, bools, duplicate IDs and unknown fields are not choices.
        sections = plan.get('sections', [])
        if not isinstance(sections, list):
            raise GroundingValidationError('output_schema_invalid')
        by_id = {item['id']: item for item in analysis.findings}
        seen = set()
        for item in sections:
            if not isinstance(item, dict) or set(item) != {'finding_id', 'variant'}:
                raise GroundingValidationError('output_schema_invalid')
            identifier, variant = item['finding_id'], item['variant']
            if not isinstance(identifier, str) or identifier not in by_id or identifier in seen:
                raise GroundingValidationError('output_evidence_invalid')
            if type(variant) is not int or not 0 <= variant < len(wording_variants(analysis, by_id[identifier])):
                raise GroundingValidationError('output_variant_invalid')
            seen.add(identifier)
    choices = {item['finding_id']: item['variant'] for item in plan.get('sections', [])}
    order = {item['finding_id']: index for index, item in enumerate(plan.get('sections', []))}
    findings = [item for item in analysis.findings if item['code'] != 'company_check_unknown']
    # Model ordering cannot hide credited findings behind zero-point coverage items.
    findings.sort(key=lambda item: (-item['contribution'], order.get(item['id'], len(order)), item['id']))
    companies = {node['company_id']: node for node in analysis.inputs['graph']['nodes'] if node['kind'] == 'company'}
    codes = {item['code'] for item in findings}
    roles = codes & {'shared_owner', 'shared_director', 'mixed_person_roles'}
    if roles:
        summary = ('Saved role records connect some companies through the same verified person. '
                   'Check the role dates and bidding responsibilities when assessing whether they bid independently.')
    elif codes & {'shared_address', 'shared_phone', 'shared_email'}:
        summary = ('The companies are grouped by matching contact details. These matches are weak signals: '
                   'they can also come from a shared office or service provider.')
    elif codes & {'company_arrears', 'company_zero_arrears'}:
        summary = 'Saved KGD results describe dated company checks. Read each amount with its company, reporting dates and latest check status.'
    elif 'stored_contract_summary' in codes:
        summary = 'The saved contracts describe procurement activity. They do not establish which companies competed against each other.'
    else:
        summary = 'The saved analysis has no supported connection or company-check finding to explain. Missing evidence remains unknown.'
    if 'company_arrears' in codes:
        summary += ' A saved company-arrears result also needs attention; its reporting date matters.'
    meanings = {
        'shared_director': 'Shared management is a reason to check who makes bidding decisions and whether the companies participate in the same tenders.',
        'shared_owner': 'Shared ownership is a reason to check control of the companies and whether their tender participation is independent.',
        'mixed_person_roles': 'Roles across companies may connect ownership and management; confirm the scope and dates of that person\'s authority.',
        'shared_address': 'A business centre or registered-office service can explain the match. An address alone does not show common control.',
        'shared_phone': 'A shared administrator or service provider can explain the match. A phone number alone does not show common control.',
        'shared_email': 'An outsourced administrator can explain the match. An email address alone does not show common control.',
        'company_arrears': 'This result concerns the company, not its owner. It needs a dated follow-up before drawing conclusions about present arrears.',
        'company_zero_arrears': 'Zero applies to this dated company check. It does not clear the owner or establish the company\'s overall reliability.',
        'stored_contract_summary': 'Contract totals describe procurement activity. They do not establish coordinated bidding.',
    }
    items = []
    for finding in findings[:6]:
        edge_ids = {item['id'] for item in finding['evidence'] if item['kind'] == 'graph_edge'}
        contact_ids = {edge['target'] for edge in analysis.inputs['graph']['links']
                       if edge['id'] in edge_ids and edge['type'] in {'address', 'phone', 'email'}}
        details = sorted({node['name'] for node in analysis.inputs['graph']['nodes']
                          if node['id'] in contact_ids and node['kind'] == 'contact'})
        labels = []
        if set(finding['company_ids']) != set(companies) or finding['dimension'] == 'company_financial':
            labels = [{'id': pk, 'name': companies[pk]['name'], 'bin': companies[pk]['bin']}
                      for pk in finding['company_ids'][:3] if pk in companies]
        items.append({'finding_id': finding['id'], 'title': TITLES.get(finding['code'], 'Saved finding'),
                      'fact': wording_variants(analysis, finding)[choices.get(finding['id'], 0)],
                      'meaning': meanings.get(finding['code'], ''), 'companies': labels,
                      'additional_companies': max(0, len(finding['company_ids']) - 3) if labels else 0,
                      'notes': finding['limitations'], 'details': details})
    checks = []
    if roles:
        checks.append('Check the recorded role dates and whether the person had authority to make tender decisions.')
    if codes & {'shared_address', 'shared_phone', 'shared_email'}:
        checks.append('Check whether the shared contact belongs to the companies themselves or to an office or service provider.')
    checks.append('Obtain lot participants, bids and outcomes; then check whether these companies competed in the same tenders and how their bids compare.')
    checks.append('Obtain dated company checks; verify any person-history information separately. Do not assign company arrears to an owner.')
    metrics = analysis.metrics
    statuses = Counter(item['status'] for item in analysis.inputs['company_checks'])
    coverage = [f"Fresh successful KGD arrears checks: {metrics['fresh_arrears_checks']} of {metrics['company_count']} companies."]
    if statuses['not_checked']:
        coverage.append(f"No KGD arrears check is saved for {company_count_label(statuses['not_checked'])}.")
    retained = sum(bool(item.get('values')) and item['latest_status'] != 'success' for item in analysis.inputs['company_checks'])
    if retained:
        coverage.append(f'The latest KGD attempt was unsuccessful for {company_count_label(retained)}; earlier successful results are retained.')
    outdated = statuses['stale'] + statuses['undated']
    if outdated:
        subject = 'company result is' if outdated == 1 else 'company results are'
        coverage.append(f'{outdated} {subject} old or undated and does not establish current arrears.' if outdated == 1 else
                        f'{outdated} {subject} old or undated and do not establish current arrears.')
    unusable = sum(count for status, count in statuses.items() if status not in {'not_checked', 'fresh', 'retained_fresh', 'stale', 'undated'})
    if unusable:
        coverage.append(f'{company_count_label(unusable)} {"has" if unusable == 1 else "have"} no usable result because a check failed or its data could not be validated.')
    coverage += ['Lot participants, bids and outcomes are missing; coordinated bidding cannot be assessed.',
                 'Verified court, bankruptcy and restricted-participant checks are not included in this analysis.']
    score_items = [{'finding_id': item['id'], 'label': TITLES.get(item['code'], 'Saved finding'), 'points': item['contribution']}
                   for item in analysis.findings if item['contribution']]
    document = {'version': DOCUMENT_VERSION, 'summary': summary, 'findings': items,
            'additional_findings': max(0, len(findings) - 6), 'checks': checks, 'coverage': coverage,
            'score': {'value': metrics['review_priority'], 'items': score_items,
                      'meaning': 'Points prioritise manual review; they are not a percentage chance of wrongdoing.'},
            'conclusion': 'The saved evidence identifies connections and follow-up questions. It does not establish collusion or a violation.'}
    if grounded is not None:
        from .narrative import company_tokens
        tokens = company_tokens(analysis)

        def expand(text):
            # Source labels enter only after model validation and remain escaped by the UI.
            return re.sub(r'\{\{(C\d+)\}\}', lambda match: tokens[match[1]]['name'], text)

        document['narrative'] = {key: [
            {'text': expand(item['text']), 'finding_ids': list(item['finding_ids'])}
            for item in grounded[key]] for key in ('paragraphs', 'checks')}
        document['grounding_policy'] = GROUNDING_POLICY
        document['summary'] = document['narrative']['paragraphs'][0]['text']
        document['checks'] = [item['text'] for item in document['narrative']['checks']]
    return document


def company_count_label(count):
    return f'{count} {"company" if count == 1 else "companies"}'


def document_text(document):
    """The downloadable text and HTML use the same saved document."""
    narrative = document.get('narrative')
    lines = ([item['text'] for item in narrative['paragraphs']] if narrative else [document['summary']])
    lines.append('Saved evidence')
    for item in document['findings']:
        labels = '; '.join(f"{company['name']} (BIN {company['bin']})" for company in item['companies'])
        lines.append(item['title'] + ': ' + item['fact'] + (' ' + labels + '.' if labels else '') + ('' if narrative else ' ' + item['meaning']))
        lines.extend(item.get('details', []))
        lines.extend(item['notes'])
    if document['additional_findings']:
        lines.append(f"{document['additional_findings']} more findings are available in the saved evidence.")
    score = document['score']
    breakdown = '; '.join(f"{item['label']}: {item['points']} points" for item in score['items']) or 'No credited findings'
    lines += [f"Review priority: {score['value']}/100. {breakdown}. {score['meaning']}",
              'What to check next', '\n'.join(f'{index}. {text}' for index, text in enumerate(document['checks'], 1)),
              'Data coverage', '\n'.join(document['coverage']), document['conclusion']]
    return '\n\n'.join(lines)
