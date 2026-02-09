"""Quote0 SDK Client for interacting with e-ink device API.

This module provides the main client class for interacting with Quote0 devices
via the Dot. App API. All API operations are synchronous and support authentication
via API key.
"""

import httpx
from typing import List, Any, Optional

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


class Quote0Client:
    """Client for interacting with Quote0 e-ink device API.

    This class provides a high-level interface for managing Quote0 devices,
    including fetching device status, sending text and image content,
    and managing device tasks.

    Attributes:
        api_key: API key for authentication
        base_url: Base URL of the API endpoint
        _client: Internal HTTP client instance

    Example:
        >>> client = Quote0Client(api_key="your-api-key")
        >>> devices = client.get_devices()
        >>> status = client.get_device_status("device-serial-number")
    """

    BASE_URL = "https://dot.mindreset.tech"

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """Initialize client with API key.

        Args:
            api_key: API key from Dot. App
            base_url: Optional base URL (default: https://dot.mindreset.tech)

        Raises:
            ValueError: If api_key is empty
        """
        if not api_key or not api_key.strip():
            raise ValueError("api_key cannot be empty")

        self.api_key = api_key
        self.base_url: str = base_url or self.BASE_URL
        self._client = httpx.Client(trust_env=False, timeout=30.0)

    def get_devices(self) -> List[Device]:
        """Get list of all registered devices.

        Returns:
            List of Device objects representing all registered devices

        Example:
            >>> client = Quote0Client(api_key="test-key")
            >>> devices = client.get_devices()
            >>> print(f"Found {len(devices)} devices")
        """
        response = self._request("GET", "/api/authV2/open/devices")
        devices_data = response.json()
        return [Device(**device) for device in devices_data]

    def get_device_status(self, device_id: str) -> DeviceStatus:
        """Get the current status of a specific device.

        Args:
            device_id: Device serial number

        Returns:
            DeviceStatus object containing device information, battery status,
            WiFi status, and rendering information

        Raises:
            NotFoundError: If device_id does not exist
            AuthenticationError: If authentication fails
            PermissionError: If insufficient permissions

        Example:
            >>> status = client.get_device_status("abc123")
            >>> print(f"Battery: {status.status.battery}")
            >>> print(f"Location: {status.location}")
        """
        response = self._request("GET", f"/api/authV2/open/device/{device_id}/status")
        return DeviceStatus(**response.json())

    def switch_to_next(self, device_id: str) -> APIResponse:
        """Switch device to the next content.

        This method advances the device to the next content in the content queue.

        Args:
            device_id: Device serial number

        Returns:
            APIResponse object with the response data

        Raises:
            NotFoundError: If device_id does not exist
            AuthenticationError: If authentication fails
            PermissionError: If insufficient permissions

        Example:
            >>> response = client.switch_to_next("abc123")
            >>> print(f"Status: {response.message}")
        """
        response = self._request("POST", f"/api/authV2/open/device/{device_id}/next")
        return APIResponse(**response.json())

    def list_tasks(self, device_id: str, task_type: str = "loop") -> List[Task]:
        """List all tasks for a specific device.

        Args:
            device_id: Device serial number
            task_type: Task type (currently only "loop" is supported)

        Returns:
            List of Task objects for the device

        Raises:
            NotFoundError: If device_id does not exist
            AuthenticationError: If authentication fails
            PermissionError: If insufficient permissions
            ValidationError: If task_type is invalid

        Example:
            >>> tasks = client.list_tasks("abc123", task_type="loop")
            >>> for task in tasks:
            ...     print(f"Task: {task.key}, Type: {task.type}")
        """
        if task_type != "loop":
            raise ValidationError(
                f"Invalid task_type: {task_type}. Only 'loop' is currently supported."
            )

        response = self._request(
            "GET", f"/api/authV2/open/device/{device_id}/{task_type}/list"
        )
        tasks_data = response.json()
        return [Task(**task) for task in tasks_data]

    def send_text(self, device_id: str, content: TextContentRequest) -> APIResponse:
        """Send text content to the device.

        This method allows sending formatted text content to the device for display.

        Args:
            device_id: Device serial number
            content: TextContentRequest object containing the text to display

        Returns:
            APIResponse object with the response data

        Raises:
            NotFoundError: If device_id does not exist
            AuthenticationError: If authentication fails
            PermissionError: If insufficient permissions
            ValidationError: If content validation fails

        Example:
            >>> text_req = TextContentRequest(
            ...     title="Hello",
            ...     message="World!",
            ...     refreshNow=True
            ... )
            >>> response = client.send_text("abc123", text_req)
            >>> print(f"Sent: {response.message}")
        """
        response = self._request(
            "POST",
            f"/api/authV2/open/device/{device_id}/text",
            json=content.model_dump(exclude_none=True),
        )
        return APIResponse(**response.json())

    def send_image(self, device_id: str, content: ImageContentRequest) -> APIResponse:
        """Send image content to the device.

        This method allows sending image content to the device for display.

        Args:
            device_id: Device serial number
            content: ImageContentRequest object containing the image to display

        Returns:
            APIResponse object with the response data

        Raises:
            NotFoundError: If device_id does not exist
            AuthenticationError: If authentication fails
            PermissionError: If insufficient permissions
            ValidationError: If content validation fails

        Example:
            >>> image_req = ImageContentRequest(
            ...     image="base64_encoded_image_data",
            ...     border=0,
            ...     refreshNow=True
            ... )
            >>> response = client.send_image("abc123", image_req)
            >>> print(f"Sent: {response.message}")
        """
        response = self._request(
            "POST",
            f"/api/authV2/open/device/{device_id}/image",
            json=content.model_dump(exclude_none=True),
        )
        return APIResponse(**response.json())

    def _request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        """Make HTTP request to the API endpoint.

        This is a private method that handles the actual HTTP communication.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path (without base URL)
            **kwargs: Additional arguments for httpx.request

        Returns:
            httpx.Response object

        Raises:
            AuthenticationError: On 401 Unauthorized
            PermissionError: On 403 Forbidden
            NotFoundError: On 404 Not Found
            ValidationError: On 400 Bad Request
            RateLimitError: On rate limit exceeded (400)
            Quote0Error: On other server errors (500)
        """
        url = f"{self.base_url}{path}"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Add headers to kwargs if not already present
        request_kwargs = kwargs.copy()
        if "headers" not in request_kwargs:
            request_kwargs["headers"] = headers
        else:
            # Merge headers, giving precedence to passed headers
            for key, value in headers.items():
                if key not in request_kwargs["headers"]:
                    request_kwargs["headers"][key] = value

        response = self._client.request(method, url, **request_kwargs)

        self._handle_response(response)

        return response

    def _handle_response(self, response: httpx.Response) -> None:
        """Handle API response and raise appropriate exceptions.

        This method maps HTTP status codes to appropriate exception types.

        Args:
            response: httpx.Response object to process

        Raises:
            AuthenticationError: On 401 Unauthorized
            PermissionError: On 403 Forbidden
            NotFoundError: On 404 Not Found
            ValidationError: On 400 Bad Request
            RateLimitError: On rate limit exceeded
            Quote0Error: On 500 Server Error
        """
        status_code = response.status_code

        if status_code == 200:
            # Success
            return
        elif status_code == 400:
            # Bad Request - validation error
            raise ValidationError("Request validation failed")
        elif status_code == 401:
            # Unauthorized - invalid credentials
            raise AuthenticationError("Invalid API key or authentication failed")
        elif status_code == 403:
            # Forbidden - insufficient permissions
            raise PermissionError("Insufficient permissions to access this resource")
        elif status_code == 404:
            # Not Found - resource doesn't exist
            raise NotFoundError("Device or resource not found")
        elif status_code == 429:
            # Rate Limit - too many requests
            raise RateLimitError(
                "Rate limit exceeded. Please reduce request frequency."
            )
        elif 500 <= status_code < 600:
            # Server Error
            raise Quote0Error(f"Server error: {status_code}")
        else:
            # Unknown status code
            raise Quote0Error(f"Unexpected status code: {status_code}")

    def close(self) -> None:
        """Close the internal HTTP client.

        This method should be called when the client is no longer needed
        to properly clean up resources.

        Example:
            >>> client = Quote0Client(api_key="test-key")
            >>> try:
            ...     # Use client...
            ...     pass
            ... finally:
            ...     client.close()
        """
        self._client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
