"""
Pytest configuration and fixtures for the test suite.
"""
import os
import tempfile
import shutil
from unittest.mock import Mock, MagicMock
import pytest
import pandas as pd


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_csv_small(temp_dir):
    """Create a small sample CSV file (<50KB)."""
    data = {
        'position_text': [f'Sample text {i}' for i in range(50)],
        'participant_id': [f'P{i % 5}' for i in range(50)],
        'round_number': [i % 3 for i in range(50)]
    }
    df = pd.DataFrame(data)
    csv_path = os.path.join(temp_dir, 'small.csv')
    df.to_csv(csv_path, index=False)
    return csv_path


@pytest.fixture
def sample_csv_medium(temp_dir):
    """Create a medium sample CSV file (50KB-500KB)."""
    data = {
        'position_text': [f'Sample text with more content {i}' * 10 for i in range(600)],
        'participant_id': [f'P{i % 10}' for i in range(600)],
        'round_number': [i % 5 for i in range(600)]
    }
    df = pd.DataFrame(data)
    csv_path = os.path.join(temp_dir, 'medium.csv')
    df.to_csv(csv_path, index=False)
    return csv_path


@pytest.fixture
def sample_csv_large(temp_dir):
    """Create a large sample CSV file (>500KB)."""
    data = {
        'position_text': [f'Sample text with lots of content {i}' * 50 for i in range(3000)],
        'participant_id': [f'P{i % 20}' for i in range(3000)],
        'round_number': [i % 10 for i in range(3000)]
    }
    df = pd.DataFrame(data)
    csv_path = os.path.join(temp_dir, 'large.csv')
    df.to_csv(csv_path, index=False)
    return csv_path


@pytest.fixture
def mock_mistral_client():
    """Create a mock Mistral client."""
    client = Mock()
    client.beta = Mock()
    client.beta.agents = Mock()
    client.beta.conversations = Mock()
    return client


@pytest.fixture
def mock_agent():
    """Create a mock agent with an ID."""
    agent = Mock()
    agent.id = 'test-agent-id-123'
    agent.name = 'test-agent'
    return agent


@pytest.fixture
def mock_message_output():
    """Create a mock MessageOutputEntry."""
    output = Mock()
    output.content = "Sample agent response text"
    return output


@pytest.fixture
def mock_tool_execution_output():
    """Create a mock ToolExecutionOutputEntry."""
    output = Mock()
    output.tool_name = 'code_interpreter'
    output.execution = Mock()
    output.execution.stdout = "Execution output"
    output.execution.stderr = ""
    output.execution.result = {'data': [1, 2, 3]}
    return output


@pytest.fixture
def mock_conversation_response(mock_message_output):
    """Create a mock conversation response."""
    response = Mock()
    response.outputs = [mock_message_output]
    return response


@pytest.fixture
def sample_learning_materials():
    """Sample learning materials content."""
    return """
### Strengths
- Good code structure
- Clear documentation

### Areas for Improvement
- Add more error handling
- Improve test coverage

### Resources
- [Python Best Practices](https://example.com)
"""


@pytest.fixture
def sample_critique_output():
    """Sample Critique agent output."""
    return """
## **Whisper Learning Materials**

### Strengths
- Clear prompt engineering
- Good structure

### Areas for Improvement
- More specific instructions needed

---

## **Spec Learning Materials**

### Strengths
- Thorough analysis

### Areas for Improvement
- Consider edge cases

---

## **Dev Learning Materials**

### Strengths
- Clean code

### Areas for Improvement
- Add logging

---

## **Quant Learning Materials**

### Strengths
- Insightful analysis

### Areas for Improvement
- More actionable recommendations

---

## **UPDATED PROMPTS**

---

### **Updated Whisper Prompt**

You are Whisper, an improved prompt engineer.

---

### **Spec Prompt Suggestions**

Consider these improvements for Spec prompts.

---

### **Dev Prompt Suggestions**

Consider these improvements for Dev prompts.

---

### **Quant Prompt Suggestions**

Consider these improvements for Quant prompts.
"""
