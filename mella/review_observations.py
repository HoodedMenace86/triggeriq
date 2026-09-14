"""Review upstream observation structure without evaluating or authorizing MELLA."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

CONTRACT_PATH = Path(__file__).with_name('mella_adapter_contract.json')


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def review_observations(packet):
    contract = json.loads(CONTRACT_PATH.read_text(encoding='utf-8'))
    rules = contract['observation']
    issues, summaries = [], []
    seen = set()

    def issue(location, code):
        issues.append({'location':location, 'code':code})

    observations = packet.get('observations') if isinstance(packet, dict) else None
    if not isinstance(observations, list) or not observations:
        issue('observations', 'nonempty_observation_list_required')
        observations = []

    for index, observation in enumerate(observations):
        loc = f'observations[{index}]'
        if not isinstance(observation, dict):
            issue(loc, 'object_required')
            continue
        start = len(issues)
        for field in rules['required']:
            value = observation.get(field)
            if field == 'provenance':
                if not isinstance(value, dict):
                    issue(loc+'.provenance', 'provenance_object_required')
            elif not _text(value):
                issue(loc+'.'+field, 'nonempty_string_required')
        oid = observation.get('observation_id')
        if _text(oid):
            if oid != oid.strip():
                issue(loc+'.observation_id', 'unpadded_id_required')
            if oid in seen:
                issue(loc+'.observation_id', 'duplicate_observation_id')
            seen.add(oid)
        status = observation.get('status')
        if status not in rules['statuses']:
            issue(loc+'.status', 'unsupported_status')
        severity = observation.get('severity')
        if severity not in rules['severities']:
            issue(loc+'.severity', 'unsupported_severity')
        provenance = observation.get('provenance')
        if isinstance(provenance, dict):
            for field in rules['provenance_required_fields']:
                if not _text(provenance.get(field)):
                    issue(loc+'.provenance.'+field, 'nonempty_string_required')
            if provenance.get('method') not in rules['provenance_methods']:
                issue(loc+'.provenance.method', 'unsupported_method')
            if isinstance(status, str):
                required = rules['status_provenance_requirements'].get(status)
                if required and not _text(provenance.get(required)):
                    issue(loc+'.provenance.'+required, 'evidence_reference_or_visibility_limit_required')
        if len(issues) == start:
            summaries.append({
                'observation_id':oid, 'check_id':observation['check_id'],
                'status':status, 'severity':severity,
                'next_action':{'unknown':'manual_verification_required',
                               'fail':'remediation_required',
                               'pass':'review_referenced_evidence',
                               'not_applicable':'review_applicability_evidence'}[status],
            })

    # No observation, score, claimed approval, or contract edit can turn this
    # structural review into kernel authorization. It never invokes a kernel.
    return {
        'schema_version':'0.1',
        'observation_validation':'INVALID' if issues else 'VALID',
        'validation_scope':'structure and reference presence only',
        'evidence_truth_verified':False,
        'supplied_observations':len(observations),
        'valid_observations':len(summaries),
        'observations':summaries, 'issues':issues,
        'integration_status':'HOLD', 'automated_routing_allowed':False,
        'kernel_evaluated':False,
        'integration_blockers':list(contract['integration_gate']['blockers']),
    }


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key is not allowed')
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError('Non-finite JSON numbers are not allowed')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('packet', type=Path)
    args = parser.parse_args(argv)
    try:
        packet = json.loads(args.packet.read_text(encoding='utf-8'),
                            object_pairs_hook=_unique_object, parse_constant=_reject_constant)
        report = review_observations(packet)
    except (OSError, ValueError) as exc:
        print(json.dumps({'observation_validation':'INVALID','integration_status':'HOLD',
                          'automated_routing_allowed':False,'error':str(exc)}),file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    # 0 = structural review ran with valid input. It never means release.
    return 0 if report['observation_validation'] == 'VALID' else 2


if __name__ == '__main__':
    raise SystemExit(main())
