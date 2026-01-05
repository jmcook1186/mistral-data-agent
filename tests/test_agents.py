"""
Tests for agent initialization and configuration.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock


class TestAgentInitialization:
    """Tests for initializing all agents."""

    @patch('agents.agents.client')
    def test_initialize_all_agents(self, mock_client):
        """Test that all 5 agents are initialized."""
        # Mock the agent creation
        mock_agent = Mock()
        mock_agent.id = 'test-id'
        mock_client.beta.agents.create.return_value = mock_agent

        from agents.agents import initialize_agents

        whisper, quant, dev, spec, critique = initialize_agents()

        # Should have created 5 agents
        assert mock_client.beta.agents.create.call_count == 5

        # All agents should be returned
        assert whisper is not None
        assert quant is not None
        assert dev is not None
        assert spec is not None
        assert critique is not None


class TestAgentConfigurations:
    """Tests for agent-specific configurations."""

    @patch('agents.agents.client')
    def test_whisper_configuration(self, mock_client):
        """Test Whisper agent configuration."""
        mock_agent = Mock()
        mock_client.beta.agents.create.return_value = mock_agent

        from agents.agents import initialize_agents
        whisper, _, _, _, _ = initialize_agents()

        # Check that whisper was created with correct parameters
        calls = mock_client.beta.agents.create.call_args_list
        whisper_call = calls[0]

        assert whisper_call[1]['model'] == 'mistral-medium-latest'
        assert whisper_call[1]['name'] == 'whisper'
        assert 'prompts' in whisper_call[1]['instructions'].lower() or 'designs' in whisper_call[1]['instructions'].lower()

    @patch('agents.agents.client')
    def test_dev_has_code_interpreter(self, mock_client):
        """Test that Dev agent has code_interpreter tool."""
        mock_agent = Mock()
        mock_client.beta.agents.create.return_value = mock_agent

        from agents.agents import initialize_agents
        _, _, dev, _, _ = initialize_agents()

        # Find the dev agent creation call
        calls = mock_client.beta.agents.create.call_args_list
        dev_call = None
        for call in calls:
            if call[1]['name'] == 'dev':
                dev_call = call
                break

        assert dev_call is not None
        tools = dev_call[1]['tools']

        # Should have both web_search and code_interpreter
        tool_types = [tool['type'] for tool in tools]
        assert 'code_interpreter' in tool_types
        assert 'web_search' in tool_types

    @patch('agents.agents.client')
    def test_all_agents_use_mistral_medium(self, mock_client):
        """Test that all agents use mistral-medium-latest."""
        mock_agent = Mock()
        mock_client.beta.agents.create.return_value = mock_agent

        from agents.agents import initialize_agents
        initialize_agents()

        calls = mock_client.beta.agents.create.call_args_list

        for call in calls:
            assert call[1]['model'] == 'mistral-medium-latest'

    @patch('agents.agents.client')
    def test_agents_have_distinct_names(self, mock_client):
        """Test that all agents have distinct names."""
        mock_agent = Mock()
        mock_client.beta.agents.create.return_value = mock_agent

        from agents.agents import initialize_agents
        initialize_agents()

        calls = mock_client.beta.agents.create.call_args_list
        names = [call[1]['name'] for call in calls]

        # Should have 5 distinct names
        assert len(names) == 5
        assert len(set(names)) == 5

        # Check expected names
        expected_names = {'whisper', 'quant', 'dev', 'spec', 'critique'}
        assert set(names) == expected_names


class TestAgentTools:
    """Tests for agent tool configurations."""

    @patch('agents.agents.client')
    def test_dev_tools_not_duplicated(self, mock_client):
        """Test that Dev tools don't have duplicate type keys."""
        mock_agent = Mock()
        mock_client.beta.agents.create.return_value = mock_agent

        from agents.agents import initialize_agents
        initialize_agents()

        calls = mock_client.beta.agents.create.call_args_list
        dev_call = None
        for call in calls:
            if call[1]['name'] == 'dev':
                dev_call = call
                break

        tools = dev_call[1]['tools']

        # Should be a list of distinct dicts
        assert isinstance(tools, list)
        assert len(tools) == 2

        # Each tool should be a separate dict
        for tool in tools:
            assert isinstance(tool, dict)
            assert 'type' in tool
            # Should only have one 'type' key per dict
            assert list(tool.keys()) == ['type']

    @patch('agents.agents.client')
    def test_quant_has_web_search(self, mock_client):
        """Test that Quant has web_search tool."""
        mock_agent = Mock()
        mock_client.beta.agents.create.return_value = mock_agent

        from agents.agents import initialize_agents
        initialize_agents()

        calls = mock_client.beta.agents.create.call_args_list
        quant_call = None
        for call in calls:
            if call[1]['name'] == 'quant':
                quant_call = call
                break

        tools = quant_call[1]['tools']
        tool_types = [tool['type'] for tool in tools]

        assert 'web_search' in tool_types

    @patch('agents.agents.client')
    def test_critique_has_web_search(self, mock_client):
        """Test that Critique has web_search tool."""
        mock_agent = Mock()
        mock_client.beta.agents.create.return_value = mock_agent

        from agents.agents import initialize_agents
        initialize_agents()

        calls = mock_client.beta.agents.create.call_args_list
        critique_call = None
        for call in calls:
            if call[1]['name'] == 'critique':
                critique_call = call
                break

        tools = critique_call[1]['tools']
        tool_types = [tool['type'] for tool in tools]

        assert 'web_search' in tool_types


class TestAgentInstructions:
    """Tests for agent instruction content."""

    @patch('agents.agents.client')
    def test_dev_instructions_mention_sandbox(self, mock_client):
        """Test that Dev instructions mention remote sandbox."""
        mock_agent = Mock()
        mock_client.beta.agents.create.return_value = mock_agent

        from agents.agents import initialize_agents
        initialize_agents()

        calls = mock_client.beta.agents.create.call_args_list
        dev_call = None
        for call in calls:
            if call[1]['name'] == 'dev':
                dev_call = call
                break

        instructions = dev_call[1]['instructions']

        assert 'sandbox' in instructions.lower()
        assert 'stdout' in instructions.lower()

    @patch('agents.agents.client')
    def test_critique_instructions_mention_learning(self, mock_client):
        """Test that Critique instructions mention learning materials."""
        mock_agent = Mock()
        mock_client.beta.agents.create.return_value = mock_agent

        from agents.agents import initialize_agents
        initialize_agents()

        calls = mock_client.beta.agents.create.call_args_list
        critique_call = None
        for call in calls:
            if call[1]['name'] == 'critique':
                critique_call = call
                break

        instructions = critique_call[1]['instructions']

        assert 'learning' in instructions.lower() or 'improve' in instructions.lower()

    @patch('agents.agents.client')
    def test_spec_instructions_mention_specification(self, mock_client):
        """Test that Spec instructions mention technical specifications."""
        mock_agent = Mock()
        mock_client.beta.agents.create.return_value = mock_agent

        from agents.agents import initialize_agents
        initialize_agents()

        calls = mock_client.beta.agents.create.call_args_list
        spec_call = None
        for call in calls:
            if call[1]['name'] == 'spec':
                spec_call = call
                break

        instructions = spec_call[1]['instructions']

        assert 'specification' in instructions.lower() or 'spec' in instructions.lower()


class TestAgentCompletionArgs:
    """Tests for agent completion arguments."""

    @patch('agents.agents.client')
    def test_agents_have_temperature_settings(self, mock_client):
        """Test that agents have temperature settings."""
        mock_agent = Mock()
        mock_client.beta.agents.create.return_value = mock_agent

        from agents.agents import initialize_agents
        initialize_agents()

        calls = mock_client.beta.agents.create.call_args_list

        for call in calls:
            assert 'completion_args' in call[1]
            assert 'temperature' in call[1]['completion_args']

    @patch('agents.agents.client')
    def test_dev_has_low_temperature(self, mock_client):
        """Test that Dev has low temperature for deterministic code generation."""
        mock_agent = Mock()
        mock_client.beta.agents.create.return_value = mock_agent

        from agents.agents import initialize_agents
        initialize_agents()

        calls = mock_client.beta.agents.create.call_args_list
        dev_call = None
        for call in calls:
            if call[1]['name'] == 'dev':
                dev_call = call
                break

        temperature = dev_call[1]['completion_args']['temperature']

        # Dev should have low temperature (0.1)
        assert temperature <= 0.2
