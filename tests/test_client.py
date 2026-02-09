"""Unit tests for Quote0Client.

This module contains comprehensive tests for all Quote0Client API methods,
including success scenarios, error handling, and parameter validation.

Test coverage:
- All 6 public API methods
- HTTP status code error mapping
- Parameter validation
- Response data type verification
- Custom exception handling
"""

import pytest
from unittest.mock import Mock, patch
from quote0_client.client import Quote0Client
from quote0_client.models import (
    Device,
    DeviceStatus,
    Task,
    TextContentRequest,
    ImageContentRequest,
    APIResponse,
    BatteryStatus,
    RenderInfo,
    CurrentRenderInfo,
    NextRenderTime,
)
from quote0_client.exceptions import (
    Quote0Error,
    AuthenticationError,
    NotFoundError,
    PermissionError,
    ValidationError,
    RateLimitError,
)


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def mock_response(status_code: int = 200, json_data: dict | list | None = None) -> Mock:
    """Create a mock HTTP response.

    Args:
        status_code: HTTP status code (default: 200)
        json_data: Response JSON data (default: empty dict)

    Returns:
        Mock HTTP response object
    """
    response = Mock()
    response.status_code = status_code
    response.json.return_value = json_data if json_data is not None else {}
    return response


@pytest.fixture
def test_client():
    """Create a test Quote0Client instance.

    Returns:
        Quote0Client instance with test API key
    """
    return Quote0Client(api_key="test-api-key-12345")


# ============================================================================
# Test: get_devices()
# ============================================================================


class TestGetDevices:
    """Test cases for get_devices() method."""

    def test_get_devices_success(self, test_client, mock_response):
        """Test successfully retrieving device list."""
        devices_data = [
            {
                "series": "quote",
                "model": "quote_0",
                "edition": 1,
                "id": "ABC123",
            },
            {
                "series": "quote",
                "model": "quote_0",
                "edition": 2,
                "id": "DEF456",
            },
        ]

        mock_response.json.return_value = devices_data

        with patch.object(test_client._client, "request", return_value=mock_response):
            devices = test_client.get_devices()

            assert len(devices) == 2
            assert isinstance(devices[0], Device)
            assert isinstance(devices[1], Device)
            assert devices[0].id == "ABC123"
            assert devices[0].model == "quote_0"
            assert devices[0].edition == 1
            assert devices[1].id == "DEF456"
            assert devices[1].edition == 2

    def test_get_devices_empty_list(self, test_client, mock_response):
        """Test retrieving empty device list."""
        mock_response.json.return_value = []

        with patch.object(test_client._client, "request", return_value=mock_response):
            devices = test_client.get_devices()

            assert len(devices) == 0

    def test_get_devices_authentication_error(self, test_client, mock_response):
        """Test authentication error when getting devices."""
        mock_response.status_code = 401

        with patch.object(test_client._client, "request", return_value=mock_response):
            with pytest.raises(AuthenticationError) as exc_info:
                test_client.get_devices()

            assert "Invalid API key" in str(exc_info.value)

    def test_get_devices_not_found_error(self, test_client, mock_response):
        """Test not found error when getting devices."""
        mock_response.status_code = 404

        with patch.object(test_client._client, "request", return_value=mock_response):
            with pytest.raises(NotFoundError) as exc_info:
                test_client.get_devices()

            assert "Device or resource not found" in str(exc_info.value)


# ============================================================================
# Test: get_device_status()
# ============================================================================


class TestGetDeviceStatus:
    """Test cases for get_device_status() method."""

    def test_get_device_status_success(self, test_client, mock_response):
        """Test successfully retrieving device status."""
        status_data = {
            "deviceId": "ABC123",
            "alias": "Living Room Quote",
            "location": "Home",
            "status": {
                "version": "1.0.0",
                "current": "100%",
                "description": "Fully charged",
                "battery": "100%",
                "wifi": "Excellent",
            },
            "renderInfo": {
                "last": "2025-02-02 12:00:00",
                "current": {
                    "rotated": False,
                    "border": 0,
                    "image": ["https://example.com/image1.png"],
                },
                "next": {
                    "battery": "2025-02-02 13:00:00",
                    "power": "2025-02-02 13:00:00",
                },
            },
        }

        mock_response.json.return_value = status_data

        with patch.object(test_client._client, "request", return_value=mock_response):
            status = test_client.get_device_status("ABC123")

            assert isinstance(status, DeviceStatus)
            assert status.deviceId == "ABC123"
            assert status.alias == "Living Room Quote"
            assert status.location == "Home"
            assert isinstance(status.status, BatteryStatus)
            assert status.status.battery == "100%"
            assert status.status.wifi == "Excellent"
            assert isinstance(status.renderInfo, RenderInfo)
            assert isinstance(status.renderInfo.current, CurrentRenderInfo)
            assert status.renderInfo.current.border == 0
            assert isinstance(status.renderInfo.next, NextRenderTime)
            assert status.renderInfo.next.battery == "2025-02-02 13:00:00"
            assert status.renderInfo.next.power == "2025-02-02 13:00:00"

    def test_get_device_status_without_alias(self, test_client, mock_response):
        """Test device status without alias."""
        status_data = {
            "deviceId": "DEF456",
            "status": {
                "version": "1.0.0",
                "current": "80%",
                "description": "Good",
                "battery": "80%",
                "wifi": "Good",
            },
            "renderInfo": {
                "last": "2025-02-02 12:00:00",
                "current": {
                    "rotated": True,
                    "border": 1,
                    "image": [],
                },
                "next": {
                    "battery": "2025-02-02 13:00:00",
                    "power": "2025-02-02 13:00:00",
                },
            },
        }

        mock_response.json.return_value = status_data

        with patch.object(test_client._client, "request", return_value=mock_response):
            status = test_client.get_device_status("DEF456")

            assert status.deviceId == "DEF456"
            assert status.alias is None
            assert status.location is None
            assert isinstance(status.renderInfo, RenderInfo)
            assert isinstance(status.renderInfo.next, NextRenderTime)
            assert status.renderInfo.next.battery == "2025-02-02 13:00:00"
            assert status.renderInfo.next.power == "2025-02-02 13:00:00"

    def test_get_device_status_not_found(self, test_client, mock_response):
        """Test not found error for non-existent device."""
        mock_response.status_code = 404

        with patch.object(test_client._client, "request", return_value=mock_response):
            with pytest.raises(NotFoundError) as exc_info:
                test_client.get_device_status("NONEXISTENT")

            assert "Device or resource not found" in str(exc_info.value)


# ============================================================================
# Test: switch_to_next()
# ============================================================================


class TestSwitchToNext:
    """Test cases for switch_to_next() method."""

    def test_switch_to_next_success(self, test_client, mock_response):
        """Test successfully switching to next content."""
        response_data = {"code": 0, "message": "Switched successfully", "result": {}}

        mock_response.json.return_value = response_data

        with patch.object(test_client._client, "request", return_value=mock_response):
            response = test_client.switch_to_next("ABC123")

            assert isinstance(response, APIResponse)
            assert response.code == 0
            assert response.success is True
            assert response.message == "Switched successfully"

    def test_switch_to_next_server_error(self, test_client):
        """Test server error response."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {}

        with patch.object(test_client._client, "request", return_value=mock_response):
            with pytest.raises(Quote0Error) as exc_info:
                test_client.switch_to_next("ABC123")

            assert "Server error: 500" in str(exc_info.value)

    def test_switch_to_next_not_found(self, test_client, mock_response):
        """Test not found error when switching."""
        mock_response.status_code = 404

        with patch.object(test_client._client, "request", return_value=mock_response):
            with pytest.raises(NotFoundError) as exc_info:
                test_client.switch_to_next("NONEXISTENT")

            assert "Device or resource not found" in str(exc_info.value)


# ============================================================================
# Test: list_tasks()
# ============================================================================


class TestListTasks:
    """Test cases for list_tasks() method."""

    def test_list_tasks_success(self, test_client, mock_response):
        """Test successfully listing tasks."""
        tasks_data = [
            {
                "type": "TEXT_API",
                "key": "task-001",
                "title": "Hello",
                "message": "World",
                "refreshNow": True,
            },
            {
                "type": "IMAGE_API",
                "key": "task-002",
                "border": 0,
                "ditherType": "DIFFUSION",
                "ditherKernel": "FLOYD_STEINBERG",
            },
        ]

        mock_response.json.return_value = tasks_data

        with patch.object(test_client._client, "request", return_value=mock_response):
            tasks = test_client.list_tasks("ABC123")

            assert len(tasks) == 2
            assert isinstance(tasks[0], Task)
            assert isinstance(tasks[1], Task)
            assert tasks[0].type == "TEXT_API"
            assert tasks[0].key == "task-001"
            assert tasks[0].title == "Hello"
            assert tasks[1].type == "IMAGE_API"
            assert tasks[1].ditherType == "DIFFUSION"

    def test_list_tasks_default_task_type(self, test_client, mock_response):
        """Test list_tasks with default task_type."""
        tasks_data = [
            {
                "type": "TEXT_API",
                "key": "default-task",
            }
        ]

        mock_response.json.return_value = tasks_data

        with patch.object(test_client._client, "request", return_value=mock_response):
            tasks = test_client.list_tasks("ABC123")

            assert len(tasks) == 1
            assert tasks[0].key == "default-task"

    def test_list_tasks_invalid_task_type(self, test_client):
        """Test ValidationError for invalid task_type."""
        with pytest.raises(ValidationError) as exc_info:
            test_client.list_tasks("ABC123", task_type="invalid")

        assert "Invalid task_type: invalid" in str(exc_info.value)
        assert "Only 'loop' is currently supported" in str(exc_info.value)

    def test_list_tasks_permission_error(self, test_client, mock_response):
        """Test permission error when listing tasks."""
        mock_response.status_code = 403

        with patch.object(test_client._client, "request", return_value=mock_response):
            with pytest.raises(PermissionError) as exc_info:
                test_client.list_tasks("ABC123")

            assert "Insufficient permissions" in str(exc_info.value)


# ============================================================================
# Test: send_text()
# ============================================================================


class TestSendText:
    """Test cases for send_text() method."""

    def test_send_text_success(self, test_client, mock_response):
        """Test successfully sending text content."""
        text_req = TextContentRequest(title="Hello", message="World!", refreshNow=True)

        response_data = {"code": 0, "message": "Text sent", "result": {}}

        mock_response.json.return_value = response_data

        with patch.object(test_client._client, "request", return_value=mock_response):
            response = test_client.send_text("ABC123", text_req)

            assert isinstance(response, APIResponse)
            assert response.code == 0
            assert response.success is True

    def test_send_text_without_optional_fields(self, test_client, mock_response):
        """Test sending text without optional fields."""
        text_req = TextContentRequest(
            title="Title", message="Message", refreshNow=False
        )

        response_data = {"code": 0, "message": "Success", "result": {}}

        mock_response.json.return_value = response_data

        with patch.object(test_client._client, "request", return_value=mock_response):
            response = test_client.send_text("ABC123", text_req)

            assert response.success is True

    def test_send_text_with_signature(self, test_client, mock_response):
        """Test sending text with signature."""
        text_req = TextContentRequest(
            title="Code",
            message="123456",
            signature="2025-02-02 20:00",
            refreshNow=True,
        )

        response_data = {"code": 0, "message": "Success", "result": {}}

        mock_response.json.return_value = response_data

        with patch.object(test_client._client, "request", return_value=mock_response):
            response = test_client.send_text("ABC123", text_req)

            assert response.success is True

    def test_send_text_validation_error(self, test_client, mock_response):
        """Test validation error when sending text."""
        mock_response.status_code = 400

        with patch.object(test_client._client, "request", return_value=mock_response):
            with pytest.raises(ValidationError) as exc_info:
                test_client.send_text("ABC123", TextContentRequest())

            assert "Request validation failed" in str(exc_info.value)

    def test_send_text_not_found(self, test_client, mock_response):
        """Test not found error when sending text."""
        mock_response.status_code = 404

        with patch.object(test_client._client, "request", return_value=mock_response):
            with pytest.raises(NotFoundError) as exc_info:
                test_client.send_text("NONEXISTENT", TextContentRequest())

            assert "Device or resource not found" in str(exc_info.value)


# ============================================================================
# Test: send_image()
# ============================================================================


class TestSendImage:
    """Test cases for send_image() method."""

    def test_send_image_success(self, test_client, mock_response):
        """Test successfully sending image content."""
        image_req = ImageContentRequest(
            image="iVBORw0KGgoAAAANSUhEUgAA...", border=0, refreshNow=True
        )

        response_data = {"code": 0, "message": "Image sent", "result": {}}

        mock_response.json.return_value = response_data

        with patch.object(test_client._client, "request", return_value=mock_response):
            response = test_client.send_image("ABC123", image_req)

            assert isinstance(response, APIResponse)
            assert response.code == 0
            assert response.success is True

    def test_send_image_with_all_options(self, test_client, mock_response):
        """Test sending image with all options."""
        image_req = ImageContentRequest(
            image="iVBORw0KGgoAAAANSUhEUgAA...",
            border=1,
            ditherType="ORDERED",
            ditherKernel="ATKINSON",
            refreshNow=False,
        )

        response_data = {"code": 0, "message": "Success", "result": {}}

        mock_response.json.return_value = response_data

        with patch.object(test_client._client, "request", return_value=mock_response):
            response = test_client.send_image("ABC123", image_req)

            assert response.success is True
            assert image_req.border == 1
            assert image_req.ditherType == "ORDERED"

    def test_send_image_validation_error(self, test_client):
        """Test validation error when sending image."""
        # Create a valid request first
        image_req = ImageContentRequest(image="iVBORw0KGgoAAAANSUhEUgAA...", border=0)
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {}

        with patch.object(test_client._client, "request", return_value=mock_response):
            with pytest.raises(ValidationError) as exc_info:
                test_client.send_image("ABC123", image_req)

            assert "Request validation failed" in str(exc_info.value)

    def test_send_image_permission_error(self, test_client):
        """Test permission error when sending image."""
        # Create a valid request first
        image_req = ImageContentRequest(image="iVBORw0KGgoAAAANSUhEUgAA...", border=0)
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {}

        with patch.object(test_client._client, "request", return_value=mock_response):
            with pytest.raises(PermissionError) as exc_info:
                test_client.send_image("ABC123", image_req)

            assert "Insufficient permissions" in str(exc_info.value)


# ============================================================================
# Test: Client Initialization
# ============================================================================


class TestClientInit:
    """Test cases for Quote0Client initialization."""

    def test_client_init_success(self):
        """Test successful client initialization."""
        client = Quote0Client(api_key="test-key")
        assert client.api_key == "test-key"
        assert client.base_url == "https://dot.mindreset.tech"

    def test_client_init_with_custom_base_url(self):
        """Test client initialization with custom base URL."""
        client = Quote0Client(api_key="test-key", base_url="https://custom.api.com")
        assert client.base_url == "https://custom.api.com"

    def test_client_init_empty_api_key(self):
        """Test ValueError when api_key is empty."""
        with pytest.raises(ValueError) as exc_info:
            Quote0Client(api_key="")

        assert "api_key cannot be empty" in str(exc_info.value)

    def test_client_init_none_api_key(self):
        """Test ValueError when api_key is None."""
        with pytest.raises(ValueError) as exc_info:
            Quote0Client(api_key=None)

        assert "api_key cannot be empty" in str(exc_info.value)

    def test_client_init_whitespace_api_key(self):
        """Test ValueError when api_key is whitespace only."""
        with pytest.raises(ValueError) as exc_info:
            Quote0Client(api_key="   ")

        assert "api_key cannot be empty" in str(exc_info.value)

    def test_client_context_manager(self):
        """Test client can be used as context manager."""
        with Quote0Client(api_key="test-key") as client:
            assert client.api_key == "test-key"

        # Client should be closed after context exit


# ============================================================================
# Test: Error Handling
# ============================================================================


class TestErrorHandling:
    """Test cases for HTTP error code mapping."""

    def test_http_400_validation_error(self, test_client):
        """Test HTTP 400 maps to ValidationError."""
        with patch.object(test_client._client, "request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 400
            mock_response.json.return_value = {"error": "Bad request"}
            mock_request.return_value = mock_response

            with pytest.raises(ValidationError) as exc_info:
                test_client.get_devices()

            assert "Request validation failed" in str(exc_info.value)

    def test_http_401_authentication_error(self, test_client):
        """Test HTTP 401 maps to AuthenticationError."""
        with patch.object(test_client._client, "request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 401
            mock_request.return_value = mock_response

            with pytest.raises(AuthenticationError) as exc_info:
                test_client.get_devices()

            assert "Invalid API key" in str(exc_info.value)

    def test_http_403_permission_error(self, test_client):
        """Test HTTP 403 maps to PermissionError."""
        with patch.object(test_client._client, "request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 403
            mock_request.return_value = mock_response

            with pytest.raises(PermissionError) as exc_info:
                test_client.get_devices()

            assert "Insufficient permissions" in str(exc_info.value)

    def test_http_404_not_found_error(self, test_client):
        """Test HTTP 404 maps to NotFoundError."""
        with patch.object(test_client._client, "request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_request.return_value = mock_response

            with pytest.raises(NotFoundError) as exc_info:
                test_client.get_devices()

            assert "Device or resource not found" in str(exc_info.value)

    def test_http_429_rate_limit_error(self, test_client):
        """Test HTTP 429 maps to RateLimitError."""
        with patch.object(test_client._client, "request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 429
            mock_request.return_value = mock_response

            with pytest.raises(RateLimitError) as exc_info:
                test_client.get_devices()

            assert "Rate limit exceeded" in str(exc_info.value)

    def test_http_500_quote0_error(self, test_client):
        """Test HTTP 500 maps to Quote0Error."""
        with patch.object(test_client._client, "request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_request.return_value = mock_response

            with pytest.raises(Quote0Error) as exc_info:
                test_client.get_devices()

            assert "Server error: 500" in str(exc_info.value)

    def test_http_503_quote0_error(self, test_client):
        """Test HTTP 503 maps to Quote0Error."""
        with patch.object(test_client._client, "request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 503
            mock_request.return_value = mock_response

            with pytest.raises(Quote0Error) as exc_info:
                test_client.get_devices()

            assert "Server error: 503" in str(exc_info.value)


# ============================================================================
# Test: Model Serialization
# ============================================================================


class TestModelSerialization:
    """Test cases for model serialization/deserialization."""

    def test_device_model_roundtrip(self, test_client, mock_response):
        """Test Device model serialization."""
        devices_data = [
            {
                "series": "quote",
                "model": "quote_0",
                "edition": 1,
                "id": "TEST123",
            }
        ]

        mock_response.json.return_value = devices_data

        with patch.object(test_client._client, "request", return_value=mock_response):
            devices = test_client.get_devices()
            device = devices[0]

            # Test model_dump() returns original data
            dumped = device.model_dump()
            assert dumped["series"] == "quote"
            assert dumped["model"] == "quote_0"
            assert dumped["edition"] == 1
            assert dumped["id"] == "TEST123"

    def test_api_response_success_property(self, test_client, mock_response):
        """Test APIResponse success property."""
        response_data = {"code": 0, "message": "Success", "result": {}}

        mock_response.json.return_value = response_data

        with patch.object(test_client._client, "request", return_value=mock_response):
            response = test_client.switch_to_next("ABC123")

            assert response.success is True
            assert response.code == 0

    def test_api_response_failure_property(self, test_client, mock_response):
        """Test APIResponse success property when code is non-zero."""
        response_data = {"code": 1, "message": "Error", "result": {}}

        mock_response.json.return_value = response_data

        with patch.object(test_client._client, "request", return_value=mock_response):
            response = test_client.switch_to_next("ABC123")

            assert response.success is False
            assert response.code == 1
