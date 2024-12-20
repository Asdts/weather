import os
from dotenv import load_dotenv

# Import the classes from the provided code
from backend.sdk.agents.base_agent import BaseAgent
from backend.sdk.agents.recommendation.agent import RecommendationAgent
from backend.sdk.agents.summaries.agent import SummaryAgent
from backend.sdk.llms.openAi_llm import OpenaiLLM
from backend.sdk.llms.groq_llm import GroqLLM

# Load environment variables
load_dotenv()

# Define a testing engine
class TestEngine:
    def __init__(self, llm_backend='openai', model='gpt-3.5-turbo', debug=True):
        llm_config = {
            'model': model,
            'temperature': 0.7,
            'max_tokens': 200,
        }
        if llm_backend == 'openai':
            self.llm = OpenaiLLM(llm_config,api_key=os.getenv('OPENAI_API_KEY'))
        elif llm_backend == 'groq':
            self.llm = GroqLLM(llm_config,api_key=os.getenv('GROQ_API_KEY'))
        else:
            raise ValueError("Unsupported LLM backend. Choose 'openai' or 'groq'.")

        self.debug = debug

    def test_recommendation_agent(self, city, weather):
        agent = RecommendationAgent(self.llm, debug=self.debug)
        try:
            result = agent.act(city=city, weather=weather)
            print("RecommendationAgent Output:", result)
        except Exception as e:
            print("Error during RecommendationAgent test:", e)

    def test_summary_agent(self, city, weather):
        agent = SummaryAgent(self.llm, debug=self.debug)
        try:
            result = agent.act(city=city, weather=weather)
            print("SummaryAgent Output:", result)
        except Exception as e:
            print("Error during SummaryAgent test:", e)

if __name__ == "__main__":
    # Initialize the testing engine
    engine = TestEngine(llm_backend='openai', model='gpt-4o', debug=True)

    # Define test inputs
    test_cases = [
        {"city": "Mumbai", "weather": "Heavy rains with strong winds."}
    ]

    # Run tests
    for test in test_cases:
        print("\n" + "=" * 50)
        engine.test_recommendation_agent(test['city'], test['weather'])
        engine.test_summary_agent(test['city'], test['weather'])
