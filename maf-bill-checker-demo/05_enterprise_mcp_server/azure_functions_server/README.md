# Azure Functions server variant (Python v2 model)

Run this locally:
```bash
cd /home/runner/work/maf-demos/maf-demos/maf-bill-checker-demo/05_enterprise_mcp_server/azure_functions_server
pip install -r requirements.txt
func start
```

Deploy sketch:
1. `func azure functionapp publish <your-app-name>`
2. Copy public HTTPS URL.
3. Register endpoint in Foundry Tool Catalog, then attach via Foundry Toolbox.
