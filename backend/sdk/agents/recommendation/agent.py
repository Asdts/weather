from backend.sdk.agents.base_agent import BaseAgent
from backend.sdk.agents.recommendation.prompt_template import *


class RecommendationAgent(BaseAgent):
    NAME = 'recommendation_agent'
    def get_messages(self, city: str , weather: str):
        return [
            {'role': 'system', 'content': 'You are a helpful assistant'},  # TEMP
            {'role': 'user', 'content': RECOMMANDATION_GENERATION_PROMPT.format(city=city, weather=weather)},
        ]

    def get_action(self, generated_text):
        return self.parse_json(generated_text)