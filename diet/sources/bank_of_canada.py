"""Daily CAD→USD reference exchange rate from the Bank of Canada Valet API."""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from diet.util import http_request

BANK_OF_CANADA_FX_URL = (
    "https://www.bankofcanada.ca/valet/observations/FXUSDCAD/json?recent=1"
)
BANK_OF_CANADA_SOURCE = "bank_of_canada_valet"


class BankOfCanadaError(RuntimeError):
    """The FX endpoint failed or returned an unusable observation."""


@dataclass(frozen=True)
class ExchangeRate:
    currency: str
    to_usd: float
    as_of: str
    observed_at: str
    source: str = BANK_OF_CANADA_SOURCE
    source_url: str = BANK_OF_CANADA_FX_URL

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


@dataclass
class BankOfCanadaClient:
    endpoint: str = BANK_OF_CANADA_FX_URL
    transport: Any = http_request

    def cad_to_usd(self) -> ExchangeRate:
        try:
            status, _headers, body = self.transport(
                self.endpoint,
                method="GET",
                headers={"Accept": "application/json"},
                data=None,
            )
        except (OSError, RuntimeError) as exc:
            raise BankOfCanadaError(f"Bank of Canada FX request failed: {exc}") from exc
        if not 200 <= status < 300:
            raise BankOfCanadaError(
                f"Bank of Canada FX request returned HTTP {status}"
            )
        try:
            payload = json.loads(body)
            observation = payload["observations"][-1]
            as_of = str(observation["d"])
            cad_per_usd = float(observation["FXUSDCAD"]["v"])
        except (KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise BankOfCanadaError(
                "Bank of Canada FX response has no valid FXUSDCAD observation"
            ) from exc
        if not math.isfinite(cad_per_usd) or cad_per_usd <= 0:
            raise BankOfCanadaError("Bank of Canada FXUSDCAD rate is non-positive")
        return ExchangeRate(
            currency="CAD",
            to_usd=1.0 / cad_per_usd,
            as_of=as_of,
            observed_at=_utc_now(),
            source_url=self.endpoint,
        )
