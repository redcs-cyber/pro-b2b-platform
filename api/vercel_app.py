"""Vercel serverless entrypoint for ProB2B.

Vercel's Python runtime imports an ASGI app object from this module. The main FastAPI
application remains in api.server so local, Docker, Kubernetes, and Vercel deployments all
share the same code path.
"""

from api.server import app

__all__ = ["app"]
