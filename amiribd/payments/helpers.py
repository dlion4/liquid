from intasend import APIService
from django.conf import settings


class MpesaStkPushSetUp:
    # publishable_key = settings.INTASEND_PUBLISHABLE_KEY
    # secret_key = settings.INTASEND_SECRET_KEY
    publishable_key =''
    secret_key = ''

    def mpesa_stk_push_service(self):

        return APIService(
            token=self.secret_key,
            publishable_key=self.publishable_key,
            test=settings.INTASEND_TEST_MODE,
        )
