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
whisper_message = f"""
We are running a project that aims to capture the underlying structure of conversations, known as 'assemblies' happening asynchronously over email.
Each assembly has a discrete time period, fixed participant set and runs in rounds where batches of responses are synthesised and shared. 
Every assembly has a definite aim; a common aim is to come to consensus over the content of a technical specification, or a position statement on a certain topic. 
There is a separate email client that extracts all the individual response texts for each round and decomposes them into a comprehensive set of distinct ideas or 'positions'.
Those positions are saved in csv files. 
I have run the script consensus_metrics.py, passing in the csv data and generated several output datasets.

To understand how the datasets were generated, review this code: {script} .

Your task is to design prompts for "quant" - a data analysis agent that will examine these data, and "dev" - a software engineer agent that will write code for additional data anlysis. 

I want Quant to: 
  - Generate a comprehensive report between 300 - 1000 words in length that explains the key values, trends and insights extracted from the data provided to it.
  - Report the most significant findings available in the topics, sentiments and clusters objects and explain what they show.
  - DO NOT simply provide generic information what the datasets are for or how they are structured, I want insights into trends, summary statistics and your intepretation of the results.
  - Actionable insights will be appreciated.
  - Quant should NEVER make up or hallucinate values - all information must be rooted in the actual data provided.
  - Quant should include a specific section in the report containing explicit instructions for Dev. This section MUST be separated with a header called "INSTRUCTIONS FOR DEV", exactly like that so I can use the key to extract the text using string splitting.
  - The section for Dev will include recommendations for additional analyses that could be done, or additional data that could be collected to enhance our understanding of the state of the assembly.
  - The recommendations from Quant will be used by Dev to return executable Python code.

I want Dev to:
  - Write code for any appropriate visualizations that would enhance the report generated by Quant.
  - Evaluate the recommendations made by Quant and write Python code to achieve Quant's recommended outcomes
  - Yield code that produces data that can be passed back to Quant for further analysis
  - Always double check and confirm code runs successfully, using the right syntax and best practises for readability, efficiency and safety.
  - Create tests and error handling for key functions.
  
You must return two prompts: one for Dev, and one for Quant. The two prompts MUST be separtated with the headings "PROMPT FOR QUANT" and "PROMPT FOR DEV" in precisely that syntax, as I will use those headings as keys to extract the text using string splitting.
I need to be able to extract these prompts and pass them to the appropriate agents programmatically.

"""

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
