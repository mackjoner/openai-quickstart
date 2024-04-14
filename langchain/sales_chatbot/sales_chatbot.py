import gradio as gr

from langchain.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI


def initialize_sales_bot(vector_store_dir: str="real_estates_sale_gpt4"):
    db = FAISS.load_local(vector_store_dir, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
    llm = ChatOpenAI(model_name="gpt-4", temperature=0.2)
    template = """你是一个虚拟的房产销售，你应该帮助客户解决他们对购房过程中遇到的问题和担忧，并提供有用的回答。你应该只在问题的背景下说话，使用以下上下文来回答最后的问题。如果你不知道答案，就说"这个问题我要问问领导"，不要试图编造答案。最多用五句话。回答要尽可能简明扼要。在回答的最后一定要说"谢谢你的提问! "
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
    global SALES_BOT
    SALES_BOT = RetrievalQA.from_chain_type(llm,
                                            retriever=db.as_retriever(search_type="similarity_score_threshold",
                                                                      search_kwargs={"score_threshold": 0.8}),
                                            return_source_documents=True,
                                            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
    # 返回向量数据库的检索结果
    SALES_BOT.return_source_documents = True

    return SALES_BOT

def sales_chat(message, history):
    print(f"[message]{message}")
    print(f"[history]{history}")
    # TODO: 从命令行参数中获取
    enable_chat = True

    ans = SALES_BOT({"query": message})
    print(ans)
    # 如果检索出结果，或者开了大模型聊天模式
    # 返回 RetrievalQA combine_documents_chain 整合的结果
    if ans["source_documents"] or enable_chat:
        print(f"[result]{ans['result']}")
        print(f"[source_documents]{ans['source_documents']}")
        return ans["result"]
    # 否则输出套路话术
    else:
        return "这个问题我要问问领导"

def launch_gradio():
    demo = gr.ChatInterface(
        fn=sales_chat,
        title="房产销售",
        # retry_btn=None,
        # undo_btn=None,
        theme="soft",
        chatbot=gr.Chatbot(height=600),
    )

    demo.launch(server_name="0.0.0.0")

if __name__ == "__main__":
    # 初始化房产销售机器人
    initialize_sales_bot()
    # 启动 Gradio 服务
    launch_gradio()
