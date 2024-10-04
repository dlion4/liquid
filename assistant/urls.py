import os
from typing import Any

import google.generativeai as genai
import markdown
from django import forms
from django.shortcuts import render
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from dotenv import load_dotenv

load_dotenv()


GOOGLE_GEMINI_API_KEY = os.environ.get("GOOGLE_GEMINI_API_KEY")
GOOGLE_GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GOOGLE_GEMINI_API_KEY}"



genai.configure(api_key=GOOGLE_GEMINI_API_KEY)




# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)



chat_session = model.start_chat(
  history=[
  ],
)





class AiPostGenerationForm(forms.Form):
    prompt = forms.CharField(
        widget=forms.Textarea, label="Blog Post Prompt")


class PostAiGenerationView(TemplateView):
    template_name = "assistant/blog/generate.html"
    form_class = AiPostGenerationForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data["prompt"]
            response = self.get_response(prompt)
            return render(
                request, self.template_name, {"response": response, "form": form})
        context = self.get_context_data(**kwargs)
        context["form"] = self.form_class()
        return render(request, self.template_name, context)


    def get_response(self, prompt):
        response = chat_session.send_message(prompt, stream=True)
        for _chunk in response:
            """"""
        return format_ai_response_content(response.text)



def format_ai_response_content(markdown_text):
    return markdown.markdown(markdown_text)


app_name="assistant"

urlpatterns = [
    path("generate/", PostAiGenerationView.as_view()),
]
