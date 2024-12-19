import os

from groq import Groq
from dotenv import load_dotenv
import tiktoken

load_dotenv()

from backend.sdk.llms.base_llm import BaseLLM


class GroqLLM(BaseLLM):
    llm_backend = 'groq'
    
    def __init__(self, llm_config,api_key, max_api_call_retries=3):
        super().__init__(llm_config, max_api_call_retries)
        api_key = os.getenv('GROQ_API_KEY')
        assert api_key, 'Empty GROQ_API_KEY'
        Groq.api_key = api_key
        self.client = Groq(api_key=api_key)
        self.name = llm_config['model']
        self.ttl_tokens_used = 0  # TEMP

    def _request(self, params):
        # TEMP
        # print(f"Requesting Groq API")
        # print(params)
        res = self.client.chat.completions.create(**params)
        # TEMP
        num_tokens = self.num_tokens_from_messages(params['messages'])
        self.ttl_tokens_used += num_tokens
        return res

    def run_function_call(self, messages, functions=[], function_call=None):
        params = {
            "messages": messages,
            "functions": functions,
            "function_call": function_call,
            **self.llm_config
        }
        res = self._try_request(params, llm_calls_retried=0)
        if res.choices[0].finish_reason == 'function_call':
            return res.choices[0].function_call
        else:
            return res.choices[0].message.content.strip()

    def run(self, messages):
        params = {
            "messages": messages,
            **self.llm_config
        }
        res = self._try_request(params, llm_calls_retried=0)
        return res.choices[0].message.content.strip()
        
    def num_tokens_from_messages(self, messages, model: str=None):
        """Returns the number of tokens used by a list of messages.
        """
        if model is None:
            model = self.name
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")
        if model in {
            "gemma2-9b-it",
            "llama-3.3-70b-versatile",
            "llama-guard-3-8b",
            "llama3-70b-8192",
            "mixtral-8x7b-32768",
            "whisper-large-v3",
            "whisper-large-v3-turbo",
            }:
            tokens_per_message = 3
            tokens_per_name = 1
        elif model == "llama-3.1-8b-instant":
            tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
            tokens_per_name = -1  # if there's a name, the role is omitted
        elif "llama3-8b-8192" in model:
            print("Warning: llama3-8b-8192 may update over time. Returning num tokens assuming llama3-8b-8192")
            return self.num_tokens_from_messages(messages, model="llama3-8b-8192")
        elif "gpt-4" in model:
            print("Warning: gpt-4 may update over time. Returning num tokens assuming")
            return self.num_tokens_from_messages(messages, model="llama3-8b-8192")
        else:
            raise NotImplementedError(
                f"""num_tokens_from_messages() is not implemented for model {model}. see Groq doc for information on how messages are converted to tokens."""
            )
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens

