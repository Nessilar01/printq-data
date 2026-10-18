from dataclasses import dataclass

from core.constants import DEFAULT_RATE_PER_MIN_THB, DEFAULT_SURCHARGES_THB, MATERIALS


@dataclass(frozen=True)
class PriceBreakdown:
    duration_min: int
    rate_per_min_thb: int
    time_cost_thb: int
    surcharge_thb: int
    total_thb: int


def quote_price(
    duration_min: int,
    material: str,
    rate: int = DEFAULT_RATE_PER_MIN_THB,
    surcharges: dict[str, int] | None = None,
) -> int:
    return quote_breakdown(duration_min, material, rate, surcharges).total_thb


def quote_breakdown(
    duration_min: int,
    material: str,
    rate: int = DEFAULT_RATE_PER_MIN_THB,
    surcharges: dict[str, int] | None = None,
) -> PriceBreakdown:
    table = DEFAULT_SURCHARGES_THB if surcharges is None else surcharges
    if duration_min <= 0:
        raise ValueError("duration_min must be positive")
    if material not in MATERIALS or material not in table:
        raise ValueError(f"unknown material: {material!r}")
    if rate < 0:
        raise ValueError("rate must not be negative")

    time_cost = duration_min * rate
    surcharge = table[material]
    return PriceBreakdown(
        duration_min=duration_min,
        rate_per_min_thb=rate,
        time_cost_thb=time_cost,
        surcharge_thb=surcharge,
        total_thb=time_cost + surcharge,
    )
