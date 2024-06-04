import logging
import sys
sys.path.append("..")

from utils import utils
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional
from langchain_core.prompts import ChatPromptTemplate

config = utils.initiate_config()
# Retrieve config details
openai_config = config['OPENAI']


class Grocery(BaseModel):
    """Information about a grocery item."""

    # ^ Doc-string for the entity Person.
    # This doc-string is sent to the LLM as the description of the schema Person,
    # and it can help to improve extraction results.

    # Note that:
    # 1. Each field is an `optional` -- this allows the model to decline to extract it!
    # 2. Each field has a `description` -- this description is used by the LLM.
    # Having a good description can help improve extraction results.
    name: str = Field(default=None, description="The name of the item")
    brand: Optional[str] = Field(
        default=None, description="The brand of the item"
    )
    comments: Optional[str] = Field(
        default=None, description="Additional comments about the item"
    )


def initiate_item_prompt():
    item_extractor_prompt2 = openai_config['ITEM_EXTRACTOR_PROMPT2']
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an expert extraction algorithm. "
            "You are provided a text message containing grocery items."
            "Only extract relevant information about grocery items from the text. "
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value.",
        ),
        # Please see the how-to about improving performance with
        # reference examples.
        # MessagesPlaceholder('examples'),
        ("user", "{text}"),  # Escape curly braces by doubling them
    ]
    )

    return prompt


def extract_items_from_message(llm, text):
    prompt = initiate_item_prompt()
    runnable = prompt | llm.with_structured_output(schema=Grocery)
    item = runnable.invoke({"text": text})
    print(item.name)
    return item
