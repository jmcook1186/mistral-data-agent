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

# create agent
quant = client.beta.agents.create(
    model="mistral-medium-latest",
    name="quant",
    description="Data analysis agent",
    instructions="""
        You are Quant, an advanced AI assistant specialized in data analysis, statistical reporting, and visualization.
        Your primary role is to help users ingest, analyze, and interpret datasets, generate summary statistics, identify trends, and create clear, actionable reports and visualizations.
        """,
    completion_args={"temperature": 0.2},
    tools=[
        {
            "type": "web-search",
            "type": "code_interpreter",
        }
    ],
)

# design prompt
message = f"""
 We are running a project that aims to capturte the underlying structure of conversations happening asynchronously over email.
 There is a separate email clients that extracts individual response text and decomposes them into distinct ideas or 'posiitons' expressed in each respopnse.
 Those positions are saved as csv data. 
 I have run the script consensus_metrics.py, passing in the csv data and generated several output datasets.
 To understand how the datasets were generated, review this code: {script} .
 The resulting datasets are as follows:
 1. clusters: {clusters},
 2. topics identified using LDA: {topic_string}, 
 3. sentiments: {sentiments}
 Your task is to analyse the data and return a summary report.
 Report the most significant findings available in the topics, sentiments and clusters objects and explain what they show.
 DO NOT simply provide generic information what the datasets are for or how they are structured, I want insights into trends, summary statistics and your intepretation of the results.
 Actionable insights will be appreciated. make sure you report actual values extracted from the datasets I provided.
 You may also provide recommendations for additional analyses I might like to run, and recommendations for what we could do to gain deeper insights.
 It is especially valuable to provide python code that I could add to consensus_metrics.py to execute the additional analyses you suggest. Provide any code as code blocks in the report.
 Structure your report as markdown data that I can extract and save to a .md file.
"""

response = client.beta.conversations.start(
    agent_id=quant.id,
    inputs=message,
)

with open(f"summary_report_3.md", "x") as f:
    f.write(response.outputs[0].content)
