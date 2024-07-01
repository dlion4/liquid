from django import forms
from django.utils.translation import gettext_lazy as _
from amiribd.articles.models import Template, YtSummarizer


class AIArticleGenerationModelForm(forms.Form):
    template = forms.ModelChoiceField(required=False, label="Select Template to use", queryset=Template.objects.all(), widget=forms.Select(
        attrs={
            "class":"form-select select2 select2-container select2-container--default",
            "tabindex":"-1",
            "aria-hidden":"true", "name":"template"
        }
    ))
    instructions = forms.CharField(widget=forms.Textarea(attrs={
        "class":"form-control", 
        "rows": 3, 
        "cols":20, 
        "placeholder": "instructions for the articles. Proper instructions will inmprove the standard format of the articles  geneated"
        }
    ))
    keywords = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "chatgpt, django, nextjs"}))
    words = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "number of words"}))


class YoutubeSummarizerForm(forms.ModelForm):
    class Meta:
        model = YtSummarizer
        fields = [
            'video_url'
        ]
        widgets = {
            "video_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://www.youtube.com/embed/watch",})
        }
    
