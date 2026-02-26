import os

from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

_header_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(api_key: str | None = Security(_header_scheme)) -> None:
    """API Key 검증 dependency.

    .env에 API_KEY가 설정된 경우에만 검증을 수행한다.
    API_KEY가 비어 있으면 개발 모드로 간주하여 인증을 건너뜀.
    """
    expected = os.getenv("API_KEY", "").strip()
    if not expected:
        return  # dev 모드: 검증 생략
    if not api_key or api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
