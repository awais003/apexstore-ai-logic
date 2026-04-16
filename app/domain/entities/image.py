from app.core.exceptions import DomainValidationError
from app.domain.entities.entity import Entity


SUPPORTED_GEMINI_MIMES = {
    "image/png",
    "image/jpeg",
    "image/webp",
    "image/heic",
    "image/heif",
}


class Image(Entity):

    def __init__(self, content: bytes, mime_type: str) -> None:
        self.content = content
        self.mime_type = mime_type

    def _validate(self):
        normalized_mime = self.mime_type.lower().strip()
        if normalized_mime == "image/jpg":
            normalized_mime = "image/jpeg"

        if normalized_mime not in SUPPORTED_GEMINI_MIMES:
            raise DomainValidationError("mime type does not support")
