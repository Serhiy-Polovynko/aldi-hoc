from dataclasses import dataclass
from pydantic import BaseModel, Field
from aldi_hoc_companion.db import Database


@dataclass
class AgentDeps:
    db: Database
    question: str


class TokenUsage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    input_cost_usd: float = 0.0
    output_cost_usd: float = 0.0
    total_cost_usd: float = 0.0
    model: str = ""


class QueryResult(BaseModel):
    answer: str = Field(description="Answer to the question")
    sql_used: str | None = None
    row_count: int = 0


class AgentResponse(BaseModel):
    result: QueryResult
    usage: TokenUsage
