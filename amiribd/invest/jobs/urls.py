from django.urls import path, include

from amiribd.invest.views import modified_jobs_view
from . import views



app_name = "jobs"

urlpatterns = [
    path(
        "",
        modified_jobs_view,
        name="jobs",
    ),
    path(
        "shelves/board/",
        views.JobBoardView.as_view(), 
        name="job_board_view",
    ),
    path(
        "shelves/board/applications/",
        views.JobBoardApplicationView.as_view(), 
        name="job_board_applications_view",
    ),
    path(
        "shelves/board/applications/<application_id>/",
        views.CancelJobApplicationView.as_view(), 
        name="job_cancel_job_application",
    ),
]
