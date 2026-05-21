from __future__ import annotations

import json
import os
from urllib import request


def main() -> None:
    url = os.getenv("A2A_SERVER_URL", "http://127.0.0.1:9100") + "/a2a/bill-check"
    req = request.Request(url, data=json.dumps({}).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
    with request.urlopen(req, timeout=5) as response:
        payload = json.loads(response.read().decode("utf-8"))
    print(json.dumps(payload["result"], indent=2))


if __name__ == "__main__":
    main()
