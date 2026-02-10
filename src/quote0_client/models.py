"""Quote0 SDK Data Models using Pydantic v2.

This module defines all data models for the Quote0 SDK, including device information,
status, rendering info, tasks, and API requests/responses.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class Device(BaseModel):
    """Represents a Quote0 device.

    Attributes:
        series: Device series (e.g., 'quote')
        model: Device model (e.g., 'quote_0')
        edition: Device edition (1 or 2)
        id: Device serial number
    """

    series: str = Field(description="Device series (e.g., 'quote')")
    model: str = Field(description="Device model (e.g., 'quote_0')")
    edition: int = Field(description="Device edition (1 or 2)")
    id: str = Field(description="Device serial number")


class BatteryStatus(BaseModel):
    """Battery status information.

    Attributes:
        version: Battery firmware version
        current: Current battery status
        description: Description of current status
        battery: Battery level status
        wifi: WiFi signal strength
    """

    version: str = Field(description="Battery firmware version")
    current: str = Field(description="Current battery status")
    description: str = Field(description="Description of current status")
    battery: str = Field(description="Battery level status")
    wifi: str = Field(description="WiFi signal strength")


class RenderInfo(BaseModel):
    """Rendering information for a device.

    Attributes:
        last: Last render timestamp
        current: Current render information
        next: Next render time information
    """

    last: str = Field(description="Last render timestamp")
    current: "CurrentRenderInfo" = Field(description="Current render information")
    next: "NextRenderTime" = Field(description="Next render time information")


class CurrentRenderInfo(BaseModel):
    """Current render information.

    Attributes:
        rotated: Whether the display is rotated
        border: Border style (0 or 1)
        image: List of render image URLs
    """

    rotated: bool = Field(description="Whether the display is rotated")
    border: int = Field(description="Border style (0=white, 1=black)")
    image: List[str] = Field(description="List of render image URLs")


class NextRenderTime(BaseModel):
    """Next render time information.

    Attributes:
        battery: Next battery update timestamp
        power: Next power update timestamp
    """

    battery: str = Field(description="Next battery update timestamp")
    power: str = Field(description="Next power update timestamp")


class DeviceStatus(BaseModel):
    """Complete device status information.

    Attributes:
        deviceId: Device serial number
        alias: Optional device alias
        location: Optional device location
        status: Battery and WiFi status
        renderInfo: Rendering information
    """

    deviceId: str = Field(description="Device serial number")
    alias: Optional[str] = Field(default=None, description="Optional device alias")
    location: Optional[str] = Field(
        default=None, description="Optional device location"
    )
    status: BatteryStatus = Field(description="Battery and WiFi status")
    renderInfo: RenderInfo = Field(description="Rendering information")


class Task(BaseModel):
    """Task information for the device.

    Attributes:
        type: Task type (TEXT_API or IMAGE_API)
        key: Unique task key
        refreshNow: Whether to refresh immediately
        title: Text title (for TEXT_API tasks)
        message: Text message (for TEXT_API tasks)
        border: Border style (for IMAGE_API tasks)
        ditherType: Dither type (for IMAGE_API tasks)
        ditherKernel: Dither kernel (for IMAGE_API tasks)
    """

    type: str = Field(description="Task type (TEXT_API or IMAGE_API)")
    key: str = Field(description="Unique task key")
    refreshNow: bool = Field(default=True, description="Whether to refresh immediately")
    title: Optional[str] = Field(
        default=None, description="Text title (for TEXT_API tasks)"
    )
    message: Optional[str] = Field(
        default=None, description="Text message (for TEXT_API tasks)"
    )
    border: Optional[int] = Field(
        default=None, description="Border style (0 or 1, for IMAGE_API tasks)"
    )
    ditherType: Optional[str] = Field(
        default="DIFFUSION",
        description="Dither type (DIFFUSION, ORDERED, or NONE, for IMAGE_API tasks)",
    )
    ditherKernel: Optional[str] = Field(
        default="FLOYD_STEINBERG", description="Dither kernel (for IMAGE_API tasks)"
    )


class TextContentRequest(BaseModel):
    """Text content request for TEXT_API tasks.

    Attributes:
        refreshNow: Whether to refresh immediately (default: True)
        title: Text title
        message: Text message
        signature: Optional signature text
        icon: Optional Base64 PNG icon (40px×40px)
        link: Optional URL link
        taskKey: Optional task key
    """

    refreshNow: Optional[bool] = Field(
        default=True, description="Whether to refresh immediately"
    )
    title: Optional[str] = Field(default=None, description="Text title")
    message: Optional[str] = Field(default=None, description="Text message")
    signature: Optional[str] = Field(
        default=None, description="Optional signature text"
    )
    icon: Optional[str] = Field(
        default=None, description="Optional Base64 PNG icon (40px×40px)"
    )
    link: Optional[str] = Field(default=None, description="Optional URL link")
    taskKey: Optional[str] = Field(default=None, description="Optional task key")


class ImageContentRequest(BaseModel):
    """Image content request for IMAGE_API tasks.

    Attributes:
        refreshNow: Whether to refresh immediately (default: True)
        image: Base64 PNG image (296px×152px, required)
        link: Optional URL link
        border: Border style (default: 0, 0=white, 1=black)
        ditherType: Dither type (default: DIFFUSION, options: DIFFUSION, ORDERED, NONE)
        ditherKernel: Dither kernel (default: FLOYD_STEINBERG)
        taskKey: Optional task key
    """

    refreshNow: Optional[bool] = Field(
        default=True, description="Whether to refresh immediately"
    )
    image: str = Field(description="Base64 PNG image (296px×152px, required)")
    link: Optional[str] = Field(default=None, description="Optional URL link")
    border: Optional[int] = Field(
        default=0, description="Border style (0=white, 1=black)"
    )
    ditherType: Optional[str] = Field(
        default="DIFFUSION", description="Dither type (DIFFUSION, ORDERED, or NONE)"
    )
    ditherKernel: Optional[str] = Field(
        default="FLOYD_STEINBERG", description="Dither kernel"
    )
    taskKey: Optional[str] = Field(default=None, description="Optional task key")


class APIResponse(BaseModel):
    """Generic API response wrapper.

    Attributes:
        code: Response code (0 for success, non-zero for errors) - can be string or int
        message: Response message
        result: Response result data (optional)

    Example:
        >>> APIResponse(code=0, message="Success", result={"message": "Done"})
    """

    code: str | int = Field(
        description="Response code (0 for success, non-zero for errors)"
    )
    message: str = Field(description="Response message")
    result: Optional[Dict[str, Any]] = Field(
        default=None, description="Response result data"
    )

    @property
    def success(self) -> bool:
        """Check if the response was successful.

        Returns:
            True if code is 0, False otherwise.
        """
        return self.code == 0
