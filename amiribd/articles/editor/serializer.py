from amiribd.users.serializers import ProfileSerializer
from amiribd.articles.models import YtSummarizer
from rest_framework import serializers


class YtSummarizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = YtSummarizer
        fields = "__all__"

        
