# Foundry hosted Bill Checker agent (Responses protocol skeleton)

Run this:
```bash
cd /home/runner/work/maf-demos/maf-demos/maf-bill-checker-demo/03_protocols_and_foundry/foundry_hosted_agent
pip install -r requirements.txt
python main.py
```

Observe this:
- `/responses` endpoint receives requests in Responses-style shape.
- Tool execution path expects tools from a Foundry Toolbox attachment.

Generic Foundry steps:
1. Create/update hosted agent from `agent.yaml` and `agent.manifest.yaml`.
2. Create Foundry Toolbox and link your remote MCP endpoint.
3. Attach toolbox to hosted agent.
4. Execute sample response and verify tool traces in Foundry logs.
