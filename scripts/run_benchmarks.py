from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from oim_sim import default_cases, run_benchmark, save_report


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def main() -> None:
    cases = default_cases()
    report = run_benchmark(cases)

    save_report(
        report,
        markdown_path=DOCS / "benchmark_results.md",
        json_path=DOCS / "benchmark_results.json",
    )

    case_dump = []
    for case in cases:
        case_dump.append(
            {
                "name": case.name,
                "coalition_bound": case.coalition_bound,
                "lambda_penalty": case.lambda_penalty,
                "instance": {
                    "robots": [asdict(r) for r in case.instance.robots],
                    "tasks": [asdict(t) for t in case.instance.tasks],
                },
            }
        )

    (DOCS / "js_groundtruth_cases.json").write_text(json.dumps(case_dump, indent=2), encoding="utf-8")
    print(f"Wrote {DOCS / 'benchmark_results.md'}")
    print(f"Wrote {DOCS / 'benchmark_results.json'}")
    print(f"Wrote {DOCS / 'js_groundtruth_cases.json'}")


if __name__ == "__main__":
    main()
