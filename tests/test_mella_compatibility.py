import json
import os
from pathlib import Path

import pytest

from mella.verify_reference import CONTRACT_PATH, ReferenceMismatch, load_reference, verify_reference
from score_posture import score

ROOT = Path(__file__).resolve().parents[1]


def test_audit_and_contract_bind_the_same_reference_and_hold():
    contract = json.loads(CONTRACT_PATH.read_text(encoding='utf-8'))
    evidence = json.loads((ROOT/'mella/compatibility_verification.json').read_text(encoding='utf-8'))
    assert evidence['reference'] == contract['reference']
    assert contract['integration_gate']['status'] == evidence['status'] == 'HOLD'
    assert contract['integration_gate']['automated_routing_allowed'] is False
    assert evidence['automated_routing_allowed'] is False
    assert contract['reference']['v0_3_5']['compatibility_verified'] is False
    assert contract['reference']['v0_3_5']['artifact_sha256'] is None
    assert evidence['signed_monotonicity']['status'] == 'FAIL'


def test_unmet_requirements_are_not_reported_as_verified_behavior():
    contract = json.loads(CONTRACT_PATH.read_text(encoding='utf-8'))
    assert contract['rules']['integer_core_required'] is True
    assert contract['numeric_contract']['integer_core_verified'] is False
    assert contract['numeric_contract']['integer_conversion_defined'] is False
    assert contract['serialization']['cross_runtime_canonical_replay_verified'] is False
    assert contract['serialization']['receipt_bytes_reproduced'] is False
    assert contract['known_open_dependency']['candidate_fix_adopted'] is False
    assert contract['evidence_contract']['observation_to_vector_mapping'] == 'unbound'


def test_fi_is_required_and_not_described_as_derived():
    contract = json.loads(CONTRACT_PATH.read_text(encoding='utf-8'))
    assert len(contract['evidence_vector']) == len(set(contract['evidence_vector'])) == 19
    assert contract['evidence_vector'][-1] == 'FI'
    assert contract['evidence_contract']['FI_required'] is True
    assert 'FI' not in contract['derived_metrics']
    assert contract['passthrough_metrics'] == ['FI']


def test_wrong_hash_is_rejected_before_source_execution(tmp_path):
    marker = tmp_path/'executed.txt'
    candidate = tmp_path/'candidate.py'
    candidate.write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\n',encoding='utf-8')
    with pytest.raises(ReferenceMismatch,match='source was not executed'):
        load_reference(candidate)
    assert not marker.exists()


def test_reference_must_stay_outside_public_checkout():
    with pytest.raises(ReferenceMismatch,match='outside the public checkout'):
        load_reference(ROOT/'mella/private_kernel.py')


def test_unknown_keeps_manual_work_and_is_not_a_secure_score():
    result = score({'checks':[{'id':'synthetic-control','status':'unknown','severity':'critical'}]})
    assert result['unknown_count'] == 1
    assert result['manual_verification'][0]['id'] == 'synthetic-control'
    assert result['score'] < score({'checks':[{'id':'synthetic-control','status':'pass','severity':'critical'}]})['score']


@pytest.mark.parametrize('status',[None,'', 'PASS',0])
def test_unrecognized_observation_status_cannot_become_pass(status):
    with pytest.raises(ValueError,match='invalid status'):
        score({'checks':[{'id':'synthetic-control','status':status,'severity':'critical'}]})


def test_pinned_external_reference():
    path = os.environ.get('MELLA_KERNEL_PATH')
    if not path:
        pytest.skip('MELLA_KERNEL_PATH absent: private reference was not verified by this run')
    result = verify_reference(path)
    assert result['reference_checks'] == 'PASS'
    assert result['candidate_subsets_checked'] == 127
    assert result['missing_field_checks'] == 19
    assert result['known_monotonicity_finding'] == 'REPRODUCED_UNPATCHED'
    assert result['integration_status'] == 'HOLD'
    assert result['automated_routing_allowed'] is False
