# -----------------------
# Model Pricing Configuration (USD per 1M tokens) - Standard tier
# Source: https://platform.openai.com/docs/pricing
# -----------------------
MODEL_PRICING = {
    # GPT-5 series (latest generation)
    "gpt-5.2": {
        "input_per_million": 1.75,
        "cached_input_per_million": 0.175,
        "output_per_million": 14.00,
        "description": "GPT-5.2 - Most advanced model",
    },
    "gpt-5.1": {
        "input_per_million": 1.25,
        "cached_input_per_million": 0.125,
        "output_per_million": 10.00,
        "description": "GPT-5.1 - High capability",
    },
    "gpt-5": {
        "input_per_million": 1.25,
        "cached_input_per_million": 0.125,
        "output_per_million": 10.00,
        "description": "GPT-5 - Fifth generation base",
    },
    "gpt-5-mini": {
        "input_per_million": 0.25,
        "cached_input_per_million": 0.025,
        "output_per_million": 2.00,
        "description": "GPT-5-mini - Fast and affordable",
    },
    "gpt-5-nano": {
        "input_per_million": 0.05,
        "cached_input_per_million": 0.005,
        "output_per_million": 0.40,
        "description": "GPT-5-nano - Ultra low-cost",
    },
    "gpt-5.2-pro": {
        "input_per_million": 21.00,
        "cached_input_per_million": None,
        "output_per_million": 168.00,
        "description": "GPT-5.2-pro - Maximum capability",
    },
    "gpt-5-pro": {
        "input_per_million": 15.00,
        "cached_input_per_million": None,
        "output_per_million": 120.00,
        "description": "GPT-5-pro - Professional grade",
    },
    # GPT-4o series
    "gpt-4o": {
        "input_per_million": 2.50,
        "cached_input_per_million": 1.25,
        "output_per_million": 10.00,
        "description": "GPT-4o - Most capable multimodal model",
    },
    "gpt-4o-mini": {
        "input_per_million": 0.15,
        "cached_input_per_million": 0.075,
        "output_per_million": 0.60,
        "description": "GPT-4o-mini - Fast and cost-effective",
    },
    # GPT-4.1 series (newer)
    "gpt-4.1": {
        "input_per_million": 2.00,
        "cached_input_per_million": 0.50,
        "output_per_million": 8.00,
        "description": "GPT-4.1 - Latest GPT-4 generation",
    },
    "gpt-4.1-mini": {
        "input_per_million": 0.40,
        "cached_input_per_million": 0.10,
        "output_per_million": 1.60,
        "description": "GPT-4.1-mini - Balanced performance/cost",
    },
    "gpt-4.1-nano": {
        "input_per_million": 0.10,
        "cached_input_per_million": 0.025,
        "output_per_million": 0.40,
        "description": "GPT-4.1-nano - Ultra low-cost option",
    },
    # O-series (reasoning models)
    "o1": {
        "input_per_million": 15.00,
        "cached_input_per_million": 7.50,
        "output_per_million": 60.00,
        "description": "O1 - Advanced reasoning model",
    },
    "o1-mini": {
        "input_per_million": 1.10,
        "cached_input_per_million": 0.55,
        "output_per_million": 4.40,
        "description": "O1-mini - Efficient reasoning",
    },
    "o3": {
        "input_per_million": 2.00,
        "cached_input_per_million": 0.50,
        "output_per_million": 8.00,
        "description": "O3 - Latest reasoning model",
    },
    "o3-mini": {
        "input_per_million": 1.10,
        "cached_input_per_million": 0.55,
        "output_per_million": 4.40,
        "description": "O3-mini - Fast reasoning",
    },
    "o4-mini": {
        "input_per_million": 1.10,
        "cached_input_per_million": 0.275,
        "output_per_million": 4.40,
        "description": "O4-mini - Newest reasoning model",
    },
    # Legacy
    "gpt-3.5-turbo": {
        "input_per_million": 0.50,
        "cached_input_per_million": None,
        "output_per_million": 1.50,
        "description": "GPT-3.5-turbo - Legacy budget option",
    },
}