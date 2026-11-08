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
        """Initializes tables with proper foreign keys and indexes."""
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
                wallet_balance REAL DEFAULT 150000.00,
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

            conn.commit()

        # Seed default demonstration user if not present
        self._seed_default_user()

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

    # User Management Methods
    def register_user(self, email: str, password: str, full_name: str, role: str = "PRO_HUNTER") -> Dict[str, Any]:
        """Registers a new user using parameterized SQL."""
        email_clean = email.strip().lower()
        salt = uuid.uuid4().hex
        pwd_hash = self._hash_password(password, salt)
        user_id = f"USR-{uuid.uuid4().hex[:10].upper()}"
        wallet_id = f"APEX-WALLET-{uuid.uuid4().hex[:8].upper()}"
        now = int(time.time())

        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Check existing
            cursor.execute("SELECT id FROM users WHERE email = ?", (email_clean,))
            if cursor.fetchone():
                raise ValueError(f"User with email '{email_clean}' is already registered.")

            cursor.execute("""
            INSERT INTO users (id, email, password_hash, salt, full_name, role, api_bank_wallet_id, wallet_balance, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, email_clean, pwd_hash, salt, full_name.strip(), role, wallet_id, 150000.00, now))
            conn.commit()

        return {
            "id": user_id,
            "email": email_clean,
            "full_name": full_name.strip(),
            "role": role,
            "api_bank_wallet_id": wallet_id,
            "wallet_balance": 150000.00,
            "created_at": now
        }

    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Verifies credentials via parameterized query and constant-time hash comparison."""
        email_clean = email.strip().lower()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT id, email, password_hash, salt, full_name, role, api_bank_wallet_id, wallet_balance, created_at
            FROM users WHERE email = ?
            """, (email_clean,))
            row = cursor.fetchone()
            if not row:
                return None

            expected_hash = row["password_hash"]
            computed_hash = self._hash_password(password, row["salt"])

            if hashlib.sha256(expected_hash.encode()).digest() != hashlib.sha256(computed_hash.encode()).digest():
                return None

            return {
                "id": row["id"],
                "email": row["email"],
                "full_name": row["full_name"],
                "role": row["role"],
                "api_bank_wallet_id": row["api_bank_wallet_id"],
                "wallet_balance": row["wallet_balance"],
                "created_at": row["created_at"]
            }

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
