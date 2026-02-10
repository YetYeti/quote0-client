"""Real API integration tests for Quote0Client.

This module contains integration tests that make actual API calls to verify
that the real API responses match the Pydantic model definitions.

These tests require:
- A valid QUOTE0_API_KEY in .env file
- A valid QUOTE0_DEVICE_ID in .env file
- Network connectivity to the Quote0 API

NOTE: These tests will make actual API calls and may:
- Send real content to your device
- Consume device battery
- Be subject to API rate limits (10 requests/second)

Run these tests separately from unit tests:
    pytest tests/test_real_api.py -v -s
"""

import os
import time
import pytest
from dotenv import load_dotenv

from quote0_client.client import Quote0Client
from quote0_client.models import (
    Device,
    DeviceStatus,
    Task,
    TextContentRequest,
    ImageContentRequest,
    APIResponse,
)

load_dotenv()


@pytest.fixture(scope="module")
def api_key() -> str:
    """Get API key from environment variable.

    Returns:
        API key from QUOTE0_API_KEY environment variable

    Raises:
        pytest.skip: If QUOTE0_API_KEY is not set
    """
    key = os.getenv("QUOTE0_API_KEY")
    if not key:
        pytest.skip("QUOTE0_API_KEY not set in .env file")
    return key


@pytest.fixture(scope="module")
def device_id() -> str:
    """Get device ID from environment variable.

    Returns:
        Device ID from QUOTE0_DEVICE_ID environment variable

    Raises:
        pytest.skip: If QUOTE0_DEVICE_ID is not set
    """
    device = os.getenv("QUOTE0_DEVICE_ID")
    if not device:
        pytest.skip("QUOTE0_DEVICE_ID not set in .env file")
    return device


@pytest.fixture(scope="module")
def real_client(api_key: str) -> Quote0Client:
    """Create a real Quote0Client instance.

    Args:
        api_key: Valid API key from environment variable

    Returns:
        Quote0Client instance configured with real API key
    """
    return Quote0Client(api_key=api_key)


@pytest.fixture
def sample_text_request() -> TextContentRequest:
    """Create a sample text content request.

    Returns:
        TextContentRequest with test data
    """
    return TextContentRequest(
        title="Real API Test",
        message="This is a test message from real API integration tests.",
        refreshNow=False,
    )


@pytest.fixture
def sample_image_request() -> ImageContentRequest:
    """Create a sample image content request.

    Returns:
        ImageContentRequest with a simple 1x1 red pixel PNG
    """
    red_pixel_png = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    return ImageContentRequest(
        image=red_pixel_png,
        border=0,
        ditherType="DIFFUSION",
        ditherKernel="FLOYD_STEINBERG",
        refreshNow=False,
    )


class TestGetDevicesReal:
    """Real API tests for get_devices() method."""

    def test_get_devices_real(self, real_client: Quote0Client):
        """Test retrieving device list from real API."""
        devices = real_client.get_devices()

        assert isinstance(devices, list)

        for device in devices:
            assert isinstance(device, Device)
            assert device.series is not None
            assert device.model is not None
            assert device.edition in [1, 2]
            assert device.id is not None

        print("\n=== Real API Response: get_devices() ===")
        for device in devices:
            print(f"Device: {device.id}")
            print(f"  series: {device.series}")
            print(f"  model: {device.model}")
            print(f"  edition: {device.edition}")


class TestGetDeviceStatusReal:
    """Real API tests for get_device_status() method."""

    def test_get_device_status_real(self, real_client: Quote0Client, device_id: str):
        """Test retrieving device status from real API."""
        status = real_client.get_device_status(device_id)

        assert isinstance(status, DeviceStatus)
        assert status.deviceId == device_id

        assert hasattr(status, "status")
        assert hasattr(status, "renderInfo")

        print("\n=== Real API Response: get_device_status() ===")
        print(f"deviceId: {status.deviceId}")
        print(f"alias: {status.alias}")
        print(f"location: {status.location}")
        print(f"status.version: {status.status.version if status.status else None}")
        print(f"status.battery: {status.status.battery if status.status else None}")
        print(f"status.wifi: {status.status.wifi if status.status else None}")
        print(f"renderInfo.last: {status.renderInfo.last}")
        print(f"renderInfo.current.rotated: {status.renderInfo.current.rotated}")
        print(f"renderInfo.current.border: {status.renderInfo.current.border}")
        print(f"renderInfo.next.battery: {status.renderInfo.next.battery}")


class TestListTasksReal:
    """Real API tests for list_tasks() method."""

    def test_list_tasks_real(self, real_client: Quote0Client, device_id: str):
        """Test listing tasks from real API."""
        tasks = real_client.list_tasks(device_id, task_type="loop")

        assert isinstance(tasks, list)

        for task in tasks:
            assert isinstance(task, Task)
            assert task.type is not None
            assert task.key is not None

        print("\n=== Real API Response: list_tasks() ===")
        for task in tasks:
            print(f"Task: {task.key}")
            print(f"  type: {task.type}")
            print(f"  title: {task.title if task.title else None}")
            print(f"  message: {task.message if task.message else None}")
            print(f"  refreshNow: {task.refreshNow if task.refreshNow else None}")
            print(f"  border: {task.border if task.border else None}")


class TestSwitchToNextReal:
    """Real API tests for switch_to_next() method."""

    def test_switch_to_next_real(self, real_client: Quote0Client, device_id: str):
        """Test switching to next content on real API."""
        response = real_client.switch_to_next(device_id)

        assert isinstance(response, APIResponse)
        assert response.code is not None
        assert response.message is not None
        assert response.result is not None

        print("\n=== Real API Response: switch_to_next() ===")
        print(f"code: {response.code}")
        print(f"message: {response.message}")
        print(f"result: {response.result}")


class TestSendTextReal:
    """Real API tests for send_text() method."""

    def test_send_text_real(
        self,
        real_client: Quote0Client,
        device_id: str,
        sample_text_request: TextContentRequest,
    ):
        """Test sending text content to real API."""
        response = real_client.send_text(device_id, sample_text_request)

        assert isinstance(response, APIResponse)
        assert response.code is not None
        assert response.message is not None
        assert response.result is not None

        print("\n=== Real API Response: send_text() ===")
        print(f"code: {response.code}")
        print(f"message: {response.message}")
        print(f"result: {response.result}")


class TestSendImageReal:
    """Real API tests for send_image() method."""

    def test_send_image_real(
        self,
        real_client: Quote0Client,
        device_id: str,
        sample_image_request: ImageContentRequest,
    ):
        """Test sending image content to real API."""
        response = real_client.send_image(device_id, sample_image_request)

        assert isinstance(response, APIResponse)
        assert response.code is not None
        assert response.message is not None
        assert response.result is not None

        print("\n=== Real API Response: send_image() ===")
        print(f"code: {response.code}")
        print(f"message: {response.message}")
        print(f"result: {response.result}")


class TestModelCompatibility:
    """Tests to verify model compatibility with real API responses."""

    def test_all_endpoints_real(
        self,
        real_client: Quote0Client,
        device_id: str,
        sample_text_request: TextContentRequest,
        sample_image_request: ImageContentRequest,
    ):
        """Test all API endpoints and verify model compatibility.

        This comprehensive test calls all 6 API endpoints and verifies that:
        1. Responses are successfully parsed
        2. All required fields are present
        3. Data types are correct
        """
        print("\n" + "=" * 60)
        print("COMPREHENSIVE REAL API COMPATIBILITY TEST")
        print("=" * 60)

        print("\n1. Testing get_devices()...")
        devices = real_client.get_devices()
        assert len(devices) > 0, "No devices returned"
        assert isinstance(devices[0], Device)
        print("   ✓ PASSED - Devices list retrieved successfully")
        print(f"   Found {len(devices)} device(s)")
        time.sleep(1)

        print("\n2. Testing get_device_status()...")
        status = real_client.get_device_status(device_id)
        assert isinstance(status, DeviceStatus)
        assert status.deviceId == device_id
        print("   ✓ PASSED - Device status retrieved successfully")
        time.sleep(1)

        print("\n3. Testing list_tasks()...")
        tasks = real_client.list_tasks(device_id, task_type="loop")
        assert isinstance(tasks, list)
        if len(tasks) > 0:
            assert isinstance(tasks[0], Task)
        print("   ✓ PASSED - Tasks list retrieved successfully")
        print(f"   Found {len(tasks)} task(s)")
        time.sleep(1)

        print("\n4. Testing switch_to_next()...")
        next_response = real_client.switch_to_next(device_id)
        assert isinstance(next_response, APIResponse)
        print("   ✓ PASSED - Switched to next content successfully")
        print(f"   Message: {next_response.message}")
        time.sleep(1)

        print("\n5. Testing send_text()...")
        text_response = real_client.send_text(device_id, sample_text_request)
        assert isinstance(text_response, APIResponse)
        print("   ✓ PASSED - Text sent successfully")
        print(f"   Message: {text_response.message}")
        time.sleep(1)

        print("\n6. Testing send_image()...")
        image_response = real_client.send_image(device_id, sample_image_request)
        assert isinstance(image_response, APIResponse)
        print("   ✓ PASSED - Image sent successfully")
        print(f"   Message: {image_response.message}")

        print("\n" + "=" * 60)
        print("ALL REAL API TESTS PASSED ✓")
        print("Models are compatible with real API responses")
        print("=" * 60)
