import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_assessment(data):
    path = ROOT / "tests" / "_assessment.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    try:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "score_posture.py"), str(path)],
            capture_output=True, text=True
        )
        assert proc.returncode == 0, proc.stderr
        return json.loads(proc.stdout)
    finally:
        path.unlink(missing_ok=True)


def test_pass_is_zero_penalty():
    result = run_assessment({"checks":[{"id":"A","severity":"critical","status":"pass"}]})
    assert result["score"] == 100.0


def test_fail_is_ordered():
    result = run_assessment({"checks":[
        {"id":"B","severity":"high","status":"fail","title":"High"},
        {"id":"A","severity":"critical","status":"fail","title":"Critical"}]})
    assert [x["id"] for x in result["open_triggers"]] == ["A","B"]


def test_unknown_is_not_pass():
    result = run_assessment({"checks":[{"id":"A","severity":"critical","status":"unknown"}]})
    assert result["score"] == 50.0
    assert result["unknown_count"] == 1
