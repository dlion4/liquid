from django.shortcuts import render
from amiribd.dashboard.views import DashboardViewMixin

# Create your views here.
from django.conf import settings
import json


additional_js_ckeditor_logic = '''
    .then(editor => {
        window.editor = editor;

        const annotationsUIs = editor.plugins.get('AnnotationsUIs');
        const sidebarElement = document.querySelector('.sidebar');
        let currentWidth;

        function refreshDisplayMode() {
            if (window.innerWidth === currentWidth) {
                return;
            }
            currentWidth = window.innerWidth;

            if (currentWidth < 1000) {
                sidebarElement.classList.remove('narrow');
                sidebarElement.classList.add('hidden');
                annotationsUIs.switchTo('inline');
            } else if (currentWidth < 1300) {
                sidebarElement.classList.remove('hidden');
                sidebarElement.classList.add('narrow');
                annotationsUIs.switchTo('narrowSidebar');
            } else {
                sidebarElement.classList.remove('hidden', 'narrow');
                annotationsUIs.switchTo('wideSidebar');
            }
        }

        editor.ui.view.listenTo(window, 'resize', refreshDisplayMode);
        refreshDisplayMode();

        return editor;
    })
    .catch(error => {
        console.error('There was a problem initializing the editor.', error);
    });
'''





class ArticleMixinView(DashboardViewMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ckeditor_config"] = json.dumps(settings.CKEDITOR_5_CONFIGS)
        context["additional_js_ckeditor_logic"] = additional_js_ckeditor_logic
        return context


class BloggingHomeView(ArticleMixinView):
    template_name = "account/dashboard/v1/articles/home.html"


class BloggingTemplateView(ArticleMixinView):
    template_name = "account/dashboard/v1/articles/templates.html"


class PostHistoryListView(ArticleMixinView):
    template_name = "account/dashboard/v1/articles/posts.html"


class PricingPlanForAiBloggingView(ArticleMixinView):
    template_name = "account/dashboard/v1/articles/pricing.html"


class PaymentPlanForAiView(ArticleMixinView):
    template_name = "account/dashboard/v1/articles/payment.html"
