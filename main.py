import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
from mistralai import Mistral
from agents.agents import initialize_agents

load_dotenv()

# initialize client
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
file_path = os.getenv("FILE_PATH")

# load script so that we can pass it to the agent later
with open("consensus_metrics.py", "r") as f:
    script = f.read()

# load input data to pass to Dev
with open(file_path, "r") as f:
    input_data = f.read()

# load_prompt
with open("prompts/whisper_message.txt", "r") as f:
    whisper_message = f.read()

# run analysis pipeline
# clusters, reduced_embeddings, lda, sentiments, topic_string = run_pipeline(file_path)

# initialize agents
whisper, quant, dev, spec = initialize_agents()

# Call Whisper agent
print("Calling whisper")
whisper_response = client.beta.conversations.start(
    agent_id=whisper.id,
    inputs=whisper_message,
)

# Parse Whisper response
spec_message, quant_message = whisper_response.outputs[0].content.split(
    "PROMPT FOR QUANT"
)

# Whisper response to disk
with open("outputs/whisper_out.md", "x") as f:
    f.write(whisper_response.outputs[0].content)

print("Calling Spec")
spec_response = client.beta.conversations.start(
    agent_id=spec.id,
    inputs=f"{spec_message}. The existing Python script to use as a starting point is: {script}",
)

try:
    for i in range(len(spec_response.outputs)):
        try:
            specification = spec_response.outputs[i].content
        except AttributeError:
            continue
except:
    print("CANNOT FIND APPROPRIATE SPEC RESPONSE DATA")

with open("outputs/specification.md", "x") as f:
    f.write(specification[0].text)


# Call Dev agent
print("Calling Dev")
dev_response = client.beta.conversations.start(
    agent_id=dev.id,
    inputs=f"{specification} \n\n Existing script to extend and run: {script} \n\n input csv data to run analysis on: {input_data}",
)

with open("outputs/dev.md", "x") as f:
    for i in dev_response.outputs:
        try:
            f.write(i.content)
        except AttributeError:
            f.write(i.arguments)
        except:
            "skipping"


## now call quant to generate report

# quant_response = client.beta.conversations.start(
#     agent_id=quant.id,
#     inputs=f"{dev_response.outputs} \n Current analysis script = {script}"
# )

# # Quant response to disk
# with open(f"outputs/dev_out.md", "x") as f:
#     f.write(dev_response.outputs[0].content)
