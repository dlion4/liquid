
def badge_callback(request):
    return 3

def badge_articles_count_callback(request):
    from amiribd.articles.models import Article
    return Article.objects.count()

def dashboard_callback(request, context):
    """
    Callback to prepare custom variables for index template which is used as dashboard
    template. It can be overridden in application by creating custom admin/index.html.
    """
    context.update(
        {
            "sample": "example",  # this will be injected into templates/admin/index.html
        }
    )
    return context


def environment_callback(request):
    """
    Callback has to return a list of two values represeting text value and the color
    type of the label displayed in top right corner.
    """
    return ["Production", "success"] # info, danger, warning, success


def staff_permissions_callback(request):
    return request.user.is_staff


def superuser_permissions_callback(request):
    return request.user.is_superuser


def navigation_reverse_callback(request):
    from django.urls import reverse

    admin_url = 'admin:index'
    earnkraft_url = 'earnkraft:index'

    if request.user.is_superuser:
        return reverse(admin_url)
    
    else:
        return reverse(earnkraft_url)
