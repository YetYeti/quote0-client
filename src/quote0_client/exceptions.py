class Quote0Error(Exception):
    """Base exception for all Quote0 SDK errors.

    All custom exceptions in the Quote0 SDK inherit from this base class,
    providing a common parent for error handling and classification.
    """

    pass


class AuthenticationError(Quote0Error):
    """Raised when API authentication fails (HTTP 401).

    This exception is raised when:
    - The API key is invalid or expired
    - Invalid authentication credentials are provided
    - The request is unauthorized

    This typically indicates a configuration issue with the API credentials.
    """

    pass


class NotFoundError(Quote0Error):
    """Raised when a requested resource is not found (HTTP 404).

    This exception is raised when:
    - A device ID does not exist or has not been registered
    - A resource is not available in the system
    - The requested entity cannot be located

    This indicates the target resource does not exist in the system.
    """

    pass


class PermissionError(Quote0Error):
    """Raised when insufficient permissions are detected (HTTP 403).

    This exception is raised when:
    - The API key does not have permission to access the requested resource
    - User lacks necessary permissions for the operation
    - Access is explicitly denied

    This indicates authentication succeeded but authorization failed.
    """

    pass


class ValidationError(Quote0Error):
    """Raised when input validation fails (HTTP 400).

    This exception is raised when:
    - Invalid device ID format is provided
    - Invalid image format is submitted
    - Invalid parameters are sent in the request
    - Other client-side validation errors occur

    This indicates the request contains invalid or malformed data.
    """

    pass


class RateLimitError(Quote0Error):
    """Raised when API rate limit is exceeded.

    This exception is raised when:
    - Too many requests are sent within the allowed rate limit (10 req/s)
    - The API's rate limiting policy is violated

    This indicates the client needs to reduce the request rate.
    """

    pass
