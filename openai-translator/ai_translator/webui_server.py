import sys
import os
import gradio as gr

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, LOG
from translator import PDFTranslatorLangChain, TranslationConfig

languages = [
    'English', 'Spanish', 'Japanese', 'Persian', 'Hindi', 'French', 'Chinese',
    'Bengali', 'Gujarati', 'German', 'Telugu', 'Italian', 'Arabic', 'Polish',
    'Tamil', 'Marathi', 'Malayalam', 'Oriya', 'Panjabi', 'Portuguese', 'Urdu',
    'Galician', 'Hebrew', 'Korean', 'Catalan', 'Thai', 'Dutch', 'Indonesian',
    'Vietnamese', 'Bulgarian', 'Filipino', 'Central Khmer', 'Lao', 'Turkish',
    'Russian', 'Croatian', 'Swedish', 'Yoruba', 'Kurdish', 'Burmese', 'Malay',
    'Czech', 'Finnish', 'Somali', 'Tagalog', 'Swahili', 'Sinhala', 'Kannada',
    'Zhuang', 'Igbo', 'Xhosa', 'Romanian', 'Haitian', 'Estonian', 'Slovak',
    'Lithuanian', 'Greek', 'Nepali', 'Assamese', 'Norwegian'
]

file_formats = ['PDF', 'Markdown']

def translation(input_file, source_language, target_language, file_format):
    LOG.debug(f"[翻译任务]\n源文件: {input_file.name}\n源语言: {source_language}\n目标语言: {target_language}\n文件格式: {file_format}")

    output_file_path, content = Translator.translate_pdf(
        input_file.name, source_language=source_language, target_language=target_language, output_file_format=file_format)

    return output_file_path, content

def launch_gradio():

    iface = gr.Interface(
        fn=translation,
        title="OpenAI-Translator v2.0(PDF 电子书翻译工具)",
        inputs=[
            gr.File(label="上传PDF文件"),
            # gr.Textbox(label="源语言（默认：英文）", placeholder="English", value="English"),
            # gr.Textbox(label="目标语言（默认：中文）", placeholder="Chinese", value="Chinese")
            gr.Dropdown(label="源语言", choices=languages, value="English"),
            gr.Dropdown(label="目标语言", choices=languages, value="Chinese"),
            gr.Dropdown(label="输出格式", choices=file_formats, value="Markdown")
        ],
        outputs=[
            gr.File(label="下载翻译文件"),
            gr.TextArea(label="翻译内容")
        ],
        allow_flagging="never"
    )

    iface.launch()

def initialize_translator():
    # 解析命令行
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()
    # 初始化配置单例
    config = TranslationConfig()
    config.initialize(args)
    # 实例化 PDFTranslatorLangChain 类，并调用 translate_pdf() 方法
    global Translator
    Translator = PDFTranslatorLangChain(config.model_name, config.deployment_name, config.api_type)


if __name__ == "__main__":
    # 初始化 translator
    initialize_translator()
    # 启动 Gradio 服务
    launch_gradio()
