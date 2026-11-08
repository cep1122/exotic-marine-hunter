"""
Algorithmic Underwriting & Maximum Allowable Bid (MAB) Engine
Proprietary Quantitative Engine by IC Neural Systems LLC (Israel Cepero)
"""

from typing import Dict, Any
from core.models import UnderwritingDetail, AssetCategory

class ExoticMarineUnderwriter:
    """
    Institutional Underwriting Oracle for Seized Luxury Exotics & Admiralty Marine Vessels.
    Calculates Maximum Allowable Bid (MAB), holding costs, haul-out survey reserves,
    and net wholesale exit spreads.
    """

    DEFAULT_DISCOUNT_FACTOR = 0.65  # 65% wholesale acquisition rule

    # Baseline transport and survey costs by asset category
    RESERVE_COSTS = {
        AssetCategory.EXOTIC_CAR: {
            "transport_haulout": 1800.0,    # Enclosed luxury carrier
            "survey_mechanical": 1500.0,   # Dealer PPI (Pre-Purchase Inspection) + Key programming
            "risk_multiplier": 1.0
        },
        AssetCategory.SUPERYACHT: {
            "transport_haulout": 12500.0,  # Drydock haul-out, bottom wash, sea trial fuel
            "survey_mechanical": 8500.0,   # SAMS/NAMS certified marine survey + oil analysis
            "risk_multiplier": 1.15
        },
        AssetCategory.SPORTFISHER: {
            "transport_haulout": 5500.0,   # Travelift haul-out & captain delivery
            "survey_mechanical": 4200.0,   # Twin diesel marine mechanical inspection
            "risk_multiplier": 1.10
        },
        AssetCategory.CATAMARAN: {
            "transport_haulout": 6000.0,   # Wide-beam catamaran haul-out fee
            "survey_mechanical": 3800.0,   # Rigging & hull moisture acoustic sounding
            "risk_multiplier": 1.08
        },
        AssetCategory.LUXURY_AIRCRAFT: {
            "transport_haulout": 15000.0,  # Ferry permit, hangarage, logbook escrow review
            "survey_mechanical": 12000.0,  # FAA A&P pre-buy borescope inspection
            "risk_multiplier": 1.25
        }
    }

    @classmethod
    def underwrite(
        cls,
        category: AssetCategory,
        retail_value: float,
        outstanding_lien_or_bid: float,
        custom_discount: float = 0.65
    ) -> UnderwritingDetail:
        """
        Executes institutional underwriting calculations.
        """
        reserves = cls.RESERVE_COSTS.get(category, cls.RESERVE_COSTS[AssetCategory.EXOTIC_CAR])
        haulout_cost = reserves["transport_haulout"]
        survey_cost = reserves["survey_mechanical"]

        gross_ceiling = retail_value * custom_discount
        total_deductions = outstanding_lien_or_bid + haulout_cost + survey_cost
        mab = max(0.0, gross_ceiling - (haulout_cost + survey_cost))

        total_acquisition_cost = outstanding_lien_or_bid + haulout_cost + survey_cost
        projected_spread = max(0.0, retail_value - total_acquisition_cost)

        roi_percentage = (projected_spread / total_acquisition_cost * 100.0) if total_acquisition_cost > 0 else 0.0

        # Assess risk profile
        if roi_percentage >= 50.0 and total_acquisition_cost <= (retail_value * 0.50):
            risk_level = "OPPORTUNISTIC (ALPHA SPREAD)"
            notes = "Deep-discount pre-auction opportunity. High equity cushion against mechanical surprises."
        elif roi_percentage >= 25.0:
            risk_level = "MODERATE (SOLID WHOLESALE)"
            notes = "Institutional margin verified. Standard marine/supercar remarketing timeline."
        else:
            risk_level = "CONSERVATIVE (TIGHT MARGIN)"
            notes = "Bid discipline required. Ensure hull/engine survey is completed prior to final gavel."

        return UnderwritingDetail(
            estimated_retail_value=round(retail_value, 2),
            discount_rate_applied=custom_discount,
            gross_acquisition_ceiling=round(gross_ceiling, 2),
            outstanding_lien_or_opening_bid=round(outstanding_lien_or_bid, 2),
            estimated_transport_haulout_cost=round(haulout_cost, 2),
            mechanical_survey_allowance=round(survey_cost, 2),
            maximum_allowable_bid_mab=round(mab, 2),
            projected_net_spread=round(projected_spread, 2),
            roi_percentage=round(roi_percentage, 1),
            risk_level=risk_level,
            underwriting_notes=notes
        )
