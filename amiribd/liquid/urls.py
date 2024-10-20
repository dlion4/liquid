from django.urls import path
from . import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("investment/", views.InvestmentView.as_view(), name="investment"),
    path("education/", views.EducationView.as_view(), name="learn"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("help/", views.HelpView.as_view(), name="help"),
    path("guide/", views.GuideView.as_view(), name="guide"),
    path("customers/", views.CustomersView.as_view(), name="customers"),
    path("career/", views.CareerView.as_view(), name="career"),
    path("policies/", views.PolicyView.as_view(), name="policies"),
    path("view-policy/<pk>/", views.view_policy, name="view_policy"),
    path(
        "careers/application", views.CareerApplication.as_view(),
        name="career_application"),
]
