import json
import logging
import re

from app.core.config import settings

logger = logging.getLogger(__name__)
LLM_METRICS = {"requests": 0, "successes": 0, "fallbacks": 0, "errors": 0}


def format_prompt(template: str, **values: object) -> str:
    escaped = template.replace("{", "{{").replace("}", "}}")
    for key in values:
        escaped = escaped.replace("{{" + key + "}}", "{" + key + "}")
    return escaped.format(**values)


async def llm_json(prompt: str) -> dict | None:
    LLM_METRICS["requests"] += 1
    if not settings.GEMINI_API_KEY:
        LLM_METRICS["fallbacks"] += 1
        return None

    try:
        from langchain_google_genai import ChatGoogleGenerativeAI

        client = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.1,
            google_api_key=settings.GEMINI_API_KEY,
        )
        msg = await client.ainvoke(prompt)
        content = msg.content
        if not isinstance(content, str):
            LLM_METRICS["fallbacks"] += 1
            return None
        content = content.strip()
        content = re.sub(r"^```(?:json)?\s*", "", content, flags=re.IGNORECASE)
        content = re.sub(r"\s*```$", "", content)
        parsed = json.loads(content)
        if isinstance(parsed, dict):
            LLM_METRICS["successes"] += 1
            return parsed
        LLM_METRICS["fallbacks"] += 1
        return None
    except Exception:
        LLM_METRICS["errors"] += 1
        LLM_METRICS["fallbacks"] += 1
        logger.exception("LLM request or JSON parsing failed; using rule fallback")
        return None
