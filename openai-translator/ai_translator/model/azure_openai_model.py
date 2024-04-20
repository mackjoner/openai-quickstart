import time
import openai

from model import Model
from utils import LOG
from openai import AzureOpenAI

class AzureOpenAIModel(Model):
    def __init__(self, model: str, api_key: str, api_version: str, api_url: str):
        self.model = model
        self.client = AzureOpenAI(api_key=api_key, api_version=api_version, azure_endpoint=api_url)

    def make_request(self, prompt):
        attempts = 0
        while attempts < 3:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                translation = response.choices[0].message.content.strip()
                return translation, True
            except openai.RateLimitError as e:
                attempts += 1
                if attempts < 3:
                    LOG.warning("Rate limit reached. Waiting for 60 seconds before retrying.")
                    time.sleep(60)
                else:
                    raise Exception("Rate limit reached. Maximum attempts exceeded.")
            except openai.APIConnectionError as e:
                print("The server could not be reached")
                print(e.__cause__)  # an underlying Exception, likely raised within httpx.            except requests.exceptions.Timeout as e:
            except openai.APIStatusError as e:
                print("Another non-200-range status code was received")
                print(e.status_code)
                print(e.response)
            except Exception as e:
                raise Exception(f"发生了未知错误：{e}")
        return "", False
