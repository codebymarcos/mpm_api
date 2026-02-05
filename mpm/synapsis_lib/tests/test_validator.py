"""Testes do validador."""
import pytest
from synapsis import sanitize, validate_schema, clean_and_validate, ValidationError


class TestSanitize:
    def test_remove_yaml_fence(self):
        raw = "```yaml\ntitle: Test\n```"
        assert sanitize(raw) == "title: Test"
    
    def test_remove_plain_fence(self):
        raw = "```\ntitle: Test\n```"
        assert sanitize(raw) == "title: Test"
    
    def test_remove_comments(self):
        raw = "# comentário\ntitle: Test\n# outro"
        assert "# comentário" not in sanitize(raw)
        assert "title: Test" in sanitize(raw)
    
    def test_strip_whitespace(self):
        raw = "  \n\ntitle: Test\n\n  "
        assert sanitize(raw) == "title: Test"
    
    def test_preserve_valid_yaml(self):
        raw = 'title: "Test"\nicon: "🎯"'
        assert sanitize(raw) == raw


class TestValidateSchema:
    def test_valid_simple(self, valid_simple_yaml):
        valid, errors = validate_schema(valid_simple_yaml)
        assert valid
        assert errors == []
    
    def test_valid_complex(self, valid_complex_yaml):
        valid, errors = validate_schema(valid_complex_yaml)
        assert valid
        assert errors == []
    
    def test_invalid_no_title(self, invalid_no_title_yaml):
        valid, errors = validate_schema(invalid_no_title_yaml)
        assert not valid
        assert any("title" in e for e in errors)
    
    def test_invalid_children_type(self, invalid_children_type_yaml):
        valid, errors = validate_schema(invalid_children_type_yaml)
        assert not valid
        assert any("children" in e for e in errors)
    
    def test_invalid_yaml_syntax(self):
        valid, errors = validate_schema("title: [invalid")
        assert not valid


class TestCleanAndValidate:
    def test_clean_valid(self, valid_simple_yaml):
        result = clean_and_validate(valid_simple_yaml)
        assert "title" in result
    
    def test_clean_with_fences(self, mock_llm_with_fences):
        raw = mock_llm_with_fences("")
        result = clean_and_validate(raw)
        assert "```" not in result
        assert "title" in result
    
    def test_raises_on_invalid(self, invalid_no_title_yaml):
        with pytest.raises(ValidationError):
            clean_and_validate(invalid_no_title_yaml)
