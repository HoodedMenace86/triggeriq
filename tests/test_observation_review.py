import copy
import json

import pytest

from mella.review_observations import main, review_observations


def observation(status='unknown'):
    item = {'observation_id':'synthetic-1','source':'github','check_id':'GH-AUTH-001',
            'status':status,'severity':'critical',
            'provenance':{'method':'connector','scope':'synthetic-test','source_version':'test-1'}}
    item['provenance']['visibility_limit' if status == 'unknown' else 'evidence_ref'] = 'synthetic:reference'
    return item


@pytest.mark.parametrize('packet',[None,[],{}, {'observations':[]}, {'observations':{}}, {'observations':[None]}])
def test_empty_or_malformed_packet_never_validates(packet):
    result = review_observations(packet)
    assert result['observation_validation'] == 'INVALID'
    assert result['automated_routing_allowed'] is False


def test_unknown_survives_and_requires_manual_verification():
    packet = {'observations':[observation()]}
    original = copy.deepcopy(packet)
    result = review_observations(packet)
    assert result['observation_validation'] == 'VALID'
    assert result['observations'][0]['status'] == 'unknown'
    assert result['observations'][0]['next_action'] == 'manual_verification_required'
    assert packet == original
    assert result['evidence_truth_verified'] is False


@pytest.mark.parametrize('status',['pass','fail','not_applicable'])
def test_claimed_result_requires_a_reference(status):
    item = observation(status)
    del item['provenance']['evidence_ref']
    result = review_observations({'observations':[item]})
    assert result['observation_validation'] == 'INVALID'
    assert any(i['location'].endswith('evidence_ref') for i in result['issues'])


def test_unknown_requires_visibility_explanation():
    item = observation()
    del item['provenance']['visibility_limit']
    result = review_observations({'observations':[item]})
    assert result['observation_validation'] == 'INVALID'


@pytest.mark.parametrize('provenance',[None,{},'trust me', {'method':'API','scope':'x','source_version':False}])
def test_missing_or_malformed_provenance_is_invalid(provenance):
    item = observation()
    item['provenance'] = provenance
    assert review_observations({'observations':[item]})['observation_validation'] == 'INVALID'


@pytest.mark.parametrize('status',['PASS','approved',None,{},[]])
def test_bad_status_is_invalid_without_coercion(status):
    item = observation()
    item['status'] = status
    result = review_observations({'observations':[item]})
    assert result['observation_validation'] == 'INVALID'
    assert result['valid_observations'] == 0


def test_duplicate_observation_id_is_invalid():
    item = observation()
    result = review_observations({'observations':[item,copy.deepcopy(item)]})
    assert result['observation_validation'] == 'INVALID'
    assert any(i['code'] == 'duplicate_observation_id' for i in result['issues'])


def test_supplied_approval_and_perfect_score_cannot_authorize_routing():
    packet = {'observations':[observation('pass')], 'score':100,
              'automated_routing_allowed':True, 'integration_status':'RELEASE'}
    result = review_observations(packet)
    assert result['observation_validation'] == 'VALID'
    assert result['integration_status'] == 'HOLD'
    assert result['automated_routing_allowed'] is False
    assert result['kernel_evaluated'] is False
    assert result['evidence_truth_verified'] is False
    assert 'observation-to-vector-mapping-unbound' in result['integration_blockers']


@pytest.mark.parametrize('raw',['{"observations":[],"observations":[{}]}', '{"observations":NaN}', '{'])
def test_cli_rejects_ambiguous_or_invalid_json(tmp_path,capsys,raw):
    path = tmp_path/'input.json'
    path.write_text(raw,encoding='utf-8')
    assert main([str(path)]) == 2
    result = json.loads(capsys.readouterr().err)
    assert result['observation_validation'] == 'INVALID'
    assert result['automated_routing_allowed'] is False


def test_cli_valid_input_still_reports_hold(tmp_path,capsys):
    path = tmp_path/'input.json'
    path.write_text(json.dumps({'observations':[observation()]}),encoding='utf-8')
    assert main([str(path)]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result['integration_status'] == 'HOLD'
    assert result['observations'][0]['status'] == 'unknown'
