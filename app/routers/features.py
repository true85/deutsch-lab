from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/features", tags=["features"])


@router.post("/ocr")
def ocr_placeholder():
    raise HTTPException(status_code=501, detail="OCR feature is deferred")


@router.post("/voice")
def voice_placeholder():
    raise HTTPException(status_code=501, detail="Voice feature is deferred")
