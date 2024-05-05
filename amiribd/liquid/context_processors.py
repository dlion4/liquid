from .forms import ContactForm


def liquid_site_data(request):
    return {
        "site_name": "AmiriBD",
        "contact_form": ContactForm(),
        "address": "Satrio Tower 16th Floor, Jl. Prof Dr Satrio Kuningan, Jakarta",
        "officephone": "(888)234-5686",
        "officeemail": "contact@liquid.co.ke",
    }
