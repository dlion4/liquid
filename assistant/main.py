import google.generativeai as genai
import os

GOOGLE_GEMINI_API_KEY = "AIzaSyCMLe1vsA9rMVxKiFRFbiROGRJ_iCw2pgs"


genai.configure(api_key=GOOGLE_GEMINI_API_KEY)


def get_response(prompt):
    # return genai.ChatCompletion.create(
    #     model="gemini-1.5-flash-latest",
    #     messages=[{"role": "user", "content": prompt}],
    # ).choices[0].message.content
    response = genai.chat(message=prompt)
    print(response)
    return response

