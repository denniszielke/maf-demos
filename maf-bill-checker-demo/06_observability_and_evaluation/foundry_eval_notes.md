# Foundry observability and evaluation notes

## Enable traces and metrics

1. Open your Foundry project and select the hosted Bill Checker agent.
2. Enable tracing/telemetry in agent runtime settings.
3. Attach a monitoring sink supported by your Foundry workspace.
4. Run a sample request and open trace view:
   - Confirm tool calls (toolbox-backed MCP tools)
   - Confirm model latency and token metrics

## Basic evaluation gate

Use two saved test inputs:
- Pass case: valid arithmetic + valid address + known customer.
- Fail case: arithmetic mismatch or invalid postal code.

Gate example:
- `pass_rate >= 0.95`
- arithmetic precision failures must be zero on pass fixtures
- address-validation failures must appear on fail fixtures

If gate fails, block promotion and inspect latest traces before redeploy.
