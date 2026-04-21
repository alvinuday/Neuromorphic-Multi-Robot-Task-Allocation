from __future__ import annotations

from oim_sim.benchmark import benchmark_markdown, default_cases, run_benchmark


def test_benchmark_report_structure() -> None:
    report = run_benchmark(default_cases()[:2], exact_node_limit=22)
    assert "rows" in report and report["rows"]
    assert "summary" in report and report["summary"]

    md = benchmark_markdown(report)
    assert "# OIM-MRTA Benchmark Results" in md
    assert "Aggregate Summary" in md
