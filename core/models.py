"""
Data Models & Schemas for Exotic & Marine Hunter AI
Proprietary Architecture by IC Neural Systems LLC (Israel Cepero)
"""

from enum import Enum
from typing import Optional, List, Dict
from pydantic import BaseModel, Field

class AssetCategory(str, Enum):
    EXOTIC_CAR = "EXOTIC_CAR"
    SUPERYACHT = "SUPERYACHT"
    SPORTFISHER = "SPORTFISHER"
    CATAMARAN = "CATAMARAN"
    LUXURY_AIRCRAFT = "LUXURY_AIRCRAFT"
    COMMERCIAL_HEAVY_DUTY = "COMMERCIAL_HEAVY_DUTY"
    LUXURY_SUV = "LUXURY_SUV"

class SeizureType(str, Enum):
    US_MARSHALS_FORFEITURE = "US_MARSHALS_FORFEITURE"
    TREASURY_IRS_SEIZURE = "TREASURY_IRS_SEIZURE"
    ADMIRALTY_MARSHAL_ARREST = "ADMIRALTY_MARSHAL_ARREST"
    MECHANIC_STORAGE_LIEN = "MECHANIC_STORAGE_LIEN"
    BANK_REPOSSESSION = "BANK_REPOSSESSION"
    CUSTOMS_BORDER_SEIZURE = "CUSTOMS_BORDER_SEIZURE"
    COUNTY_SHERIFF_SALE = "COUNTY_SHERIFF_SALE"
    TEXAS_STORAGE_LIEN = "TEXAS_STORAGE_LIEN"
    CALIFORNIA_STORAGE_LIEN = "CALIFORNIA_STORAGE_LIEN"

class TitleStatus(str, Enum):
    CLEAN_DMV_TITLE = "CLEAN_DMV_TITLE"
    USCG_BILL_OF_SALE_FORM_1340 = "USCG_BILL_OF_SALE_FORM_1340"
    MARITIME_CERTIFICATE_OF_DOCUMENTATION = "MARITIME_CERTIFICATE_OF_DOCUMENTATION"
    FAA_AC_FORM_8050_2 = "FAA_AC_FORM_8050_2"
    CERTIFICATE_OF_TITLE_REPOSSESSION = "CERTIFICATE_OF_TITLE_REPOSSESSION"
    STORAGE_LIEN_STATUTORY_BILL = "STORAGE_LIEN_STATUTORY_BILL"
    TEXAS_VTR_265_LIEN_TITLE = "TEXAS_VTR_265_LIEN_TITLE"
    GSA_STANDARD_FORM_97 = "GSA_STANDARD_FORM_97"

class DealStage(str, Enum):
    PRE_AUCTION_LIEN_NOTICE = "PRE_AUCTION_LIEN_NOTICE"
    SCHEDULED_FORFEITURE_AUCTION = "SCHEDULED_FORFEITURE_AUCTION"
    ADMIRALTY_RULE_C_SALE = "ADMIRALTY_RULE_C_SALE"
    DIRECT_STORAGE_BUYOUT = "DIRECT_STORAGE_BUYOUT"
    CONFIRMED_SOLD = "CONFIRMED_SOLD"

class AuctionPlatform(str, Enum):
    APPLE_AUCTIONEERING = "Apple Auctioneering Co. (US Marshals Service)"
    CWS_MARKETING = "CWS Marketing Group (U.S. Treasury / IRS / CBP)"
    NATIONAL_LIQUIDATORS = "National Liquidators (YachtAuctions.com / Admiralty)"
    GSA_AUCTIONS = "GSA Federal Surplus & Seized Property"
    COUNTY_MUNICIPAL_TOW = "Florida Stat. 713.78 & Marina Liens"
    APPLE_TOWING_CO = "Apple Towing Co. (Texas Gov & Seizure Auctions)"
    GOVDEALS_AUCTIONS = "GovDeals Liquidity Services (Police & Municipal)"
    FLORIDA_SHERIFF_SALES = "Florida County Sheriff Foreclosure Sales"

class CustodianContact(BaseModel):
    facility_name: str
    contact_person: str
    phone: str
    email: str
    physical_address: str
    slip_or_bay_number: str
    statutory_deadline: str

class UnderwritingDetail(BaseModel):
    estimated_retail_value: float
    discount_rate_applied: float = 0.65
    gross_acquisition_ceiling: float
    outstanding_lien_or_opening_bid: float
    estimated_transport_haulout_cost: float
    mechanical_survey_allowance: float
    maximum_allowable_bid_mab: float
    projected_net_spread: float
    roi_percentage: float
    risk_level: str  # "LOW", "MODERATE", "OPPORTUNISTIC"
    underwriting_notes: str

class AssetLead(BaseModel):
    id: str
    title: str
    category: AssetCategory
    make: str
    model: str
    year: int
    identifier_type: str  # "VIN", "HIN", "N-NUMBER", "EQUIP-SN"
    identifier_value: str
    identifier_masked: str
    location_port_city: str
    county: str = "Federal Jurisdiction"
    state: str
    docket_or_case_number: str
    court_docket_authority: str = "U.S. District Court"
    seizure_type: SeizureType
    deal_stage: DealStage
    auction_platform: AuctionPlatform
    auction_date: str
    underwriting: UnderwritingDetail
    images: List[str]
    title_status: TitleStatus
    statutory_governing_law: str
    custodian: Optional[CustodianContact] = None
    is_hot_deal: bool = True
    verified_by_sentinel: bool = True

class AssetMaskedPreview(BaseModel):
    id: str
    title: str
    category: AssetCategory
    make: str
    model: str
    year: int
    identifier_type: str
    identifier_masked: str
    location_port_city: str
    county: str = "Federal Jurisdiction"
    state: str
    docket_or_case_number_masked: str
    court_docket_authority: str = "U.S. District Court"
    seizure_type: SeizureType
    deal_stage: DealStage
    auction_platform: str
    auction_date: str
    estimated_retail_value: float
    outstanding_lien_or_opening_bid: float
    maximum_allowable_bid_mab: float
    projected_net_spread: float
    roi_percentage: float
    images: List[str]
    title_status: str
    requires_tier_unlock: bool = True

class SearchFilter(BaseModel):
    category: Optional[AssetCategory] = None
    state: Optional[str] = None
    county: Optional[str] = None
    make: Optional[str] = None
    min_spread: Optional[float] = None
    deal_stage: Optional[DealStage] = None
    seizure_type: Optional[SeizureType] = None
    auction_platform: Optional[str] = None
    q: Optional[str] = None

class PayEngineSessionCreate(BaseModel):
    tier_id: str
    asset_id: Optional[str] = None
    buyer_email: str
    buyer_name: str
    payment_method: str = "CARD"  # "CARD", "BANK_ACH", "API_BANK_VAULT"
    # Credit Card details
    card_number: Optional[str] = None
    card_exp: Optional[str] = None
    card_cvc: Optional[str] = None
    billing_zip: Optional[str] = None
    # Bank ACH details
    bank_routing: Optional[str] = None
    bank_account: Optional[str] = None
    bank_name: Optional[str] = None
    # API Bank Vault details
    vault_account_id: Optional[str] = None
    vault_pin: Optional[str] = None

class PayEngineSessionResponse(BaseModel):
    session_id: str
    tier_name: str
    amount: float
    currency: str
    vault_destination: str
    inflow_fee: float
    merkle_dag_seal: str
    checkout_url: str
    status: str

class PayEngineVerification(BaseModel):
    session_id: str
    merkle_dag_seal: str
    status: str
    access_token: str
    unlocked_asset_id: Optional[str] = None
    valid_until: str

class LegalDisclosure(BaseModel):
    entity: str
    governing_jurisdiction: str
    admiralty_law_notice: str
    u_c_c_article_9_compliance: str
    disclaimer: str

class UserRegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str
    role: str = "PRO_HUNTER"

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserAuthResponse(BaseModel):
    token: str
    user_id: str
    email: str
    full_name: str
    role: str
    api_bank_wallet_id: str
    wallet_balance: float
    message: str

class WatchlistToggleRequest(BaseModel):
    asset_id: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    email: str
    code: str
    new_password: str

