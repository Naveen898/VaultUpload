"""Simple email service for password reset links.

Environment variables used:
 SMTP_HOST (required)
 SMTP_PORT (default 587)
 SMTP_USER (optional if server allows anonymous)
 SMTP_PASS (optional)
 SMTP_STARTTLS ("1" to use STARTTLS, default 1)
 FROM_EMAIL (fallback: SMTP_USER)
 FRONTEND_BASE_URL (e.g. https://yourdomain or http://localhost:5173)

No external dependency (uses smtplib from stdlib).
"""
from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from utils.logger import logger


def _smtp_config():
    """Return SMTP config tuple or None if missing mandatory host.

    We treat absence of SMTP_HOST as "email disabled" instead of raising.
    """
    host = os.getenv("SMTP_HOST")
    if not host:
        return None
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASS")
    starttls = os.getenv("SMTP_STARTTLS", "1") == "1"
    from_email = os.getenv("FROM_EMAIL") or user
    if not from_email:
        logger.warning("Email disabled: FROM_EMAIL / SMTP_USER not set")
        return None
    return host, port, user, password, starttls, from_email


def send_reset_email(to_email: str, username: str, token: str):
    cfg = _smtp_config()
    if not cfg:
        logger.info("Skipping reset email send (SMTP not configured)")
        return
    try:
        host, port, user, password, starttls, from_email = cfg
        base = os.getenv("FRONTEND_BASE_URL", "http://localhost:5173")
        reset_link = f"{base.rstrip('/')}/reset?token={token}"
        msg = EmailMessage()
        msg["Subject"] = "VaultUpload Password Reset"
        msg["From"] = from_email
        msg["To"] = to_email
        msg.set_content(
            f"Hello {username},\n\nA password reset was requested for your VaultUpload account.\n"
            f"If you initiated this request, open the link below (valid 20 minutes):\n\n{reset_link}\n\n"
            "If you did not request this, you can ignore this email.\n\n— VaultUpload"
        )
        with smtplib.SMTP(host, port, timeout=15) as smtp:
            if starttls:
                try:
                    smtp.starttls()
                except Exception:
                    logger.warning("STARTTLS failed; attempting to continue without encryption")
            if user and password:
                smtp.login(user, password)
            smtp.send_message(msg)
        logger.info(f"Reset email sent to {to_email}")
    except Exception as e:
        logger.exception(f"Failed to send reset email to {to_email}: {e}")
