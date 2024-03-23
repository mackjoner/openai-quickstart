import time
import anthropic

from model import Model
from utils import LOG
from anthropic import Anthropic

class ClaudeAIModel(Model):
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.client = Anthropic(api_key=api_key)

    def make_request(self, prompt):
        attempts = 0
        while attempts < 3:
            try:
                response = self.client.messages.create(
                    max_tokens=1024,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    model=self.model
                )
                print(response.content)
                translation = response.content[0].text
                return translation, True
            except anthropic.RateLimitError as e:
                attempts += 1
                if attempts < 3:
                    LOG.warning("Rate limit reached. Waiting for 60 seconds before retrying.")
                    time.sleep(60)
                else:
                    raise Exception("Rate limit reached. Maximum attempts exceeded.")
            except anthropic.APIConnectionError as e:
                print("The server could not be reached")
                print(e.__cause__)  # an underlying Exception, likely raised within httpx.            except requests.exceptions.Timeout as e:
            except anthropic.APIStatusError as e:
                print("Another non-200-range status code was received")
                print(e.status_code)
                print(e.response)
            except Exception as e:
                raise Exception(f"发生了未知错误：{e}")
        return "", False
