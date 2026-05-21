from __future__ import annotations

import re

ALLOWED_COUNTRIES = {"DE", "NL", "FR", "BE", "ES", "IT", "US", "GB"}


def normalize_postal_code(postal_code: str) -> str:
    return re.sub(r"\s+", "", postal_code).upper()


def validate_tool_params(tool_name: str, payload: dict) -> dict:
    if tool_name == "get_customer_master":
        customer_id = str(payload.get("customer_id", "")).strip()
        if not customer_id or len(customer_id) > 32:
            raise ValueError("customer_id invalid")
        payload["customer_id"] = customer_id
        return payload

    if tool_name == "validate_address":
        address = dict(payload.get("address", {}))
        for field, max_len in {"street": 120, "city": 80, "postal_code": 20}.items():
            value = str(address.get(field, "")).strip()
            if len(value) > max_len:
                raise ValueError(f"address.{field} exceeds max length")
            address[field] = value

        country = str(address.get("country", "")).strip().upper()
        if country not in ALLOWED_COUNTRIES:
            raise ValueError("country code rejected")
        address["country"] = country
        address["postal_code"] = normalize_postal_code(address.get("postal_code", ""))
        payload["address"] = address
        return payload

    return payload
