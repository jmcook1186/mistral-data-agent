import os
from dotenv import load_dotenv

from mistralai import Mistral

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

agent = client.beta.agents.create(
    model="mistral-medium-2025",
    name="data-analyst",
    description="Data analysis agent",
    instructions="You are a data analysis expert."

)
