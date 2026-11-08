"""
Autonomous Exotic & Marine Hunter AI (A.E.M.H. AI)
Institutional Intelligence, Maritime Admiralty Seizures & Pre-Auction Storage Lien Harvester

Engineered and Owned Exclusively by:
IC Neural Systems LLC (Israel Cepero, Founder & Principal Systems Architect)
Integrated with API Bank AI Empire Sovereign Treasury (apibankaiempire.com)
"""

import os
from pydantic import BaseModel, Field
from typing import List, Dict

class BuyBoxConfig(BaseModel):
    min_market_value: float = Field(default=50000.0, description="Minimum wholesale market valuation ($50k)")
    max_market_value: float = Field(default=25000000.0, description="Upper luxury ceiling ($25M)")
    mab_discount_factor: float = Field(default=0.65, description="65% wholesale baseline for Maximum Allowable Bid")
    min_net_spread: float = Field(default=15000.0, description="Minimum net profit spread ($15k)")
    target_asset_categories: List[str] = [
        "EXOTIC_CAR",
        "SUPERYACHT",
        "SPORTFISHER",
        "CATAMARAN",
        "LUXURY_AIRCRAFT"
    ]
    primary_hotspot_regions: List[str] = [
        "Miami-Dade County, FL (Biscayne Bay / PortMiami)",
        "Broward County, FL (Fort Lauderdale Yachting Capital)",
        "Palm Beach County, FL (West Palm Beach Marina District)",
        "Monroe County, FL (Florida Keys Admiralty Seizures)",
        "Orange County, CA (Newport Beach Harbor)",
        "San Diego County, CA (San Diego Bay Naval & Repos)",
        "Harris County, TX (Houston Ship Channel / Galveston)",
        "Clark County, NV (Las Vegas Luxury Vehicle Seizures)",
        "Suffolk County, NY (Hamptons Yacht Basin)"
    ]

class PayEngineConfig(BaseModel):
    vault_id: str = "VAULT-EXOTIC-MARINE-PRIMARY"
    treasury_platform: str = "API Bank AI Empire Sovereign Ledger"
    inflow_fee_rate: float = 0.00  # 0% Inflow Fee
    currency: str = "USD"
    tiers: Dict[str, Dict] = {
        "SINGLE_PASS": {
            "name": "Single Asset Unredacted Dossier",
            "price": 49.00,
            "description": "Full VIN/HIN, Custodian Contact, Marina Slip / Tow Yard GPS, Direct Lien Payoff Docket",
            "assets_unlocked": 1
        },
        "PRO_HUNTER": {
            "name": "Pro Hunter Monthly Syndicate",
            "price": 199.00,
            "description": "Unlimited unmasked access to all 50 States Seizures, Pre-Auction Lien Alerts & Marine MAB Calculator",
            "assets_unlocked": 9999
        },
        "INSTITUTIONAL_VIP": {
            "name": "Institutional Fleet & Admiralty Desk",
            "price": 599.00,
            "description": "Real-time Webhook feed, Automated U.S. Marshal Pre-Bidding Bot, Escrow Title Guarantee",
            "assets_unlocked": 99999
        },
        "BIRD_DOG_FINDER": {
            "name": "Verified Bird-Dog Assignment Fee",
            "price": 1495.00,
            "description": "Turn-key contract assignment lock on pre-auction storage lien buyout with title bond guarantee",
            "assets_unlocked": 1
        }
    }

class SystemConfig(BaseModel):
    app_name: str = "Autonomous Exotic & Marine Hunter AI"
    version: str = "1.0.0"
    legal_entity: str = "IC Neural Systems LLC"
    architect: str = "Israel Cepero"
    security_engine: str = "Argus Cyber Sentinel v3.0 Zero-Trust & Anti-Cloning Shield"
    merkle_notary: str = "LEX AI Sovereign Legal Sentry"
    environment: str = os.getenv("APP_ENV", "production")
    port: int = int(os.getenv("PORT", 8080))

SYSTEM_CONFIG = SystemConfig()
BUYBOX_CONFIG = BuyBoxConfig()
PAYENGINE_CONFIG = PayEngineConfig()
