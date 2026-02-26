import logging


logger = logging.getLogger("errors")


def track_exception(request, exc: Exception):
    logger.exception("Unhandled error path=%s", request.url.path, exc_info=exc)
