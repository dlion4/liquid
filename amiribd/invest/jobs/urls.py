from django.urls import path
from .views import upload_submission

from amiribd.invest.views import modified_jobs_view

from . import views

app_name = "jobs"

urlpatterns = [
    path(
        "",
        modified_jobs_view,
    
        name="jobs",
    ),
    
    path('upload-submission/<int:application_id>/', upload_submission, name='upload_submission'),
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
    path(
        "shelves/board/applications/<application_id>/reactivate/",
        views.ReactivateJobApplicationView.as_view(),
        name="job_reactivate_job_application",
    ),
]
