#!/usr/bin/env python3
"""
Quote0 Client SDK Basic Usage Examples

This script demonstrates how to use the Quote0 Python SDK to interact
with Quote0 e-ink devices.

Note: This is a community-maintained client library, not the official Quote0 API.

Requirements:
- Install Quote0 Client SDK: pip install quote0-client
- Get API key from Dot App > More > API Key
- Get device ID from Dot App > Device Details
"""

from quote0_client.client import Quote0Client
from quote0_client.models import TextContentRequest, ImageContentRequest
from quote0_client.exceptions import (
    AuthenticationError,
    NotFoundError,
    Quote0Error,
    ValidationError,
)

# Configuration - Replace with your actual values
API_KEY = "your-api-key-from-dot-app"
DEVICE_ID = "your-device-serial-number"


def example_get_devices():
    """Example: Get list of all connected devices."""
    print("=" * 50)
    print("Example 1: Get Devices List")
    print("=" * 50)

    try:
        client = Quote0Client(api_key=API_KEY)
        devices = client.get_devices()

        if devices:
            print(f"Found {len(devices)} device(s):")
            for device in devices:
                print(f"  - ID: {device.id}")
                print(f"    Model: {device.model}")
                print(f"    Edition: {device.edition}")
                print()
        else:
            print("No devices found. Make sure your device is connected.")

    except AuthenticationError as e:
        print(f"Authentication failed: {e}")
        print("Please check your API key.")
    except Quote0Error as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def example_get_device_status():
    """Example: Get current status of a specific device."""
    print("\n" + "=" * 50)
    print("Example 2: Get Device Status")
    print("=" * 50)

    try:
        client = Quote0Client(api_key=API_KEY)
        status = client.get_device_status(DEVICE_ID)

        print(f"Device ID: {status.deviceId}")
        if status.alias:
            print(f"Device Alias: {status.alias}")
        if status.location:
            print(f"Location: {status.location}")
        print("\nStatus:")
        print(f"  Battery: {status.status.battery}")
        print(f"  WiFi: {status.status.wifi}")
        print("\nRender Info:")
        print(f"  Last: {status.renderInfo.last}")
        print(f"  Next Battery: {status.renderInfo.next.battery}")
        print(f"  Next Power: {status.renderInfo.next.power}")

    except NotFoundError:
        print(f"Error: Device '{DEVICE_ID}' not found!")
        print("Please check your DEVICE_ID configuration.")
    except AuthenticationError as e:
        print(f"Authentication failed: {e}")
    except Quote0Error as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def example_switch_to_next():
    """Example: Switch to the next content on the device."""
    print("\n" + "=" * 50)
    print("Example 3: Switch to Next Content")
    print("=" * 50)

    try:
        client = Quote0Client(api_key=API_KEY)

        response = client.switch_to_next(DEVICE_ID)

        if response.success:
            print("✓ Success: Switched to next content")
            print(f"  Message: {response.message}")
        else:
            print(f"✗ Failed: {response.message}")

    except NotFoundError:
        print(f"Error: Device '{DEVICE_ID}' not found!")
    except ValidationError as e:
        print(f"Validation error: {e}")
    except Quote0Error as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def example_list_tasks():
    """Example: List tasks for a specific device and task type."""
    print("\n" + "=" * 50)
    print("Example 4: List Device Tasks")
    print("=" * 50)

    task_types = ["loop"]

    try:
        client = Quote0Client(api_key=API_KEY)

        for task_type in task_types:
            print(f"\nTask Type: {task_type}")
            tasks = client.list_tasks(DEVICE_ID, task_type)

            if tasks:
                for task in tasks:
                    print(f"  - Key: {task.key}")
                    print(f"    Type: {task.type}")
                    if task.title:
                        print(f"    Title: {task.title}")
                    if task.message:
                        print(f"    Message: {task.message}")
            else:
                print(f"  No tasks found for type: {task_type}")

    except NotFoundError:
        print(f"Error: Device '{DEVICE_ID}' not found!")
    except AuthenticationError as e:
        print(f"Authentication failed: {e}")
    except Quote0Error as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def example_send_text():
    """Example: Send text content to a device."""
    print("\n" + "=" * 50)
    print("Example 5: Send Text Content")
    print("=" * 50)

    try:
        client = Quote0Client(api_key=API_KEY)

        # Create text content request
        text_req = TextContentRequest(
            title="Hello Quote0",
            message="This is a test message from the Python SDK!",
            signature="SDK Example",
            refreshNow=True,
        )

        print("Sending text content...")
        response = client.send_text(DEVICE_ID, text_req)

        if response.success:
            print("✓ Success: Text content sent successfully!")
            print(f"  Message: {response.message}")
        else:
            print(f"✗ Failed: {response.message}")

    except NotFoundError:
        print(f"Error: Device '{DEVICE_ID}' not found!")
    except ValidationError as e:
        print(f"Validation error: {e}")
    except Quote0Error as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def example_send_image():
    """Example: Send image content to a device."""
    print("\n" + "=" * 50)
    print("Example 6: Send Image Content")
    print("=" * 50)

    try:
        client = Quote0Client(api_key=API_KEY)

        # For a real scenario, you would read an image file and convert it to base64:
        #
        # import base64
        # def read_image_as_base64(image_path):
        #     with open(image_path, "rb") as f:
        #         return base64.b64encode(f.read()).decode()
        #
        # image_data = read_image_as_base64("my-image.png")

        # For this example, we'll use a placeholder (you can replace with actual base64 data)
        # You can generate a simple base64 image using tools like:
        # - https://www.base64-image.de/
        # - Online base64 converters

        image_data = "iVBORw0KGgoAAAANSUhEUgAA..."  # Your base64 image data here

        if image_data == "iVBORw0KGgoAAAANSUhEUgAA...":
            print("⚠ Warning: Using placeholder image data.")
            print(
                "  Please replace 'iVBORw0KGgoAAAANSUhEUgAA...' with actual base64 image data."
            )
            print("  Example: Image file converted to base64 using base64.b64encode()")
            return

        image_req = ImageContentRequest(
            image=image_data,
            link="https://dot.mindreset.tech",
            border=0,
            ditherType="NONE",  # No dithering for text images
            refreshNow=True,
        )

        print("Sending image content...")
        response = client.send_image(DEVICE_ID, image_req)

        if response.success:
            print("✓ Success: Image content sent successfully!")
            print(f"  Message: {response.message}")
        else:
            print(f"✗ Failed: {response.message}")

    except NotFoundError:
        print(f"Error: Device '{DEVICE_ID}' not found!")
    except ValidationError as e:
        print(f"Validation error: {e}")
    except Quote0Error as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    """Run all examples."""
    print("\n" + "=" * 50)
    print("Quote0 Python SDK - Basic Usage Examples")
    print("=" * 50)
    print("\n📋 Configuration:")
    print(
        f"  API Key: {API_KEY[:10]}..."
        if len(API_KEY) > 10
        else f"  API Key: {API_KEY}"
    )
    print(f"  Device ID: {DEVICE_ID}")
    print("\n⚠️  IMPORTANT:")
    print("  - Replace API_KEY and DEVICE_ID with your actual values")
    print("  - Get your API key from Dot App > More > API Key")
    print("  - Get your device ID from Dot App > Device Details")
    print("  - Make sure your device is connected to WiFi")
    print("  - Only uncomment the examples you want to run\n")

    # Uncomment the examples you want to run:
    # example_get_devices()
    # example_get_device_status()
    # example_switch_to_next()
    # example_list_tasks()
    # example_send_text()
    # example_send_image()

    print("\n" + "=" * 50)
    print("Ready to run examples!")
    print("=" * 50)


if __name__ == "__main__":
    main()
