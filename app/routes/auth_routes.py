"""
RythuCrop Authentication Routes Module (Alias / Re-export)
Exposes auth_bp from app.routes.auth for route consistency.
"""

from app.routes.auth import auth_bp

__all__ = ["auth_bp"]
