from amiribd.users.models import Profile
from .models import Post
from django import forms
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.widgets import UnfoldAdminTextInputWidget, UnfoldAdminSelectWidget
"""
title
slug
content
author
"""



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            'content',
            'author',
        ]
        widgets = {
            "title":UnfoldAdminTextInputWidget(),
            "content":WysiwygWidget(),
            "author":UnfoldAdminSelectWidget(choices=Profile.objects.all())
        }