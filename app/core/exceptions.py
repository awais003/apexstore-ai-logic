class AppError(Exception):
    code: str = "APP_ERROR"
    status_code: int = 400
    retryable: bool = False

    def __init__(
        self, message: str, code: str | None = None, status_code: int | None = None
    ):
        super().__init__(message)
        self.code = code or self.code
        self.message = message
        self.status_code = status_code or self.status_code

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
        }


class InvalidAIResponse(AppError):
    code: str = "INVALID-AI-RESPONSE"


class TransientError(AppError):
    pass


class InfrastractureError(TransientError):
    code: str = "INFRASTRACTURE-ERROR"


class LLMTimeoutError(InfrastractureError):
    code: str = "LLM_TIMEOUT_ERROR"
    message: str = "LLM Timeout Error"


class ApiTimeoutError(InfrastractureError):
    code: str = "API_TIMEOUT_ERROR"
    message: str = "API Timeout Error"


class VectorStoreError(InfrastractureError):
    code: str = "VECTOR-STORE-ERROR"


class VectorStoreInitializationError(VectorStoreError):
    code: str = "VECTOR-STORE-INIT-ERROR"


class VectorStoreOperationError(VectorStoreError):
    code: str = "VECTOR-STORE-OPERATION-ERROR"


class FetalError(AppError):
    pass


class DomainValidationError(FetalError):
    code: str = "DOMAIN-VALIDATION-ERROR"


class LLMSafetyBlockedError(FetalError):
    code: str = "LLM-SAFETY-BLOCKED-ERROR"


class ValueError(FetalError):
    code: str = "VALUE-ERROR"


class RetryableError(AppError):
    retryable: bool = True
    status_code: int = 503


class NonRetryableError(AppError):
    retryable: bool = False
    status_code: int = 400


class ImageDownloadError(AppError):
    code: str = "IMAGE-DOWNLOAD-ERROR"
