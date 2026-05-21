# 03 Protocols and Foundry integration

## A2A run

Run this:
```bash
# terminal A
cd /home/runner/work/maf-demos/maf-demos/maf-bill-checker-demo/03_protocols_and_foundry
python a2a_server.py

# terminal B
cd /home/runner/work/maf-demos/maf-demos/maf-bill-checker-demo/03_protocols_and_foundry
python a2a_client.py
```

Observe this:
- A2A-style server exposes one bill-check operation.
- Client prints a `BillCheckResult` payload.

## Foundry hosted agent

Run this:
```bash
cd /home/runner/work/maf-demos/maf-demos/maf-bill-checker-demo/03_protocols_and_foundry/foundry_hosted_agent
docker build -t bill-checker-hosted .
```

Observe this:
- Responses protocol style endpoint in `main.py`.
- `agent.yaml` + `agent.manifest.yaml` placeholders for Foundry hosted deployment.

## Foundry Toolbox (generic)

1. In Foundry portal, create a **Toolbox**.
2. Register remote MCP endpoint (`https://<public-mcp-endpoint>`).
3. Verify tools discovered: `get_customer_master`, `validate_address`, `match_customer_by_name`.
4. Attach this toolbox to the hosted Bill Checker agent.
5. Re-run a hosted response and inspect tool call traces.
