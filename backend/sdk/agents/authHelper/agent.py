from backend.sdk.agents.base_agent import BaseAgent
from backend.sdk.agents.authHelper.prompt_template import *


class AuthHelperAgent(BaseAgent):
    NAME = 'auth_helper_agent'
    def get_messages(self, issue:str):
        return [
            {'role': 'system', 'content': 'You are a helpful assistant'},  # TEMP
            {'role': 'user', 'content': AUTH_HELPER_PROMPT.format(issue=issue)},
        ]

    def get_action(self, generated_text):
        return self.parse_json(generated_text)