from pydantic_ai import Agent, RunContext
from pydantic_ai.usage import UsageLimits

from aldi_hoc_companion.core.config import get_settings
from aldi_hoc_companion.db import Database
from aldi_hoc_companion.models.agent_models import AgentDeps, AgentResponse, QueryResult, TokenUsage

_settings = get_settings()

SYSTEM_PROMPT = """You are a data analyst. Answer questions about the Aldi marketing database.
The database content is provided below - analyze it to answer the user's question.
Think semantically - if user asks about anything, field values that are shown to you.
Answer in the user's language. Be specific with examples from the data."""

agent = Agent(
    _settings.pydantic_ai_model_string,
    deps_type=AgentDeps,
    system_prompt=SYSTEM_PROMPT,
)

@agent.system_prompt
async def add_database_content(ctx: RunContext[AgentDeps]) -> str:
    """Load ALL database content into context."""
    db = ctx.deps.db
    
    # Get all projects
    projects = await db.execute("SELECT project_id, project_name, year FROM projects ORDER BY year DESC")
    
    # Get asset summaries with content descriptions
    assets = await db.execute("""
        SELECT p.project_name, p.year, a.asset_kind, a.asset_content, a.language, a.file_name, a.description, a.version, a.document_content, a.campaign_context
        FROM assets a 
        JOIN projects p ON a.project_id = p.id
        ORDER BY p.year DESC, p.project_name
    """)
    
    # Get stats
    stats = await db.execute("""
        SELECT 
            (SELECT COUNT(*) FROM projects) as total_projects,
            (SELECT COUNT(*) FROM assets) as total_assets
    """)
    
    # Format for LLM
    content = f"\n\n=== DATABASE CONTENT ===\n"
    content += f"\nSTATS: {stats[0]['total_projects']} projects, {stats[0]['total_assets']} assets\n"
    
    content += f"\n--- PROJECTS ({len(projects)}) ---\n"
    for p in projects:
        content += f"- {p['project_name']} ({p['year']})\n"
    
    content += f"\n--- ALL ASSETS ({len(assets)}) ---\n"
    for a in assets:
        desc = str(a.get('asset_content', ''))
        content += f"[{a['asset_kind']}] {a['project_name']}: {desc}\n"
    
    return content


async def ask(question: str) -> AgentResponse:
    settings = get_settings()
    db = Database()
    deps = AgentDeps(db=db, question=question)
    
    # Just 1 API call - no tools, all data in context
    result = await agent.run(question, deps=deps, usage_limits=UsageLimits(request_limit=2))
    
    answer = str(result.output) if result.output else ""
    
    usage = result.usage()
    input_tokens = usage.request_tokens or 0
    output_tokens = usage.response_tokens or 0
    input_cost = input_tokens * settings.model_input_cost_per_token
    output_cost = output_tokens * settings.model_output_cost_per_token
    
    token_usage = TokenUsage(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=usage.total_tokens or 0,
        input_cost_usd=round(input_cost, 6),
        output_cost_usd=round(output_cost, 6),
        total_cost_usd=round(input_cost + output_cost, 6),
        model=settings.openai_model,
    )
    
    query_result = QueryResult(answer=answer)
    return AgentResponse(result=query_result, usage=token_usage)
