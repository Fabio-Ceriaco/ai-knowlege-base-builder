"""
X-Webhook-Secret header authentication via Starlette middleware.

Every incoming request hits this middleware before FastAPI route matching.
Public paths (listed in PUBLIC_PATHS) bypass the check; everything else
requires a matching X-Webhook-Secret header or returns 401 Unauthorized.
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from server.utils.config import settings

# Paths that skip auth entirely
PUBLIC_PATHS = {
    "/health",
    "/docs",
    "/openapi.json",
    "/redoc",
}


class WebhookSecretMiddleware(BaseHTTPMiddleware):
    """
    Validates the X-Webhook-Secret header against the env var WEBHOOK_SECRET.

    BaseHTTPMiddleware gives us clean async integration with Starlette's ASGI pipeline, including
    correct exception propagation and request/response lifecycle hooks that a decorator-based
    approach would miss.
    """

    async def dispatch(self, request, call_next):
        # Public paths go stright through - no header check at all

        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        # Compare againt env var on every request rather than caching
        # at module load.
        expected = settings.WEBHOOK_SECRET
        if not expected:
            return JSONResponse(
                {"error": "Server auth not configured"},
                status_code=500,
            )

        provided = request.headers.get("X-Webhook-Secret")

        if provided != expected:
            return JSONResponse(
                {"error": "Invalid or missing X-Webhook-Secret"},
                status_code=401,
            )

        return await call_next(request)
