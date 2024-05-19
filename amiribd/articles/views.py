from django.shortcuts import render
from amiribd.dashboard.views import DashboardViewMixin
# Create your views here.

class ArticleMixinView(DashboardViewMixin):
    pass



class BloggingHomeView(ArticleMixinView):
    template_name = 'account/dashboard/v1/articles/home.html'



class BloggingTemplateView(ArticleMixinView):
    template_name = 'account/dashboard/v1/articles/templates.html'


class PostHistoryListView(ArticleMixinView):
    template_name = 'account/dashboard/v1/articles/posts.html'


class PricingPlanForAiBloggingView(ArticleMixinView):
    template_name = 'account/dashboard/v1/articles/pricing.html'


class PaymentPlanForAiView(ArticleMixinView):
    template_name = 'account/dashboard/v1/articles/payment.html'