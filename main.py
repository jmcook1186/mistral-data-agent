import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
from mistralai import Mistral
from consensus_metrics import run_pipeline
from agents.agents import initialize_agents

load_dotenv()

# initialize client
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
file_path = os.getenv("FILE_PATH")

# load script so that we can pass it to the agent later
with open("consensus_metrics.py", "r") as f:
    script = f.read()

# load_prompt
with open("prompts/whisper_message.txt", 'r') as f:
    whisper_message = f.read()

# run analysis pipeline
clusters, reduced_embeddings, lda, sentiments, topic_string = run_pipeline(file_path)

# initialize agents
whisper, quant, dev = initialize_agents()


# Call Whisper agent
whisper_response = client.beta.conversations.start(
    agent_id=whisper.id,
    inputs=whisper_message,
)

# Parse Whisper response
whisper_preamble, whisper_content = whisper_response.outputs[0].content.split("PROMPT FOR QUANT")
quant_message, dev_message = whisper_content.split("PROMPT FOR DEV")

# Whisper response to disk
with open(f"outputs/whisper_out.md", "x") as f:
    f.write(whisper_response.outputs[0].content)

# Call Quant agent
quant_response = client.beta.conversations.start(
    agent_id=quant.id,
    inputs= f"{quant_message} \n\n clusters:{clusters} \n reduced_embeddings :{reduced_embeddings} \n lda: {lda} \n sentiments: {sentiments} \n topic_string: {topic_string} \n the script used for generated these data is: {script}"
)
# parse Quant response
quant_report, dev_instructions = quant_response.outputs[0].content.split("INSTRUCTIONS FOR DEV")

# Quant response to disk
with open(f"outputs/quant_out.md", "x") as f:
    f.write(quant_response.outputs[0].content)

# Call Dev agent
dev_response = client.beta.conversations.start(
    agent_id=dev.id,
    inputs=f"{dev_message} \n INSTRUCTIONS FROM QUANT: {dev_instructions}. Current analysis script = {script}"
)

# Dev response to disk
with open(f"outputs/dev_out.md", "x") as f:
    f.write(dev_response.outputs[0].content)
