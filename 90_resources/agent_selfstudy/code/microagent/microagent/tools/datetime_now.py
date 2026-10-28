from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from .base import Tool


def _datetime_now(timezone: str = "Asia/Shanghai") -> str:
    tz = ZoneInfo(timezone)
    now = datetime.now(tz)
    return now.strftime(f"%Y-%m-%d %H:%M:%S {timezone}")


DATETIME_NOW_PARAMETERS: dict = {
    "type": "object",
    "properties": {
        "timezone": {
            "type": "string",
            "description": "IANA timezone string, e.g. 'Asia/Shanghai', 'America/New_York', 'UTC'. Defaults to 'Asia/Shanghai'.",
        }
    },
    "required": [],
}


datetime_now_tool = Tool(
    name="datetime_now",
    description=(
        "Returns the current date and time in the specified timezone. "
        "Use this tool when you need to know the current time or date. "
        "Accepts an optional timezone parameter (defaults to Asia/Shanghai)."
    ),
    parameters=DATETIME_NOW_PARAMETERS,
    func=_datetime_now,
)
