# 01 DevUI local BillChecker agent

Run this:
```bash
cd /home/runner/work/maf-demos/maf-demos/maf-bill-checker-demo/01_devui_local_agent
python main.py --devui --port 8010
```

Observe this:
- Programmatic `serve(...)` startup pattern.
- Foundry model endpoint/model env banner (optional).
- Middleware redacts `supplier_vat_id` and validates tool arguments.
- Open `http://127.0.0.1:8010` and click **Run bill check**.
