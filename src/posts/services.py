from django.shortcuts import get_object_or_404


class PostService:
    def get_post_by_slug(self, slug:str, Model=None):  # noqa: N803
        return get_object_or_404(Model, slug=slug)
