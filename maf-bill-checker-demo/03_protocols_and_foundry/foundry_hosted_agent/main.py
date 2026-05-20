from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


class ResponseRequest(BaseModel):
    input: str
    tools: list[dict] | None = None


app = FastAPI(title="Foundry Hosted Bill Checker")


@app.post("/responses")
async def responses(req: ResponseRequest) -> dict:
    toolbox_tools = [tool.get("name", "unknown") for tool in (req.tools or [])]
    return {
        "output_text": "Bill Checker hosted response completed.",
        "toolbox_tools_seen": toolbox_tools,
        "note": "Attach Foundry Toolbox with enterprise MCP tools for real tool calls.",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
