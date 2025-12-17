import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
from mistralai import Mistral
from consensus_metrics import run_pipeline


client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
file_path=os.getenv("FILE_PATH")

clusters, reduced_embeddings, lda, sentiments = run_pipeline(file_path)

quant = client.beta.agents.create(
    model="mistral-medium-latest",
    name="quant",
    description="Data analysis agent",
    instructions= """
        You are Quant, an advanced AI assistant specialized in data analysis, statistical reporting, and visualization.
        Your primary role is to help users ingest, analyze, and interpret datasets, generate summary statistics, identify trends, and create clear, actionable reports and visualizations.
        """,
        completion_args={"temperature": 0.2},
        tools=[{"type": "web-search",
                "type":"code_interpreter",
                }],
    )

message = f"""I have run the script consensus_metrics.py and generated the following datasets: 
 clusters: {clusters},
 reduced_embeddings: {reduced_embeddings}, 
 lda: {lda}, 
 sentiments: {reduced_embeddings}
 Your task is to analyse those datasets and return a summary report for the state of the conversation as it is represented in those datasets.
 You may also provide recommendations for additional analyses I might like to run, and reccomendations for what we could do to advance the conversation.
 Structure your response appropriately so that I can extract the content and save it as a markdown file.
"""

response = client.beta.conversations.start(
    agent_id=quant.id,
    inputs=message,
    
)

with open(f"summary_report.md", 'x') as f:
    f.write(response.outputs[0].content)
