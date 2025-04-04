from backend.sdk.agents.base_agent import BaseAgent
from backend.sdk.agents.errorHandler.prompt_template import *


class ErrorHandlerAgent(BaseAgent):
    NAME = 'error_handler_agent'
    def get_messages(self, error: str):
        return [
            {'role': 'system', 'content': 'You are a helpful assistant'},  # TEMP
            {'role': 'user', 'content': ERROR_HANDLER_PROMPT.format(error_message=error)},
        ]

    def get_action(self, generated_text):
        return self.parse_json(generated_text)