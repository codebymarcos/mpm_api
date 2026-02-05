"""Testes dos agentes."""
import pytest
from synapsis import Planner, Expander


class TestPlanner:
    def test_create_returns_string(self, mock_llm):
        planner = Planner(mock_llm)
        result = planner.create("Python")
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_prompt_contains_topic(self, mock_llm):
        calls = []
        def tracking_llm(prompt):
            calls.append(prompt)
            return mock_llm(prompt)
        
        planner = Planner(tracking_llm)
        planner.create("Machine Learning")
        
        assert len(calls) == 1
        assert "Machine Learning" in calls[0]


class TestExpander:
    def test_expand_returns_string(self, mock_llm):
        expander = Expander(mock_llm)
        result = expander.expand("Python")
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_expand_with_plan(self, mock_llm):
        expander = Expander(mock_llm)
        plan = "title: Python\nchildren:\n  - title: Básico"
        result = expander.expand("Python", plan=plan)
        assert isinstance(result, str)
    
    def test_expand_with_style(self, mock_llm):
        calls = []
        def tracking_llm(prompt):
            calls.append(prompt)
            return mock_llm(prompt)
        
        expander = Expander(tracking_llm)
        expander.expand("Python", style="técnico e detalhado")
        
        assert "técnico e detalhado" in calls[0]
