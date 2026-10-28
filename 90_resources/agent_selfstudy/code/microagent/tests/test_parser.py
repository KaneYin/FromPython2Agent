from __future__ import annotations

from microagent.parser import parse


class TestParseNormalAction:
    def test_basic_action(self):
        text = """Thought: I need to calculate something
Action: calculator
Action Input: {"expression": "2 + 3"}"""
        result = parse(text)
        assert result.thought == "I need to calculate something"
        assert result.action == "calculator"
        assert result.action_input == {"expression": "2 + 3"}
        assert not result.is_final
        assert result.parse_error is None

    def test_action_with_extra_whitespace(self):
        text = """Thought:   do math
Action:   calculator
Action Input:   {"expression": "10 * 5"}  """
        result = parse(text)
        assert result.action == "calculator"
        assert result.action_input == {"expression": "10 * 5"}

    def test_multiline_thought(self):
        text = """Thought: I should use the calculator
to compute this expression
Action: calculator
Action Input: {"expression": "99"}"""
        result = parse(text)
        assert "calculator" in result.thought
        assert "expression" in result.thought
        assert result.action == "calculator"


class TestParseFinalAnswer:
    def test_basic_final_answer(self):
        text = """Thought: I now know the answer
Final Answer: The result is 42"""
        result = parse(text)
        assert result.is_final is True
        assert result.final_answer == "The result is 42"
        assert result.action is None
        assert result.parse_error is None

    def test_final_answer_priority_over_action(self):
        """When both Final Answer and Action exist, Final Answer wins"""
        text = """Thought: I have enough info
Final Answer: The answer is 5
Action: calculator
Action Input: {"expression": "5"}"""
        result = parse(text)
        assert result.is_final is True
        assert result.final_answer == "The answer is 5"

    def test_final_answer_multiline(self):
        text = """Thought: done
Final Answer: The result of the calculation
is 123. That's the final number."""
        result = parse(text)
        assert result.is_final
        assert "123" in result.final_answer


class TestParseNoActionOrAnswer:
    def test_plain_text(self):
        text = "Just some random text without structure"
        result = parse(text)
        assert result.parse_error == "No Action or Final Answer found"
        assert not result.is_final

    def test_thought_only(self):
        text = "Thought: I'm thinking about it"
        result = parse(text)
        assert result.parse_error == "No Action or Final Answer found"


class TestParseInvalidJson:
    def test_malformed_json(self):
        text = """Thought: compute
Action: calculator
Action Input: {expression: bad json}"""
        result = parse(text)
        assert result.action == "calculator"
        assert result.parse_error is not None
        assert "Invalid JSON" in result.parse_error

    def test_non_object_json(self):
        text = """Thought: compute
Action: calculator
Action Input: "just a string" """
        result = parse(text)
        assert result.action == "calculator"
        assert result.parse_error == "Action Input must be a JSON object"

    def test_array_json(self):
        text = """Thought: compute
Action: calculator
Action Input: [1, 2, 3]"""
        result = parse(text)
        assert result.action == "calculator"
        assert result.parse_error == "Action Input must be a JSON object"


class TestParseIndentedOutput:
    """LLM may indent Action/Action Input when prompt template is indented."""

    def test_indented_action(self):
        text = """Thought: I need to calculate something
    Action: calculator
    Action Input: {"expression": "2 + 3"}"""
        result = parse(text)
        assert result.action == "calculator"
        assert result.action_input == {"expression": "2 + 3"}
        assert result.parse_error is None

    def test_indented_final_answer(self):
        text = """Thought: done
    Final Answer: The result is 42"""
        result = parse(text)
        assert result.is_final
        assert result.final_answer == "The result is 42"

    def test_indented_multiline(self):
        text = """    Thought: I need to calculate
    Action: calculator
    Action Input: {"expression": "123 * 456"}"""
        result = parse(text)
        assert result.action == "calculator"
        assert result.action_input == {"expression": "123 * 456"}


class TestParseMultipleActions:
    def test_takes_first_action(self):
        text = """Thought: step one
Action: calculator
Action Input: {"expression": "1+1"}
Thought: step two
Action: calculator
Action Input: {"expression": "2+2"}"""
        result = parse(text)
        assert result.action == "calculator"
        assert result.action_input == {"expression": "1+1"}
        assert not result.is_final

    def test_missing_action_input(self):
        text = """Thought: compute
Action: calculator"""
        result = parse(text)
        assert result.action == "calculator"
        assert result.parse_error == "No Action Input found"
