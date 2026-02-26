import logging
import os
from logging.handlers import RotatingFileHandler

from app.config import log_dir


def setup_logging():
    os.makedirs(log_dir(), exist_ok=True)
    log_path = os.path.join(log_dir(), "app.log")
    err_path = os.path.join(log_dir(), "errors.log")

    file_handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    err_handler = RotatingFileHandler(err_path, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    err_handler.setLevel(logging.ERROR)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        handlers=[logging.StreamHandler(), file_handler, err_handler],
    )

    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
