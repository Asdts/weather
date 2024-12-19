from backend.sdk.agents.base_agent import BaseAgent
from backend.sdk.agents.nlpQuery.prompt_template import *


class LogAgent(BaseAgent):
    NAME = 'log_managemenr_agent'
    def get_messages(self, weather_log: str):
        return [
            {'role': 'system', 'content': 'You are a helpful assistant'},  # TEMP
            {'role': 'user', 'content': NATURAL_LANGUAGE_QUERY_PROMPT.format(weather_log=weather_log)},
        ]

    def get_action(self, generated_text):
        return self.parse_json(generated_text)