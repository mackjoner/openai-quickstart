import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, ConfigLoader, LOG
from model import GLMModel, OpenAIModel, AzureOpenAIModel, ClaudeAIModel
from translator import PDFTranslator

if __name__ == "__main__":
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()
    config_loader = ConfigLoader(args.config)

    config = config_loader.load_config()
    if args.model_type == 'AzureOpenAIModel':
        model_name = os.getenv('AZURE_OPENAI_MODEL') if os.getenv('AZURE_OPENAI_MODEL') else config['AzureOpenAIModel']['model']
        api_key = os.getenv('AZURE_OPENAI_API_KEY') if os.getenv('AZURE_OPENAI_API_KEY') else config['AzureOpenAIModel']['api_key']
        api_version = os.getenv('AZURE_OPENAI_API_VERSION') if os.getenv('AZURE_OPENAI_API_VERSION') else config['AzureOpenAIModel']['api_version']
        api_url = os.getenv('AZURE_OPENAI_ENDPOINT') if os.getenv('AZURE_OPENAI_ENDPOINT') else config['AzureOpenAIModel']['endpoint']
        model = AzureOpenAIModel(model=model_name, api_key=api_key, api_version=api_version, api_url=api_url)
    elif args.model_type == 'ClaudeAIModel':
        model_name = os.getenv('CLAUDE_AI_MODEL') if os.getenv('CLAUDE_AI_MODEL') else config['ClaudeAIModel']['model']
        api_key = os.getenv('ANTHROPIC_API_KEY') if os.getenv('ANTHROPIC_API_KEY') else config['ClaudeAIModel']['api_key']
        print(model_name, api_key)
        model = ClaudeAIModel(model=model_name, api_key=api_key)
    elif args.model_type == 'GLMModel':
        model_url = args.glm_model_url if args.glm_model_url else config['GLMModel']['model_url']
        timeout = args.timeout if args.timeout else config['GLMModel']['timeout']
        model = GLMModel(model_url=model_url, timeout=timeout)
    else:
        model_name = args.openai_model if args.openai_model else config['OpenAIModel']['model']
        api_key = args.openai_api_key if args.openai_api_key else os.getenv('OPENAI_API_KEY') if os.getenv('OPENAI_API_KEY') else config['OpenAIModel']['api_key']
        model = OpenAIModel(model=model_name, api_key=api_key)


    pdf_file_path = args.input_file if args.input_file else config['common']['book']
    file_format = args.output_file_format if args.output_file_format else config['common']['file_format']

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    translator.translate_pdf(pdf_file_path, file_format)
