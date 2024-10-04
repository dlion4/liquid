from django.urls import path
from . import views


app_name = "streams"

urlpatterns = [
    path("<slug:room_slug>/", views.RoomView.as_view(), name="room-detail"),
    path(
        "network/hello/",
        views.create_retrieve_message,
        name="hello",
    ),
    path(
        "network/create-retrieve-message/",
        views.MessageInboxRetrieveCreateView.as_view(),
        name="message_create_retrieve_inbox",
    ),
    path(
        "message/<int:pk>/<receiver>/",
        views.MessageInboxView.as_view(),
        name="message-detail",
    ),

    # path("subscribe/<int:pk>/<receiver>", name="subscribe"),
    # path("subscribe",views.subscribe, name="subscribe"),

    # # to check the state of the subscription
    # path('check-post-expiry/<int:post_id>/', views.check_post_expiry, name='check_post_expiry'),

    # include other urls
    # path('news/',include("amiribd.streams.news.")),
]

