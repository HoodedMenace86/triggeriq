import json
import subprocess
import sys
from pathlib import Path

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


ROOT = Path(__file__).resolve().parents[1]


def _score_cli(tmp_path, raw):
    path = tmp_path / "assessment.json"
    path.write_text(raw, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(ROOT / "score_posture.py"), str(path)],
        capture_output=True, text=True, check=False,
    )


@pytest.mark.parametrize("raw", [
    '{"checks":[{"id":"A","severity":"critical","status":"fail","status":"pass"}]}',
    '{"checks":[],"checks":[{"id":"A","severity":"high","status":"pass"}]}',
    '{"checks":[{"id":"A","severity":"high","status":"pass","title":NaN}]}',
    '{"checks":[{"id":"A","severity":"high","status":"pass","title":Infinity}]}',
    '{"checks":[{"id":"A","severity":"high","status":"pass","title":1e400}]}',
    '{"checks":[{"id":"A","severity":"high","status":"pass","title":-1e400}]}',
])
def test_cli_rejects_ambiguous_json(tmp_path, raw):
    proc = _score_cli(tmp_path, raw)
    assert proc.returncode == 1
    assert proc.stdout == ""
    assert proc.stderr.startswith("ERROR: ")
    assert "JSON" in proc.stderr


def test_cli_strict_json_accepts_unambiguous_input(tmp_path):
    proc = _score_cli(tmp_path, json.dumps({"checks": [
        {"id": "A", "severity": "critical", "status": "unknown"}
    ]}))
    assert proc.returncode == 0, proc.stderr
    result = json.loads(proc.stdout)
    assert result["assessment_status"] == "verification_required"
    assert result["unknown_count"] == 1
    assert result["score"] == 50.0
