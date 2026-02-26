from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.config import rate_limit_per_min, validate_env
from app.error_tracker import track_exception
from app.logging_config import setup_logging
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.request_logger import RequestLoggingMiddleware
from app.routers.health import router as health_router
from app.routers.words import router as words_router
from app.routers.grammar import router as grammar_router
from app.routers.expressions import router as expressions_router
from app.routers.scenarios import router as scenarios_router
from app.routers.user_state import router as user_state_router
from app.routers.study import router as study_router
from app.routers.analysis import router as analysis_router
from app.routers.search import router as search_router
from app.routers.recommend import router as recommend_router
from app.routers.coach import router as coach_router
from app.routers.stats import router as stats_router
from app.routers.achievements import router as achievements_router
from app.routers.transfer import router as transfer_router
from app.routers.ops import router as ops_router
from app.routers.features import router as features_router

setup_logging()

app = FastAPI()
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimitMiddleware, max_requests=rate_limit_per_min())
app.include_router(health_router)
app.include_router(words_router)
app.include_router(grammar_router)
app.include_router(expressions_router)
app.include_router(scenarios_router)
app.include_router(user_state_router)
app.include_router(study_router)
app.include_router(analysis_router)
app.include_router(search_router)
app.include_router(recommend_router)
app.include_router(coach_router)
app.include_router(stats_router)
app.include_router(achievements_router)
app.include_router(transfer_router)
app.include_router(ops_router)
app.include_router(features_router)


@app.on_event("startup")
def on_startup():
    validate_env()


@app.exception_handler(HTTPException)
def http_exception_handler(_: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "detail": exc.detail},
    )


@app.exception_handler(Exception)
def unhandled_exception_handler(request: Request, exc: Exception):
    track_exception(request, exc)
    return JSONResponse(
        status_code=500,
        content={"status": "error", "detail": str(exc)},
    )
