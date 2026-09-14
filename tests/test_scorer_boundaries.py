import pytest

from score_posture import score


@pytest.mark.parametrize('assessment',[{}, {'checks':[]}, {'checks':[{'id':'A','severity':'high','status':'not_applicable'}]}])
def test_no_applicable_evidence_has_no_score(assessment):
    result = score(assessment)
    assert result['score'] is None
    assert result['assessment_status'] == 'not_assessed'
    assert result['applicable_checks'] == 0


@pytest.mark.parametrize('assessment',[None,[], {'checks':[None]}, {'checks':[[]]},
    {'checks':[{'id':'A','status':'pass'}]},
    {'checks':[{'id':[],'status':'pass','severity':'high'}]},
    {'checks':[{'id':' A ','status':'pass','severity':'high'}]},
    {'checks':[{'id':'A','status':[],'severity':'high'}]},
    {'checks':[{'id':'A','status':'pass','severity':{}}]}])
def test_invalid_check_shape_is_rejected(assessment):
    with pytest.raises(ValueError):
        score(assessment)


def test_duplicate_checks_cannot_dilute_failed_control():
    with pytest.raises(ValueError,match='Duplicate check id'):
        score({'checks':[{'id':'A','status':'fail','severity':'critical'},
                         {'id':'A','status':'pass','severity':'critical'}]})


@pytest.mark.parametrize('status,expected_score,expected_state',[
    ('pass',100.0,'observed_checks_pass'),
    ('fail',0.0,'action_required'),
    ('unknown',50.0,'verification_required')])
def test_existing_weighting_has_explicit_assessment_state(status,expected_score,expected_state):
    result = score({'checks':[{'id':'A','status':status,'severity':'critical'}]})
    assert result['score'] == expected_score
    assert result['assessment_status'] == expected_state
    assert result['applicable_checks'] == 1
