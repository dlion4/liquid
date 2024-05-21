import json
from django.http import JsonResponse
from django.views import View
from g4f.client import Client
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator




client = Client()




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
