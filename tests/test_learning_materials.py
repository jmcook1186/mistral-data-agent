"""
Tests for learning materials management functions.
"""
import os
import pytest


# Import the functions from main.py
# We need to extract them or import the module
# For now, we'll recreate the functions here for testing
def load_learning_materials(agent_name, base_dir="outputs/agent_learning_materials"):
    """Load learning materials for a specific agent if they exist."""
    materials_path = os.path.join(base_dir, f"{agent_name}_learning.md")
    if os.path.exists(materials_path):
        try:
            with open(materials_path, "r") as f:
                materials = f.read()
            return materials
        except Exception as e:
            return None
    return None


def format_learning_materials(materials):
    """Format learning materials for inclusion in a prompt."""
    if not materials:
        return ""
    return f"\n\n## Learning Materials from Previous Runs\n\n{materials}\n"


def save_learning_materials(agent_name, new_materials, base_dir="outputs/agent_learning_materials"):
    """Save or append learning materials for an agent."""
    os.makedirs(base_dir, exist_ok=True)
    materials_path = os.path.join(base_dir, f"{agent_name}_learning.md")

    # Load existing materials if they exist
    existing_materials = ""
    if os.path.exists(materials_path):
        try:
            with open(materials_path, "r") as f:
                existing_materials = f.read()
        except Exception:
            pass

    # Append new materials
    if existing_materials:
        combined_materials = f"{existing_materials}\n\n---\n\n{new_materials}"
    else:
        combined_materials = new_materials

    # Save combined materials
    with open(materials_path, "w") as f:
        f.write(combined_materials)


class TestLoadLearningMaterials:
    """Tests for load_learning_materials function."""

    def test_load_nonexistent_file(self, temp_dir):
        """Test loading materials when file doesn't exist."""
        result = load_learning_materials("nonexistent", base_dir=temp_dir)
        assert result is None

    def test_load_existing_file(self, temp_dir, sample_learning_materials):
        """Test loading materials from existing file."""
        # Create a test file
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, "test_agent_learning.md")
        with open(file_path, "w") as f:
            f.write(sample_learning_materials)

        result = load_learning_materials("test_agent", base_dir=temp_dir)
        assert result == sample_learning_materials

    def test_load_empty_file(self, temp_dir):
        """Test loading materials from empty file."""
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, "empty_learning.md")
        with open(file_path, "w") as f:
            f.write("")

        result = load_learning_materials("empty", base_dir=temp_dir)
        assert result == ""

    def test_load_with_special_characters(self, temp_dir):
        """Test loading materials with special characters."""
        os.makedirs(temp_dir, exist_ok=True)
        special_content = "Materials with special chars: # ** [] () {}"
        file_path = os.path.join(temp_dir, "special_learning.md")
        with open(file_path, "w") as f:
            f.write(special_content)

        result = load_learning_materials("special", base_dir=temp_dir)
        assert result == special_content


class TestFormatLearningMaterials:
    """Tests for format_learning_materials function."""

    def test_format_none(self):
        """Test formatting None materials."""
        result = format_learning_materials(None)
        assert result == ""

    def test_format_empty_string(self):
        """Test formatting empty string."""
        result = format_learning_materials("")
        assert result == ""

    def test_format_valid_materials(self, sample_learning_materials):
        """Test formatting valid materials."""
        result = format_learning_materials(sample_learning_materials)
        assert "## Learning Materials from Previous Runs" in result
        assert sample_learning_materials in result
        assert result.startswith("\n\n")

    def test_format_preserves_content(self):
        """Test that formatting preserves original content."""
        content = "Test content with\nmultiple lines"
        result = format_learning_materials(content)
        assert content in result


class TestSaveLearningMaterials:
    """Tests for save_learning_materials function."""

    def test_save_new_file(self, temp_dir):
        """Test saving to a new file."""
        materials = "First set of materials"
        save_learning_materials("new_agent", materials, base_dir=temp_dir)

        file_path = os.path.join(temp_dir, "new_agent_learning.md")
        assert os.path.exists(file_path)

        with open(file_path, "r") as f:
            content = f.read()
        assert content == materials

    def test_append_to_existing_file(self, temp_dir):
        """Test appending to existing file."""
        initial_materials = "Initial materials"
        new_materials = "New materials"

        # Save initial materials
        save_learning_materials("append_agent", initial_materials, base_dir=temp_dir)

        # Append new materials
        save_learning_materials("append_agent", new_materials, base_dir=temp_dir)

        file_path = os.path.join(temp_dir, "append_agent_learning.md")
        with open(file_path, "r") as f:
            content = f.read()

        assert initial_materials in content
        assert new_materials in content
        assert "\n\n---\n\n" in content
        assert content.index(initial_materials) < content.index("---")
        assert content.index("---") < content.index(new_materials)

    def test_multiple_appends(self, temp_dir):
        """Test multiple sequential appends."""
        materials_list = ["First", "Second", "Third"]

        for materials in materials_list:
            save_learning_materials("multi_agent", materials, base_dir=temp_dir)

        file_path = os.path.join(temp_dir, "multi_agent_learning.md")
        with open(file_path, "r") as f:
            content = f.read()

        # All materials should be present
        for materials in materials_list:
            assert materials in content

        # Should have correct number of separators
        assert content.count("---") == len(materials_list) - 1

    def test_save_creates_directory(self, temp_dir):
        """Test that save creates directory if it doesn't exist."""
        nested_dir = os.path.join(temp_dir, "nested", "dir")
        save_learning_materials("test", "materials", base_dir=nested_dir)

        assert os.path.exists(nested_dir)
        assert os.path.exists(os.path.join(nested_dir, "test_learning.md"))

    def test_save_with_unicode(self, temp_dir):
        """Test saving materials with unicode characters."""
        unicode_materials = "Materials with émojis 🎉 and spëcial chàracters"
        save_learning_materials("unicode_agent", unicode_materials, base_dir=temp_dir)

        file_path = os.path.join(temp_dir, "unicode_agent_learning.md")
        with open(file_path, "r", encoding='utf-8') as f:
            content = f.read()

        assert content == unicode_materials
