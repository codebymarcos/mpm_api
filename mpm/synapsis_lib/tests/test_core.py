"""Testes do core (Builder e generate)."""
import pytest
import tempfile
from pathlib import Path
from synapsis import generate, SynapsisBuilder, ValidationError


class TestSynapsisBuilder:
    def test_init(self, mock_llm):
        builder = SynapsisBuilder(mock_llm)
        assert builder.llm == mock_llm
    
    def test_expand(self, mock_llm):
        builder = SynapsisBuilder(mock_llm)
        result = builder.expand("Python")
        assert result == builder
        assert builder.get_yaml() != ""
    
    def test_validate(self, mock_llm):
        builder = SynapsisBuilder(mock_llm)
        builder.expand("Python").validate()
        yaml = builder.get_yaml()
        assert "title" in yaml
    
    def test_render(self, mock_llm):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "test.html"
            builder = SynapsisBuilder(mock_llm)
            path = builder.expand("Python").validate().render(str(output))
            
            assert Path(path).exists()
            content = Path(path).read_text()
            assert "Synapsis" in content
            assert "renderNode" in content
    
    def test_plan_and_expand(self, mock_llm):
        builder = SynapsisBuilder(mock_llm)
        yaml = builder.plan_and_expand("Python", style="conciso")
        assert "title" in yaml
    
    def test_chain_methods(self, mock_llm):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "chain.html"
            builder = SynapsisBuilder(mock_llm)
            path = builder.plan("Python").expand("Python").validate().render(str(output))
            assert Path(path).exists()


class TestGenerate:
    def test_generate_creates_html(self, mock_llm):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "gen.html"
            path = generate("Python", mock_llm, output=str(output))
            
            assert Path(path).exists()
            content = Path(path).read_text()
            assert "<html" in content
            assert "DATA" in content
    
    def test_generate_default_output(self, mock_llm):
        import os
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            try:
                path = generate("Python", mock_llm)
                assert Path(path).exists()
                assert "mindmap.html" in path
            finally:
                os.chdir(old_cwd)
    
    def test_generate_with_style(self, mock_llm):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "styled.html"
            path = generate("Python", mock_llm, output=str(output), style="técnico")
            assert Path(path).exists()
    
    def test_generate_handles_fences(self, mock_llm_with_fences):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "fences.html"
            path = generate("Python", mock_llm_with_fences, output=str(output))
            
            content = Path(path).read_text()
            assert "```" not in content
