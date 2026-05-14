"""P5 market adapters.

The fake adapter returns local records. Live market access is intentionally
represented as a disabled error until a future explicit approval task enables a
specific integration.
"""

from __future__ import annotations

from dataclasses import dataclass

from keiji.market_monitoring.models import MarketObservation


class LiveMarketAccessDisabledError(RuntimeError):
    """Raised when code attempts to use live market access in the MVP."""


@dataclass(frozen=True)
class FakeMarketAdapter:
    """Deterministic local-only market adapter for tests and offline operation."""

    observations: tuple[MarketObservation, ...]

    @classmethod
    def from_observations(cls, observations: list[MarketObservation]) -> "FakeMarketAdapter":
        return cls(tuple(observations))

    def search(self, *, jan: str | None = None, asin: str | None = None, model_number: str | None = None) -> list[MarketObservation]:
        """Return local observations matching any supplied identifier."""

        return [
            observation
            for observation in self.observations
            if (jan and observation.jan == jan)
            or (asin and observation.asin == asin)
            or (model_number and observation.model_number == model_number)
        ]

    def fetch_live(self, *_args: object, **_kwargs: object) -> list[MarketObservation]:
        """Reject live access in the initial offline-first MVP."""

        raise LiveMarketAccessDisabledError("Live market API access is disabled for the KEIJI initial MVP.")
