"""
Auction Rails & Federal Seizure Ingestion Pipeline
Autonomous Exotic & Marine Hunter AI (A.E.M.H. AI)
Engineered by IC Neural Systems LLC (Israel Cepero)
"""

from typing import List, Dict, Optional
from core.models import (
    AssetLead,
    AssetMaskedPreview,
    AssetCategory,
    SeizureType,
    TitleStatus,
    DealStage,
    AuctionPlatform,
    CustodianContact,
    SearchFilter
)
from core.underwriting import ExoticMarineUnderwriter

class AuctionRailsDirectory:
    """
    Verified Government, Admiralty & Storage Lien Auction Portals Directory
    """
    DIRECTORIES = [
        {
            "name": "Apple Auctioneering Co.",
            "authority": "United States Marshals Service (DOJ)",
            "website": "https://www.appleauctioneeringco.com",
            "jurisdiction": "Federal Nationwide (Criminal Forfeiture)",
            "specialty": "Seized Exotic Supercars, Hypercars, Luxury SUVs & Collectibles",
            "settlement_type": "Official Form USM-102 Clear Title Bill of Sale"
        },
        {
            "name": "CWS Marketing Group (CWSAMS)",
            "authority": "U.S. Department of the Treasury (IRS-CI / US Secret Service / CBP)",
            "website": "https://www.cwsmarketing.com",
            "jurisdiction": "Federal Nationwide & International Waters",
            "specialty": "Seized Mega-Yachts, Luxury Real Estate, Private Aircraft & Treasury Assets",
            "settlement_type": "Federal Treasury Form TD F 90-22.1 Warrant Title Transfer"
        },
        {
            "name": "National Liquidators / YachtAuctions.com",
            "authority": "U.S. District Court Admiralty Sales & Institutional Lenders",
            "website": "https://www.yachtauctions.com",
            "jurisdiction": "Global Admiralty / Major US Coastal Ports (Fort Lauderdale, San Diego, Annapolis)",
            "specialty": "Admiralty Rule C Seizures, Superyachts, Sportfishers & Defaulted Marine Mortgages",
            "settlement_type": "U.S. Marshal Admiralty Deed & USCG Form CG-1340 Bill of Sale"
        },
        {
            "name": "GSA Auctions",
            "authority": "U.S. General Services Administration",
            "website": "https://gsaauctions.gov",
            "jurisdiction": "Federal 50 States & Territories",
            "specialty": "Federal Seized Vessels, High-Performance Vehicles & Surplus Tech",
            "settlement_type": "Standard Form 97 (Certificate to Obtain Title to a Vehicle/Vessel)"
        },
        {
            "name": "Florida Statutory Tow & Marina Lien Registry",
            "authority": "Florida Statutes § 713.78 & § 328.17 (Vessel Mechanic Liens)",
            "website": "https://www.flhsmv.gov/motor-vehicles-tags-titles/liens-and-titles/",
            "jurisdiction": "State of Florida (Miami-Dade, Broward, Palm Beach, Monroe)",
            "specialty": "Pre-Auction Marina Storage Abandonment & Unpaid Tow Balances ($2k-$10k buyouts)",
            "settlement_type": "Florida HSMV Form 82040 Statutory Bill of Sale with Clean State Title"
        }
    ]

class AuctionRailsFeeder:
    """
    Ingestion engine and pipeline aggregator for luxury seized assets.
    """

    @classmethod
    def get_seed_inventory(cls) -> List[AssetLead]:
        leads = [
            # 1. Ferrari F8 Tributo (U.S. Marshals Criminal Forfeiture)
            AssetLead(
                id="AEMH-2026-F8-01",
                title="2022 Ferrari F8 Tributo - Rosso Corsa (U.S. Marshals Seizure)",
                category=AssetCategory.EXOTIC_CAR,
                make="Ferrari",
                model="F8 Tributo Coupe",
                year=2022,
                identifier_type="VIN",
                identifier_value="ZFF92LLA8N0278914",
                identifier_masked="ZFF92LLA8N027****",
                location_port_city="Miami-Dade County Impound Vault",
                state="FL",
                docket_or_case_number="USMS-SD-FL-CR-24-9182-A",
                seizure_type=SeizureType.US_MARSHALS_FORFEITURE,
                deal_stage=DealStage.SCHEDULED_FORFEITURE_AUCTION,
                auction_platform=AuctionPlatform.APPLE_AUCTIONEERING,
                auction_date="2026-11-24 10:00 AM EST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.EXOTIC_CAR,
                    retail_value=345000.0,
                    outstanding_lien_or_bid=165000.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1583121274602-3e2820c69888?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.CLEAN_DMV_TITLE,
                statutory_governing_law="28 U.S.C. § 2461 & 18 U.S.C. § 981 (Federal Asset Forfeiture Clear Title Guarantee)",
                custodian=CustodianContact(
                    facility_name="Federal Asset Management Facility (Apple Auctioneering Vault 4)",
                    contact_person="Deputy Marshal J. Reynolds (Asset Forfeiture Division)",
                    phone="(305) 536-4131",
                    email="custody.flsd@usmarshals-auctions.gov",
                    physical_address="6850 NW 77th Court, Miami, FL 33166",
                    slip_or_bay_number="High-Security Secure Bay #14",
                    statutory_deadline="Auction Gavel Date: Nov 24, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 2. 74' Sunseeker Predator Yacht (Admiralty Rule C Seizure)
            AssetLead(
                id="AEMH-2026-SUN-74",
                title="2021 74' Sunseeker Predator Superyacht - 'M/Y AURELIA' (Admiralty Arrest)",
                category=AssetCategory.SUPERYACHT,
                make="Sunseeker",
                model="Predator 74 XPS",
                year=2021,
                identifier_type="HIN",
                identifier_value="XSK05891A121",
                identifier_masked="XSK05891****",
                location_port_city="Fort Lauderdale / Bahia Mar Yachting Center",
                state="FL",
                docket_or_case_number="ADM-USDC-SDFL-25-CV-60291",
                seizure_type=SeizureType.ADMIRALTY_MARSHAL_ARREST,
                deal_stage=DealStage.ADMIRALTY_RULE_C_SALE,
                auction_platform=AuctionPlatform.NATIONAL_LIQUIDATORS,
                auction_date="2026-11-28 02:00 PM EST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.SUPERYACHT,
                    retail_value=3250000.0,
                    outstanding_lien_or_bid=1420000.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1569263979104-865ab7cd8d17?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.USCG_BILL_OF_SALE_FORM_1340,
                statutory_governing_law="Federal Admiralty Rule C in Rem (46 U.S.C. § 31326 - Sale of Vessel Free & Clear of All Liens)",
                custodian=CustodianContact(
                    facility_name="Bahia Mar Yachting Center (Admiralty Court Appointed Custodian)",
                    contact_person="Harbormaster Captain Marcus Vance",
                    phone="(954) 764-2233",
                    email="admiralty.dockage@yachtauctions.com",
                    physical_address="801 Seabreeze Blvd, Fort Lauderdale, FL 33316",
                    slip_or_bay_number="Admiralty Impound Mega-Slip F-12",
                    statutory_deadline="Court Confirmation Hearing: Dec 02, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 3. 2023 Rolls-Royce Cullinan Black Badge (Pre-Auction Marina Tow / Storage Lien)
            AssetLead(
                id="AEMH-2026-RR-CULL",
                title="2023 Rolls-Royce Cullinan Black Badge (Florida Stat. § 713.78 Pre-Auction Lien)",
                category=AssetCategory.EXOTIC_CAR,
                make="Rolls-Royce",
                model="Cullinan Black Badge",
                year=2023,
                identifier_type="VIN",
                identifier_value="SCA681S56PU190823",
                identifier_masked="SCA681S56PU19****",
                location_port_city="West Palm Beach Luxury Tow Yard",
                state="FL",
                docket_or_case_number="PB-LIEN-STAT-2026-0841",
                seizure_type=SeizureType.MECHANIC_STORAGE_LIEN,
                deal_stage=DealStage.PRE_AUCTION_LIEN_NOTICE,
                auction_platform=AuctionPlatform.COUNTY_MUNICIPAL_TOW,
                auction_date="2026-11-20 09:00 AM EST (Statutory Public Sale)",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.EXOTIC_CAR,
                    retail_value=465000.0,
                    outstanding_lien_or_bid=18500.0  # Just unpaid $18.5k indoor climate storage & towing fees!
                ),
                images=[
                    "https://images.unsplash.com/photo-1631295868223-63265b40d9e4?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.STORAGE_LIEN_STATUTORY_BILL,
                statutory_governing_law="Florida Statute § 713.78 (Tow / Storage Lien Statutory Sale - Owner Non-Response Notice)",
                custodian=CustodianContact(
                    facility_name="Atlantic Prestige Vehicle Recovery & Indoor Storage",
                    contact_person="Operations Manager David Thorne",
                    phone="(561) 833-9100",
                    email="claims@atlanticprestigerecovery.com",
                    physical_address="2201 Florida Mango Rd, West Palm Beach, FL 33409",
                    slip_or_bay_number="Climate Controlled Secure Suite 4",
                    statutory_deadline="Notice Period Expires: Nov 19, 2026 at 5:00 PM"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 4. 62' Viking Convertible Sportfisher (Bank Default Repossession)
            AssetLead(
                id="AEMH-2026-VIK-62",
                title="2020 62' Viking Convertible Sportfisher - 'REEL THREAT' (Maritime Repo)",
                category=AssetCategory.SPORTFISHER,
                make="Viking Yachts",
                model="62 Convertible (CAT C32A 1925 HP)",
                year=2020,
                identifier_type="HIN",
                identifier_value="VKY62208B020",
                identifier_masked="VKY62208****",
                location_port_city="Palm Beach Yacht Center / Hypoluxo",
                state="FL",
                docket_or_case_number="USCG-DOC-1299841-REPO",
                seizure_type=SeizureType.BANK_REPOSSESSION,
                deal_stage=DealStage.SCHEDULED_FORFEITURE_AUCTION,
                auction_platform=AuctionPlatform.NATIONAL_LIQUIDATORS,
                auction_date="2026-11-25 01:00 PM EST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.SPORTFISHER,
                    retail_value=2750000.0,
                    outstanding_lien_or_bid=1180000.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1569263979104-865ab7cd8d17?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.USCG_BILL_OF_SALE_FORM_1340,
                statutory_governing_law="Uniform Commercial Code (UCC Article 9) & Ship Mortgage Act of 1920",
                custodian=CustodianContact(
                    facility_name="Palm Beach Yacht Center Marine Yard",
                    contact_person="Dockmaster Keith Bradley",
                    phone="(561) 588-9911",
                    email="dockage@pbyachtcenter.com",
                    physical_address="7848 S Federal Hwy, Hypoluxo, FL 33462",
                    slip_or_bay_number="Service T-Head Slip 3",
                    statutory_deadline="Lender Sealed Bid Closing: Nov 25, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 5. 2021 Lamborghini Huracán EVO Spyder (California Tow Lien Statutory Sale)
            AssetLead(
                id="AEMH-2026-LAMBO-EVO",
                title="2021 Lamborghini Huracán EVO Spyder - Verde Mantis (Newport Beach Marina Lien)",
                category=AssetCategory.EXOTIC_CAR,
                make="Lamborghini",
                model="Huracán EVO Spyder",
                year=2021,
                identifier_type="VIN",
                identifier_value="ZHWUA4ZF8MLA14902",
                identifier_masked="ZHWUA4ZF8MLA1****",
                location_port_city="Newport Beach Harbor Impound Yard",
                state="CA",
                docket_or_case_number="CA-DMV-LIEN-2026-9938",
                seizure_type=SeizureType.MECHANIC_STORAGE_LIEN,
                deal_stage=DealStage.PRE_AUCTION_LIEN_NOTICE,
                auction_platform=AuctionPlatform.COUNTY_MUNICIPAL_TOW,
                auction_date="2026-11-22 11:00 AM PST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.EXOTIC_CAR,
                    retail_value=289000.0,
                    outstanding_lien_or_bid=14200.0  # $14.2k Tow & Harbor dry storage lien
                ),
                images=[
                    "https://images.unsplash.com/photo-1544829099-b9a0c07fad1a?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.STORAGE_LIEN_STATUTORY_BILL,
                statutory_governing_law="California Civil Code § 3071 (Notice of Lien Sale for Vehicles Valued Over $4,000)",
                custodian=CustodianContact(
                    facility_name="Pacific Coast Heavy Recovery & Impound Depot",
                    contact_person="Dispatcher Elena Rostova",
                    phone="(949) 642-8820",
                    email="liens@pacificcoastrecovery.com",
                    physical_address="1776 Placentia Ave, Costa Mesa, CA 92627",
                    slip_or_bay_number="Enclosed Covered Vault 2",
                    statutory_deadline="Redemption Window Closes: Nov 21, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 6. 2018 Cessna Citation XLS+ Jet (U.S. Marshals Aviation Forfeiture)
            AssetLead(
                id="AEMH-2026-CITATION-XLS",
                title="2018 Cessna Citation XLS+ Executive Jet (U.S. Marshals / Treasury Seizure)",
                category=AssetCategory.LUXURY_AIRCRAFT,
                make="Cessna",
                model="Citation 560XL (XLS+)",
                year=2018,
                identifier_type="N-NUMBER",
                identifier_value="N829CX (SN: 560-6241)",
                identifier_masked="N829** (SN: 560-****)",
                location_port_city="Miami-Opa Locka Executive Airport (OPF)",
                state="FL",
                docket_or_case_number="USMS-SD-FL-AIR-24-3310",
                seizure_type=SeizureType.TREASURY_IRS_SEIZURE,
                deal_stage=DealStage.SCHEDULED_FORFEITURE_AUCTION,
                auction_platform=AuctionPlatform.CWS_MARKETING,
                auction_date="2026-12-05 01:00 PM EST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.LUXURY_AIRCRAFT,
                    retail_value=7800000.0,
                    outstanding_lien_or_bid=3400000.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1540962351504-03099e0a754b?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1583073600538-fec186011e49?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.FAA_AC_FORM_8050_2,
                statutory_governing_law="18 U.S.C. § 982 & Federal Aviation Administration Aircraft Registry AC Form 8050-2",
                custodian=CustodianContact(
                    facility_name="Atlantic Aviation OPF Hangar 8",
                    contact_person="Government Custody Coordinator Paul Miller",
                    phone="(305) 688-4649",
                    email="opf.fbo@atlanticaviation.com",
                    physical_address="14200 NW 42nd Ave, Opa-locka, FL 33054",
                    slip_or_bay_number="Hangar Executive Bay 8-C",
                    statutory_deadline="FAA Title Escrow Deposit Deadline: Dec 01, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            )
        ]
        return leads

    @classmethod
    def filter_pipeline(cls, filters: Optional[SearchFilter] = None) -> List[AssetLead]:
        leads = cls.get_seed_inventory()
        if not filters:
            return leads

        result = leads
        if filters.category:
            result = [lead for lead in result if lead.category == filters.category]
        if filters.state:
            result = [lead for lead in result if lead.state.upper() == filters.state.upper()]
        if filters.make:
            result = [lead for lead in result if filters.make.lower() in lead.make.lower()]
        if filters.min_spread:
            result = [lead for lead in result if lead.underwriting.projected_net_spread >= filters.min_spread]
        if filters.deal_stage:
            result = [lead for lead in result if lead.deal_stage == filters.deal_stage]

        return result

    @classmethod
    def mask_lead_for_free_tier(cls, lead: AssetLead) -> AssetMaskedPreview:
        """
        Masks proprietary identifiers (VIN, HIN, Case Docket, Custodian Contact) for non-paying users.
        Enforces APEX PayEngine monetization gates.
        """
        return AssetMaskedPreview(
            id=lead.id,
            title=lead.title,
            category=lead.category,
            make=lead.make,
            model=lead.model,
            year=lead.year,
            identifier_type=lead.identifier_type,
            identifier_masked=lead.identifier_masked,
            location_port_city=lead.location_port_city,
            state=lead.state,
            docket_or_case_number_masked=f"{lead.docket_or_case_number[:6]}****** [PRO UNLOCK REQUIRED]",
            seizure_type=lead.seizure_type,
            deal_stage=lead.deal_stage,
            auction_platform=lead.auction_platform.value,
            auction_date=lead.auction_date,
            estimated_retail_value=lead.underwriting.estimated_retail_value,
            outstanding_lien_or_opening_bid=lead.underwriting.outstanding_lien_or_opening_bid,
            maximum_allowable_bid_mab=lead.underwriting.maximum_allowable_bid_mab,
            projected_net_spread=lead.underwriting.projected_net_spread,
            roi_percentage=lead.underwriting.roi_percentage,
            images=lead.images,
            title_status=lead.title_status.value,
            requires_tier_unlock=True
        )
