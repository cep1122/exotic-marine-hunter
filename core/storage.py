"""
Encrypted Evidence & Document Storage Engine
Proprietary Vault for Exotic & Marine Hunter AI (IC Neural Systems LLC)
Stores Title Abstracts, USCG Form 1340, USMS Form 102 & Marine Surveys with AES-256-GCM
"""

import uuid
import time
from typing import Dict, List, Optional, Any
from core.database import DB
from core.crypto_vault_256 import CRYPTO_VAULT_256

class DocumentStorageManager:
    """
    Sovereign Asset Evidence & Title Documentation Vault.
    Encrypts all sensitive legal papers at rest using AES-256-GCM.
    """

    _seeded = False

    @classmethod
    def seed_initial_evidence(cls):
        """Seeds initial verified government title dockets and mechanical surveys."""
        if cls._seeded:
            return

        sample_docs = [
            {
                "asset_id": "AEMH-2026-F8-01",
                "filename": "USMS_Form_102_Ferrari_F8_Forfeiture_Decree.pdf",
                "doc_type": "US_MARSHALS_FORFEITURE_DECREE",
                "content": "UNITED STATES DISTRICT COURT SOUTHERN DISTRICT OF FLORIDA. Docket: USMS-SD-FL-CR-24-9182-A. Final Order of Forfeiture transferring 2022 Ferrari F8 Tributo (VIN: ZFF92LLA8N0278914) to the United States Marshals Service free and clear of all liens and encumbrances pursuant to 18 U.S.C. 981."
            },
            {
                "asset_id": "AEMH-2026-SUN-74",
                "filename": "USCG_Abstract_of_Title_Sunseeker_74_Aurelia.pdf",
                "doc_type": "USCG_ABSTRACT_OF_TITLE",
                "content": "UNITED STATES COAST GUARD NATIONAL VESSEL DOCUMENTATION CENTER. Official Number: 1290812. Vessel Name: AURELIA (HIN: XSK05891A121). Admiralty Rule C in Rem Arrest confirmed by U.S. District Court. Judicial sale conveys clear maritime title free of all prior maritime liens and bottomry bonds."
            },
            {
                "asset_id": "AEMH-2026-RR-CULL",
                "filename": "Florida_Statute_713_78_Tow_Storage_Lien_Affidavit.pdf",
                "doc_type": "STORAGE_LIEN_AFFIDAVIT",
                "content": "STATE OF FLORIDA, COUNTY OF PALM BEACH. Statutory Notice of Public Sale pursuant to Florida Statute 713.78. Vehicle: 2023 Rolls-Royce Cullinan (VIN: SCA681S56PU190823). Unpaid towing and climate-controlled storage balance: $18,500.00. Statutory redemption notice served. Florida HSMV Form 82040 issued to purchaser."
            },
            {
                "asset_id": "AEMH-2026-VIK-62",
                "filename": "SAMS_Marine_Survey_Viking_62_Convertible.pdf",
                "doc_type": "SAMS_MARINE_SURVEY",
                "content": "SOCIETY OF ACCREDITED MARINE SURVEYORS (SAMS) CONDITION & VALUATION SURVEY. 2020 62' Viking Convertible Sportfisher. Hull Sounding: Moisture meter tests normal across cored fiberglass hull. Twin CAT C32A Diesel Engines (1,925 HP each) oil spectrochemical analysis: Normal wear metals within OEM Caterpillar baseline."
            }
        ]

        for doc in sample_docs:
            cls.store_document(
                asset_id=doc["asset_id"],
                filename=doc["filename"],
                doc_type=doc["doc_type"],
                raw_text=doc["content"]
            )
        cls._seeded = True

    @classmethod
    def store_document(cls, asset_id: str, filename: str, doc_type: str, raw_text: str) -> Dict[str, Any]:
        """Encrypts raw text with AES-256-GCM and stores in database."""
        encrypted_token = CRYPTO_VAULT_256.encrypt_256(raw_text, associated_data=f"DOC_{asset_id}")
        checksum = CRYPTO_VAULT_256.sha256_hash(raw_text)
        doc_id = f"DOC-{uuid.uuid4().hex[:10].upper()}"
        now = int(time.time())

        with DB.get_connection() as conn:
            cursor = conn.cursor()
            # Check if filename already exists for asset
            cursor.execute("SELECT id FROM stored_documents WHERE asset_id = ? AND filename = ?", (asset_id, filename))
            existing = cursor.fetchone()
            if existing:
                return {"id": existing["id"], "asset_id": asset_id, "filename": filename, "checksum": checksum}

            cursor.execute("""
            INSERT INTO stored_documents (id, asset_id, filename, document_type, encrypted_payload, sha256_checksum, uploaded_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (doc_id, asset_id, filename, doc_type, encrypted_token, checksum, now))
            conn.commit()

        return {
            "id": doc_id,
            "asset_id": asset_id,
            "filename": filename,
            "document_type": doc_type,
            "sha256_checksum": checksum,
            "uploaded_at": now
        }

    @classmethod
    def get_documents_for_asset(cls, asset_id: str) -> List[Dict[str, Any]]:
        cls.seed_initial_evidence()
        with DB.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT id, asset_id, filename, document_type, sha256_checksum, uploaded_at
            FROM stored_documents WHERE asset_id = ? ORDER BY uploaded_at DESC
            """, (asset_id,))
            return [dict(row) for row in cursor.fetchall()]

    @classmethod
    def retrieve_and_decrypt_document(cls, doc_id: str) -> Optional[Dict[str, Any]]:
        cls.seed_initial_evidence()
        with DB.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT id, asset_id, filename, document_type, encrypted_payload, sha256_checksum, uploaded_at
            FROM stored_documents WHERE id = ?
            """, (doc_id,))
            row = cursor.fetchone()
            if not row:
                return None

            try:
                decrypted_content = CRYPTO_VAULT_256.decrypt_256(
                    row["encrypted_payload"],
                    associated_data=f"DOC_{row['asset_id']}"
                )
            except Exception as e:
                decrypted_content = f"[DECRYPTION_ERROR: {str(e)}]"

            return {
                "id": row["id"],
                "asset_id": row["asset_id"],
                "filename": row["filename"],
                "document_type": row["document_type"],
                "sha256_checksum": row["sha256_checksum"],
                "uploaded_at": row["uploaded_at"],
                "decrypted_content": decrypted_content
            }

DOCUMENT_STORAGE = DocumentStorageManager
