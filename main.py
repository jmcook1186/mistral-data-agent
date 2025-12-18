import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
from mistralai import Mistral
from consensus_metrics import run_pipeline

# initialize client
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
file_path = os.getenv("FILE_PATH")

# load script so that we can pass it to the agent later
with open("consensus_metrics.py", "r") as f:
    script = f.read()

# run analysis pipeline
clusters, reduced_embeddings, lda, sentiments, topic_string = run_pipeline(file_path)


# initialize agents
# create agent
whisper = client.beta.agents.create(
    model="mistral-medium-latest",
    name="whisper",
    description="prompt engineer",
    instructions="""
        You are Whisper, an agent that designs and optimizes prompts to pass to other agents.
        Your primary role is to manage a team of agents and ensuire they generate outputs that meet my needs. 
        You'll do this by engineering great prompts specific to each agent.
        """,
    completion_args={"temperature": 0.2},
)

quant = client.beta.agents.create(
    model="mistral-medium-latest",
    name="quant",
    description="Data analyst",
    instructions="""
        You are Quant, an advanced AI assistant specialized in data analysis, statistics and scientific writing.
        Your primary role is to ingest, analyze, and interpret data and generate detailed reports. Your reports should identify key results and trends, interpret them and provide clear, actionable reports.
        """,
    completion_args={"temperature": 0.2},
    tools=[
        {
            "type": "web-search",
            "type": "code_interpreter",
        }
    ],
)

dev = client.beta.agents.create(
    model="mistral-medium-latest",
    name="dev",
    description="Software developer",
    instructions="""
        You are Dev, an advanced AI assistant specialized in software engineering. Your specific strength is coding for data analysis and visualization.
        You are skilled using packages such as scikit-learn, numpy, pandas, scipy, matplotlib, and seaborn.
        Your primary role is to write Python code from scratch, improve, extend or debug existing Python code.
        When you return code, you shoul;d always return code that executes successfully. You should double check your work to ensure high standards ofcode efficiency, readability and accuracy.
        Always document your work using comments, docstrings, and for larger pieces of work, dedicated markdown documentation files.
        """,
    completion_args={"temperature": 0.2},
    tools=[
        {
            "type": "web-search",
            "type": "code_interpreter",
        }
    ],
)

# load_prompt
with open("prompts/whisper_message.txt", 'r') as f:
    whisper_message = f.read()


whisper_response = client.beta.conversations.start(
    agent_id=whisper.id,
    inputs=whisper_message,
)

whisper_preamble, whisper_content = whisper_response.outputs[0].content.split("PROMPT FOR QUANT")
quant_message, dev_message = whisper_content.split("PROMPT FOR DEV")

with open(f"whisper_out.md", "x") as f:
    f.write(whisper_response.outputs[0].content)

quant_response = client.beta.conversations.start(
    agent_id=quant.id,
    inputs= f"{quant_message} \n\n clusters:{clusters} \n reduced_embeddings :{reduced_embeddings} \n lda: {lda} \n sentiments: {sentiments} \n topic_string: {topic_string} \n the script used for generated these data is: {script}"
)

quant_report, dev_instructions = quant_response.outputs[0].content.split("INSTRUCTIONS FOR DEV")

with open(f"quant_out.md", "x") as f:
    f.write(quant_response.outputs[0].content)

dev_response = client.beta.conversations.start(
    agent_id=quant.id,
    inputs=f"{dev_message} \n INSTRUCTIONS FROM QUANT: {dev_instructions}. Current analysis script = {script}"
)

with open(f"dev_out.md", "x") as f:
    f.write(dev_response.outputs[0].content)
