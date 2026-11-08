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
            "name": "Apple Towing Co. (HiBid Platform)",
            "authority": "Texas Municipal, County & Seized Impounds",
            "website": "https://appletowing.hibid.com",
            "jurisdiction": "State of Texas (Houston, San Antonio, McAllen, El Paso)",
            "specialty": "Commercial Class 8 Fleets, Seized Semis, Heavy Machinery & Seized Vehicles",
            "settlement_type": "Texas VTR-265 Tow/Storage Lien Title & Judicial Sale Certificate"
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
        },
        {
            "name": "GovDeals Liquidity Services",
            "authority": "15,000+ Municipal Police Departments & County Governments",
            "website": "https://www.govdeals.com",
            "jurisdiction": "Nationwide Municipal & County Impounds",
            "specialty": "Civil Asset Forfeiture, Seized Commercial Equipment, Surplus Government Fleets",
            "settlement_type": "Official Municipal Bill of Sale with Clean County Title Warrant"
        }
    ]

class AuctionRailsFeeder:
    """
    Ingestion engine and pipeline aggregator for luxury and commercial seized assets.
    """

    @classmethod
    def get_seed_inventory(cls) -> List[AssetLead]:
        leads = [
            # 1. Ferrari F8 Tributo (Miami-Dade County, FL / US Marshals Criminal Forfeiture)
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
                county="Miami-Dade County",
                state="FL",
                docket_or_case_number="USMS-SD-FL-CR-24-9182-A",
                court_docket_authority="U.S. District Court for the Southern District of Florida",
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
                statutory_governing_law="28 U.S.C. § 2461 & 18 U.S.C. § 981 (Federal Clear Title Guarantee)",
                custodian=CustodianContact(
                    facility_name="Federal Asset Management Facility (Apple Vault 4)",
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

            # 2. 74' Sunseeker Predator Yacht (Broward County, FL / Admiralty Rule C Arrest)
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
                county="Broward County",
                state="FL",
                docket_or_case_number="ADM-USDC-SDFL-25-CV-60291",
                court_docket_authority="U.S. District Court (Admiralty Division - Rule C in Rem)",
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
                statutory_governing_law="Federal Admiralty Rule C in Rem (46 U.S.C. § 31326 - Sale Free & Clear)",
                custodian=CustodianContact(
                    facility_name="Bahia Mar Yachting Center (Admiralty Appointed Custodian)",
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

            # 3. Rolls-Royce Cullinan (Palm Beach County, FL / Florida Stat. § 713.78 Storage Lien)
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
                county="Palm Beach County",
                state="FL",
                docket_or_case_number="PB-LIEN-STAT-2026-0841",
                court_docket_authority="15th Judicial Circuit Court of Florida (Palm Beach)",
                seizure_type=SeizureType.MECHANIC_STORAGE_LIEN,
                deal_stage=DealStage.PRE_AUCTION_LIEN_NOTICE,
                auction_platform=AuctionPlatform.COUNTY_MUNICIPAL_TOW,
                auction_date="2026-11-20 09:00 AM EST (Statutory Public Sale)",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.EXOTIC_CAR,
                    retail_value=465000.0,
                    outstanding_lien_or_bid=18500.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1631295868223-63265b40d9e4?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.STORAGE_LIEN_STATUTORY_BILL,
                statutory_governing_law="Florida Statute § 713.78 (Tow / Storage Lien Statutory Notice Sale)",
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

            # 4. 2009 Volvo VNL Cummins ISX Diesel (Harris County, TX / Apple Towing Co. Lot 308)
            AssetLead(
                id="AEMH-2026-VOLVO-VNL",
                title="2009 Volvo VNL Sleeper - Cummins ISX Diesel (Apple Towing Lot 308)",
                category=AssetCategory.COMMERCIAL_HEAVY_DUTY,
                make="Volvo",
                model="VNL 670 Sleeper (Cummins ISX / 10-Spd Manual)",
                year=2009,
                identifier_type="VIN",
                identifier_value="4V4NC9EH99N482019",
                identifier_masked="4V4NC9EH99N48****",
                location_port_city="Houston Regional Impound Yard",
                county="Harris County",
                state="TX",
                docket_or_case_number="APPLE-HIBID-LOT-328423623",
                court_docket_authority="Harris County Justice Court & Texas DMV Impound Lien",
                seizure_type=SeizureType.TEXAS_STORAGE_LIEN,
                deal_stage=DealStage.SCHEDULED_FORFEITURE_AUCTION,
                auction_platform=AuctionPlatform.APPLE_TOWING_CO,
                auction_date="2026-11-09 11:01 AM EST (Live Online)",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.COMMERCIAL_HEAVY_DUTY,
                    retail_value=14500.0,
                    outstanding_lien_or_bid=2050.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1519003722824-194d4455a60c?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.TEXAS_VTR_265_LIEN_TITLE,
                statutory_governing_law="Texas Occupations Code § 2303.151 (Storage Lien Foreclosure Title)",
                custodian=CustodianContact(
                    facility_name="Apple Towing Co. Heavy Commercial Depot",
                    contact_person="Commercial Fleet Dispatcher Raul Mendez",
                    phone="(713) 682-2550",
                    email="auctions@appletowing.com",
                    physical_address="2020 S Dairy Ashford Rd, Houston, TX 77077",
                    slip_or_bay_number="Heavy Commercial Row L-308",
                    statutory_deadline="Auction Closes: Monday, Nov 9 at 11:01 AM"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 5. 62' Viking Sportfisher (Palm Beach County, FL / Maritime Bank Repo)
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
                county="Palm Beach County",
                state="FL",
                docket_or_case_number="USCG-DOC-1299841-REPO",
                court_docket_authority="U.S. Coast Guard National Vessel Documentation Center",
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
                statutory_governing_law="UCC Article 9 & Ship Mortgage Act of 1920 (46 U.S.C. § 31325)",
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

            # 6. 2023 Porsche 911 GT3 RS (Miami-Dade County, FL / Florida Sheriff Foreclosure)
            AssetLead(
                id="AEMH-2026-PORSCHE-GT3RS",
                title="2023 Porsche 911 GT3 RS Weissach Package (Sheriff Execution Levy)",
                category=AssetCategory.EXOTIC_CAR,
                make="Porsche",
                model="911 GT3 RS (992)",
                year=2023,
                identifier_type="VIN",
                identifier_value="WP0AF2A97PS289104",
                identifier_masked="WP0AF2A97PS28****",
                location_port_city="Miami Police Impound Yard",
                county="Miami-Dade County",
                state="FL",
                docket_or_case_number="MDC-SHERIFF-LEVY-2026-4419",
                court_docket_authority="11th Judicial Circuit Court of Florida (Civil Division)",
                seizure_type=SeizureType.COUNTY_SHERIFF_SALE,
                deal_stage=DealStage.SCHEDULED_FORFEITURE_AUCTION,
                auction_platform=AuctionPlatform.FLORIDA_SHERIFF_SALES,
                auction_date="2026-11-26 11:30 AM EST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.EXOTIC_CAR,
                    retail_value=395000.0,
                    outstanding_lien_or_bid=180000.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.CLEAN_DMV_TITLE,
                statutory_governing_law="Florida Statute § 56.061 (Sheriff's Levy & Execution Sale)",
                custodian=CustodianContact(
                    facility_name="Miami-Dade County Sheriff Evidence Depot",
                    contact_person="Sergeant M. Alvarez (Civil Process Bureau)",
                    phone="(305) 375-5100",
                    email="civilprocess@mdpd.com",
                    physical_address="601 NW 1st Court, Miami, FL 33136",
                    slip_or_bay_number="Armored Compound Row 8",
                    statutory_deadline="Writ of Execution Sale: Nov 26, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 7. 88' Azimut Grande Superyacht (Miami-Dade County, FL / Admiralty Rule C PACER)
            AssetLead(
                id="AEMH-2026-AZIMUT-88",
                title="2022 88' Azimut Grande Superyacht - 'VITA NOSTRA' (Federal Marshal Arrest)",
                category=AssetCategory.SUPERYACHT,
                make="Azimut",
                model="Grande 27 Metri (88')",
                year=2022,
                identifier_type="HIN",
                identifier_value="AZM88019E222",
                identifier_masked="AZM88019****",
                location_port_city="Miami River Shipyard / Port of Miami",
                county="Miami-Dade County",
                state="FL",
                docket_or_case_number="ADM-USDC-SDFL-26-CV-21903",
                court_docket_authority="U.S. District Court (Southern District of Florida PACER)",
                seizure_type=SeizureType.ADMIRALTY_MARSHAL_ARREST,
                deal_stage=DealStage.ADMIRALTY_RULE_C_SALE,
                auction_platform=AuctionPlatform.NATIONAL_LIQUIDATORS,
                auction_date="2026-12-04 03:00 PM EST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.SUPERYACHT,
                    retail_value=6400000.0,
                    outstanding_lien_or_bid=2800000.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1569263979104-865ab7cd8d17?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.USCG_BILL_OF_SALE_FORM_1340,
                statutory_governing_law="Federal Admiralty Rule C & 46 U.S.C. § 31326 (Judicial Bill of Sale)",
                custodian=CustodianContact(
                    facility_name="Miami River Marine Center",
                    contact_person="Dockmaster Frank Gamboa",
                    phone="(305) 633-8555",
                    email="admiralty@miamirivermarine.com",
                    physical_address="1975 NW South River Dr, Miami, FL 33125",
                    slip_or_bay_number="Mega Yacht Wet Dock 2",
                    statutory_deadline="Hearing Date: Dec 01, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 8. 2024 Mercedes-AMG G63 Brabus 800 (Broward County, FL / Stat. § 713.78 Tow Lien)
            AssetLead(
                id="AEMH-2026-G63-BRABUS",
                title="2024 Mercedes-AMG G63 Brabus 800 Widestar (Florida Storage Lien)",
                category=AssetCategory.LUXURY_SUV,
                make="Mercedes-Benz",
                model="G63 AMG Brabus 800",
                year=2024,
                identifier_type="VIN",
                identifier_value="W1N4632761X492011",
                identifier_masked="W1N4632761X49****",
                location_port_city="Fort Lauderdale Luxury Impound",
                county="Broward County",
                state="FL",
                docket_or_case_number="BROWARD-LIEN-2026-7810",
                court_docket_authority="17th Judicial Circuit Court of Florida (Broward)",
                seizure_type=SeizureType.MECHANIC_STORAGE_LIEN,
                deal_stage=DealStage.PRE_AUCTION_LIEN_NOTICE,
                auction_platform=AuctionPlatform.COUNTY_MUNICIPAL_TOW,
                auction_date="2026-11-21 10:00 AM EST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.LUXURY_SUV,
                    retail_value=385000.0,
                    outstanding_lien_or_bid=16200.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1520031441872-265e4ff70366?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.STORAGE_LIEN_STATUTORY_BILL,
                statutory_governing_law="Florida Statute § 713.78 (Unclaimed Impound Lien Sale)",
                custodian=CustodianContact(
                    facility_name="Broward Executive Tow & Transport",
                    contact_person="Impound Manager Leo Hernandez",
                    phone="(954) 525-8800",
                    email="liens@browardtow.com",
                    physical_address="1400 SW 1st Ave, Fort Lauderdale, FL 33315",
                    slip_or_bay_number="Secure Bay #9",
                    statutory_deadline="Lien Cure Deadline: Nov 20, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 9. 2022 Freightliner Cascadia 126 DD15 (Harris County, TX / Texas Storage Lien)
            AssetLead(
                id="AEMH-2026-CASCADIA-126",
                title="2022 Freightliner Cascadia 126 Sleeper - Detroit DD15 (Harris County Lien)",
                category=AssetCategory.COMMERCIAL_HEAVY_DUTY,
                make="Freightliner",
                model="Cascadia 126 (Detroit DD15 / DT12 Auto)",
                year=2022,
                identifier_type="VIN",
                identifier_value="3AKJHHDR5NSMJ9182",
                identifier_masked="3AKJHHDR5NSMJ****",
                location_port_city="Houston Commercial Yard",
                county="Harris County",
                state="TX",
                docket_or_case_number="TX-HARRIS-LIEN-2026-1294",
                court_docket_authority="Texas Department of Motor Vehicles (TxDMV)",
                seizure_type=SeizureType.TEXAS_STORAGE_LIEN,
                deal_stage=DealStage.PRE_AUCTION_LIEN_NOTICE,
                auction_platform=AuctionPlatform.APPLE_TOWING_CO,
                auction_date="2026-11-23 01:00 PM CST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.COMMERCIAL_HEAVY_DUTY,
                    retail_value=68000.0,
                    outstanding_lien_or_bid=12500.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1519003722824-194d4455a60c?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.TEXAS_VTR_265_LIEN_TITLE,
                statutory_governing_law="Texas Occupations Code § 2303.155 (Commercial Fleet Lien Recovery)",
                custodian=CustodianContact(
                    facility_name="Lone Star Fleet Storage Facility",
                    contact_person="Yard Manager Travis Miller",
                    phone="(713) 455-9011",
                    email="claims@lonestarfleetstorage.com",
                    physical_address="11200 Beaumont Hwy, Houston, TX 77078",
                    slip_or_bay_number="Tractor Lot Spot 44",
                    statutory_deadline="Redemption Window Ends: Nov 22, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 10. 2021 Lamborghini Huracán EVO (Orange County, CA / Calif. Civil Code § 3071)
            AssetLead(
                id="AEMH-2026-LAMBO-EVO",
                title="2021 Lamborghini Huracán EVO Spyder - Verde Mantis (Newport Beach Lien)",
                category=AssetCategory.EXOTIC_CAR,
                make="Lamborghini",
                model="Huracán EVO Spyder",
                year=2021,
                identifier_type="VIN",
                identifier_value="ZHWUA4ZF8MLA14902",
                identifier_masked="ZHWUA4ZF8MLA1****",
                location_port_city="Newport Beach Harbor Impound",
                county="Orange County",
                state="CA",
                docket_or_case_number="CA-DMV-LIEN-2026-9938",
                court_docket_authority="Orange County Superior Court & California DMV",
                seizure_type=SeizureType.CALIFORNIA_STORAGE_LIEN,
                deal_stage=DealStage.PRE_AUCTION_LIEN_NOTICE,
                auction_platform=AuctionPlatform.COUNTY_MUNICIPAL_TOW,
                auction_date="2026-11-22 11:00 AM PST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.EXOTIC_CAR,
                    retail_value=289000.0,
                    outstanding_lien_or_bid=14200.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1544829099-b9a0c07fad1a?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.STORAGE_LIEN_STATUTORY_BILL,
                statutory_governing_law="California Civil Code § 3071 (Notice of Lien Sale >$4,000)",
                custodian=CustodianContact(
                    facility_name="Pacific Coast Heavy Recovery Depot",
                    contact_person="Dispatcher Elena Rostova",
                    phone="(949) 642-8820",
                    email="liens@pacificcoastrecovery.com",
                    physical_address="1776 Placentia Ave, Costa Mesa, CA 92627",
                    slip_or_bay_number="Enclosed Covered Vault 2",
                    statutory_deadline="Redemption Window: Nov 21, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 11. 2018 Cessna Citation XLS+ Jet (Miami-Dade County, FL / US Marshals Aviation Seizure)
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
                county="Miami-Dade County",
                state="FL",
                docket_or_case_number="USMS-SD-FL-AIR-24-3310",
                court_docket_authority="U.S. District Court (Federal Asset Forfeiture Unit)",
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
                statutory_governing_law="18 U.S.C. § 982 & FAA Aircraft Registry AC Form 8050-2",
                custodian=CustodianContact(
                    facility_name="Atlantic Aviation OPF Hangar 8",
                    contact_person="Government Custody Coordinator Paul Miller",
                    phone="(305) 688-4649",
                    email="opf.fbo@atlanticaviation.com",
                    physical_address="14200 NW 42nd Ave, Opa-locka, FL 33054",
                    slip_or_bay_number="Hangar Executive Bay 8-C",
                    statutory_deadline="FAA Title Escrow Deadline: Dec 01, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 12. 2021 51' Cigarette 515 Marauder (Monroe County - Key West, FL / USCG Seizure)
            AssetLead(
                id="AEMH-2026-CIGARETTE-515",
                title="2021 51' Cigarette 515 Marauder - Dual Mercury Racing 1350/1550 HP",
                category=AssetCategory.SPORTFISHER,
                make="Cigarette Racing",
                model="515 Marauder Offshore",
                year=2021,
                identifier_type="HIN",
                identifier_value="CRT51508K021",
                identifier_masked="CRT51508****",
                location_port_city="Key West Naval Air Station Impound",
                county="Monroe County",
                state="FL",
                docket_or_case_number="USCG-KEYWEST-SEIZURE-2026-091",
                court_docket_authority="U.S. District Court for the Southern District of Florida (Key West)",
                seizure_type=SeizureType.CUSTOMS_BORDER_SEIZURE,
                deal_stage=DealStage.SCHEDULED_FORFEITURE_AUCTION,
                auction_platform=AuctionPlatform.CWS_MARKETING,
                auction_date="2026-11-30 11:00 AM EST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.SPORTFISHER,
                    retail_value=1650000.0,
                    outstanding_lien_or_bid=620000.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1569263979104-865ab7cd8d17?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.USCG_BILL_OF_SALE_FORM_1340,
                statutory_governing_law="19 U.S.C. § 1607 (Customs Seizure Title Conveyance)",
                custodian=CustodianContact(
                    facility_name="U.S. Coast Guard Sector Key West Maritime Compound",
                    contact_person="Lieutenant Commander S. Hayes",
                    phone="(305) 292-8727",
                    email="kw.property@uscg.mil",
                    physical_address="100 Trumbo Rd, Key West, FL 33040",
                    slip_or_bay_number="Slip C-04",
                    statutory_deadline="Auction Date: Nov 30, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 13. 2022 McLaren 765LT Spider (Palm Beach County, FL / Pre-Auction Storage Lien)
            AssetLead(
                id="AEMH-2026-MCLAREN-765LT",
                title="2022 McLaren 765LT Spider - MSO Carbon Edition (Florida Stat. § 713.78)",
                category=AssetCategory.EXOTIC_CAR,
                make="McLaren",
                model="765LT Spider MSO",
                year=2022,
                identifier_type="VIN",
                identifier_value="SBM11DAA6NW002914",
                identifier_masked="SBM11DAA6NW00****",
                location_port_city="Boca Raton Luxury Storage Yard",
                county="Palm Beach County",
                state="FL",
                docket_or_case_number="PB-LIEN-STAT-2026-1102",
                court_docket_authority="Palm Beach County Clerk of Courts",
                seizure_type=SeizureType.MECHANIC_STORAGE_LIEN,
                deal_stage=DealStage.PRE_AUCTION_LIEN_NOTICE,
                auction_platform=AuctionPlatform.COUNTY_MUNICIPAL_TOW,
                auction_date="2026-11-25 09:30 AM EST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.EXOTIC_CAR,
                    retail_value=485000.0,
                    outstanding_lien_or_bid=21500.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1544829099-b9a0c07fad1a?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.STORAGE_LIEN_STATUTORY_BILL,
                statutory_governing_law="Florida Statute § 713.78 (Lien for Recovering and Towing Vehicles)",
                custodian=CustodianContact(
                    facility_name="Palm Beach Prestige Auto Custody",
                    contact_person="Director Carlos Valdes",
                    phone="(561) 391-4400",
                    email="claims@pbprestigeauto.com",
                    physical_address="950 NW 1st Ave, Boca Raton, FL 33432",
                    slip_or_bay_number="Vault 1",
                    statutory_deadline="Settlement Expiry: Nov 24, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 14. 2021 Peterbilt 389 Extended Hood (Bexar County - San Antonio, TX / Apple Towing)
            AssetLead(
                id="AEMH-2026-PETERBILT-389",
                title="2021 Peterbilt 389 Extended Hood - CAT C15 Glider Kit / 18-Speed",
                category=AssetCategory.COMMERCIAL_HEAVY_DUTY,
                make="Peterbilt",
                model="389 Extended Hood Sleeper",
                year=2021,
                identifier_type="VIN",
                identifier_value="1XPXD49X4MD829104",
                identifier_masked="1XPXD49X4MD82****",
                location_port_city="San Antonio Regional Impound",
                county="Bexar County",
                state="TX",
                docket_or_case_number="BEXAR-SHERIFF-IMPOUND-2026-881",
                court_docket_authority="Bexar County District Court & Apple Towing Co.",
                seizure_type=SeizureType.TEXAS_STORAGE_LIEN,
                deal_stage=DealStage.SCHEDULED_FORFEITURE_AUCTION,
                auction_platform=AuctionPlatform.APPLE_TOWING_CO,
                auction_date="2026-11-17 10:00 AM CST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.COMMERCIAL_HEAVY_DUTY,
                    retail_value=125000.0,
                    outstanding_lien_or_bid=34000.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1519003722824-194d4455a60c?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.TEXAS_VTR_265_LIEN_TITLE,
                statutory_governing_law="Texas Occupations Code § 2303.151 (Lien Foreclosure)",
                custodian=CustodianContact(
                    facility_name="Apple Towing San Antonio Yard",
                    contact_person="Superintendent Hector Gomez",
                    phone="(210) 223-4100",
                    email="sa.auctions@appletowing.com",
                    physical_address="5000 Interstate 10, San Antonio, TX 78219",
                    slip_or_bay_number="Heavy Lot Bay 12",
                    statutory_deadline="Auction Gavel: Nov 17, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 15. 2023 Lamborghini Urus Performante (Dallas County, TX / Sheriff Foreclosure)
            AssetLead(
                id="AEMH-2026-URUS-PERF",
                title="2023 Lamborghini Urus Performante - Bianco Monocerus (Dallas County Sheriff)",
                category=AssetCategory.LUXURY_SUV,
                make="Lamborghini",
                model="Urus Performante",
                year=2023,
                identifier_type="VIN",
                identifier_value="ZPBUA1ZL8PLA20914",
                identifier_masked="ZPBUA1ZL8PLA2****",
                location_port_city="Dallas County Sheriff Compound",
                county="Dallas County",
                state="TX",
                docket_or_case_number="DC-SHERIFF-CIVIL-2026-9014",
                court_docket_authority="193rd Judicial District Court of Dallas County, Texas",
                seizure_type=SeizureType.COUNTY_SHERIFF_SALE,
                deal_stage=DealStage.SCHEDULED_FORFEITURE_AUCTION,
                auction_platform=AuctionPlatform.GOVDEALS_AUCTIONS,
                auction_date="2026-11-28 10:00 AM CST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.LUXURY_SUV,
                    retail_value=315000.0,
                    outstanding_lien_or_bid=135000.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1520031441872-265e4ff70366?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1544829099-b9a0c07fad1a?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.CLEAN_DMV_TITLE,
                statutory_governing_law="Texas Civil Practice & Remedies Code § 34.041 (Sheriff Execution Sale)",
                custodian=CustodianContact(
                    facility_name="Dallas County Vehicle Forfeiture Depot",
                    contact_person="Deputy Sheriff J. Campbell",
                    phone="(214) 653-3450",
                    email="sheriff.civil@dallascounty.org",
                    physical_address="133 N Riverfront Blvd, Dallas, TX 75207",
                    slip_or_bay_number="Evidence Bay D-3",
                    statutory_deadline="Sheriff Auction Date: Nov 28, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 16. 2019 Gulfstream G280 Executive Jet (SDNY Federal Forfeiture Docket)
            AssetLead(
                id="AEMH-2026-GULFSTREAM-G280",
                title="2019 Gulfstream G280 Super-Midsize Business Jet (DOJ Forfeiture)",
                category=AssetCategory.LUXURY_AIRCRAFT,
                make="Gulfstream",
                model="G280 (Honeywell HTF7250G)",
                year=2019,
                identifier_type="N-NUMBER",
                identifier_value="N280GA (SN: 2154)",
                identifier_masked="N280** (SN: 21**)",
                location_port_city="Teterboro Airport (TEB) / Fort Lauderdale",
                county="Broward County",
                state="FL",
                docket_or_case_number="USDC-SDNY-CR-24-1049-JSR",
                court_docket_authority="U.S. District Court for the Southern District of New York",
                seizure_type=SeizureType.US_MARSHALS_FORFEITURE,
                deal_stage=DealStage.SCHEDULED_FORFEITURE_AUCTION,
                auction_platform=AuctionPlatform.CWS_MARKETING,
                auction_date="2026-12-10 02:00 PM EST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.LUXURY_AIRCRAFT,
                    retail_value=14500000.0,
                    outstanding_lien_or_bid=6800000.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1540962351504-03099e0a754b?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1583073600538-fec186011e49?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.FAA_AC_FORM_8050_2,
                statutory_governing_law="18 U.S.C. § 981 & FAA Special Aviation Forfeiture Transfer",
                custodian=CustodianContact(
                    facility_name="Sheltair Aviation FLL Hangar",
                    contact_person="Director of Operations Marc Steiner",
                    phone="(954) 359-1200",
                    email="fll.operations@sheltairaviation.com",
                    physical_address="1100 Lee Wagener Blvd, Fort Lauderdale, FL 33315",
                    slip_or_bay_number="Executive Hangar 4",
                    statutory_deadline="Deposit Guarantee: Dec 05, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 17. 2022 68' Sunreef Supreme Power Catamaran (San Diego County, CA / Admiralty Arrest)
            AssetLead(
                id="AEMH-2026-SUNREEF-68",
                title="2022 68' Sunreef Supreme Power Catamaran - 'SOLAR OASIS' (Admiralty Arrest)",
                category=AssetCategory.CATAMARAN,
                make="Sunreef Yachts",
                model="Supreme 68 Power",
                year=2022,
                identifier_type="HIN",
                identifier_value="SRF68029C222",
                identifier_masked="SRF68029****",
                location_port_city="Port of San Diego Marine Basin",
                county="San Diego County",
                state="CA",
                docket_or_case_number="ADM-USDC-SDCA-25-CV-0189",
                court_docket_authority="U.S. District Court for the Southern District of California",
                seizure_type=SeizureType.ADMIRALTY_MARSHAL_ARREST,
                deal_stage=DealStage.ADMIRALTY_RULE_C_SALE,
                auction_platform=AuctionPlatform.NATIONAL_LIQUIDATORS,
                auction_date="2026-12-08 01:00 PM PST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.CATAMARAN,
                    retail_value=4200000.0,
                    outstanding_lien_or_bid=1900000.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1569263979104-865ab7cd8d17?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.USCG_BILL_OF_SALE_FORM_1340,
                statutory_governing_law="Federal Admiralty Rule C (46 U.S.C. § 31326)",
                custodian=CustodianContact(
                    facility_name="San Diego Marine Exchange Admiralty Slip",
                    contact_person="Harbor Custodian Robert Sterling",
                    phone="(619) 223-7159",
                    email="admiralty@sdmarine.com",
                    physical_address="2636 Shelter Island Dr, San Diego, CA 92106",
                    slip_or_bay_number="Slip C-20",
                    statutory_deadline="Hearing Confirmation: Dec 10, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 18. 2021 Caterpillar 336 Next Gen Hydraulic Excavator (Duval County - Jacksonville, FL)
            AssetLead(
                id="AEMH-2026-CAT-336",
                title="2021 Caterpillar 336 Next Gen Hydraulic Excavator (GovDeals / Municipal Impound)",
                category=AssetCategory.COMMERCIAL_HEAVY_DUTY,
                make="Caterpillar",
                model="336 Next Gen Excavator (Tier 4 Final)",
                year=2021,
                identifier_type="EQUIP-SN",
                identifier_value="CAT00336LDK09142",
                identifier_masked="CAT00336LDK09****",
                location_port_city="Jacksonville Port Industrial Depot",
                county="Duval County",
                state="FL",
                docket_or_case_number="DUVAL-GOVDEALS-LOT-8819",
                court_docket_authority="City of Jacksonville Public Works & Duval County Sheriff",
                seizure_type=SeizureType.COUNTY_SHERIFF_SALE,
                deal_stage=DealStage.SCHEDULED_FORFEITURE_AUCTION,
                auction_platform=AuctionPlatform.GOVDEALS_AUCTIONS,
                auction_date="2026-11-29 02:00 PM EST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.COMMERCIAL_HEAVY_DUTY,
                    retail_value=245000.0,
                    outstanding_lien_or_bid=78000.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.CLEAN_DMV_TITLE,
                statutory_governing_law="Florida Statute § 705.103 (Disposal of Abandoned Property)",
                custodian=CustodianContact(
                    facility_name="Duval County Heavy Equipment Impound",
                    contact_person="Logistics Chief Raymond Clark",
                    phone="(904) 630-1000",
                    email="surplus@coj.net",
                    physical_address="214 N Hogan St, Jacksonville, FL 32202",
                    slip_or_bay_number="Equipment Pad 7",
                    statutory_deadline="Auction Date: Nov 29, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 19. 2023 Aston Martin DBS Superleggera (Los Angeles County, CA / Sheriff Execution)
            AssetLead(
                id="AEMH-2026-ASTON-DBS",
                title="2023 Aston Martin DBS Superleggera - Onyx Black (Los Angeles County Sheriff)",
                category=AssetCategory.EXOTIC_CAR,
                make="Aston Martin",
                model="DBS Superleggera V12 Twin Turbo",
                year=2023,
                identifier_type="VIN",
                identifier_value="SCFRMFAW6PGL08912",
                identifier_masked="SCFRMFAW6PGL0****",
                location_port_city="Beverly Hills / Los Angeles Sheriff Depot",
                county="Los Angeles County",
                state="CA",
                docket_or_case_number="LASD-CIVIL-LEVY-2026-3021",
                court_docket_authority="Los Angeles County Superior Court (Civil Enforcement)",
                seizure_type=SeizureType.COUNTY_SHERIFF_SALE,
                deal_stage=DealStage.SCHEDULED_FORFEITURE_AUCTION,
                auction_platform=AuctionPlatform.COUNTY_MUNICIPAL_TOW,
                auction_date="2026-11-27 10:30 AM PST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.EXOTIC_CAR,
                    retail_value=335000.0,
                    outstanding_lien_or_bid=140000.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1544829099-b9a0c07fad1a?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.CLEAN_DMV_TITLE,
                statutory_governing_law="California Code of Civil Procedure § 701.540 (Sheriff Sale Notice)",
                custodian=CustodianContact(
                    facility_name="LASD Civil Management Branch",
                    contact_person="Deputy K. Johnson",
                    phone="(213) 974-6610",
                    email="civil@lasd.org",
                    physical_address="110 N Grand Ave, Los Angeles, CA 90012",
                    slip_or_bay_number="Secured Bay 11",
                    statutory_deadline="Sheriff Sale: Nov 27, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 20. 2022 Beechcraft King Air 350i (GSA Auctions / Fort Worth, TX)
            AssetLead(
                id="AEMH-2026-KINGAIR-350",
                title="2022 Beechcraft King Air 350i Executive Turboprop (GSA Federal Seizure)",
                category=AssetCategory.LUXURY_AIRCRAFT,
                make="Beechcraft",
                model="King Air 350i (Pro Line Fusion)",
                year=2022,
                identifier_type="N-NUMBER",
                identifier_value="N350FL (SN: FL-1289)",
                identifier_masked="N350** (SN: FL-****)",
                location_port_city="Fort Worth Meacham International (FTW)",
                county="Tarrant County",
                state="TX",
                docket_or_case_number="GSA-REG7-SEIZURE-2026-440",
                court_docket_authority="General Services Administration (GSA Auctions Regional)",
                seizure_type=SeizureType.US_MARSHALS_FORFEITURE,
                deal_stage=DealStage.SCHEDULED_FORFEITURE_AUCTION,
                auction_platform=AuctionPlatform.GSA_AUCTIONS,
                auction_date="2026-12-02 01:00 PM CST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.LUXURY_AIRCRAFT,
                    retail_value=6100000.0,
                    outstanding_lien_or_bid=2600000.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1540962351504-03099e0a754b?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1583073600538-fec186011e49?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.GSA_STANDARD_FORM_97,
                statutory_governing_law="40 U.S.C. § 545 (GSA Standard Form 97 Clear Transfer)",
                custodian=CustodianContact(
                    facility_name="Meacham Executive Aviation Depot",
                    contact_person="Federal Property Officer Alan Wright",
                    phone="(817) 392-5400",
                    email="property@gsa.gov",
                    physical_address="4201 N Main St, Fort Worth, TX 76106",
                    slip_or_bay_number="Hangar 2B",
                    statutory_deadline="Deposit Guarantee: Dec 01, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 21. 2023 Ford F-450 Super Duty Limited 6.7L (Hidalgo County - McAllen, TX / Border Seizure)
            AssetLead(
                id="AEMH-2026-F450-LIMITED",
                title="2023 Ford F-450 Super Duty Limited 6.7L High Output Dually 4x4",
                category=AssetCategory.LUXURY_SUV,
                make="Ford",
                model="F-450 Super Duty Limited Crew Cab Dually",
                year=2023,
                identifier_type="VIN",
                identifier_value="1FT8W4DT4PEC91820",
                identifier_masked="1FT8W4DT4PEC9****",
                location_port_city="McAllen Border Logistics Compound",
                county="Hidalgo County",
                state="TX",
                docket_or_case_number="CBP-HIDALGO-CR-2026-0941",
                court_docket_authority="U.S. Customs and Border Protection / Apple Towing",
                seizure_type=SeizureType.CUSTOMS_BORDER_SEIZURE,
                deal_stage=DealStage.SCHEDULED_FORFEITURE_AUCTION,
                auction_platform=AuctionPlatform.APPLE_TOWING_CO,
                auction_date="2026-11-19 11:00 AM CST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.LUXURY_SUV,
                    retail_value=105000.0,
                    outstanding_lien_or_bid=32000.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1520031441872-265e4ff70366?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.CLEAN_DMV_TITLE,
                statutory_governing_law="19 U.S.C. § 1607 (Summary Forfeiture Clear Title)",
                custodian=CustodianContact(
                    facility_name="Apple Towing McAllen Impound Facility",
                    contact_person="Regional Coordinator Javier Garza",
                    phone="(956) 682-1200",
                    email="mcallen@appletowing.com",
                    physical_address="1201 E Highway 83, McAllen, TX 78501",
                    slip_or_bay_number="Truck Bay 19",
                    statutory_deadline="Auction Gavel: Nov 19, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 22. 2021 83' Pershing 8X Carbon Superyacht (Monroe County - Marathon Keys, FL)
            AssetLead(
                id="AEMH-2026-PERSHING-8X",
                title="2021 83' Pershing 8X Carbon Superyacht - 'SILVER BULLET' (Admiralty Arrest)",
                category=AssetCategory.SUPERYACHT,
                make="Pershing",
                model="8X Carbon Yacht (Twin MTU 2638 HP)",
                year=2021,
                identifier_type="HIN",
                identifier_value="IT-PER08X04D121",
                identifier_masked="IT-PER08X04****",
                location_port_city="Marathon Key Marina Basin",
                county="Monroe County",
                state="FL",
                docket_or_case_number="ADM-USDC-SDFL-26-CV-8012",
                court_docket_authority="U.S. District Court (Admiralty Division PACER)",
                seizure_type=SeizureType.ADMIRALTY_MARSHAL_ARREST,
                deal_stage=DealStage.ADMIRALTY_RULE_C_SALE,
                auction_platform=AuctionPlatform.NATIONAL_LIQUIDATORS,
                auction_date="2026-12-12 02:00 PM EST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.SUPERYACHT,
                    retail_value=5900000.0,
                    outstanding_lien_or_bid=2500000.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1569263979104-865ab7cd8d17?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.USCG_BILL_OF_SALE_FORM_1340,
                statutory_governing_law="Federal Admiralty Rule C (46 U.S.C. § 31326)",
                custodian=CustodianContact(
                    facility_name="Faro Blanco Marina & Yacht Resort",
                    contact_person="Dockmaster Tyler Brooks",
                    phone="(305) 743-9018",
                    email="admiralty@faroblancoresort.com",
                    physical_address="1996 Overseas Hwy, Marathon, FL 33050",
                    slip_or_bay_number="Mega Yacht Pier 1",
                    statutory_deadline="Hearing Date: Dec 10, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 23. 2023 Bentley Continental GT Speed (Clark County - Las Vegas, NV / Judgment Foreclosure)
            AssetLead(
                id="AEMH-2026-BENTLEY-GT",
                title="2023 Bentley Continental GT Speed W12 - Beluga Edition (Casino Judgment Lien)",
                category=AssetCategory.EXOTIC_CAR,
                make="Bentley",
                model="Continental GT Speed W12",
                year=2023,
                identifier_type="VIN",
                identifier_value="SCBCG4ZG8PC091823",
                identifier_masked="SCBCG4ZG8PC09****",
                location_port_city="Las Vegas Luxury Impound Compound",
                county="Clark County",
                state="NV",
                docket_or_case_number="NV-CLARK-CIVIL-2026-4401",
                court_docket_authority="Eighth Judicial District Court of Nevada (Clark County)",
                seizure_type=SeizureType.COUNTY_SHERIFF_SALE,
                deal_stage=DealStage.SCHEDULED_FORFEITURE_AUCTION,
                auction_platform=AuctionPlatform.GOVDEALS_AUCTIONS,
                auction_date="2026-11-26 01:30 PM PST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.EXOTIC_CAR,
                    retail_value=320000.0,
                    outstanding_lien_or_bid=125000.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1583121274602-3e2820c69888?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.CLEAN_DMV_TITLE,
                statutory_governing_law="Nevada Revised Statutes § 21.130 (Execution and Sheriff Sales)",
                custodian=CustodianContact(
                    facility_name="Clark County Special Civil Execution Depot",
                    contact_person="Constable Office Deputy M. Ross",
                    phone="(702) 455-4055",
                    email="constables@clarkcountynv.gov",
                    physical_address="309 S 3rd St, Las Vegas, NV 89101",
                    slip_or_bay_number="Vault Strip Row 3",
                    statutory_deadline="Execution Sale: Nov 26, 2026"
                ),
                is_hot_deal=True,
                verified_by_sentinel=True
            ),

            # 24. 2020 42' Yellowfin Offshore Center Console (Hillsborough County - Tampa, FL)
            AssetLead(
                id="AEMH-2026-YELLOWFIN-42",
                title="2020 42' Yellowfin Offshore Center Console - Quad Mercury 450R (FWC Seizure)",
                category=AssetCategory.SPORTFISHER,
                make="Yellowfin",
                model="42 Offshore Center Console",
                year=2020,
                identifier_type="HIN",
                identifier_value="YFY42019A020",
                identifier_masked="YFY42019****",
                location_port_city="Tampa Bay Marine Operations Center",
                county="Hillsborough County",
                state="FL",
                docket_or_case_number="FL-FWC-SEIZURE-2026-092",
                court_docket_authority="13th Judicial Circuit Court (Hillsborough County, Florida)",
                seizure_type=SeizureType.CUSTOMS_BORDER_SEIZURE,
                deal_stage=DealStage.SCHEDULED_FORFEITURE_AUCTION,
                auction_platform=AuctionPlatform.COUNTY_MUNICIPAL_TOW,
                auction_date="2026-11-27 10:00 AM EST",
                underwriting=ExoticMarineUnderwriter.underwrite(
                    category=AssetCategory.SPORTFISHER,
                    retail_value=720000.0,
                    outstanding_lien_or_bid=285000.0
                ),
                images=[
                    "https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1569263979104-865ab7cd8d17?auto=format&fit=crop&w=1200&q=80"
                ],
                title_status=TitleStatus.USCG_BILL_OF_SALE_FORM_1340,
                statutory_governing_law="Florida Statute § 328.07 (Registration & Judicial Title Transfer)",
                custodian=CustodianContact(
                    facility_name="Tampa Bay Port Authority Marine Depot",
                    contact_person="Harbor Specialist Sean O'Donnell",
                    phone="(813) 905-7678",
                    email="marine.custody@tampaport.com",
                    physical_address="1101 Channelside Dr, Tampa, FL 33602",
                    slip_or_bay_number="Slip M-8",
                    statutory_deadline="Public Sale: Nov 27, 2026"
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
        if filters.county:
            result = [lead for lead in result if filters.county.lower() in lead.county.lower()]
        if filters.make:
            result = [lead for lead in result if filters.make.lower() in lead.make.lower()]
        if filters.min_spread:
            result = [lead for lead in result if lead.underwriting.projected_net_spread >= filters.min_spread]
        if filters.deal_stage:
            result = [lead for lead in result if lead.deal_stage == filters.deal_stage]
        if filters.seizure_type:
            result = [lead for lead in result if lead.seizure_type == filters.seizure_type]
        if filters.auction_platform:
            result = [lead for lead in result if filters.auction_platform.lower() in lead.auction_platform.value.lower()]
        if filters.q:
            query = filters.q.lower()
            result = [
                lead for lead in result if (
                    query in lead.title.lower() or
                    query in lead.make.lower() or
                    query in lead.model.lower() or
                    query in lead.county.lower() or
                    query in lead.location_port_city.lower() or
                    query in lead.docket_or_case_number.lower() or
                    query in lead.court_docket_authority.lower() or
                    query in lead.identifier_value.lower()
                )
            ]

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
            county=lead.county,
            state=lead.state,
            docket_or_case_number_masked=f"{lead.docket_or_case_number[:6]}****** [PRO UNLOCK REQUIRED]",
            court_docket_authority=lead.court_docket_authority,
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
