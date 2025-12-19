import asyncio
from dataclasses import dataclass
from functools import partial
from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor

from aldi_hoc_companion.core.config import get_settings


@dataclass
class Project:
    project_id: str
    project_name: str
    year: int


class Database:

    def __init__(self):
        self._settings = get_settings()

    def _get_conn(self):
        return psycopg2.connect(
            host=self._settings.db_host,
            port=self._settings.db_port,
            dbname=self._settings.db_name,
            user=self._settings.db_user,
            password=self._settings.db_password,
            cursor_factory=RealDictCursor,
        )

    def _execute_sync(self, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
        """Execute SQL synchronously."""
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                return [dict(row) for row in cur.fetchall()]
        finally:
            conn.close()

    async def execute(self, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
        """Execute SQL asynchronously (runs sync code in executor)."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(self._execute_sync, sql, params))

    async def get_schema(self) -> str:
        """Return database schema description for LLM."""
        return """
DATABASE SCHEMA & RELATIONSHIPS:

TABLE: projects (Marketing campaigns/initiatives)
  - id: internal primary key
  - project_id: unique project identifier (e.g., "2024_ALDI_Christmas")
  - project_name: Dutch name describing the campaign (e.g., "Kerstcampagne 2024")
  - year: the year of the project (2023, 2024, 2025...)

TABLE: assets (Files belonging to projects)
  - id: internal primary key
  - project_id: FOREIGN KEY → links to projects.project_id (EVERY asset belongs to a project)
  - file_name: original filename
  - file_path: storage location
  - file_type: extension (.psd, .jpg, .mp4, .pdf, etc.)
  - file_size: size in bytes
  - description: metadata about the asset
  - language: French, Dutch, English, Multilingual, None
  - version: version number if applicable
  - asset_kind: type category (banner, photo, document, email, video, etc.)
  - asset_content: AI-generated description of what the visual/content shows
  - document_content: extracted text from PDFs/documents
  - campaign_context: 'briefing' (planning docs) or 'execution' (final deliverables)

RELATIONSHIPS:
  projects (1) ──→ (many) assets
  - One project has MANY assets
  - Use JOIN when you need project info alongside asset info
  - Example: SELECT p.project_name, COUNT(a.id) FROM projects p LEFT JOIN assets a ON p.project_id = a.project_id GROUP BY p.project_id

KEY QUERY PATTERNS:
  - Count projects: SELECT COUNT(DISTINCT project_id) FROM projects
  - Projects by year: WHERE year = 2024
  - Projects by theme: WHERE project_name ILIKE '%kerst%' OR project_name ILIKE '%christmas%'
  - Language distribution: SELECT language, COUNT(*) FROM assets GROUP BY language
  - Recent items: ORDER BY id DESC LIMIT N (higher id = more recent)
  - Asset types: GROUP BY asset_kind
  - Search content: WHERE asset_content ILIKE '%keyword%' OR project_name ILIKE '%keyword%'

DUTCH KEYWORDS (project_name is usually Dutch):
  - Christmas/Holiday: kerst, feest, nieuwjaar, eind jaar
  - Seasonal: zomer (summer), lente (spring), herfst (autumn), winter
  - Promotions: promo, actie, korting, folder
  - Always-on: always-on, doorlopend, permanent

TOOLS AVAILABLE:
1. explore_asset_content - Sample random assets to see what's in the database (USE THIS FIRST)
2. query_database - Run specific SQL queries when you need filtered results  
3. get_database_stats - Get counts and statistics

STRATEGY: 
1. FIRST understand the question type (counting, searching, aggregating)
2. For counts/stats: use direct queries with COUNT, GROUP BY
3. For thematic searches: explore first, then query with discovered keywords
4. Always JOIN tables when you need both project and asset information
""".strip()

    async def get_stats(self) -> dict[str, Any]:
        """Get quick database statistics."""
        stats = {}
        
        result = await self.execute("SELECT COUNT(*) as count FROM projects")
        stats["total_projects"] = result[0]["count"] if result else 0
        
        result = await self.execute("SELECT COUNT(*) as count FROM assets")
        stats["total_assets"] = result[0]["count"] if result else 0
        
        result = await self.execute(
            "SELECT year, COUNT(*) as count FROM projects GROUP BY year ORDER BY year DESC LIMIT 5"
        )
        stats["projects_by_year"] = result
        
        return stats

