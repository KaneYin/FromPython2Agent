from __future__ import annotations

import pytest

from microagent.tools.base import Tool, ToolRegistry
from microagent.tools.calculator import calculator_tool


class TestCalculatorNormal:
    def test_addition(self):
        assert calculator_tool.invoke(expression="2 + 3") == "5"

    def test_multiplication(self):
        assert calculator_tool.invoke(expression="123 * 456") == "56088"

    def test_division(self):
        assert calculator_tool.invoke(expression="10 / 4") == "2.5"

    def test_integer_division_result(self):
        assert calculator_tool.invoke(expression="10 / 2") == "5"

    def test_power(self):
        assert calculator_tool.invoke(expression="2 ** 10") == "1024"

    def test_sqrt(self):
        assert calculator_tool.invoke(expression="sqrt(144)") == "12"

    def test_sin_pi_over_2(self):
        result = calculator_tool.invoke(expression="sin(pi/2)")
        assert result == "1"

    def test_nested_expression(self):
        assert calculator_tool.invoke(expression="(2 + 3) * (4 - 1)") == "15"

    def test_log(self):
        result = calculator_tool.invoke(expression="log(E)")
        assert float(result) == pytest.approx(1.0)

    def test_abs(self):
        assert calculator_tool.invoke(expression="abs(-42)") == "42"

    def test_large_numbers(self):
        result = calculator_tool.invoke(expression="999999 * 999999")
        assert result == "999998000001"

    def test_float_result(self):
        result = calculator_tool.invoke(expression="1 / 3")
        assert float(result) == pytest.approx(1 / 3, rel=1e-6)


class TestCalculatorDivisionByZero:
    def test_divide_by_zero(self):
        result = calculator_tool.invoke(expression="1 / 0")
        assert "Error" in result

    def test_zero_denominator_complex(self):
        result = calculator_tool.invoke(expression="100 / (5 - 5)")
        assert "Error" in result


class TestCalculatorInvalidExpression:
    def test_empty_expression(self):
        result = calculator_tool.invoke(expression="")
        assert "Error" in result

    def test_nonsense_string(self):
        result = calculator_tool.invoke(expression="hello world")
        assert "Error" in result

    def test_missing_operand(self):
        result = calculator_tool.invoke(expression="2 + ")
        assert "Error" in result


class TestCalculatorInjectionAttack:
    def test_eval_injection(self):
        result = calculator_tool.invoke(expression="__import__('os').system('echo pwned')")
        assert "Error" in result

    def test_dunder_access(self):
        result = calculator_tool.invoke(expression="__builtins__")
        assert "Error" in result

    def test_lambda_injection(self):
        result = calculator_tool.invoke(expression="(lambda: __import__('os'))()")
        assert "Error" in result

    def test_subprocess_injection(self):
        result = calculator_tool.invoke(expression="__import__('subprocess').run(['ls'])")
        assert "Error" in result


class TestToolInvokeErrorWrapping:
    def test_invoke_catches_exception(self):
        def _boom(x: str) -> str:
            raise ValueError("something broke")

        tool = Tool(
            name="boom",
            description="always fails",
            parameters={"type": "object", "properties": {"x": {"type": "string"}}, "required": ["x"]},
            func=_boom,
        )
        result = tool.invoke(x="test")
        assert result == "Error: ValueError: something broke"

    def test_invoke_success_path(self):
        tool = Tool(
            name="echo",
            description="echoes input",
            parameters={"type": "object", "properties": {"msg": {"type": "string"}}, "required": ["msg"]},
            func=lambda msg: f"Echo: {msg}",
        )
        assert tool.invoke(msg="hello") == "Echo: hello"


class TestToolRegistry:
    def setup_method(self):
        self.registry = ToolRegistry()
        self.registry.register(calculator_tool)

    def test_register_and_get(self):
        tool = self.registry.get("calculator")
        assert tool is not None
        assert tool.name == "calculator"

    def test_get_nonexistent(self):
        assert self.registry.get("nonexistent") is None

    def test_list_all(self):
        tools = self.registry.list_all()
        assert len(tools) == 1
        assert tools[0].name == "calculator"

    def test_tool_names(self):
        assert self.registry.tool_names == ["calculator"]

    def test_render_for_prompt(self):
        rendered = self.registry.render_for_prompt()
        assert "calculator" in rendered
        assert "expression" in rendered
