"""
Tests for parsing agent responses.
"""
import pytest
from unittest.mock import Mock


class TestWhisperResponseParsing:
    """Tests for parsing Whisper agent responses."""

    def test_parse_valid_whisper_response(self):
        """Test parsing valid Whisper response with delimiter."""
        whisper_content = """
### PROMPT FOR SPEC
This is the spec prompt with detailed instructions.

PROMPT FOR QUANT
This is the quant prompt with analysis requirements.
"""

        spec_message, quant_message = whisper_content.split("PROMPT FOR QUANT", 1)

        assert "PROMPT FOR SPEC" in spec_message
        assert "This is the spec prompt" in spec_message
        assert "This is the quant prompt" in quant_message
        assert "PROMPT FOR QUANT" not in quant_message

    def test_parse_whisper_missing_delimiter(self):
        """Test parsing Whisper response without delimiter."""
        whisper_content = "Just some content without delimiter"

        with pytest.raises(ValueError):
            if "PROMPT FOR QUANT" not in whisper_content:
                raise ValueError("Missing delimiter")

    def test_parse_whisper_empty_sections(self):
        """Test parsing with empty sections."""
        whisper_content = "PROMPT FOR QUANT"

        spec_message, quant_message = whisper_content.split("PROMPT FOR QUANT", 1)

        assert spec_message == ""
        assert quant_message == ""

    def test_parse_whisper_multiple_delimiters(self):
        """Test that split only splits on first occurrence."""
        whisper_content = "Section 1 PROMPT FOR QUANT Section 2 PROMPT FOR QUANT Section 3"

        spec_message, quant_message = whisper_content.split("PROMPT FOR QUANT", 1)

        # Second delimiter should remain in quant_message
        assert "PROMPT FOR QUANT" in quant_message


class TestDevResponseParsing:
    """Tests for parsing Dev agent responses."""

    def test_parse_message_output_entry(self):
        """Test parsing MessageOutputEntry."""
        output = Mock()
        output.content = "This is a text message"

        if hasattr(output, 'content') and output.content:
            content = output.content
            assert content == "This is a text message"

    def test_parse_tool_execution_entry(self):
        """Test parsing ToolExecutionOutputEntry."""
        output = Mock()
        output.tool_name = 'code_interpreter'
        output.execution = Mock()
        output.execution.stdout = "Standard output"
        output.execution.stderr = "Error messages"
        output.execution.result = {'key': 'value'}

        if hasattr(output, 'tool_name') and output.tool_name == 'code_interpreter':
            if hasattr(output, 'execution'):
                exec_data = {
                    'stdout': getattr(output.execution, 'stdout', ''),
                    'stderr': getattr(output.execution, 'stderr', ''),
                    'result': getattr(output.execution, 'result', None)
                }

                assert exec_data['stdout'] == "Standard output"
                assert exec_data['stderr'] == "Error messages"
                assert exec_data['result'] == {'key': 'value'}

    def test_parse_multiple_outputs(self):
        """Test parsing multiple Dev outputs."""
        message_output = Mock()
        message_output.content = "Text message"
        message_output.tool_name = None

        tool_output = Mock()
        tool_output.tool_name = 'code_interpreter'
        tool_output.execution = Mock()
        tool_output.execution.stdout = "Execution output"
        tool_output.execution.stderr = ""
        tool_output.execution.result = None
        tool_output.content = None

        outputs = [message_output, tool_output]

        dev_text_content = []
        dev_code_executions = []

        for output in outputs:
            if hasattr(output, 'content') and output.content:
                dev_text_content.append(output.content)

            if hasattr(output, 'tool_name') and output.tool_name == 'code_interpreter':
                if hasattr(output, 'execution'):
                    exec_data = {
                        'stdout': getattr(output.execution, 'stdout', ''),
                        'stderr': getattr(output.execution, 'stderr', ''),
                        'result': getattr(output.execution, 'result', None)
                    }
                    dev_code_executions.append(exec_data)

        assert len(dev_text_content) == 1
        assert len(dev_code_executions) == 1
        assert dev_text_content[0] == "Text message"
        assert dev_code_executions[0]['stdout'] == "Execution output"

    def test_parse_empty_execution_result(self):
        """Test parsing execution with no result."""
        output = Mock()
        output.tool_name = 'code_interpreter'
        output.execution = Mock()
        output.execution.stdout = ""
        output.execution.stderr = ""
        output.execution.result = None

        exec_data = {
            'stdout': getattr(output.execution, 'stdout', ''),
            'stderr': getattr(output.execution, 'stderr', ''),
            'result': getattr(output.execution, 'result', None)
        }

        assert exec_data['stdout'] == ""
        assert exec_data['stderr'] == ""
        assert exec_data['result'] is None


class TestCritiqueResponseParsing:
    """Tests for parsing Critique agent responses."""

    def test_extract_learning_materials(self, sample_critique_output):
        """Test extracting learning materials from Critique output."""
        content = sample_critique_output

        # Test extraction patterns
        whisper_start = content.find("## **Whisper Learning Materials**")
        spec_start = content.find("## **Spec Learning Materials**")

        assert whisper_start != -1
        assert spec_start != -1
        assert whisper_start < spec_start

    def test_extract_updated_prompts(self, sample_critique_output):
        """Test extracting updated prompts from Critique output."""
        content = sample_critique_output

        whisper_prompt_start = content.find("### **Updated Whisper Prompt**")
        spec_suggestions_start = content.find("### **Spec Prompt Suggestions**")

        assert whisper_prompt_start != -1
        assert spec_suggestions_start != -1
        assert whisper_prompt_start < spec_suggestions_start

    def test_extract_specific_learning_section(self, sample_critique_output):
        """Test extracting a specific learning materials section."""
        content = sample_critique_output

        whisper_marker = "## **Whisper Learning Materials**"
        spec_marker = "## **Spec Learning Materials**"

        if whisper_marker in content and spec_marker in content:
            start_idx = content.find(whisper_marker) + len(whisper_marker)
            end_idx = content.find(spec_marker)
            whisper_learning = content[start_idx:end_idx].strip()

            assert "Clear prompt engineering" in whisper_learning
            assert "Good structure" in whisper_learning

    def test_extract_all_learning_sections(self, sample_critique_output):
        """Test extracting all agent learning sections."""
        content = sample_critique_output

        agent_markers = [
            "## **Whisper Learning Materials**",
            "## **Spec Learning Materials**",
            "## **Dev Learning Materials**",
            "## **Quant Learning Materials**"
        ]

        for marker in agent_markers:
            assert marker in content

    def test_handle_missing_sections(self):
        """Test handling critique output with missing sections."""
        incomplete_content = """
## **Whisper Learning Materials**
Some content

## **UPDATED PROMPTS**
Some prompts
"""

        # Should handle missing sections gracefully
        assert "## **Spec Learning Materials**" not in incomplete_content
        assert "## **Whisper Learning Materials**" in incomplete_content


class TestOutputTypeDetection:
    """Tests for detecting output types."""

    def test_detect_message_output(self):
        """Test detecting MessageOutputEntry."""
        output = Mock(spec=['content'])
        output.content = "Some content"

        is_message = hasattr(output, 'content') and output.content
        is_tool = hasattr(output, 'tool_name')

        assert bool(is_message) is True
        assert bool(is_tool) is False

    def test_detect_tool_output(self):
        """Test detecting ToolExecutionOutputEntry."""
        output = Mock()
        output.tool_name = 'code_interpreter'
        output.content = None

        is_message = hasattr(output, 'content') and output.content
        is_tool = hasattr(output, 'tool_name') and output.tool_name == 'code_interpreter'

        assert bool(is_message) is False
        assert bool(is_tool) is True

    def test_detect_unknown_output(self):
        """Test detecting unknown output type."""
        output = Mock(spec=['some_field'])
        output.some_field = "value"

        is_message = hasattr(output, 'content') and output.content if hasattr(output, 'content') else False
        is_tool = hasattr(output, 'tool_name')

        assert bool(is_message) is False
        assert bool(is_tool) is False


class TestContentTypeConversion:
    """Tests for ensuring content is properly converted to strings."""

    def test_string_content_unchanged(self):
        """Test that string content remains unchanged."""
        content = "Sample string"
        content_str = str(content) if not isinstance(content, str) else content

        assert content_str == content
        assert isinstance(content_str, str)

    def test_list_content_converted(self):
        """Test that list content is converted to string."""
        content = ["item1", "item2", "item3"]
        content_str = str(content) if not isinstance(content, str) else content

        assert isinstance(content_str, str)
        assert "item1" in content_str

    def test_dict_content_converted(self):
        """Test that dict content is converted to string."""
        content = {"key": "value"}
        content_str = str(content) if not isinstance(content, str) else content

        assert isinstance(content_str, str)
        assert "key" in content_str

    def test_none_content_handled(self):
        """Test that None content is handled."""
        content = None
        content_str = str(content) if content is not None else ""

        assert content_str == "" or content_str == "None"
