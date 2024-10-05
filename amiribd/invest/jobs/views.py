import json
from django.contrib.auth import get_user
from django.db import transaction
from django.http import HttpRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from amiribd.dashboard.guard import DashboardGuard
from amiribd.dashboard.views import DashboardViewMixin
from amiribd.invest.models import Account
from amiribd.jobs.models import JobApplication, JobApplicationSubmission
from amiribd.users.models import Profile
from django.db import IntegrityError
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError

class JobBoardView(DashboardGuard, DashboardViewMixin):
    """
    This class is responsible for showing the job application
    rejected applications and the ongoing ones"""
    queryset = Account
    template_name = "account/dashboard/v1/investment/jobs/index.html"



class JobBoardApplicationView(DashboardGuard, DashboardViewMixin):
    """
    This class is responsible for showing the job application
    rejected applications and the ongoing ones"""
    queryset = Account
    template_name = "account/dashboard/v1/investment/jobs/applications.html"

    def get_applications(self):
        """
        This function retrieves job applications associated with the current
        user's profile.

        Parameters:
        self (JobBoardApplicationView): The instance of the
        JobBoardApplicationView class.

        Returns:
        QuerySet: A queryset containing job applications related to
        the current user's profile.
        The queryset is prefetched with the related 'profile' field for
        efficient database querying.
        """
        return (JobApplication.objects.prefetch_related(
            "applicant").filter(applicant=self.get_profile()))

    def get_context_data(self, **kwargs):
        """
            This function is responsible for preparing the context data for the
            job board application view.
            Parameters:
                **kwargs (dict): Additional keyword arguments passed to the function.
            Returns:
                dict: A dictionary containing the context data for the job board
                application view.
                The dictionary includes the following keys:
                - 'applications': A list of job applications retrieved from the
                database using the get_applications method.
        """
        context = super().get_context_data(**kwargs)
        context["applications"] = self.get_applications()
        return context


class CancelJobApplicationView(View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        This function handles the cancellation of a job application.
        Parameters:	post_id: int
                    applicant:Profile
                    job_applied: Job
        Procedure:
        """

        application = JobApplication.objects.get(pk=kwargs.get("application_id"))
        job = application.job
        profile = Profile.objects.get(user=get_user(request))
        profile.job_applications.remove(job)
        profile.save()
        application.status = "CANCELLED"
        application.save()
        return JsonResponse({"message": "success"})

class ReactivateJobApplicationView(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        This function handles the reactivation of a job application.
        Parameters:    post_id: int
                    applicant:Profile
                    job_applied: Job
        Procedure:
        """
        application = JobApplication.objects.get(pk=kwargs.get("application_id"))
        job = application.job
        profile = Profile.objects.get(user=get_user(request))
        profile.job_applications.add(job)
        profile.save()
        application.status = "ACCEPTED"
        application.save()
        return JsonResponse({"message": "success"})


class UploadCompletedJobFileView(View):

    @transaction.atomic
    def post(self, request:HttpRequest, *args, **kwargs):
        try:
            file = request.FILES.get("submission")
            job_application = JobApplication.objects.get(
                pk=kwargs.get("application_id")).job
            submission = JobApplicationSubmission.objects.create(
                job_application=job_application,
                uploader=Profile.objects.get(user=get_user(request)),
                submission_file=file,
            )
            submission.job_application.is_completed = True
            submission.job_application.save()
            submission.save()
            return JsonResponse(
                {"status": "success", "message": "File uploaded successfully!"},
                status=201)
        except (IntegrityError, ValidationError) as e:
            return JsonResponse(
                {"status": "failed", "message": json.dumps(e)}, status=400)




upload_submission = UploadCompletedJobFileView.as_view()


