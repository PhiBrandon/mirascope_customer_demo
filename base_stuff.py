from mirascope import BasePrompt


class CustomerClassification(BasePrompt):
    prompt_template="""
    Given customer information and business industry, classify the customer into one of the categories.
    customer information:
    {customer_information}
    Industry:
    {industry}
    """

    customer_information: str
    industry: str


prompt = CustomerClassification(customer_information="Brandon is a cool guy who loves dogs.", industry="Cat ecommerce store")
print(prompt.messages())
