# 06 Observability and evaluation

Run this:
```bash
cd /home/runner/work/maf-demos/maf-demos/maf-bill-checker-demo/06_observability_and_evaluation
python local_observability.py
pytest -q tests/test_bill_checker.py
```

Observe this:
- OpenTelemetry trace emitted for bill-check run.
- Metrics-like counters printed with result.
- Tests cover one passing and one failing bill scenario.
