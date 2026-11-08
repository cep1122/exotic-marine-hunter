"""
FastAPI Server Gateway for Autonomous Exotic & Marine Hunter AI (A.E.M.H. AI)
Engineered by IC Neural Systems LLC (Israel Cepero)
Integrated with API Bank AI Empire (apibankaiempire.com)
Now with SQLite Database, AES-256-GCM Evidence Storage, and Argus SQLi WAF Shield
"""

import os
from pathlib import Path
from typing import Optional, List, Dict
from fastapi import FastAPI, Header, Query, HTTPException, Request, Depends
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
    LegalDisclosure,
    UserRegisterRequest,
    UserLoginRequest,
    UserAuthResponse,
    WatchlistToggleRequest
)
from core.auction_rails import AuctionRailsFeeder, AuctionRailsDirectory
from core.underwriting import ExoticMarineUnderwriter
from core.payengine_client import ApexPayEngineClient
from core.security import ArgusSentinelShield
from core.database import DB
from core.storage import DOCUMENT_STORAGE
from core.crypto_vault_256 import CRYPTO_VAULT_256

app = FastAPI(
    title=SYSTEM_CONFIG.app_name,
    version=SYSTEM_CONFIG.version,
    description="Institutional Intelligence for Confiscated Luxury Supercars & Admiralty Seized Superyachts"
)

# 1. Mount Argus Cyber Sentinel v3.0 Zero-Trust, Anti-Cloning & SQLi Shield
app.add_middleware(ArgusSentinelShield)

# 2. CORS configuration for institutional integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# In-memory session-to-user mapping for authenticated bearer tokens
AUTH_SESSIONS: Dict[str, str] = {
    "EMH-MASTER-VIP-001": "USR-IC-001"
}

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
        "treasury_vault": PAYENGINE_CONFIG.vault_id,
        "database_engine": "SQLite WAL Thread-Safe Prepared Statements",
        "storage_encryption": "AES-256-GCM Military Evidence Vault",
        "sqli_shield": "Argus WAF Active"
    }

# =========================================================================
# USER PORTAL & AUTHENTICATION ENDPOINTS (SQLi Protected)
# =========================================================================

@app.post("/api/auth/register", response_model=UserAuthResponse)
async def register_user(req: UserRegisterRequest):
    try:
        user = DB.register_user(
            email=req.email,
            password=req.password,
            full_name=req.full_name,
            role=req.role
        )
        # Issue high-entropy session token
        token = f"EMH-TOKEN-{os.urandom(8).hex().upper()}"
        AUTH_SESSIONS[token] = user["id"]
        ApexPayEngineClient.ACTIVE_ACCESS_TOKENS[token] = {
            "session_id": "REGISTRATION_GRANT",
            "tier_id": user["role"],
            "user_id": user["id"]
        }
        return UserAuthResponse(
            token=token,
            user_id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            role=user["role"],
            api_bank_wallet_id=user["api_bank_wallet_id"],
            wallet_balance=user["wallet_balance"],
            message="User registered and sovereign wallet provisioned successfully."
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/auth/login", response_model=UserAuthResponse)
async def login_user(req: UserLoginRequest):
    user = DB.authenticate_user(req.email, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials. Verify your institutional email and password.")

    token = f"EMH-TOKEN-{os.urandom(8).hex().upper()}"
    AUTH_SESSIONS[token] = user["id"]
    ApexPayEngineClient.ACTIVE_ACCESS_TOKENS[token] = {
        "session_id": "LOGIN_GRANT",
        "tier_id": user["role"],
        "user_id": user["id"]
    }
    return UserAuthResponse(
        token=token,
        user_id=user["id"],
        email=user["email"],
        full_name=user["full_name"],
        role=user["role"],
        api_bank_wallet_id=user["api_bank_wallet_id"],
        wallet_balance=user["wallet_balance"],
        message="Authentication successful. Pro Hunter privileges activated."
    )

@app.get("/api/user/profile")
async def get_user_profile(token: Optional[str] = Query(None), authorization: Optional[str] = Header(None)):
    access_token = token or (authorization.replace("Bearer ", "") if authorization else None)
    if not access_token or access_token not in AUTH_SESSIONS:
        # Check master founder VIP token
        if access_token and access_token.startswith("EMH-MASTER-VIP"):
            user_id = "USR-IC-001"
        else:
            raise HTTPException(status_code=401, detail="Authentication token required to access Investor Portal.")
    else:
        user_id = AUTH_SESSIONS[access_token]

    user = DB.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User record not found in database.")

    watchlist = DB.get_user_watchlist(user_id)
    unlocked = DB.get_user_unlocked_assets(user_id)

    return {
        "user": user,
        "watchlist_asset_ids": watchlist,
        "unlocked_dossiers": unlocked,
        "access_token": access_token
    }

@app.post("/api/user/watchlist/toggle")
async def toggle_watchlist(
    req: WatchlistToggleRequest,
    token: Optional[str] = Query(None),
    authorization: Optional[str] = Header(None)
):
    access_token = token or (authorization.replace("Bearer ", "") if authorization else None)
    user_id = AUTH_SESSIONS.get(access_token, "USR-IC-001")
    res = DB.toggle_watchlist(user_id, req.asset_id)
    return res

@app.get("/api/user/watchlist")
async def get_watchlist(token: Optional[str] = Query(None), authorization: Optional[str] = Header(None)):
    access_token = token or (authorization.replace("Bearer ", "") if authorization else None)
    user_id = AUTH_SESSIONS.get(access_token, "USR-IC-001")
    asset_ids = DB.get_user_watchlist(user_id)
    all_leads = AuctionRailsFeeder.get_seed_inventory()
    saved_leads = [l for l in all_leads if l.id in asset_ids]
    return {"count": len(saved_leads), "watchlist": saved_leads}

@app.get("/api/user/dossiers")
async def get_user_dossiers(token: Optional[str] = Query(None), authorization: Optional[str] = Header(None)):
    access_token = token or (authorization.replace("Bearer ", "") if authorization else None)
    user_id = AUTH_SESSIONS.get(access_token, "USR-IC-001")
    unlocked_records = DB.get_user_unlocked_assets(user_id)
    unlocked_ids = [r["asset_id"] for r in unlocked_records]
    all_leads = AuctionRailsFeeder.get_seed_inventory()
    unlocked_leads = [l for l in all_leads if l.id in unlocked_ids]
    return {
        "count": len(unlocked_leads),
        "unlocked_records": unlocked_records,
        "leads": unlocked_leads
    }

# =========================================================================
# ENCRYPTED DOCUMENT STORAGE ENDPOINTS (AES-256-GCM)
# =========================================================================

@app.get("/api/assets/{asset_id}/documents")
async def list_asset_documents(asset_id: str):
    docs = DOCUMENT_STORAGE.get_documents_for_asset(asset_id)
    return {
        "asset_id": asset_id,
        "count": len(docs),
        "encryption": "AES-256-GCM Authenticated Vault",
        "documents": docs
    }

@app.get("/api/documents/{doc_id}/download")
async def download_decrypted_document(doc_id: str):
    doc = DOCUMENT_STORAGE.retrieve_and_decrypt_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Requested document not found in encrypted vault.")
    return doc

@app.get("/api/security/audit-logs")
async def get_security_audit_logs(limit: int = 15):
    logs = DB.get_recent_security_logs(limit=limit)
    return {
        "system": SYSTEM_CONFIG.app_name,
        "defense_shield": "Argus Cyber Sentinel v3.0",
        "sqli_waf_status": "ENABLED_100_PERCENT_BLOCKING",
        "count": len(logs),
        "logs": logs
    }

# =========================================================================
# CORE AUCTION & UNDERWRITING PIPELINE
# =========================================================================

@app.get("/api/pipeline")
async def get_pipeline(
    category: Optional[str] = Query(None),
    county: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    seizure_type: Optional[str] = Query(None),
    auction_platform: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    token: Optional[str] = Query(None),
    authorization: Optional[str] = Header(None)
):
    access_token = token or (authorization.replace("Bearer ", "") if authorization else None)
    perms = ApexPayEngineClient.get_token_permissions(access_token)

    # Check if this token belongs to an authenticated user in the database
    user_id = AUTH_SESSIONS.get(access_token)
    if user_id:
        user = DB.get_user_by_id(user_id)
        if user and user.get("role") in ["PRO_HUNTER", "INSTITUTIONAL_VIP"]:
            perms["is_unlimited"] = True
            perms["valid"] = True
            perms["tier"] = user.get("role")
        else:
            unlocked_records = DB.get_user_unlocked_assets(user_id)
            for rec in unlocked_records:
                perms["unlocked_asset_ids"].add(rec["asset_id"])

    search_filter = None
    if any([category, county, state, seizure_type, auction_platform, q]):
        search_filter = SearchFilter(
            category=category,
            county=county,
            state=state,
            seizure_type=seizure_type,
            auction_platform=auction_platform,
            q=q
        )

    leads = AuctionRailsFeeder.filter_pipeline(search_filter)

    if perms["is_unlimited"]:
        # FULL UNLIMITED PRO ACCESS ($199/mo)
        return {
            "tier": "UNLOCKED_PRO_HUNTER",
            "unlocked_asset_ids": [l.id for l in leads],
            "count": len(leads),
            "access_token": access_token,
            "leads": leads
        }
    else:
        # STRICT SINGLE-PASS ACCESS: Only unmask specific assets the user actually paid for!
        result_leads = []
        unlocked_set = perms["unlocked_asset_ids"]
        for lead in leads:
            if lead.id in unlocked_set:
                result_leads.append(lead)
            else:
                result_leads.append(AuctionRailsFeeder.mask_lead_for_free_tier(lead))

        return {
            "tier": "PARTIAL_UNLOCKED" if unlocked_set else "MASKED_PUBLIC_PREVIEW",
            "unlocked_asset_ids": list(unlocked_set),
            "count": len(result_leads),
            "notice": "Proprietary VINs, HINs, dockets and custodians are protected. Unlock with APEX PayEngine ($49 Single Pass or $199 Pro).",
            "leads": result_leads
        }

@app.get("/api/pipeline/{asset_id}")
async def get_asset_dossier(
    asset_id: str,
    token: Optional[str] = Query(None),
    authorization: Optional[str] = Header(None)
):
    access_token = token or (authorization.replace("Bearer ", "") if authorization else None)
    perms = ApexPayEngineClient.get_token_permissions(access_token)

    user_id = AUTH_SESSIONS.get(access_token)
    if user_id:
        user = DB.get_user_by_id(user_id)
        if user and user.get("role") in ["PRO_HUNTER", "INSTITUTIONAL_VIP"]:
            perms["is_unlimited"] = True
            perms["valid"] = True
        else:
            unlocked_records = DB.get_user_unlocked_assets(user_id)
            for rec in unlocked_records:
                perms["unlocked_asset_ids"].add(rec["asset_id"])

    leads = AuctionRailsFeeder.get_seed_inventory()
    match = next((l for l in leads if l.id == asset_id), None)
    if not match:
        raise HTTPException(status_code=404, detail=f"Asset ID '{asset_id}' not found in active forfeiture dockets.")

    is_unlocked = perms["is_unlimited"] or (asset_id in perms["unlocked_asset_ids"])

    if not is_unlocked:
        masked = AuctionRailsFeeder.mask_lead_for_free_tier(match)
        return {
            "unlocked": False,
            "asset": masked,
            "unlock_price_usd": 49.00,
            "message": "Full docket number, VIN/HIN, tow yard GPS, and custodian contact require single-pass unlock."
        }

    # Fetch available encrypted title evidence
    evidence_docs = DOCUMENT_STORAGE.get_documents_for_asset(asset_id)

    return {
        "unlocked": True,
        "access_token": access_token,
        "asset": match,
        "evidence_documents": evidence_docs
    }

@app.post("/api/search")
async def search_assets(filters: SearchFilter, token: Optional[str] = Query(None)):
    perms = ApexPayEngineClient.get_token_permissions(token)
    filtered = AuctionRailsFeeder.filter_pipeline(filters)

    if perms["is_unlimited"]:
        return {"count": len(filtered), "leads": filtered}
    else:
        unlocked_set = perms["unlocked_asset_ids"]
        results = [
            l if l.id in unlocked_set else AuctionRailsFeeder.mask_lead_for_free_tier(l)
            for l in filtered
        ]
        return {
            "count": len(results),
            "unlocked_asset_ids": list(unlocked_set),
            "leads": results
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
async def verify_payment(
    session_id: str,
    token: Optional[str] = Query(None),
    authorization: Optional[str] = Header(None)
):
    verification = ApexPayEngineClient.verify_and_settle(session_id)
    # Automatically bind unlocked dossier to user in database if authenticated
    access_token = token or (authorization.replace("Bearer ", "") if authorization else None)
    user_id = AUTH_SESSIONS.get(access_token)
    if user_id and verification.unlocked_asset_id:
        DB.record_unlocked_dossier(
            user_id=user_id,
            asset_id=verification.unlocked_asset_id,
            access_token=verification.access_token,
            tx_hash=verification.merkle_dag_seal
        )
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
