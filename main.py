import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
from mistralai import Mistral
from agents.agents import initialize_agents

load_dotenv()

# Validate environment variables
api_key = os.getenv("MISTRAL_API_KEY")
file_path = os.getenv("FILE_PATH")

if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in environment variables")
if not file_path:
    raise ValueError("FILE_PATH not found in environment variables")

# Initialize client
client = Mistral(api_key=api_key)

# Load script
try:
    with open("consensus_metrics.py", "r") as f:
        script = f.read()
    print("✓ Loaded consensus_metrics.py")
except FileNotFoundError:
    raise FileNotFoundError("consensus_metrics.py not found")
except Exception as e:
    raise Exception(f"Error reading consensus_metrics.py: {e}")

# Load input data
try:
    with open(file_path, "r") as f:
        input_data = f.read()
    print(f"✓ Loaded input data from {file_path}")
except FileNotFoundError:
    raise FileNotFoundError(f"Data file not found: {file_path}")
except Exception as e:
    raise Exception(f"Error reading data file: {e}")

# Load prompt
try:
    with open("prompts/whisper_message.txt", "r") as f:
        whisper_message = f.read()
    print("✓ Loaded whisper prompt")
except FileNotFoundError:
    raise FileNotFoundError("prompts/whisper_message.txt not found")
except Exception as e:
    raise Exception(f"Error reading whisper prompt: {e}")

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

# Initialize agents
try:
    whisper, quant, dev, spec = initialize_agents()
    print("✓ Initialized all agents\n")
except Exception as e:
    raise Exception(f"Error initializing agents: {e}")

# ============================================================================
# WHISPER AGENT - Prompt Engineering
# ============================================================================
print("=" * 80)
print("CALLING WHISPER AGENT")
print("=" * 80)

try:
    whisper_response = client.beta.conversations.start(
        agent_id=whisper.id,
        inputs=whisper_message,
    )
    print(f"✓ Whisper responded with {len(whisper_response.outputs)} output(s)")
except Exception as e:
    raise Exception(f"Error calling Whisper agent: {e}")

# Parse Whisper response
try:
    if not whisper_response.outputs:
        raise ValueError("Whisper returned no outputs")

    whisper_content = whisper_response.outputs[0].content
    if not whisper_content:
        raise ValueError("Whisper returned empty content")

    # Split the response to extract spec and quant messages
    if "PROMPT FOR QUANT" not in whisper_content:
        raise ValueError("Whisper response missing 'PROMPT FOR QUANT' delimiter")

    spec_message, quant_message = whisper_content.split("PROMPT FOR QUANT", 1)

    print(f"✓ Parsed Spec message ({len(spec_message)} chars)")
    print(f"✓ Parsed Quant message ({len(quant_message)} chars)")

except Exception as e:
    raise Exception(f"Error parsing Whisper response: {e}")

# Save Whisper response to disk
try:
    with open("outputs/whisper_out.md", "w") as f:
        f.write(whisper_content)
    print("✓ Saved whisper_out.md\n")
except Exception as e:
    print(f"⚠ Warning: Could not save whisper_out.md: {e}\n")

# ============================================================================
# SPEC AGENT - Software Architecture
# ============================================================================
print("=" * 80)
print("CALLING SPEC AGENT")
print("=" * 80)

try:
    spec_response = client.beta.conversations.start(
        agent_id=spec.id,
        inputs=f"{spec_message}. The existing Python script to use as a starting point is: {script}",
    )
    print(f"✓ Spec responded with {len(spec_response.outputs)} output(s)")
except Exception as e:
    raise Exception(f"Error calling Spec agent: {e}")

# Parse Spec response - extract all text content from MessageOutputEntry
specification = []

for i, output in enumerate(spec_response.outputs):
    try:
        # Check if this is a MessageOutputEntry with text content
        if hasattr(output, 'content') and output.content:
            specification.append(output.content)
            print(f"✓ Output {i}: Found text content ({len(output.content)} chars)")
        # Skip tool outputs (web search results)
        elif hasattr(output, 'tool_name'):
            print(f"  Output {i}: Tool output ({output.tool_name}) - skipping")
        else:
            print(f"  Output {i}: Unknown output type - skipping")
    except Exception as e:
        print(f"⚠ Warning: Error processing output {i}: {e}")

if not specification:
    raise ValueError("Spec agent returned no text content")

specification_text = "\n\n".join(specification)
print(f"✓ Combined specification: {len(specification_text)} chars")

# Save Spec response to disk
try:
    with open("outputs/specification.md", "w") as f:
        f.write(specification_text)
    print("✓ Saved specification.md\n")
except Exception as e:
    print(f"⚠ Warning: Could not save specification.md: {e}\n")


# ============================================================================
# DEV AGENT - Software Engineering & Execution
# ============================================================================
print("=" * 80)
print("CALLING DEV AGENT")
print("=" * 80)

try:
    dev_response = client.beta.conversations.start(
        agent_id=dev.id,
        inputs=f"{specification_text} \n\n Existing script to extend and run: {script} \n\n input csv data to run analysis on: {input_data}",
    )
    print(f"✓ Dev responded with {len(dev_response.outputs)} output(s)")
except Exception as e:
    raise Exception(f"Error calling Dev agent: {e}")

# Parse Dev response - extract text messages and code execution results
dev_text_content = []
dev_code_executions = []

for i, output in enumerate(dev_response.outputs):
    output_type = type(output).__name__
    print(f"\nOutput {i}: {output_type}")

    try:
        # Extract text content from MessageOutputEntry
        if hasattr(output, 'content') and output.content:
            dev_text_content.append(output.content)
            print(f"  ✓ Found text content ({len(output.content)} chars)")

        # Extract code execution results from ToolExecutionOutputEntry
        if hasattr(output, 'tool_name') and output.tool_name == 'code_interpreter':
            if hasattr(output, 'execution'):
                execution_result = output.execution
                exec_data = {
                    'stdout': getattr(execution_result, 'stdout', ''),
                    'stderr': getattr(execution_result, 'stderr', ''),
                    'result': getattr(execution_result, 'result', None)
                }
                dev_code_executions.append(exec_data)
                print(f"  ✓ Found code execution result")
                if exec_data['stdout']:
                    print(f"    - stdout: {len(exec_data['stdout'])} chars")
                if exec_data['stderr']:
                    print(f"    - stderr: {len(exec_data['stderr'])} chars")
                if exec_data['result']:
                    print(f"    - result: {str(exec_data['result'])[:100]}...")
            else:
                print(f"  ⚠ Tool execution has no 'execution' attribute")
    except Exception as e:
        print(f"  ⚠ Error processing output {i}: {e}")

if not dev_text_content and not dev_code_executions:
    raise ValueError("Dev agent returned no text content or code execution results")

print(f"\n✓ Collected {len(dev_text_content)} text message(s)")
print(f"✓ Collected {len(dev_code_executions)} code execution(s)")

# Save Dev output to file
try:
    with open("outputs/dev.md", "w") as f:
        f.write("# Dev Agent Output\n\n")

        if dev_text_content:
            f.write("## Agent Messages\n\n")
            for idx, content in enumerate(dev_text_content, 1):
                f.write(f"### Message {idx}\n\n")
                f.write(content + "\n\n")

        if dev_code_executions:
            f.write("## Code Execution Results\n\n")
            for idx, exec_result in enumerate(dev_code_executions, 1):
                f.write(f"### Execution {idx}\n\n")
                if exec_result['stdout']:
                    f.write("**Standard Output:**\n```\n")
                    f.write(exec_result['stdout'])
                    f.write("\n```\n\n")
                if exec_result['stderr']:
                    f.write("**Standard Error:**\n```\n")
                    f.write(exec_result['stderr'])
                    f.write("\n```\n\n")
                if exec_result['result']:
                    f.write(f"**Result:** {exec_result['result']}\n\n")

        if not dev_code_executions:
            f.write("\n⚠ **Warning:** No code execution results found. The Dev agent may not have used the code_interpreter tool.\n")

    print("✓ Saved dev.md\n")
except Exception as e:
    print(f"⚠ Warning: Could not save dev.md: {e}\n")

# ============================================================================
# QUANT AGENT - Data Analysis & Reporting
# ============================================================================
print("=" * 80)
print("CALLING QUANT AGENT")
print("=" * 80)

# Prepare data for Quant agent - combine all text and execution results
quant_input_parts = [quant_message, "\n## Dev Agent Analysis Results\n"]

if dev_text_content:
    quant_input_parts.append("\n### Dev Messages\n")
    quant_input_parts.extend(dev_text_content)

if dev_code_executions:
    quant_input_parts.append("\n## Code Execution Output\n")
    for idx, exec_result in enumerate(dev_code_executions, 1):
        quant_input_parts.append(f"\n### Execution {idx}\n")
        if exec_result['stdout']:
            quant_input_parts.append(f"\n**stdout:**\n```\n{exec_result['stdout']}\n```\n")
        if exec_result['stderr']:
            quant_input_parts.append(f"\n**stderr:**\n```\n{exec_result['stderr']}\n```\n")
        if exec_result['result']:
            quant_input_parts.append(f"\n**result:** {exec_result['result']}\n")
else:
    quant_input_parts.append("\n⚠ Note: No code execution results available from Dev agent.\n")

quant_input_data = "\n".join(quant_input_parts)
print(f"Prepared Quant input ({len(quant_input_data)} chars)")

# Call Quant agent
try:
    quant_response = client.beta.conversations.start(
        agent_id=quant.id,
        inputs=quant_input_data
    )
    print(f"✓ Quant responded with {len(quant_response.outputs)} output(s)")
except Exception as e:
    raise Exception(f"Error calling Quant agent: {e}")

# Parse Quant response - extract all text content
quant_content = []

for i, output in enumerate(quant_response.outputs):
    try:
        # Extract text content from MessageOutputEntry
        if hasattr(output, 'content') and output.content:
            quant_content.append(output.content)
            print(f"✓ Output {i}: Found text content ({len(output.content)} chars)")
        # Skip tool outputs (web search results)
        elif hasattr(output, 'tool_name'):
            print(f"  Output {i}: Tool output ({output.tool_name}) - skipping")
        else:
            print(f"  Output {i}: Unknown output type - skipping")
    except Exception as e:
        print(f"⚠ Warning: Error processing output {i}: {e}")

if not quant_content:
    raise ValueError("Quant agent returned no text content")

quant_report = "\n\n".join(quant_content)
print(f"✓ Combined report: {len(quant_report)} chars")

# Save Quant response to disk
try:
    with open("outputs/quant_out.md", "w") as f:
        f.write(quant_report)
    print("✓ Saved quant_out.md\n")
except Exception as e:
    print(f"⚠ Warning: Could not save quant_out.md: {e}\n")

# ============================================================================
# PIPELINE COMPLETE
# ============================================================================
print("=" * 80)
print("PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 80)
print("\nGenerated files:")
print("  - outputs/whisper_out.md")
print("  - outputs/specification.md")
print("  - outputs/dev.md")
print("  - outputs/quant_out.md")
print("\nAll agents executed successfully!")
