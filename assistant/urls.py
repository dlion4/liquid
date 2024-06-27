from typing import Any
from django.urls import path, include
from django.views.generic import TemplateView
import requests
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import os
from dotenv import load_dotenv

from django import forms


import google.generativeai as genai
import os

load_dotenv()


GOOGLE_GEMINI_API_KEY = os.eviron.get('GOOGLE_GEMINI_API_KEY')
GOOGLE_GEMINI_ENDPOINT = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GOOGLE_GEMINI_API_KEY}'



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
  ]
)


import markdown


import time

from django.http import HttpResponse
from django.utils.safestring import mark_safe


class AiPostGenerationForm(forms.Form):
    prompt = forms.CharField(widget=forms.Textarea, label='Blog Post Prompt')


class PostAiGenerationView(TemplateView):
    template_name = "assistant/blog/generate.html"
    form_class = AiPostGenerationForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            response = self.get_response(prompt)
            return render(request, self.template_name, {"response": response, "form": form})
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = self.form_class()
            return render(request, self.template_name, context)
        
    def get_response(self, prompt):
        response = chat_session.send_message(prompt, stream=True)
        for chunk in response:
            # time.sleep(3)
            print(chunk.text)
            print("_"*80)
        # print(response.text)
        # print(response)
        return format_ai_response_content(response.text)



def format_ai_response_content(markdown_text):
    formatted_html = markdown.markdown(markdown_text)
    return formatted_html

    



app_name='assistant'

urlpatterns = [
    path("generate/", PostAiGenerationView.as_view())
]
