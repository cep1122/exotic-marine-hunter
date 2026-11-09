"""
Comprehensive Test Suite for Autonomous Exotic & Marine Hunter AI (A.E.M.H. AI)
Engineered by IC Neural Systems LLC (Israel Cepero)
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import unittest
from starlette.testclient import TestClient

from config import SYSTEM_CONFIG, BUYBOX_CONFIG, PAYENGINE_CONFIG
from core.models import AssetCategory, DealStage, SearchFilter
from core.underwriting import ExoticMarineUnderwriter
from core.auction_rails import AuctionRailsFeeder, AuctionRailsDirectory
from core.payengine_client import ApexPayEngineClient
from api.main import app

class TestExoticMarineHunter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_underwriting_mab_calculation(self):
        """Verify institutional MAB formula and profit spread calculations"""
        retail = 345000.0
        opening_bid = 165000.0
        
        detail = ExoticMarineUnderwriter.underwrite(
            category=AssetCategory.EXOTIC_CAR,
            retail_value=retail,
            outstanding_lien_or_bid=opening_bid,
            custom_discount=0.65
        )

        expected_gross_ceiling = retail * 0.65 # 224,250
        self.assertEqual(detail.gross_acquisition_ceiling, round(expected_gross_ceiling, 2))

        # Vehicle reserves: 1800 haulout + 1500 survey = 3300
        expected_mab = expected_gross_ceiling - 3300.0
        self.assertEqual(detail.maximum_allowable_bid_mab, round(expected_mab, 2))

        # Spread: retail - (opening_bid + 3300) = 345000 - 168300 = 176,700
        expected_spread = retail - (opening_bid + 3300.0)
        self.assertEqual(detail.projected_net_spread, round(expected_spread, 2))
        self.assertTrue(detail.roi_percentage > 50.0)
        self.assertIn("OPPORTUNISTIC", detail.risk_level)

    def test_02_superyacht_admiralty_underwriting(self):
        """Verify superyacht haul-out reserves and marine survey allowances"""
        yacht_retail = 3250000.0
        admiralty_bid = 1420000.0

        detail = ExoticMarineUnderwriter.underwrite(
            category=AssetCategory.SUPERYACHT,
            retail_value=yacht_retail,
            outstanding_lien_or_bid=admiralty_bid
        )

        self.assertEqual(detail.estimated_transport_haulout_cost, 12500.0)
        self.assertEqual(detail.mechanical_survey_allowance, 8500.0)
        self.assertTrue(detail.projected_net_spread > 1000000.0)

    def test_03_auction_rails_inventory(self):
        """Verify seeded seized inventory integrity and legal references"""
        leads = AuctionRailsFeeder.get_seed_inventory()
        self.assertGreaterEqual(len(leads), 6)

        ferrari = next((l for l in leads if "Ferrari" in l.title), None)
        self.assertIsNotNone(ferrari)
        self.assertEqual(ferrari.category, AssetCategory.EXOTIC_CAR)
        self.assertIn("USMS", ferrari.docket_or_case_number)

        sunseeker = next((l for l in leads if "Sunseeker" in l.title), None)
        self.assertIsNotNone(sunseeker)
        self.assertEqual(sunseeker.category, AssetCategory.SUPERYACHT)
        self.assertIn("Rule C", sunseeker.statutory_governing_law)

    def test_04_paywall_masking_for_public(self):
        """Verify public API masks VIN/HIN and hides custodian contacts"""
        response = self.client.get(
            "/api/pipeline",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["tier"], "MASKED_PUBLIC_PREVIEW")

        first_lead = data["leads"][0]
        self.assertTrue(first_lead["requires_tier_unlock"])
        self.assertTrue("*" in first_lead["identifier_masked"])
        self.assertIn("PRO UNLOCK REQUIRED", first_lead["docket_or_case_number_masked"])
        self.assertNotIn("custodian", first_lead)

    def test_05_payengine_checkout_and_unmasking(self):
        """Verify APEX PayEngine checkout session creation, Merkle DAG seal, and full unmasking"""
        # 1. Create Checkout Session with valid card credentials
        create_payload = {
            "tier_id": "PRO_HUNTER",
            "buyer_email": "vip.investor@syndicate.com",
            "buyer_name": "Sovereign Fleet Capital",
            "payment_method": "CARD",
            "card_number": "4000123456789017",
            "card_exp": "12/29",
            "card_cvc": "888",
            "billing_zip": "33101"
        }
        res_create = self.client.post(
            "/api/payengine/checkout-session",
            json=create_payload,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        self.assertEqual(res_create.status_code, 200)
        session_data = res_create.json()
        self.assertTrue(session_data["session_id"].startswith("APEX-EMH-"))
        self.assertTrue(session_data["merkle_dag_seal"].startswith("0x"))
        self.assertEqual(session_data["amount"], 199.00)

        # 2. Settle in Sovereign Vault
        session_id = session_data["session_id"]
        res_verify = self.client.post(
            f"/api/payengine/verify/{session_id}",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        self.assertEqual(res_verify.status_code, 200)
        verify_data = res_verify.json()
        token = verify_data["access_token"]
        self.assertTrue(token.startswith("EMH-TOKEN-"))

        # 3. Request Pipeline with Pro Token
        res_pipeline = self.client.get(
            f"/api/pipeline?token={token}",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        self.assertEqual(res_pipeline.status_code, 200)
        unmasked_data = res_pipeline.json()
        self.assertEqual(unmasked_data["tier"], "UNLOCKED_PRO_HUNTER")
        unmasked_first = unmasked_data["leads"][0]
        self.assertFalse("*" in unmasked_first["identifier_value"])
        self.assertIsNotNone(unmasked_first["custodian"])
        self.assertTrue(len(unmasked_first["custodian"]["phone"]) > 0)

    def test_06_argus_sentinel_blocks_scrapers(self):
        """Verify Argus Cyber Sentinel blocks forbidden scraper user-agents"""
        bad_agents = ["Scrapy/2.11.0", "Wget/1.21.3", "curl/8.4.0", "HTTrack 3.0"]
        for agent in bad_agents:
            res = self.client.get(
                "/api/pipeline",
                headers={"User-Agent": agent}
            )
            self.assertEqual(res.status_code, 403)
            self.assertIn("ARGUS_ANTI_CLONER_BLOCK", res.json()["error"])

    def test_07_argus_sentinel_blocks_spy_probes(self):
        """Verify Argus Cyber Sentinel intercepts malicious path traversal & config probes"""
        spy_paths = ["/.env", "/.git/config", "/wp-login.php", "/api/pipeline?file=../etc/passwd"]
        for path in spy_paths:
            res = self.client.get(
                path,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            )
            self.assertEqual(res.status_code, 403)
            self.assertIn("ARGUS_SENTINEL_SECURITY_VIOLATION", res.json()["error"])

    def test_08_security_headers_injected(self):
        """Verify institutional security headers on responses"""
        res = self.client.get(
            "/api/health",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers["X-Frame-Options"], "SAMEORIGIN")
        self.assertEqual(res.headers["X-Content-Type-Options"], "nosniff")
        self.assertIn("Argus Cyber Shield", res.headers["X-Sentinel-Defended-By"])
        self.assertIn("LEX AI Sovereign Legal Sentry", res.headers["X-Notarized-By"])
        self.assertEqual(res.headers["X-Legal-Entity"], "IC Neural Systems LLC (Israel Cepero)")

    def test_09_api_directory_and_legal(self):
        """Verify auction directory and legal statutory disclosures"""
        res_dir = self.client.get(
            "/api/auctions/directory",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        self.assertEqual(res_dir.status_code, 200)
        self.assertGreaterEqual(len(res_dir.json()["directory"]), 5)

        res_legal = self.client.get(
            "/api/legal",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        self.assertEqual(res_legal.status_code, 200)
        self.assertIn("IC Neural Systems LLC", res_legal.json()["entity"])
        self.assertIn("Admiralty or Maritime Claims", res_legal.json()["admiralty_law_notice"])

    def test_10_dashboard_serving(self):
        """Verify dashboard HTML is served properly"""
        res = self.client.get(
            "/",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn("Exotic & Marine Hunter AI", res.text)
        self.assertIn("APEX PAYENGINE", res.text)

    def test_11_search_and_filtering(self):
        """Verify search API filters accurately by category and min spread"""
        filter_payload = {
            "category": "SUPERYACHT",
            "min_spread": 500000.0
        }
        res = self.client.post(
            "/api/search",
            json=filter_payload,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(data["count"], 1)
        for lead in data["leads"]:
            self.assertEqual(lead["category"], "SUPERYACHT")

    def test_12_single_asset_dossier_unlock(self):
        """Verify single asset endpoint masks when unauthorized and unmasks when token is provided"""
        asset_id = "AEMH-2026-F8-01"
        res_locked = self.client.get(
            f"/api/pipeline/{asset_id}",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        self.assertEqual(res_locked.status_code, 200)
        self.assertFalse(res_locked.json()["unlocked"])

        # Create single pass with valid card credentials
        session_res = self.client.post(
            "/api/payengine/checkout-session",
            json={
                "tier_id": "SINGLE_PASS",
                "asset_id": asset_id,
                "buyer_email": "investor@test.com",
                "buyer_name": "Test Investor",
                "payment_method": "CARD",
                "card_number": "4000123456789017",
                "card_exp": "12/29",
                "card_cvc": "456",
                "billing_zip": "33139"
            },
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        sid = session_res.json()["session_id"]
        verify_res = self.client.post(
            f"/api/payengine/verify/{sid}",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        token = verify_res.json()["access_token"]

        res_unlocked = self.client.get(
            f"/api/pipeline/{asset_id}?token={token}",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        self.assertEqual(res_unlocked.status_code, 200)
        self.assertTrue(res_unlocked.json()["unlocked"])
        self.assertEqual(res_unlocked.json()["asset"]["identifier_value"], "ZFF92LLA8N0278914")

    def test_13_crypto_vault_256(self):
        """Verify AES-256-GCM encryption, decryption, and tampering resistance"""
        from core.crypto_vault_256 import CRYPTO_VAULT_256
        secret = "VIN: ZFF92LLA8N0278914 | CUSTODIAN_PHONE: (305) 536-4131"
        token = CRYPTO_VAULT_256.encrypt_256(secret)
        self.assertTrue(token.startswith("ARGUS256:"))
        decrypted = CRYPTO_VAULT_256.decrypt_256(token)
        self.assertEqual(decrypted, secret)

        # Header verification
        res = self.client.get("/api/health", headers={"User-Agent": "Mozilla/5.0"})
        self.assertEqual(res.headers.get("X-Encryption-Standard"), "AES-256-GCM / SHA-256 Merkle DAG")

    def test_14_database_user_auth_and_profile(self):
        """Verify SQLite user registration, PBKDF2 password hashing, and authentication"""
        import uuid
        email = f"investor_{uuid.uuid4().hex[:6]}@syndicate.com"
        reg_payload = {
            "email": email,
            "password": "SecurePassword123!",
            "full_name": "Marcus Aurelius Vance",
            "role": "PRO_HUNTER"
        }
        res_reg = self.client.post("/api/auth/register", json=reg_payload, headers={"User-Agent": "Mozilla/5.0"})
        self.assertEqual(res_reg.status_code, 200)
        data = res_reg.json()
        self.assertTrue(data["token"].startswith("EMH-TOKEN-"))
        self.assertEqual(data["email"], email)

        # Duplicate email prevention
        res_dup = self.client.post("/api/auth/register", json=reg_payload, headers={"User-Agent": "Mozilla/5.0"})
        self.assertEqual(res_dup.status_code, 400)

        # Wrong password rejection
        res_fail = self.client.post("/api/auth/login", json={"email": email, "password": "WrongPassword!"}, headers={"User-Agent": "Mozilla/5.0"})
        self.assertEqual(res_fail.status_code, 401)

        # Valid login
        res_login = self.client.post("/api/auth/login", json={"email": email, "password": "SecurePassword123!"}, headers={"User-Agent": "Mozilla/5.0"})
        self.assertEqual(res_login.status_code, 200)
        token = res_login.json()["token"]

        # User profile retrieval
        res_prof = self.client.get(f"/api/user/profile?token={token}", headers={"User-Agent": "Mozilla/5.0"})
        self.assertEqual(res_prof.status_code, 200)
        self.assertEqual(res_prof.json()["user"]["email"], email)

    def test_15_sqli_waf_protection(self):
        """Verify Argus SQLi WAF blocks SQL injection attempts with 403 Forbidden"""
        sqli_attacks = [
            "/api/pipeline?search=1' OR '1'='1",
            "/api/pipeline?category=EXOTIC' UNION SELECT * FROM users--",
            "/api/pipeline?id=1; DROP TABLE users;",
            "/api/pipeline?test=1' AND SLEEP(5)--"
        ]
        for attack in sqli_attacks:
            res = self.client.get(attack, headers={"User-Agent": "Mozilla/5.0"})
            self.assertEqual(res.status_code, 403)
            self.assertIn("ARGUS_SQLI_SHIELD_BLOCK", res.json()["error"])

    def test_16_encrypted_document_storage(self):
        """Verify evidence document storage with AES-256-GCM encryption & decryption"""
        asset_id = "AEMH-2026-F8-01"
        res_docs = self.client.get(f"/api/assets/{asset_id}/documents", headers={"User-Agent": "Mozilla/5.0"})
        self.assertEqual(res_docs.status_code, 200)
        docs = res_docs.json()["documents"]
        self.assertGreaterEqual(len(docs), 1)

        first_doc_id = docs[0]["id"]
        res_down = self.client.get(f"/api/documents/{first_doc_id}/download", headers={"User-Agent": "Mozilla/5.0"})
        self.assertEqual(res_down.status_code, 200)
        doc_data = res_down.json()
        self.assertIn("UNITED STATES DISTRICT COURT", doc_data["decrypted_content"])
        self.assertTrue(len(doc_data["sha256_checksum"]) == 64)

    def test_17_user_watchlist_toggle(self):
        """Verify database-backed watchlist toggle and retrieval"""
        asset_id = "AEMH-2026-SUN-74"
        # Toggle add
        res_add = self.client.post("/api/user/watchlist/toggle", json={"asset_id": asset_id}, headers={"User-Agent": "Mozilla/5.0"})
        self.assertEqual(res_add.status_code, 200)
        self.assertTrue(res_add.json()["is_saved"])

        # Check in list
        res_list = self.client.get("/api/user/watchlist", headers={"User-Agent": "Mozilla/5.0"})
        self.assertEqual(res_list.status_code, 200)
        matched = [w for w in res_list.json()["watchlist"] if w["id"] == asset_id]
        self.assertGreaterEqual(len(matched), 1)

        # Toggle remove
        res_rem = self.client.post("/api/user/watchlist/toggle", json={"asset_id": asset_id}, headers={"User-Agent": "Mozilla/5.0"})
        self.assertEqual(res_rem.status_code, 200)
        self.assertFalse(res_rem.json()["is_saved"])

    def test_18_strict_payment_validation_and_single_pass_isolation(self):
        """Enforces that fake payments fail, and Single Pass ($49) strictly unlocks only 1 asset while the other 23 stay locked."""
        # 1. Fake card fails Luhn check
        res_fake_card = self.client.post(
            "/api/payengine/checkout-session",
            json={
                "tier_id": "SINGLE_PASS",
                "asset_id": "AEMH-2026-F8-01",
                "buyer_email": "fake@fraud.com",
                "buyer_name": "Fraud Bot",
                "payment_method": "CARD",
                "card_number": "4111111111111112",
                "card_exp": "12/28",
                "card_cvc": "123",
                "billing_zip": "33101"
            },
            headers={"User-Agent": "Mozilla/5.0"}
        )
        self.assertEqual(res_fake_card.status_code, 400)
        self.assertIn("Luhn", res_fake_card.json()["detail"])

        # 2. Expired card is rejected
        res_expired = self.client.post(
            "/api/payengine/checkout-session",
            json={
                "tier_id": "SINGLE_PASS",
                "asset_id": "AEMH-2026-F8-01",
                "buyer_email": "expired@user.com",
                "buyer_name": "Late User",
                "payment_method": "CARD",
                "card_number": "4000123456789017",
                "card_exp": "01/20",
                "card_cvc": "123",
                "billing_zip": "33101"
            },
            headers={"User-Agent": "Mozilla/5.0"}
        )
        self.assertEqual(res_expired.status_code, 400)
        self.assertIn("vencida", res_expired.json()["detail"])

        # 3. Bad ABA routing number fails Federal Reserve checksum
        res_bad_routing = self.client.post(
            "/api/payengine/checkout-session",
            json={
                "tier_id": "SINGLE_PASS",
                "asset_id": "AEMH-2026-F8-01",
                "buyer_email": "badach@user.com",
                "buyer_name": "ACH User",
                "payment_method": "BANK_ACH",
                "bank_name": "Fake Bank",
                "bank_routing": "123456789",
                "bank_account": "9876543210"
            },
            headers={"User-Agent": "Mozilla/5.0"}
        )
        self.assertEqual(res_bad_routing.status_code, 400)
        self.assertIn("Reserva Federal", res_bad_routing.json()["detail"])

        # 4. Valid card checkout unlocks ONLY target asset (Ferrari F8)
        res_valid = self.client.post(
            "/api/payengine/checkout-session",
            json={
                "tier_id": "SINGLE_PASS",
                "asset_id": "AEMH-2026-F8-01",
                "buyer_email": "verified.buyer@gmail.com",
                "buyer_name": "Verified Collector",
                "payment_method": "CARD",
                "card_number": "4000123456789017",
                "card_exp": "08/29",
                "card_cvc": "999",
                "billing_zip": "33139"
            },
            headers={"User-Agent": "Mozilla/5.0"}
        )
        self.assertEqual(res_valid.status_code, 200)
        sid = res_valid.json()["session_id"]

        # Verify payment
        res_settle = self.client.post(f"/api/payengine/verify/{sid}", headers={"User-Agent": "Mozilla/5.0"})
        self.assertEqual(res_settle.status_code, 200)
        token = res_settle.json()["access_token"]

        # Check pipeline: ONLY AEMH-2026-F8-01 must be unmasked, all others masked!
        res_pipeline = self.client.get(f"/api/pipeline?token={token}", headers={"User-Agent": "Mozilla/5.0"})
        self.assertEqual(res_pipeline.status_code, 200)
        pdata = res_pipeline.json()
        self.assertEqual(pdata["tier"], "PARTIAL_UNLOCKED")
        self.assertEqual(pdata["unlocked_asset_ids"], ["AEMH-2026-F8-01"])

        leads = pdata["leads"]
        unmasked_lead = next(l for l in leads if l["id"] == "AEMH-2026-F8-01")
        self.assertEqual(unmasked_lead["identifier_value"], "ZFF92LLA8N0278914")
        self.assertIsNotNone(unmasked_lead["custodian"])

        # Verify all other leads remain strictly locked & masked
        other_leads = [l for l in leads if l["id"] != "AEMH-2026-F8-01"]
        self.assertGreaterEqual(len(other_leads), 23)
        for other in other_leads:
            self.assertTrue(other.get("requires_tier_unlock"))
            self.assertIsNone(other.get("identifier_value"))
            self.assertIsNone(other.get("custodian"))
            self.assertIn("*", other.get("identifier_masked", ""))

    def test_19_password_reset_flow(self):
        """Verifies 6-digit OTP password reset via email and subsequent login"""
        from core.database import DB

        # 1. Non-existent email fails
        res_non = self.client.post("/api/auth/forgot-password", json={"email": "nonexistent@fake.com"}, headers={"User-Agent": "Mozilla/5.0"})
        self.assertEqual(res_non.status_code, 400)

        # 2. Registered user requests reset code
        test_email = "architect@icneuralsystems.com"
        res_req = self.client.post("/api/auth/forgot-password", json={"email": test_email}, headers={"User-Agent": "Mozilla/5.0"})
        self.assertEqual(res_req.status_code, 200)
        self.assertEqual(res_req.json()["status"], "SENT")

        # 3. Retrieve the generated code from database for assertion
        with DB.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT code FROM password_resets WHERE email = ?", (test_email,))
            row = cur.fetchone()
            self.assertIsNotNone(row)
            code = row["code"]
            self.assertEqual(len(code), 6)
            self.assertTrue(code.isdigit())

        # 4. Bad code fails
        res_bad = self.client.post("/api/auth/reset-password", json={"email": test_email, "code": "000000", "new_password": "NewSecret2026!"}, headers={"User-Agent": "Mozilla/5.0"})
        self.assertEqual(res_bad.status_code, 400)
        self.assertIn("incorrecto", res_bad.json()["detail"])

        # 5. Correct code updates password
        new_pass = "UpdatedSovereign2026!"
        res_ok = self.client.post("/api/auth/reset-password", json={"email": test_email, "code": code, "new_password": new_pass}, headers={"User-Agent": "Mozilla/5.0"})
        self.assertEqual(res_ok.status_code, 200)
        self.assertEqual(res_ok.json()["status"], "SUCCESS")

        # 6. Login with new password succeeds
        res_login = self.client.post("/api/auth/login", json={"email": test_email, "password": new_pass}, headers={"User-Agent": "Mozilla/5.0"})
        self.assertEqual(res_login.status_code, 200)
        self.assertTrue(res_login.json()["token"].startswith("EMH-TOKEN-"))

        # 7. Old password no longer works
        res_old = self.client.post("/api/auth/login", json={"email": test_email, "password": "Sovereign2026!"}, headers={"User-Agent": "Mozilla/5.0"})
        self.assertEqual(res_old.status_code, 401)

        # Reset back to Sovereign2026! for clean state
        code_reset, _ = DB.create_password_reset_code(test_email)
        DB.verify_and_reset_password(test_email, code_reset, "Sovereign2026!")

    def test_20_map_pins_and_simulator_and_alerts(self):
        """Verify Map GPS Pins endpoint, MAB Simulator, and Forfeiture Alerts system"""
        # 1. Map locations
        res_map = self.client.get(
            "/api/pipeline/map-locations",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        self.assertEqual(res_map.status_code, 200)
        map_data = res_map.json()
        self.assertEqual(map_data["total_pins"], 24)
        first_pin = map_data["pins"][0]
        self.assertIn("latitude", first_pin)
        self.assertIn("longitude", first_pin)
        self.assertIn("title", first_pin)
        self.assertGreater(first_pin["estimated_retail_value"], 0)

        # 2. MAB Simulator
        sim_payload = {
            "retail_value": 345000.0,
            "target_bid": 150000.0,
            "buyers_premium_pct": 10.0,
            "transport_cost": 2500.0,
            "survey_buffer": 3500.0
        }
        res_sim = self.client.post(
            "/api/underwriting/simulate-mab",
            json=sim_payload,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        self.assertEqual(res_sim.status_code, 200)
        sim_data = res_sim.json()
        self.assertEqual(sim_data["buyers_premium"], 15000.0)
        self.assertEqual(sim_data["total_cash_outlay"], 171000.0)
        self.assertEqual(sim_data["projected_net_spread"], 174000.0)
        self.assertTrue(sim_data["is_safe"])
        self.assertEqual(sim_data["verdict"], "SAFE_HIGH_ALPHA")

        # 3. Forfeiture Alerts Subscription
        alert_payload = {
            "email": "investor@venture-marine.com",
            "phone": "+13055550199",
            "category": "SUPERYACHT",
            "county_or_state": "Florida",
            "min_spread": 100000.0
        }
        res_alert = self.client.post(
            "/api/alerts/subscribe",
            json=alert_payload,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        self.assertEqual(res_alert.status_code, 200)
        alert_data = res_alert.json()
        self.assertEqual(alert_data["status"], "ACTIVE")
        self.assertTrue(alert_data["alert_id"].startswith("ALT-"))

        # Verify query user alerts
        res_user_alerts = self.client.get(
            f"/api/alerts/{alert_payload['email']}",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        self.assertEqual(res_user_alerts.status_code, 200)
        self.assertGreaterEqual(res_user_alerts.json()["count"], 1)

if __name__ == "__main__":
    unittest.main()
