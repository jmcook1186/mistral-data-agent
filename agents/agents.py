import os
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()

# initialize client
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


def initialize_agents():

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
        completion_args={"temperature": 0.3},
    )

    quant = client.beta.agents.create(
        model="mistral-medium-latest",
        name="quant",
        description="Data analyst",
        instructions="""
            You are Quant, an advanced AI assistant specialized in data analysis, statistics and scientific writing.
            Your primary role is to ingest, analyze, and interpret data and generate detailed reports. 
            Your reports should identify key results and trends, interpret them and provide clear, actionable reports.
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
            Prioritise these packages whereer possible. Especially prioritise matplotlib and seaborn for visualisation.
            Your primary role is to write Python code from scratch, improve, extend or debug existing Python code.
            When you return code, you shoul;d always return code that executes successfully. 
            You should double check your work to ensure high standards of code efficiency, readability and accuracy.
            Always document your work using comments and docstrings.
            """,
        completion_args={"temperature": 0.1},
        tools=[
            {
                "type": "web-search",
                "type": "code_interpreter",
            }
        ],
    )

    return whisper, quant, dev
