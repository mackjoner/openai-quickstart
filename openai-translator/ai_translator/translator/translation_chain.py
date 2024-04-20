from langchain.chat_models import ChatOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.schema.messages import AIMessage
from langchain_community.llms.chatglm3 import ChatGLM3
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from utils import LOG


class TranslationChain:
    def __init__(self, model_name: str = "gpt-3.5-turbo", deployment_name: str = None, api_type: str = "openai",
                 verbose: bool = True):

        # 翻译任务指令始终由 System 角色承担
        template = (
            """You are a translation expert, proficient in various languages. \n
            Translates {source_language} to {target_language}."""
        )
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)

        # 待翻译文本由 Human 角色输入
        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        # 使用 System 和 Human 角色的提示模板构造 ChatPromptTemplate
        chat_prompt_template = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        # for ChatGLM3
        messages = [
            AIMessage(content="You are a translation expert, proficient in various languages. The translated content needs to keep the symbols in the original, i.e. [], ()."),
            # AIMessage(content="欢迎问我任何问题。"),
        ]
        human_template = """Translates {source_language} to {target_language}.\n{text}"""
        prompt = PromptTemplate.from_template(human_template)

        # 为了翻译结果的稳定性，将 temperature 设置为 0
        if api_type == "azure":
            print("Using Azure API")
            llm = AzureChatOpenAI(deployment_name=deployment_name, model_name=model_name, temperature=0,
                                  verbose=verbose)
        elif api_type == "claude":
            print("Using Anthropic API")
            llm = ChatAnthropic(model_name=model_name, temperature=0, verbose=verbose)
        elif api_type == "chatglm3":
            print("Using ChatGLM3 API")
            # ChatGLM3的部署参考
            # https://github.com/THUDM/ChatGLM3/tree/main/openai_api_demo
            llm = ChatGLM3(model_name="chatglm3-6b", endpoint_url="http://127.0.0.1:11344/v1/chat/completions", prefix_messages=messages, max_tokens=16000)
            # llm = OpenAI(api_key="", base_url="http://127.0.0.1:11344/v1/")
        else:
            print("Using OpenAI API")
            llm = ChatOpenAI(model_name=model_name, temperature=0, verbose=verbose)

        self.chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)

    def run(self, text: str, source_language: str, target_language: str) -> (str, bool):
        result = ""
        try:
            result = self.chain.run({
                "text": text,
                "source_language": source_language,
                "target_language": target_language,
            })
        except Exception as e:
            LOG.error(f"An error occurred during translation: {e}")
            return result, False

        return result, True