import openai
from langchain_community.chat_models import ChatOpenAI
import logging
from utils import utils
from langchain_core.prompts import PromptTemplate


config = utils.initiate_config()
# Retrieve config details
openai_config = config['OPENAI']
GPT_TOKEN = openai_config['TOKEN']
PROMPT = openai_config['PROMPT']


def initiate_llm(model_name):
    llm = ChatOpenAI(
        model_name=model_name,  # 'gpt-3.5-turbo' or 'gpt-4'
        temperature=0,
        openai_api_key=GPT_TOKEN,
        max_tokens=50)

    return llm

def initiate_prompt(PROMPT):
    PROMPT_SUMMARY = PromptTemplate(template=PROMPT, input_variables=['context', 'question'])
    return PROMPT_SUMMARY

def extract_items_from_message(message):
    logging.info('initiating llm')
    llm = initiate_llm('gpt-3.5-turbo')

    logging.info('initiating prompt')
    PROMPT_SUMMARY = initiate_prompt(PROMPT)

    response = llm.send_message(PROMPT)
    items = response['choices'][0]['text'].strip().split("\n")
    return items

