import json
from django.http import JsonResponse
from django.views import View
from g4f.client import Client
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


keywords = ["GPT", "Nvidia", "Generative AI"]

input_messages = [
    {
        "role": "system",
        "content": """Generate articles that follow the users instructions exactly.""",
    },
    {
        "role": "user",
        "content": f"""Please generate an article using every keyword from the following list of words at least once in the article: {keywords}.
Do not cluster the keywords together. The keywords must be sprinkled through the article in an organic manner, and each one used sparingly.
Ensure the article is at least 500 words long, and no longer than 1000 words.""",
    },
    {
        "role": "assistant",
        "content": f"""Here is an article using each keyword in this list {keywords}:

Article: """,
    },
]
# print(input_messages)


# completion = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo-16k-0613",
#     messages=input_messages
# )


client = Client()

paragraph = (
    "Write a blog of 300 words with the heading 'The rise of alexander the great'"
)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": paragraph},
    ],
    temperature=0.7,
)
print(response.choices[0].message.content)


class AIGenerateContentView(View):

    @method_decorator(csrf_exempt, name="dispatch")
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return JsonResponse({"message": "success", "success": True})

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        template = data.get("template")
        content = data.get("content")
        keywords = data.get("keywords")
        samples_n = data.get("samples")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Generate articles that follow the users instructions exactly.",
                },
                {"role": "user", "content": content},
            ],
            temperature=0.7,
            stream=True,  # Add this optional property.
        )

        for chunk in response:
            data = chunk.choices[0].delta.get("content", "")
            return JsonResponse({"content": data})
        
        return JsonResponse(
            {
                "message": "success",
                "success": True,
                "content": response.choices[0].message.content,
                "end": True,
            }
        )
