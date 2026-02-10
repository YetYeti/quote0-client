"""Quote0 Client SDK for interacting with e-ink devices.

This package provides a Python SDK for controlling Quote0 e-ink devices
via the Dot. App API.

Note: This is a community-maintained client library, not the official Quote0 API.
"""

from .client import Quote0Client
from .models import (
    Device,
    DeviceStatus,
    Task,
    TextContentRequest,
    ImageContentRequest,
    APIResponse,
)
from .exceptions import (
    Quote0Error,
    AuthenticationError,
    NotFoundError,
    PermissionError,
    ValidationError,
    RateLimitError,
)

__version__ = "0.1.0"

__all__ = [
    "Quote0Client",
    "Device",
    "DeviceStatus",
    "Task",
    "TextContentRequest",
    "ImageContentRequest",
    "APIResponse",
    "Quote0Error",
    "AuthenticationError",
    "NotFoundError",
    "PermissionError",
    "ValidationError",
    "RateLimitError",
    "__version__",
]
