"""
Database Engine & Persistence Layer for Exotic & Marine Hunter AI
Proprietary Architecture by IC Neural Systems LLC (Israel Cepero)
Thread-safe SQLite with Parameterized Prepared Statements & Cryptographic Passwords
"""

import os
import sqlite3
import hashlib
import time
import uuid
import json
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
from core.crypto_vault_256 import CRYPTO_VAULT_256

# In serverless (Vercel), write to /tmp; in local/persistent environments write to local project root
def get_db_path() -> str:
    if os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        return "/tmp/exotic_marine_hunter.db"
    return str(Path(__file__).resolve().parent.parent / "exotic_marine_hunter.db")

class DatabaseManager:
    """
    Thread-safe SQLite Database Manager with 100% Parameterized Queries.
    Prevents SQL injection vulnerabilities and enforces 256-bit password hashing.
    """

    _instance = None

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or get_db_path()
        self._init_db()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=15.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA foreign_keys = ON;")
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self):
        """Initializes normalized database schema with prepared constraints."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Users Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'PRO_HUNTER',
                api_bank_wallet_id TEXT NOT NULL,
                wallet_balance REAL DEFAULT 0.0,
                created_at INTEGER NOT NULL
            );
            """)

            # 2. User Unlocked Dossiers Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_unlocked_dossiers (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                asset_id TEXT NOT NULL,
                unlocked_at INTEGER NOT NULL,
                access_token TEXT NOT NULL,
                transaction_hash TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
            """)

            # 3. User Watchlist Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_watchlist (
                user_id TEXT NOT NULL,
                asset_id TEXT NOT NULL,
                saved_at INTEGER NOT NULL,
                PRIMARY KEY (user_id, asset_id),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
            """)

            # 4. Encrypted Evidence Documents Storage Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS stored_documents (
                id TEXT PRIMARY KEY,
                asset_id TEXT NOT NULL,
                filename TEXT NOT NULL,
                document_type TEXT NOT NULL,
                encrypted_payload TEXT NOT NULL,
                sha256_checksum TEXT NOT NULL,
                uploaded_at INTEGER NOT NULL
            );
            """)

            # 5. Security & Access Audit Logs Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS security_audit_logs (
                id TEXT PRIMARY KEY,
                ip_address TEXT NOT NULL,
                user_agent TEXT NOT NULL,
                action TEXT NOT NULL,
                status TEXT NOT NULL,
                details TEXT,
                timestamp INTEGER NOT NULL
            );
            """)

            # 5b. Password Resets OTP Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS password_resets (
                email TEXT PRIMARY KEY,
                code TEXT NOT NULL,
                expires_at INTEGER NOT NULL,
                created_at INTEGER NOT NULL
            );
            """)

            # 6. Master Asset Leads Pipeline Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS asset_leads (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER NOT NULL,
                identifier_type TEXT NOT NULL,
                identifier_value TEXT NOT NULL,
                identifier_masked TEXT NOT NULL,
                location_port_city TEXT NOT NULL,
                county TEXT NOT NULL,
                state TEXT NOT NULL,
                docket_or_case_number TEXT NOT NULL,
                court_docket_authority TEXT NOT NULL,
                seizure_type TEXT NOT NULL,
                deal_stage TEXT NOT NULL,
                auction_platform TEXT NOT NULL,
                auction_date TEXT NOT NULL,
                estimated_retail_value REAL NOT NULL,
                outstanding_lien_or_opening_bid REAL NOT NULL,
                maximum_allowable_bid_mab REAL NOT NULL,
                projected_net_spread REAL NOT NULL,
                roi_percentage REAL NOT NULL,
                title_status TEXT NOT NULL,
                statutory_governing_law TEXT NOT NULL,
                raw_json TEXT NOT NULL,
                updated_at INTEGER NOT NULL
            );
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_assets_county ON asset_leads(county);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_assets_category ON asset_leads(category);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_assets_state ON asset_leads(state);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_assets_platform ON asset_leads(auction_platform);")

            conn.commit()

        # Seed default demonstration user if not present
        self._seed_default_user()
        # Seed master asset catalog
        self._sync_seed_assets()

    def _hash_password(self, password: str, salt: str) -> str:
        """Derives a PBKDF2-HMAC-SHA256 password hash (100,000 iterations)."""
        return hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100_000
        ).hex()

    def _seed_default_user(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = ?", ("architect@icneuralsystems.com",))
            if not cursor.fetchone():
                salt = uuid.uuid4().hex
                pwd_hash = self._hash_password("Sovereign2026!", salt)
                user_id = "USR-IC-001"
                now = int(time.time())
                cursor.execute("""
                INSERT INTO users (id, email, password_hash, salt, full_name, role, api_bank_wallet_id, wallet_balance, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    "architect@icneuralsystems.com",
                    pwd_hash,
                    salt,
                    "Israel Cepero (Founder & Principal)",
                    "INSTITUTIONAL_VIP",
                    "VAULT-EXOTIC-MARINE-PRIMARY",
                    500000.00,
                    now
                ))
                # Seed default unlocked assets for the founder
                cursor.execute("""
                INSERT OR IGNORE INTO user_unlocked_dossiers (id, user_id, asset_id, unlocked_at, access_token, transaction_hash)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    f"UNL-{uuid.uuid4().hex[:8]}",
                    user_id,
                    "AEMH-2026-F8-01",
                    now,
                    "EMH-MASTER-VIP-001",
                    "0x" + hashlib.sha256(b"SEED_UNLOCKED_F8").hexdigest()
                ))
                conn.commit()

    def _sync_seed_assets(self):
        """Populates the SQLite asset table with rich pipeline leads."""
        try:
            from core.auction_rails import AuctionRailsFeeder
            leads = AuctionRailsFeeder.get_seed_inventory()
            now = int(time.time())
            with self.get_connection() as conn:
                cursor = conn.cursor()
                for lead in leads:
                    cursor.execute("""
                    INSERT OR REPLACE INTO asset_leads (
                        id, title, category, make, model, year, identifier_type,
                        identifier_value, identifier_masked, location_port_city,
                        county, state, docket_or_case_number, court_docket_authority,
                        seizure_type, deal_stage, auction_platform, auction_date,
                        estimated_retail_value, outstanding_lien_or_opening_bid,
                        maximum_allowable_bid_mab, projected_net_spread, roi_percentage,
                        title_status, statutory_governing_law, raw_json, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        lead.id, lead.title, lead.category.value, lead.make, lead.model, lead.year,
                        lead.identifier_type, lead.identifier_value, lead.identifier_masked,
                        lead.location_port_city, lead.county, lead.state, lead.docket_or_case_number,
                        lead.court_docket_authority, lead.seizure_type.value, lead.deal_stage.value,
                        lead.auction_platform.value, lead.auction_date,
                        lead.underwriting.estimated_retail_value,
                        lead.underwriting.outstanding_lien_or_opening_bid,
                        lead.underwriting.maximum_allowable_bid_mab,
                        lead.underwriting.projected_net_spread,
                        lead.underwriting.roi_percentage,
                        lead.title_status.value, lead.statutory_governing_law,
                        lead.model_dump_json(), now
                    ))
                conn.commit()
        except Exception:
            pass

    # User Management Methods
    def register_user(self, email: str, password: str, full_name: str, role: str = "PRO_HUNTER") -> Dict[str, Any]:
        """Registers a new user using parameterized SQL."""
        email_clean = email.strip().lower()
        salt = uuid.uuid4().hex
        pwd_hash = self._hash_password(password, salt)
        user_id = f"USR-{uuid.uuid4().hex[:10].upper()}"
        wallet_id = f"APEX-WALLET-{uuid.uuid4().hex[:8].upper()}"
        initial_balance = 1000.0 if role == "PRO_HUNTER" else 0.0
        now = int(time.time())

        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                INSERT INTO users (id, email, password_hash, salt, full_name, role, api_bank_wallet_id, wallet_balance, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (user_id, email_clean, pwd_hash, salt, full_name.strip(), role, wallet_id, initial_balance, now))
                conn.commit()
                return {
                    "id": user_id,
                    "email": email_clean,
                    "full_name": full_name,
                    "role": role,
                    "api_bank_wallet_id": wallet_id,
                    "wallet_balance": initial_balance
                }
            except sqlite3.IntegrityError:
                raise ValueError("An account with this email address already exists.")

    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticates user with constant-time password hash comparison."""
        email_clean = email.strip().lower()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT id, email, password_hash, salt, full_name, role, api_bank_wallet_id, wallet_balance
            FROM users WHERE email = ?
            """, (email_clean,))
            row = cursor.fetchone()
            if not row:
                return None

            expected_hash = self._hash_password(password, row["salt"])
            if hashlib.sha256(expected_hash.encode()).digest() == hashlib.sha256(row["password_hash"].encode()).digest():
                return {
                    "id": row["id"],
                    "email": row["email"],
                    "full_name": row["full_name"],
                    "role": row["role"],
                    "api_bank_wallet_id": row["api_bank_wallet_id"],
                    "wallet_balance": row["wallet_balance"]
                }
            return None

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT id, email, full_name, role, api_bank_wallet_id, wallet_balance, created_at
            FROM users WHERE id = ?
            """, (user_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(row)

    def create_password_reset_code(self, email: str) -> Tuple[str, str]:
        """Generates a secure 6-digit OTP code for password recovery."""
        import secrets
        email_clean = email.strip().lower()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, full_name FROM users WHERE email = ?", (email_clean,))
            user = cursor.fetchone()
            if not user:
                raise ValueError(f"No existe ninguna cuenta de inversionista registrada con el correo '{email_clean}'.")

            # Generate random 6-digit number
            code = f"{secrets.randbelow(900000) + 100000}"
            now = int(time.time())
            expires_at = now + 900  # 15 minutes

            cursor.execute("""
            INSERT OR REPLACE INTO password_resets (email, code, expires_at, created_at)
            VALUES (?, ?, ?, ?)
            """, (email_clean, code, expires_at, now))
            conn.commit()

            return code, user["full_name"]

    def verify_and_reset_password(self, email: str, code: str, new_password: str) -> bool:
        """Validates OTP code and resets user password with PBKDF2-HMAC-SHA256."""
        email_clean = email.strip().lower()
        code_clean = code.strip()

        if len(new_password) < 6:
            raise ValueError("La nueva contraseña debe tener al menos 6 caracteres.")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT code, expires_at FROM password_resets WHERE email = ?", (email_clean,))
            reset_row = cursor.fetchone()

            if not reset_row:
                raise ValueError("No se ha solicitado ningún código de recuperación para este correo o ya fue utilizado.")

            now = int(time.time())
            if reset_row["expires_at"] < now:
                cursor.execute("DELETE FROM password_resets WHERE email = ?", (email_clean,))
                conn.commit()
                raise ValueError("El código de recuperación ha expirado (validez de 15 minutos). Solicite uno nuevo.")

            if reset_row["code"] != code_clean:
                raise ValueError("El código de verificación de 6 dígitos ingresado es incorrecto.")

            # Generate new salt and hash
            salt = uuid.uuid4().hex
            pwd_hash = self._hash_password(new_password, salt)

            cursor.execute("""
            UPDATE users SET password_hash = ?, salt = ? WHERE email = ?
            """, (pwd_hash, salt, email_clean))

            # Invalidate the used OTP code
            cursor.execute("DELETE FROM password_resets WHERE email = ?", (email_clean,))
            conn.commit()

            return True

    # Watchlist Methods
    def toggle_watchlist(self, user_id: str, asset_id: str) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM user_watchlist WHERE user_id = ? AND asset_id = ?", (user_id, asset_id))
            exists = cursor.fetchone()
            if exists:
                cursor.execute("DELETE FROM user_watchlist WHERE user_id = ? AND asset_id = ?", (user_id, asset_id))
                conn.commit()
                return {"user_id": user_id, "asset_id": asset_id, "is_saved": False}
            else:
                cursor.execute("INSERT INTO user_watchlist (user_id, asset_id, saved_at) VALUES (?, ?, ?)",
                               (user_id, asset_id, int(time.time())))
                conn.commit()
                return {"user_id": user_id, "asset_id": asset_id, "is_saved": True}

    def get_user_watchlist(self, user_id: str) -> List[str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT asset_id FROM user_watchlist WHERE user_id = ? ORDER BY saved_at DESC", (user_id,))
            return [row["asset_id"] for row in cursor.fetchall()]

    # Unlocked Dossiers
    def record_unlocked_dossier(self, user_id: str, asset_id: str, access_token: str, tx_hash: str) -> str:
        record_id = f"UNL-{uuid.uuid4().hex[:10].upper()}"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO user_unlocked_dossiers (id, user_id, asset_id, unlocked_at, access_token, transaction_hash)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (record_id, user_id, asset_id, int(time.time()), access_token, tx_hash))
            conn.commit()
        return record_id

    def get_user_unlocked_assets(self, user_id: str) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT asset_id, unlocked_at, access_token, transaction_hash
            FROM user_unlocked_dossiers WHERE user_id = ? ORDER BY unlocked_at DESC
            """, (user_id,))
            return [dict(row) for row in cursor.fetchall()]

    # Security Audit Logging
    def log_security_event(self, ip_address: str, user_agent: str, action: str, status: str, details: str = ""):
        log_id = f"SEC-{uuid.uuid4().hex[:10].upper()}"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO security_audit_logs (id, ip_address, user_agent, action, status, details, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (log_id, ip_address, user_agent[:255], action, status, details[:500], int(time.time())))
            conn.commit()

    def get_recent_security_logs(self, limit: int = 15) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT id, ip_address, action, status, details, timestamp
            FROM security_audit_logs ORDER BY timestamp DESC LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]

DB = DatabaseManager.get_instance()
