import os
from google import genai as genAi
from backend.sdk.llms.base_llm import BaseLLM
from dotenv import load_dotenv

load_dotenv()

class GeminiLLM(BaseLLM):
    llm_backend = "gemini"

    def __init__(self, llm_config, api_key, max_api_call_retries=3):
        super().__init__(llm_config, max_api_call_retries)
        api_key = os.getenv("GEMINI_API_KEY") or api_key
        assert api_key, "Empty GEMINI_API_KEY"
        self.api_key = api_key
        self.name = llm_config["model"]
        self.ttl_tokens_used = 0  # TEMP
        self.model = genAi.Client(api_key=self.api_key)
        print(f"Initialized Gemini LLM with model {self.name}")

    def _request(self, params):
        try:
            # print("Requesting Gemini API with params:", params["messages"])
            res = self.model.models.generate_content(
                model=self.name,
                contents=params["messages"][0]["content"],)

            print("Response from Gemini API:", res.text)
            
            num_tokens = self.num_tokens_from_messages(params["messages"])
            self.ttl_tokens_used += num_tokens
            
            return res
        except Exception as e:
            print(f"Error in _request: {e}")
            return None

    def run_function_call(self, messages, functions=[], function_call=None):
        # print("run_function_call not implemented for GeminiLLM")
        params = {
            "messages": messages,
            "functions": functions,
            "function_call": function_call,
            **self.llm_config,
        }
        res = self._try_request(params, llm_calls_retried=0)
        
        if res and res.candidates:
            choice = res.candidates[0]
            if hasattr(choice, "function_call"):
                return choice.function_call
            else:
                return choice.text.strip()
        else:
            return res

    def run(self, messages):
        # print("Running Gemini LLM with messages:", messages)
        params = {
            "messages": messages,
            **self.llm_config,
        }
        res = self._try_request(params, llm_calls_retried=0)
        return res.candidates[0].text.strip() if res and res.candidates else None

    def num_tokens_from_messages(self, messages):
        """Estimates token usage based on message length."""
        token_estimate = sum(len(message["content"].split()) for message in messages)
        return token_estimate
