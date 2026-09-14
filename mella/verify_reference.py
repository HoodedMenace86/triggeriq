"""Inspect an external pinned kernel; never implement or authorize routing."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / 'mella' / 'mella_adapter_contract.json'


class ReferenceMismatch(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise ReferenceMismatch(message)


def load_reference(path):
    """Hash bytes before executing those same bytes, without copying source."""
    path = Path(path).resolve()
    _require(not path.is_relative_to(ROOT), 'Keep private reference source outside the public checkout')
    contract = json.loads(CONTRACT_PATH.read_text(encoding='utf-8'))
    source = path.read_bytes()
    _require(hashlib.sha256(source).hexdigest() == contract['reference']['sha256'],
             'Kernel SHA-256 does not match the pinned reference; source was not executed')
    namespace = {'__name__': '_hash_verified_mella_reference', '__file__': str(path)}
    exec(compile(source, '<hash-verified-mella-reference>', 'exec'), namespace)
    kernel = namespace['MellaUnifiedKernel']()
    _require(kernel.version == contract['reference']['version'], 'Kernel version mismatch')
    return kernel, contract


def verify_reference(path):
    kernel, contract = load_reference(path)
    fields = contract['evidence_vector']
    _require(kernel.REQUIRED_INPUTS + ['FI'] == fields, 'Required field order mismatch')
    precedence = contract['rules']['route_precedence']
    actual = sorted(kernel.ROUTE_PRECEDENCE, key=kernel.ROUTE_PRECEDENCE.get, reverse=True)
    _require(actual == precedence, 'Route precedence mismatch')
    _require(contract['integration_gate']['status'] == 'HOLD' and
             contract['integration_gate']['automated_routing_allowed'] is False,
             'This verifier cannot approve or promote integration')

    # Exercise selection on every nonempty candidate subset in both orders.
    # This calls the reference helper; it does not evaluate rule predicates.
    subsets = 0
    for size in range(1, len(precedence) + 1):
        for candidates in itertools.combinations(precedence, size):
            _require(kernel._get_strictest_route(candidates) == candidates[0],
                     'Candidate selection mismatch')
            _require(kernel._get_strictest_route(tuple(reversed(candidates))) == candidates[0],
                     'Candidate order changed selection')
            subsets += 1

    # Fresh synthetic probes. No private fixture or proof vector is loaded.
    benign = dict.fromkeys(fields, 0.0)
    benign.update(dict.fromkeys(['V', 'KC', 'AG', 'RC', 'EQ', 'DR', 'RE'], 1.0))
    released = kernel.evaluate(benign)
    _require(released['final_route'] == 'RELEASE' and released['triggered_routes'] == ['RELEASE'],
             'RELEASE/LIMIT eligibility coupling mismatch')
    _require(released['release_allowed'] is False, 'RELEASE must not authorize production')
    _require(released['denied_claims'] == kernel.DENIED_CLAIMS, 'Denied claims were lost')

    missing_checks = 0
    for field in fields:
        partial = dict(benign)
        del partial[field]
        response = kernel.evaluate(partial)
        _require(response['malformed_input'] is True, 'Missing field was accepted')
        _require(response['final_route'] not in ('LIMIT', 'RELEASE'),
                 'Missing evidence produced a permissive route')
        _require(response['verification_state'] == 'UNKNOWN', 'Unknown state was lost')
        _require(response['release_allowed'] is False, 'Missing evidence granted authority')
        missing_checks += 1
    empty = kernel.evaluate({})
    _require(empty['final_route'] == 'ABSTAIN', 'Empty evidence fallback mismatch')

    malformed_checks = 0
    for value in (None, True, '0.5', float('nan'), float('inf'), -0.01, 1.01):
        response = kernel.evaluate({**benign, 'FI': value})
        _require(response['malformed_input'] is True and
                 response['final_route'] not in ('LIMIT', 'RELEASE'),
                 'Malformed FI became permissive')
        malformed_checks += 1

    fallback = {**benign, **dict.fromkeys(['H','A','R','D','E','P'], 0.5), 'V':0.5}
    _require(kernel.evaluate(fallback)['final_route'] == 'REVIEW', 'Fallback changed')

    # Expected OPEN defects, not passing monotonicity assertions or fixes.
    harm_before = {**benign, **dict.fromkeys(['H','A','R','D','E','P'], 0.6), 'V':0.42}
    harm_after = {**harm_before, 'E':0.63}
    readiness_before = {**benign, **dict.fromkeys(['H','A','R','D','E','P'], 0.2), 'V':0.5, 'KC':0.38}
    readiness_after = {**readiness_before, 'KC':0.4}
    harm_routes = [kernel.evaluate(x)['final_route'] for x in (harm_before, harm_after)]
    readiness_routes = [kernel.evaluate(x)['final_route'] for x in (readiness_before, readiness_after)]
    _require(harm_routes == ['REVIEW','DEFER'], 'Pinned M/fallback finding did not reproduce')
    _require(readiness_routes == ['DEFER','REVIEW'], 'Pinned readiness/fallback finding did not reproduce')

    return {
        'reference_checks':'PASS',
        'verification_scope':'pinned identity and synthetic compatibility probes only',
        'reference_version':kernel.version, 'reference_sha256':contract['reference']['sha256'],
        'candidate_subsets_checked':subsets, 'missing_field_checks':missing_checks,
        'malformed_value_checks':malformed_checks,
        'known_monotonicity_finding':'REPRODUCED_UNPATCHED',
        'canonical_receipt_replay_verified':False,
        'v0_3_5_verified':False,
        'integration_status':'HOLD', 'automated_routing_allowed':False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kernel', required=True, type=Path,
                        help='External private mella_unified_kernel.py; never place it in this checkout')
    args = parser.parse_args(argv)
    try:
        result = verify_reference(args.kernel)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'reference_checks':'FAIL', 'integration_status':'HOLD',
                          'automated_routing_allowed':False, 'error':str(exc)}),file=sys.stderr)
        return 1
    # Display JSON is diagnostic output, NOT a MELLA canonical receipt.
    print(json.dumps(result,indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
