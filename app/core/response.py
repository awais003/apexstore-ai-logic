from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from fastapi.responses import JSONResponse


@dataclass
class APIResponse:
    success: bool  # type: ignore
    errors: Optional[Dict[str, Any]] = field(default_factory=dict)
    status_code: int = 200
    message: Optional[str] = None
    data: Optional[Any] = None
    meta: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "error": self.errors if self.errors else None,
            "meta": self.meta,
        }

    @classmethod
    def success(
        cls,
        status_code: int = 200,
        message: str = "Success",
        data: Any = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> JSONResponse:
        return JSONResponse(
            content=cls(
                success=True,
                message=message,
                data=data,
                status_code=status_code,
                meta=meta,
            ).to_dict(),
            status_code=status_code,
        )

    @classmethod
    def error(
        cls,
        status_code: int = 400,
        message: str = "Error",
        errors: Optional[Dict[str, Any]] = None,
    ) -> JSONResponse:
        return JSONResponse(
            content=cls(
                success=False,
                message=message,
                errors=errors or {},
                status_code=status_code,
            ).to_dict(),
            status_code=status_code,
        )
