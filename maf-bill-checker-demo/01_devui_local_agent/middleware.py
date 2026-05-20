from __future__ import annotations

from copy import deepcopy


ALLOWED_COUNTRIES = {"DE", "NL", "FR", "BE", "ES", "IT", "US", "GB"}


def redact_sensitive_fields(payload: dict) -> dict:
    clone = deepcopy(payload)
    if "supplier_vat_id" in clone:
        clone["supplier_vat_id"] = "***REDACTED***"
    return clone


def validate_tool_args(tool_name: str, args: dict) -> dict:
    if tool_name == "get_customer_master":
        customer_id = str(args.get("customer_id", "")).strip()
        if not customer_id or len(customer_id) > 32:
            raise ValueError("Invalid customer_id for get_customer_master")
        args["customer_id"] = customer_id
    if tool_name == "validate_address":
        address = args.get("address", {})
        postal_code = str(address.get("postal_code", "")).strip().replace(" ", "")
        country = str(address.get("country", "")).strip().upper()
        if not postal_code:
            raise ValueError("postal_code is required")
        if country not in ALLOWED_COUNTRIES:
            raise ValueError("Unsupported country code")
        address["postal_code"] = postal_code.upper()
        address["country"] = country
        args["address"] = address
    return args
