from abc import ABC, abstractmethod

from backend.sdk.errors import LLMMaxRetryError


class BaseLLM(ABC):
    def __init__(self, llm_config, max_api_call_retries=3):
        self.max_api_call_retries = max_api_call_retries
        self.llm_config = llm_config

    def _request(self, params):
        # reminder: fung: will there be some cases that we dont need to reqest anything?
        raise NotImplementedError
    
    def _try_request(self, params, llm_calls_retried=0):
        # Use chat completion API
        try:
            # return llm.ChatCompletion.create(**params)
            return self._request(params)
        except Exception as err:
            # try again
            if llm_calls_retried < self.max_api_call_retries:
                print(f"Error calling llm. {err}\nRetrying {llm_calls_retried} of {self.max_api_call_retries}...")
                return self._try_request(params, llm_calls_retried=llm_calls_retried+1)
            else:
                raise LLMMaxRetryError(calls_retried=llm_calls_retried)
    
    @abstractmethod
    def run(self):
        return
