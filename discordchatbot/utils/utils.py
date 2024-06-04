import os
from configparser import ConfigParser
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import openai
import os
from langchain_mistralai import ChatMistralAI


def initiate_config():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.path.dirname(current_directory)
    config_filepath = dir_path + "\\config.ini"
    print(config_filepath)

    exists = os.path.exists(config_filepath)
    config = None

    if exists:
        print("--------config.ini file found at ", config_filepath)
        config = ConfigParser()
        config.read(config_filepath)
    else:
        print("---------config.ini file not found at ", config_filepath)

    return config


config = initiate_config()
# Retrieve config details
openai_config = config['OPENAI']
GPT_TOKEN = openai_config['TOKEN']
LANGSMITH_TOKEN = openai_config['LANGSMITH_TOKEN']

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = LANGSMITH_TOKEN


def initiate_llm(model_name):
    llm = ChatOpenAI(
        model_name=model_name,  # 'gpt-3.5-turbo' or 'gpt-4'
        temperature=0,
        openai_api_key=GPT_TOKEN,
        max_tokens=50)

    return llm


def initiate_item_llm(model_name):
    # item_llm = ChatMistralAI(model=model_name, temperature=0)
    item_llm = ChatOpenAI(
        model_name=model_name,  # 'gpt-3.5-turbo' or 'gpt-4'
        temperature=0,
        openai_api_key=GPT_TOKEN,
        max_tokens=50)
    return item_llm


def initiate_prompt(PROMPT):
    PROMPT_SUMMARY = PromptTemplate(template=PROMPT, input_variables=['context', 'question'])
    return PROMPT_SUMMARY
