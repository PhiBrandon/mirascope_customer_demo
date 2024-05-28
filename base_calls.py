from mirascope.anthropic import AnthropicCall, AnthropicCallParams
from dotenv import load_dotenv
from pydantic import computed_field

load_dotenv()


class CustomerClassification(AnthropicCall):
    prompt_template = """
    Given customer information and business industry, classify the customer into one of the categories.
    customer information:
    {customer_information}
    Industry:
    {industry}
    Classifications:
    {classifications}
    """

    customer_information: str
    industry: str
    classifications: list[str]


customer_information = (
    "Brandon Loves dogs and Parrots, but doesn't have an affinity towards cats."
)
industry = "Eccomerce store that sells cat toys"
classifications = ["BEST", "MID", "WORST"]

classify_call = CustomerClassification(
    customer_information=customer_information,
    industry=industry,
    classifications=classifications,
)
output = classify_call.call()
print(output.content)
print(classify_call.dump())


class ListSelector(CustomerClassification):
    prompt_template = """
    Given the customer classification and business industry, add the customer to the given email lists best fitted to the customer preferences.
    Customer classification:
    {customer_classification}
    Industry:
    {industry}
    """

    industry: str
    email_lists: list[str]
    call_params = AnthropicCallParams(max_tokens=4000)

    @computed_field
    def customer_classification(self) -> str:
        """Uses `CustomerClassification` to classify the customer. """
        return CustomerClassification(customer_information=self.customer_information, industry=self.industry, classifications=self.classifications).call().content
    
email_list = ["CAT LIST", "DOG LIST", "PARROT LIST"]

list_call = ListSelector(customer_information=customer_information, industry=industry, classifications=classifications, email_lists=email_list)
output = list_call.call()
print(output.content)
print(list_call.dump())