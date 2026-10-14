
from google import genai

api_key = "Ab8RN6KsMRLS47XZBOulHqqjnwOSvSf0vvwrmcLkrBSKs5znRA"

client = genai.Client(api_key=api_key)

def get_budget_plan(response_data):

    monthly_total = response_data.get("monthly_total")
    category_summary = response_data.get("category_summary")

    category_summary_text = ""

    for di in category_summary:

        category_summary_text += f". {di.get("category")} : ₹{di.get("total")}\n"

    print(category_summary_text)

        