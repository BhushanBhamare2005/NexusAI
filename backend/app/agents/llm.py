import json
import logging
import re

from app.core.config import settings

logger = logging.getLogger(__name__)
LLM_METRICS = {"requests": 0, "successes": 0, "fallbacks": 0, "errors": 0}


class LLMConfigurationError(RuntimeError):
    pass


class LLMRequestError(RuntimeError):
    pass


def format_prompt(template: str, **values: object) -> str:
    escaped = template.replace("{", "{{").replace("}", "}}")
    for key in values:
        escaped = escaped.replace("{{" + key + "}}", "{" + key + "}")
    return escaped.format(**values)


async def llm_text(prompt: str) -> str:
    LLM_METRICS["requests"] += 1
    if not settings.GEMINI_API_KEY:
        raise LLMConfigurationError("Gemini is not configured")

    try:
        from langchain_google_genai import ChatGoogleGenerativeAI

        client = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            temperature=0.2,
            max_output_tokens=768,
            google_api_key=settings.GEMINI_API_KEY,
        )
        response = await client.ainvoke(prompt)
        if not isinstance(response.content, str) or not response.content.strip():
            raise LLMRequestError("Gemini returned an empty response")
        LLM_METRICS["successes"] += 1
        return response.content.strip()
    except LLMRequestError:
        LLM_METRICS["errors"] += 1
        raise
    except Exception as exc:
        LLM_METRICS["errors"] += 1
        logger.error("Gemini text request failed (%s)", type(exc).__name__)
        raise LLMRequestError("Gemini request failed") from exc


async def llm_json(prompt: str) -> dict | None:
    LLM_METRICS["requests"] += 1
    if not settings.GEMINI_API_KEY:
        LLM_METRICS["fallbacks"] += 1
        return None

    try:
        from langchain_google_genai import ChatGoogleGenerativeAI

        client = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
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
