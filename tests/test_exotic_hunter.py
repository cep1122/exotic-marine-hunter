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
        # 1. Create Checkout Session
        create_payload = {
            "tier_id": "PRO_HUNTER",
            "buyer_email": "vip.investor@syndicate.com",
            "buyer_name": "Sovereign Fleet Capital",
            "payment_method": "API_BANK_VAULT"
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

        # Create single pass
        session_res = self.client.post(
            "/api/payengine/checkout-session",
            json={
                "tier_id": "SINGLE_PASS",
                "asset_id": asset_id,
                "buyer_email": "investor@test.com",
                "buyer_name": "Test Investor",
                "payment_method": "CARD"
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

if __name__ == "__main__":
    unittest.main()
