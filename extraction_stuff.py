from mirascope.anthropic import AnthropicCallParams, AnthropicExtractor
from mirascope import tags
from dotenv import load_dotenv
from typing import Literal, Type
from pydantic import  BaseModel

load_dotenv()


class ListOutput(BaseModel):
    email_lists: list[Literal["CAT LIST", "DOG LIST", "PARROT LIST"]]
    explanation: str


class CustomerOutput(BaseModel):
    classification: Literal["BEST", "MID", "WORST"]
    explanation: str


class CustomerClassification(AnthropicExtractor[CustomerOutput]):
    extract_schema: Type[CustomerOutput] = CustomerOutput
    prompt_template = """
    Given customer information and business industry, classify the customer into one of the categories.
    customer information:
    {customer_information}
    Industry:
    {industry}
    """

    customer_information: str
    industry: str

@tags(["List", "Classification"])
class ListSelector(AnthropicExtractor[ListOutput]):
    extract_schema: Type[ListOutput] = ListOutput
    prompt_template = """
    Given the customer classification and business industry, select the email lists the customer should be added to, best fitted to the customer preferences.
    Customer classification:
    {customer_classification}
    Industry:
    {industry}
    """

    customer_classification: CustomerOutput
    industry: str
    call_params = AnthropicCallParams(max_tokens=4000)


customer_information = (
    "Brandon Loves dogs and Parrots, but doesn't have an affinity towards cats."
)
industry = "Eccomerce store that sells cat toys"



customer_extract = CustomerClassification(
    industry=industry, customer_information=customer_information
)
customer_output = customer_extract.extract()
print(customer_extract.dump())
print(customer_output)

list_call = ListSelector(customer_classification=customer_output, industry=industry)
list_selected = list_call.extract()
print(list_call.dump())
print(list_selected)
