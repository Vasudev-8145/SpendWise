
# pip install google-genai

from google import genai

api_key = "AQ.Ab8RN6KsMRLS47XZBOulHqqjnwOSvSf0vvwrmcLkrBSKs5znRA"

# step1 : authenticate

client = genai.Client(api_key=api_key)

# set valid prompt

prompt = "what is ai agent in simple words"

# return response

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt
)

print(response.text)