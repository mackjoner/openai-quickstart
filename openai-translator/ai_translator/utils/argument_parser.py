import argparse

class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Translate English PDF book to Chinese.')
        self.parser.add_argument('--config_file', type=str, default='config.yaml', help='Configuration file with model and API settings.')
        self.parser.add_argument('--model_type', type=str, default='OpenAIModel', choices=['GLMModel', 'OpenAIModel', 'AzureOpenAIModel', 'ClaudeAIModel'], help='The type of translation model to use. Choose between "GLMModel", "OpenAIModel", "AzureOpenAIModel" and "ClaudeAIModel".')        
        self.parser.add_argument('--model_name', type=str, help='Name of the Large Language Model.')
        self.parser.add_argument('--deployment_name', type=str, help='The deployment name for deploying a large language model in Azure OpenAI Studio.')
        self.parser.add_argument('--api_type', type=str, help='Api type of the Large Language Model.')
        self.parser.add_argument('--glm_model_url', type=str, help='The URL of the ChatGLM model URL.')
        self.parser.add_argument('--timeout', type=int, help='Timeout for the API request in seconds.')
        self.parser.add_argument('--openai_model', type=str, help='The model name of OpenAI Model. Required if model_type is "OpenAIModel".')
        self.parser.add_argument('--openai_api_key', type=str, help='The API key for OpenAIModel. Required if model_type is "OpenAIModel".')
        self.parser.add_argument('--input_file', type=str, help='PDF file to translate.')
        self.parser.add_argument('--output_file_format', type=str, help='The file format of translated book. Now supporting PDF and Markdown')
        self.parser.add_argument('--source_language', type=str, help='The language of the original book to be translated.')
        self.parser.add_argument('--target_language', type=str, help='The target language for translating the original book.')

    def parse_arguments(self):
        args = self.parser.parse_args()
        # if args.model_type == 'OpenAIModel' and not args.openai_model and not args.openai_api_key:
        #     self.parser.error("--openai_model and --openai_api_key is required when using OpenAIModel")
        return args
