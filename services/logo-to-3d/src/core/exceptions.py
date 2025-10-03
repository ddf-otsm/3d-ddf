"""Custom exceptions for the Logo to 3D service."""


class LogoTo3DException(Exception):
    """Base exception for Logo to 3D service."""

    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(LogoTo3DException):
    """Raised when input validation fails."""

    def __init__(self, message: str, field: str = None):
        super().__init__(
            message=message,
            status_code=400,
            details={"field": field} if field else {}
        )


class FileProcessingError(LogoTo3DException):
    """Raised when file processing fails."""

    def __init__(self, message: str, file_path: str = None):
        super().__init__(
            message=message,
            status_code=400,
            details={"file_path": file_path} if file_path else {}
        )


class FontNotFoundError(LogoTo3DException):
    """Raised when requested font is not available."""

    def __init__(self, font_name: str):
        super().__init__(
            message=f"Font '{font_name}' not found or not supported",
            status_code=400,
            details={"font_name": font_name}
        )


class MaterialNotFoundError(LogoTo3DException):
    """Raised when requested material is not available."""

    def __init__(self, material_name: str):
        super().__init__(
            message=f"Material '{material_name}' not found or not supported",
            status_code=400,
            details={"material_name": material_name}
        )


class ProcessingTimeoutError(LogoTo3DException):
    """Raised when processing takes too long."""

    def __init__(self, timeout_seconds: int):
        super().__init__(
            message=f"Processing timed out after {timeout_seconds} seconds",
            status_code=408,
            details={"timeout_seconds": timeout_seconds}
        )


class BlenderError(LogoTo3DException):
    """Raised when Blender processing fails."""

    def __init__(self, message: str, blender_output: str = None):
        super().__init__(
            message=f"Blender processing failed: {message}",
            status_code=500,
            details={"blender_output": blender_output} if blender_output else {}
        )


class ExportError(LogoTo3DException):
    """Raised when file export fails."""

    def __init__(self, format_name: str, reason: str = None):
        super().__init__(
            message=f"Failed to export to {format_name} format",
            status_code=500,
            details={"format": format_name, "reason": reason} if reason else {"format": format_name}
        )


class JobNotFoundError(LogoTo3DException):
    """Raised when requested job is not found."""

    def __init__(self, job_id: str):
        super().__init__(
            message=f"Job '{job_id}' not found",
            status_code=404,
            details={"job_id": job_id}
        )


class JobProcessingError(LogoTo3DException):
    """Raised when job processing fails."""

    def __init__(self, job_id: str, reason: str):
        super().__init__(
            message=f"Job processing failed: {reason}",
            status_code=500,
            details={"job_id": job_id, "reason": reason}
        )


class ConfigurationError(LogoTo3DException):
    """Raised when service configuration is invalid."""

    def __init__(self, message: str):
        super().__init__(
            message=f"Configuration error: {message}",
            status_code=500
        )


class ResourceLimitExceededError(LogoTo3DException):
    """Raised when resource limits are exceeded."""

    def __init__(self, resource: str, limit: int, actual: int):
        super().__init__(
            message=f"Resource limit exceeded for {resource}: {actual} > {limit}",
            status_code=429,
            details={"resource": resource, "limit": limit, "actual": actual}
        )

