"""
SQLite Persistence for Mobile OTP Auth, User Profiles, and Price Alerts
Provides secure storage with parameterized queries and schema initialization.
"""

import os
import sqlite3
import datetime
from typing import Dict, List, Optional, Tuple

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "rythucrop.db"
)


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mobile TEXT UNIQUE NOT NULL,
        full_name TEXT,
        state TEXT,
        district TEXT,
        preferred_language TEXT DEFAULT 'en',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP
    );
    """)

    # OTP Verification Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS otp_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mobile TEXT NOT NULL,
        otp_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        attempts INTEGER DEFAULT 0,
        expires_at TIMESTAMP NOT NULL,
        verified INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Price Alerts Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS price_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mobile TEXT NOT NULL,
        crop TEXT NOT NULL,
        market TEXT NOT NULL,
        condition_type TEXT NOT NULL, -- 'above', 'below', 'change'
        target_price REAL NOT NULL,
        unit TEXT DEFAULT '₹/Quintal',
        status TEXT DEFAULT 'active', -- 'active', 'triggered', 'cancelled'
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_checked TIMESTAMP,
        last_notified TIMESTAMP,
        notification_log TEXT
    );
    """)

    # Saved Farm Plans Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_farm_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mobile TEXT NOT NULL,
        plan_name TEXT,
        land REAL,
        season TEXT,
        soil TEXT,
        irrigation TEXT,
        goal TEXT,
        experience TEXT,
        recommended_crops TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()


def save_otp_request(mobile: str, otp_hash: str, salt: str, expires_at: datetime.datetime):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Invalidate older pending OTPs for this number
    cursor.execute("UPDATE otp_requests SET verified = 2 WHERE mobile = ? AND verified = 0", (mobile,))
    cursor.execute(
        "INSERT INTO otp_requests (mobile, otp_hash, salt, expires_at) VALUES (?, ?, ?, ?)",
        (mobile, otp_hash, salt, expires_at.isoformat())
    )
    conn.commit()
    conn.close()


def get_latest_otp_request(mobile: str) -> Optional[sqlite3.Row]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM otp_requests WHERE mobile = ? AND verified = 0 ORDER BY id DESC LIMIT 1",
        (mobile,)
    )
    row = cursor.fetchone()
    conn.close()
    return row


def mark_otp_verified(request_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE otp_requests SET verified = 1 WHERE id = ?", (request_id,))
    conn.commit()
    conn.close()


def increment_otp_attempts(request_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE otp_requests SET attempts = attempts + 1 WHERE id = ?", (request_id,))
    conn.commit()
    conn.close()


def get_or_create_user(mobile: str, lang: str = "en") -> Dict:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE mobile = ?", (mobile,))
    user = cursor.fetchone()
    now = datetime.datetime.now().isoformat()
    if user:
        cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (now, user["id"]))
        conn.commit()
        user_dict = dict(user)
        user_dict["last_login"] = now
    else:
        cursor.execute(
            "INSERT INTO users (mobile, preferred_language, last_login) VALUES (?, ?, ?)",
            (mobile, lang, now)
        )
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE mobile = ?", (mobile,))
        user_dict = dict(cursor.fetchone())
    conn.close()
    return user_dict


def update_user_profile(mobile: str, state: str = None, district: str = None, lang: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    updates = []
    params = []
    if state:
        updates.append("state = ?")
        params.append(state)
    if district:
        updates.append("district = ?")
        params.append(district)
    if lang:
        updates.append("preferred_language = ?")
        params.append(lang)
    if updates:
        params.append(mobile)
        query = f"UPDATE users SET {', '.join(updates)} WHERE mobile = ?"
        cursor.execute(query, tuple(params))
        conn.commit()
    conn.close()


def create_price_alert(
    mobile: str,
    crop: str,
    market: str,
    condition_type: str,
    target_price: float,
    unit: str = "₹/Quintal"
) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO price_alerts (mobile, crop, market, condition_type, target_price, unit, status)
        VALUES (?, ?, ?, ?, ?, ?, 'active')
        """,
        (mobile, crop, market, condition_type, target_price, unit)
    )
    alert_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return alert_id


def get_user_alerts(mobile: str) -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM price_alerts WHERE mobile = ? ORDER BY id DESC",
        (mobile,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def cancel_price_alert(alert_id: int, mobile: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE price_alerts SET status = 'cancelled' WHERE id = ? AND mobile = ?",
        (alert_id, mobile)
    )
    changed = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return changed


def get_active_alerts() -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM price_alerts WHERE status = 'active'")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_alert_notification(alert_id: int, message: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now().isoformat()
    cursor.execute(
        """
        UPDATE price_alerts
        SET status = 'triggered', last_checked = ?, last_notified = ?, notification_log = ?
        WHERE id = ?
        """,
        (now, now, message, alert_id)
    )
    conn.commit()
    conn.close()


# Initialize schema immediately on import
init_db()
