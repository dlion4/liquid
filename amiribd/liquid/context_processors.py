from .forms import ContactForm
from .models import CompanyTermsAndPolicy

def liquid_site_data(request):
    return {
        "site_name": "AmiriBD",
        "contact_form": ContactForm(),
        "address": "Satrio Tower 16th Floor, Jl. Prof Dr Satrio Kuningan, Jakarta",
        "officephone": "contact Us",
        "officeemail": "support@earnkraft.com",
        "company_privacy_document":CompanyTermsAndPolicy.objects.first(),
        "external_links": {
            "blogging_site":{
                "domain": "earnkraft.com",
                "url": "https://earnkraft.com"
            }
        }
    }


