"""
FastAPI Server Gateway for Autonomous Exotic & Marine Hunter AI (A.E.M.H. AI)
Engineered by IC Neural Systems LLC (Israel Cepero)
Integrated with API Bank AI Empire (apibankaiempire.com)
"""

import os
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI, Header, Query, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from config import SYSTEM_CONFIG, BUYBOX_CONFIG, PAYENGINE_CONFIG
from core.models import (
    AssetCategory,
    DealStage,
    SearchFilter,
    PayEngineSessionCreate,
    PayEngineSessionResponse,
    PayEngineVerification,
    LegalDisclosure
)
from core.auction_rails import AuctionRailsFeeder, AuctionRailsDirectory
from core.underwriting import ExoticMarineUnderwriter
from core.payengine_client import ApexPayEngineClient
from core.security import ArgusSentinelShield

app = FastAPI(
    title=SYSTEM_CONFIG.app_name,
    version=SYSTEM_CONFIG.version,
    description="Institutional Intelligence for Confiscated Luxury Supercars & Admiralty Seized Superyachts"
)

# 1. Mount Argus Cyber Sentinel v3.0 Zero-Trust & Anti-Cloning Shield
app.add_middleware(ArgusSentinelShield)

# 2. CORS configuration for institutional integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_dashboard_html() -> str:
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "dashboard", "index.html"),
        os.path.join(os.path.dirname(__file__), "dashboard", "index.html"),
        os.path.join(os.getcwd(), "dashboard", "index.html"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dashboard", "index.html"),
    ]
    for p in possible_paths:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return f.read()
    return "<h1>Exotic & Marine Hunter AI Dashboard Initializing...</h1>"

@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
async def serve_dashboard():
    return HTMLResponse(content=get_dashboard_html())

@app.get("/api/health")
async def health_check():
    leads = AuctionRailsFeeder.get_seed_inventory()
    total_retail = sum(l.underwriting.estimated_retail_value for l in leads)
    total_spread = sum(l.underwriting.projected_net_spread for l in leads)

    return {
        "status": "HEALTHY",
        "system": SYSTEM_CONFIG.app_name,
        "version": SYSTEM_CONFIG.version,
        "owner": SYSTEM_CONFIG.legal_entity,
        "architect": SYSTEM_CONFIG.architect,
        "security_sentinel": SYSTEM_CONFIG.security_engine,
        "notarized_by": SYSTEM_CONFIG.merkle_notary,
        "active_seizures_count": len(leads),
        "total_retail_pipeline_usd": round(total_retail, 2),
        "total_net_spread_pipeline_usd": round(total_spread, 2),
        "treasury_vault": PAYENGINE_CONFIG.vault_id
    }

@app.get("/api/pipeline")
async def get_pipeline(token: Optional[str] = Query(None), authorization: Optional[str] = Header(None)):
    """
    Returns high-yield seized exotics & yachts.
    Masked for public visitors; unmasked for authenticated Pro Hunters.
    """
    access_token = token or (authorization.replace("Bearer ", "") if authorization else None)
    is_authorized = ApexPayEngineClient.validate_token(access_token)

    leads = AuctionRailsFeeder.get_seed_inventory()

    if is_authorized:
        return {
            "tier": "UNLOCKED_PRO_HUNTER",
            "count": len(leads),
            "access_token": access_token,
            "leads": leads
        }
    else:
        masked = [AuctionRailsFeeder.mask_lead_for_free_tier(lead) for lead in leads]
        return {
            "tier": "MASKED_PUBLIC_PREVIEW",
            "count": len(masked),
            "notice": "Proprietary VINs, HINs, dockets and custodians are protected. Unlock with APEX PayEngine ($49 Single Pass or $199 Pro).",
            "leads": masked
        }

@app.get("/api/pipeline/{asset_id}")
async def get_asset_dossier(
    asset_id: str,
    token: Optional[str] = Query(None),
    authorization: Optional[str] = Header(None)
):
    """
    Returns unredacted, single asset dossier with full custodian contacts & docket coordinates.
    """
    access_token = token or (authorization.replace("Bearer ", "") if authorization else None)
    is_authorized = ApexPayEngineClient.validate_token(access_token)

    leads = AuctionRailsFeeder.get_seed_inventory()
    match = next((l for l in leads if l.id == asset_id), None)
    if not match:
        raise HTTPException(status_code=404, detail=f"Asset ID '{asset_id}' not found in active forfeiture dockets.")

    if not is_authorized:
        masked = AuctionRailsFeeder.mask_lead_for_free_tier(match)
        return {
            "unlocked": False,
            "asset": masked,
            "unlock_price_usd": 49.00,
            "message": "Full docket number, VIN/HIN, tow yard GPS, and custodian contact require single-pass unlock."
        }

    return {
        "unlocked": True,
        "access_token": access_token,
        "asset": match
    }

@app.post("/api/search")
async def search_assets(filters: SearchFilter, token: Optional[str] = Query(None)):
    is_authorized = ApexPayEngineClient.validate_token(token)
    filtered = AuctionRailsFeeder.filter_pipeline(filters)

    if is_authorized:
        return {"count": len(filtered), "leads": filtered}
    else:
        return {
            "count": len(filtered),
            "leads": [AuctionRailsFeeder.mask_lead_for_free_tier(l) for l in filtered]
        }

@app.get("/api/auctions/directory")
async def get_auction_directory():
    return {
        "directory": AuctionRailsDirectory.DIRECTORIES,
        "statutory_rules": [
            "U.S. Marshals Service Form USM-102 transfers valid judicial title free of criminal liens.",
            "Federal Admiralty Rule C in Rem extinguishes all prior maritime liens upon court confirmation of sale.",
            "Florida Statute § 713.78 grants clean Certificate of Title upon statutory public notice expiry."
        ]
    }

@app.post("/api/payengine/checkout-session", response_model=PayEngineSessionResponse)
async def create_checkout_session(request: PayEngineSessionCreate):
    try:
        session = ApexPayEngineClient.create_checkout_session(request)
        return session
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/payengine/verify/{session_id}", response_model=PayEngineVerification)
async def verify_payment(session_id: str):
    verification = ApexPayEngineClient.verify_and_settle(session_id)
    return verification

@app.get("/api/legal", response_model=LegalDisclosure)
async def get_legal_notice():
    return LegalDisclosure(
        entity="IC Neural Systems LLC (Israel Cepero, Principal)",
        governing_jurisdiction="State of Florida / United States Federal Maritime Admiralty Jurisdiction",
        admiralty_law_notice="All marine vessels indexed herein are subject to Federal Supplemental Rules for Admiralty or Maritime Claims (Rule C & Rule E). Purchasers acquire title free and clear of all maritime liens upon judicial confirmation.",
        u_c_c_article_9_compliance="Non-judicial repossessions comply with Uniform Commercial Code Article 9 and state-specific mechanic/storage lien statutes (e.g., Fla. Stat. § 713.78, Cal. Civ. Code § 3071).",
        disclaimer="Autonomous Exotic & Marine Hunter AI is an intelligence and algorithmic underwriting platform. Users are advised to conduct physical pre-bid surveys and inspect USCG Abstract of Titles prior to executing financial commitments."
    )
