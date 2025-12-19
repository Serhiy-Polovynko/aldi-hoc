from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    question: str


class TokenUsageResponse(BaseModel):
    """Token usage and cost information."""
    input_tokens: int = Field(description="Number of input/prompt tokens")
    output_tokens: int = Field(description="Number of output/completion tokens")
    total_tokens: int = Field(description="Total tokens used")
    input_cost_usd: float = Field(description="Cost of input tokens in USD")
    output_cost_usd: float = Field(description="Cost of output tokens in USD")
    total_cost_usd: float = Field(description="Total cost in USD")
    model: str = Field(description="Model used for the request")


class ChatResponse(BaseModel):
    answer: str
    sql_used: str | None = None
    row_count: int = 0
    usage: TokenUsageResponse = Field(description="Token usage and cost breakdown")


class ModelInfo(BaseModel):
    """Information about an available model."""
    name: str
    input_cost_per_million: float
    output_cost_per_million: float
    description: str


class ModelsResponse(BaseModel):
    """List of available models."""
    current_model: str
    available_models: list[ModelInfo]