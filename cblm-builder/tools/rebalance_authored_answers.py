import argparse
import json
from pathlib import Path

from authored_exam_utils import rebalance_mcq_answers, validate_authored_mcq_state


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebalance correct answer positions in a CODEX-authored MCQ state JSON.")
    parser.add_argument("state_json", help="Path to state/tos/<COURSE_CODE>/<TERM>.json")
    args = parser.parse_args()

    path = Path(args.state_json)
    payload = json.loads(path.read_text(encoding="utf-8"))
    rebalance_mcq_answers(payload)
    validation = validate_authored_mcq_state(payload)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({"state_json": str(path), "answer_counts": validation["answer_counts"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
