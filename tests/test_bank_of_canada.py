from __future__ import annotations

from pathlib import Path

import pytest

from diet.sources.bank_of_canada import (
    BANK_OF_CANADA_FX_URL,
    BankOfCanadaClient,
    BankOfCanadaError,
)

FIXTURE = Path(__file__).parent / "fixtures" / "bank_of_canada" / "fx.json"


class FixtureTransport:
    def __init__(self, body=FIXTURE.read_bytes(), status=200):
        self.body = body
        self.status = status
        self.calls = []

    def __call__(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return self.status, {"Content-Type": "application/json"}, self.body


def test_converts_cad_per_usd_observation_to_usd_per_cad():
    transport = FixtureTransport()
    rate = BankOfCanadaClient(transport=transport).cad_to_usd()

    assert rate.currency == "CAD"
    assert rate.to_usd == pytest.approx(1 / 1.3943)
    assert rate.as_of == "2026-08-07"
    assert rate.observed_at.endswith("Z")
    assert transport.calls == [(BANK_OF_CANADA_FX_URL, {
        "method": "GET",
        "headers": {"Accept": "application/json"},
        "data": None,
    })]


@pytest.mark.parametrize("body", [b"not-json", b'{"observations":[]}'])
def test_rejects_missing_or_malformed_observations(body):
    with pytest.raises(BankOfCanadaError, match="no valid FXUSDCAD"):
        BankOfCanadaClient(transport=FixtureTransport(body)).cad_to_usd()


def test_exposes_http_failure():
    with pytest.raises(BankOfCanadaError, match="HTTP 503"):
        BankOfCanadaClient(transport=FixtureTransport(status=503)).cad_to_usd()
