from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

DJANGO_UNFOLD_SIDEBAR_NAVIGATION = [
            {
                "title": _("Navigation"),
                "separator": False,  # Top border
                "items": [
                    {
                        "title": _("Home"),
                        "icon": "home",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        "badge": "",
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": reverse_lazy("admin:users_user_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Profile"),
                        "icon": "person",
                        "link": reverse_lazy("admin:users_profile_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Groups"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    }
                ],
            },
            {
                "title": _("Investment"),
                "separator":True,
                "items": [
                    {
                        "title": _("Pool"),
                        "icon": "savings",
                       "link": reverse_lazy("admin:invest_pool_changelist"),
                        "permissions": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Account"),
                        "icon": "savings",
                       "link": reverse_lazy("earnkraft:invest_account_changelist"),
                        "permissions": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title":_("Advertisement"),
                "separator":True,
                "items": [
                    {
                        "title": _("Advertisement"),
                        "icon": "storefront",
                         "link": reverse_lazy("admin:adverts_adcategory_changelist"),
                         "permissions": lambda request: request.user.is_staff
                    },
                ]
            },
            {
                "title":_("Podium"),
                "separator":True,
                "items": [
                    {
                        "title": _("Agents"),
                        "icon": "real_estate_agent",
                         "link": reverse_lazy("admin:profiles_agent_changelist"),
                         "permissions": lambda request: request.user.is_superuser
                    },
                    {
                        "title": _("Positions"),
                        "icon": "jump_to_element",
                        "link": reverse_lazy("admin:profiles_position_changelist"),
                        "permissions": lambda request: request.user.is_superuser
                    },
                    {
                        "title": _("Plantform"),
                        "icon": "podium",
                        "link": reverse_lazy("admin:profiles_plantformtype_changelist"),
                        "permissions": lambda request: request.user.is_superuser
                    },
                ]
            },

            {
                "title":_("Money Matters"),
                "separator":True,
                "items": [
                    {
                        "title": _("Exchange Rates"),
                        "icon": "money",
                         "link": reverse_lazy("admin:rates_kenyaconversion_changelist"),
                         "permissions": lambda request: request.user.is_superuser
                    },
                ]
             },
            {
                "title":_("Subscriptions"),
                "separator":True,
                "items": [
                    {
                        "title": _("Issues"),
                        "icon": "settings", # TODO add the write icon
                         "link": reverse_lazy("admin:subscriptions_issue_changelist"),
                         "permissions": lambda request: request.user.is_superuser
                    },
                ]
             }
    ]
