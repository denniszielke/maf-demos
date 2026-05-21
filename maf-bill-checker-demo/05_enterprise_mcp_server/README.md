# 05 Enterprise MCP server

This step provides a static-data MCP-style HTTP tool endpoint for demo use.

## Local server

Run this:
```bash
cd /home/runner/work/maf-demos/maf-demos/maf-bill-checker-demo/05_enterprise_mcp_server/local_server
python server.py
```

Observe this:
- Data loaded once from `../data/customer_master.json`.
- HTTP tools exposed:
  - `POST /tools/get_customer_master`
  - `POST /tools/validate_address`
  - `POST /tools/match_customer_by_name`

## Azure Functions variant

See `azure_functions_server/README.md` for deployment skeleton and endpoint publication.

## Foundry Tool Catalog / Toolbox

1. Deploy local server or Functions variant publicly.
2. In Foundry Tool Catalog, add MCP endpoint URL.
3. Verify tool discovery and attach through Foundry Toolbox.
4. Use attached toolbox in hosted Bill Checker agent.
