from __future__ import annotations

import re
from typing import Any

import sympy
from sympy import sin, cos, tan, sqrt, log, exp, Abs, pi, E

from .base import Tool

_ALLOWED_LOCALS: dict[str, Any] = {
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "sqrt": sqrt,
    "log": log,
    "exp": exp,
    "abs": Abs,
    "pi": pi,
    "e": E,
    "E": E,
}


def _calculate(expression: str) -> str:
    if re.search(r"__\w+__", expression):
        raise ValueError(f"Dunder patterns not allowed: {expression}")
    result = sympy.sympify(expression, locals=_ALLOWED_LOCALS)
    # Evaluate to a numeric value if possible
    if result.is_number:
        result = float(result)
        # Return int if it's a whole number
        if result == int(result):
            return str(int(result))
        return str(result)
    return str(result)


CALCULATOR_PARAMETERS: dict = {
    "type": "object",
    "properties": {
        "expression": {
            "type": "string",
            "description": "A mathematical expression to evaluate, e.g. '2 + 3 * 4', 'sqrt(144)', 'sin(pi/2)'",
        }
    },
    "required": ["expression"],
}


calculator_tool = Tool(
    name="calculator",
    description=(
        "Evaluates mathematical expressions. Supports basic arithmetic (+, -, *, /, **), "
        "and common functions: sin, cos, tan, sqrt, log, exp, abs, pi, e. "
        "Use this tool whenever you need to perform a numerical calculation."
    ),
    parameters=CALCULATOR_PARAMETERS,
    func=_calculate,
)

str_tool = Tool(
    name="string_tool",
    description="A dummy string tool that echoes the input",
    parameters={},
    func=lambda: "This is a string tool",
)