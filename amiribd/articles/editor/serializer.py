from rest_framework import serializers

from amiribd.articles.models import YtSummarizer


class YtSummarizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = YtSummarizer
        fields = "__all__"


