
import json
import logging
import threading
from datetime import datetime, timezone
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Any
from dataclasses import dataclass, field, asdict
from uuid import uuid4

from aldi_hoc_companion.core.config import get_settings
from aldi_hoc_companion.models import RequestStats, ResponseStats, TokenStats, DBStats

@dataclass
class LogEntry:
    """Complete log entry for a request/response cycle."""
    request: RequestStats
    response: ResponseStats
    tokens: TokenStats
    db: DBStats

    def to_dict(self, level: str = "INFO") -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "level": level,
            "request": asdict(self.request),
            "response": asdict(self.response),
            "tokens": asdict(self.tokens),
            "db": asdict(self.db),
        }

    def to_json(self, level: str = "INFO") -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(level), ensure_ascii=False)


class AppLogger:

    _instance = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls) -> "AppLogger":
        if cls._instance is None:
            with cls._lock:
                # Double-checked locking pattern
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # Thread-safe initialization
        with self._lock:
            if AppLogger._initialized:
                return
            self._setup_logger()
            AppLogger._initialized = True

    def _setup_logger(self) -> None:
        self._settings = get_settings()
        self._log_dir = Path(self._settings.log_dir)
        self._log_dir.mkdir(parents=True, exist_ok=True)

        # Main application logger
        self._logger = logging.getLogger("aldi_hoc_companion")
        self._logger.setLevel(getattr(logging, self._settings.log_level))

        # Prevent duplicate handlers
        if not self._logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_format = logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            console_handler.setFormatter(console_format)
            self._logger.addHandler(console_handler)

            # Daily rotating file handler for structured JSON logs
            log_file = self._log_dir / "requests.log"
            file_handler = TimedRotatingFileHandler(
                filename=str(log_file),
                when="midnight",
                interval=1,
                backupCount=30,  # Keep 30 days of logs
                encoding="utf-8",
            )
            file_handler.suffix = "%Y-%m-%d"
            file_handler.setLevel(logging.INFO)
            file_format = logging.Formatter("%(message)s")
            file_handler.setFormatter(file_format)
            self._logger.addHandler(file_handler)

    def log_request(self, entry: LogEntry) -> None:
        """Log a complete request/response cycle."""
        # JSON log for file (structured)
        self._logger.info(entry.to_json())

        # Summary log for console
        summary = (
            f"[{entry.request.request_id}] "
            f"Q: \"{entry.request.question[:50]}...\" | "
            f"Model: {entry.request.model} | "
            f"Tokens: {entry.tokens.total_tokens} (${entry.tokens.total_cost_usd:.6f}) | "
            f"Duration: {entry.response.duration_ms:.0f}ms | "
            f"{'✓' if entry.response.success else '✗'}"
        )
        if entry.response.success:
            self._logger.info(summary)
        else:
            self._logger.error(summary)

    def info(self, message: str) -> None:
        """Log info message."""
        self._logger.info(message)

    def error(self, message: str) -> None:
        """Log error message."""
        self._logger.error(message)

    def warning(self, message: str) -> None:
        """Log warning message."""
        self._logger.warning(message)

    def debug(self, message: str) -> None:
        """Log debug message."""
        self._logger.debug(message)


# -----------------------
# Singleton Accessor
# -----------------------
def get_logger() -> AppLogger:
    """Get the singleton logger instance."""
    return AppLogger()

