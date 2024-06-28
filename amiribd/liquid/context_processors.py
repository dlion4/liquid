from .forms import ContactForm
from .models import CompanyTermsAndPolicy

def liquid_site_data(request):
    return {
        "site_name": "AmiriBD",
        "contact_form": ContactForm(),
        "address": "Satrio Tower 16th Floor, Jl. Prof Dr Satrio Kuningan, Jakarta",
        "officephone": "(888)234-5686",
        "officeemail": "contact@liquid.co.ke",
        "company_privacy_document":CompanyTermsAndPolicy.objects.first(),
        "external_links": {
            "blogging_site":{
                "domain": "earnkraft.com",
                "url": "https://earnkraft.com"
            }
        }
    }


