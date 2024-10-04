from django.utils.text import slugify


def advertizement_design_upload_url(instance, filename):
    return f"""
            adverts/{instance.updated_at.year}/{instance.updated_at.month}/{instance.updated_at.day}/{slugify(instance.category.title)}/{slugify(instance.title)}/{filename}
            """
