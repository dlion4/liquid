from amiribd.articles.editor.serializer import YtSummarizerSerializer
from amiribd.articles.models import Article, YtSummarizer
from amiribd.articles.views import ArticleMixinView
from amiribd.articles.forms import ArticleForm
from django.shortcuts import get_object_or_404, redirect, render
from typing import Any
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user

import google.generativeai as genai

from .forms import AIArticleGenerationModelForm, YoutubeSummarizerForm

from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.core.files.storage import default_storage
from django_ckeditor_5.views import upload_file
from django.conf import settings


# configure genai

genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)

# chats

GOOGLE_GEMINI_ENDPOINT = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GOOGLE_GEMINI_API_KEY}'





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
  history=[]
)


import markdown


import time

from django.http import HttpResponse
from django.utils.safestring import mark_safe




class UploadFile(View):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        upload_view = upload_file
        return upload_view(request, *args, **kwargs)


ck_editor_upload_files = UploadFile.as_view()


class ContentCreationEditorView(ArticleMixinView):
    template_name = "account/dashboard/v1/articles/editor/editor.html"
    form_class = ArticleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if not form.is_valid():
            print(form.errors)
            return render(request, self.template_name, {"form": form})
        instance = form.save(commit=False)
        instance.profile = self.request.user.profile_user
        instance.save()
        return redirect(instance)


class ContentArticleUpdateView(ArticleMixinView):
    template_name = "account/dashboard/v1/articles/editor/editor.html"
    form_class = ArticleForm

    def get_object(self, **kwargs):
        return get_object_or_404(
            Article,
            profile=self.get_profile(),
            slug=self.kwargs.get("slug"),
            created_at__year=self.kwargs.get("tm__year"),
            created_at__month=self.kwargs.get("tm__month"),
            created_at__day=self.kwargs.get("tm__day"),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(instance=self.get_object(**kwargs))
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            request.POST, request.FILES, instance=self.get_object(**kwargs)
        )
        if not form.is_valid():
            print(form.errors)
            return render(request, self.template_name, {"form": form})
        instance = form.save(commit=False)
        instance.profile = self.request.user.profile_user
        instance.save()
        return redirect(instance)

import json
import after_response

from amiribd.articles.editor.ai.models import AIHistory

class ContentAiGeneratorView(ArticleMixinView):
    template_name = "account/dashboard/v1/articles/editor/generate.html"
    form_class  = AIArticleGenerationModelForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        context["histories"] = AIHistory.objects.filter(profile=self.get_profile()).order_by("-id")[:3]
        return context




def format_ai_response_content(markdown_text):
    formatted_html = markdown.markdown(markdown_text)
    return formatted_html


class ArticleAiCreationView(View):
    form_class  = AIArticleGenerationModelForm

    def get_profile(self):
        return get_user(self.request).profile_user


    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        form = self.form_class(data=data)

        if form.is_valid():
            template_statement = ''
            keywords_statment = ''

            template = form.cleaned_data.get('template', None)

            
            instructions = form.cleaned_data.get('instructions', '')
            keywords = form.cleaned_data.get('keywords', None)

            template_statement = f"I want you to write an article based on {template}."

            keywords_statment = f"Use the following keywords, {keywords} in your response."

            ai_prompt = f"""
                Your are an AI assistant. 
                {template_statement}.
                Follow these instructions to come up with the article, {instructions}. 
                {keywords_statment}
                At the end include a summary title for the article.
            """
            response = self.get_response(ai_prompt)

            title = f"{self.extract_substring(response.split('.')[0])}"

            create_ai_save_history.after_response(
                profile=self.get_profile(),
                question=instructions,
                response=response,
                title=title,
                **kwargs
            )

            reduce_tokens.after_response(
                profile=self.get_profile(),
                **kwargs
            )

            return JsonResponse({"success": True, 'data': response})
        


    def get_response(self, prompt):
        response = chat_session.send_message(prompt, stream=True)
        for chunk in response:
            # time.sleep(3)
            print(chunk.text)
            print("_"*80)
        # print(response.text)
        # print(response)
        data = response.to_dict()
        # print(data)
        return format_ai_response_content(data['candidates'][0]['content']['parts'][0]['text'])
    
    def extract_substring(self, substring):
        first_h2_html_tag = substring.find("<h2>")
        last_h2_html_tag = substring.find("</h2>")

        return substring[first_h2_html_tag+4:last_h2_html_tag]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class SaveAiArticleResponse(View):
    '''profile
title
question
response
created_at'''


@after_response.enable
def create_ai_save_history(
    profile,
    question, 
    response, 
    title='', 
    **kwargs
    ):
    history, _ = AIHistory.objects.get_or_create(
        profile=profile,
        question=question,
        response=response,
    )

    history.title = title
    history.save()
    return history

@after_response.enable
def reduce_tokens(profile, **kwargs):
    print("reducing the days tokens count")
    return 3



class ContentAiEditPostView(ArticleMixinView):
    template_name = "account/dashboard/v1/articles/editor/edit.html"

    def get_history(self):
        try:
            return get_object_or_404(AIHistory, pk=self.kwargs.get("pk"), slug=self.kwargs.get("slug"))	
        except:
            return None
    
    def get_histories(self):
        try:
            return AIHistory.objects.select_related("profile").filter(profile=self.get_history().profile).exclude(slug=self.get_history().slug)
        except:
            return None
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["history"] = self.get_history()
        context["histories"] = self.get_histories().order_by("-id")[:3]
        return context
    
from .download import download_youtube_from_video_url
from .transcribe import transcribe_audio
from django.db import transaction
from .summarize import TranscriptSummarizer, summarize_transcript

class YoutubeSummarizerView(ArticleMixinView):
    template_name = 'account/dashboard/v1/articles/editor/summarizer.html'
    form_class = YoutubeSummarizerForm

    @transaction.atomic
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context
    
    def post(self, request, *args, **kwargs):
        form  = self.form_class(data=json.loads(request.body))
        if form.is_valid():
            instance = form.save(commit=False)
            instance.profile = self.request.user.profile_user

            video_url = form.cleaned_data.get("video_url", '')

            time.sleep(1)

            # audio_url, length = download_youtube_from_video_url(video_url)
            audio_url = 'https://earnkraft.s3.eu-north-1.amazonaws.com/audio/youtube/Ko52pn1KXS0.mp3'
            length=100
            instance.duration = length
            instance.audio_url = audio_url
            instance.save()
            form.save()

            response = YtSummarizerSerializer(instance).data

            if audio_url:
                return JsonResponse({"success": True, 'data': audio_url, 'instance': response}, safe=False)
        return JsonResponse({"success": False, 'data': json.dumps(form.errors)})


class AudioTranscriptionView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        audio_link = data.get("audio_link")
        audio_pk = data.get("audio_pk", '')

        yt_summarizer = get_object_or_404(YtSummarizer, pk=audio_pk)
        print("yt_summarizer: ", yt_summarizer)

        time.sleep(3)

        file_link, transcript = transcribe_audio(filename=audio_link)


        yt_summarizer.video_transcript = transcript
        yt_summarizer.transcript_file = file_link

        yt_summarizer.save()

        instance = YtSummarizerSerializer(yt_summarizer).data
        
        return JsonResponse({
                "success": True, 
                'data': instance, 
                'response': transcript,
            }, 
            safe=False
        )



class SummarizeTranscriptionView(ArticleMixinView):
    filename_url = "https://earnkraft.s3.eu-north-1.amazonaws.com/transcripts/files/transcript.pdf"  #TODO: REMOVE ONCE TEST DONE
    template_name = 'account/dashboard/v1/articles/editor/summary.html' #TODO: REMOVE ONCE TEST DONE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, pk):
        return get_object_or_404(YtSummarizer, pk=pk)
    
    def post(self, request, *args, **kwargs):
        # data = json.loads(request.body)
        # print("data", data)

        summarizer = summarize_transcript(self.filename_url)

        # instance = self.get_object(pk=data["transcript_instance"]['id'])
        # print("transcript", instance)
        # transcript_text = instance.video_transcript
        # # file = instance.transcript_file

        # print("instance", instance, "transcript_text", transcript_text)
        summary = summarizer
        print("summary", summary)
        data = {
            "summary": summary,
        }


        return JsonResponse({"success": True, "response":data})

        