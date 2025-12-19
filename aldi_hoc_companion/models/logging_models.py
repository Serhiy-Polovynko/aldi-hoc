from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

@dataclass
class DBStats:
    """Database connection statistics."""
    connected: bool = False
    query_count: int = 0
    total_query_time_ms: float = 0.0
    last_query_time_ms: float = 0.0


@dataclass
class RequestStats:
    """Request statistics."""
    request_id: str = field(default_factory=lambda: str(uuid4())[:8])
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    question: str = ""
    model: str = ""


@dataclass
class ResponseStats:
    """Response statistics."""
    answer: str = ""
    sql_used: str | None = None
    row_count: int = 0
    duration_ms: float = 0.0
    success: bool = True
    error: str | None = None


@dataclass
class TokenStats:
    """Token usage and cost statistics."""
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    input_cost_usd: float = 0.0
    output_cost_usd: float = 0.0
    total_cost_usd: float = 0.0