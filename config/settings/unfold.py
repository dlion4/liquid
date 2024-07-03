from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

DJANGO_UNFOLD_SIDEBAR_NAVIGATION = [
            {
                "title": _("Navigation"),
                "separator": False,  # Top border
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        "badge": "core.badge_callback",
                        "permission": "core.staff_permissions_callback",
                    },
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": reverse_lazy("admin:users_user_changelist"),
                        "permission": "core.superuser_permissions_callback",
                    },
                   
                    {
                        "title": _("Groups"),
                        "icon": "holiday_village",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                        "permission": "core.superuser_permissions_callback",
                    }
                ],
            },
             {
                "title":_("Profile"),
                "separator":True,
                "items": [
                    {
                        "title": _("Profile"),
                        "icon": "person",
                        "link": reverse_lazy("admin:users_profile_changelist"),
                        "permission": "core.superuser_permissions_callback",
                    },
                    {
                        "title": _("Notifications"),
                        "icon": "notifications",
                        "link": reverse_lazy("earnkraft:profilesettings_notification_changelist"),
                        "permission": "core.superuser_permissions_callback",
                    },
                ]
            },

            {
                "title": _("Secret Credentials"),
                "separator":True,
                "items": [
                    {
                        "title": _("Credentials"),
                        "icon": "key",
                        "link": reverse_lazy("admin:tokens_secretcredential_changelist"),
                        "permission": "core.superuser_permissions_callback",
                    },
                    {
                        "title": _("AuthToken"),
                        "icon": "security",
                        "link": reverse_lazy("admin:tokens_authtoken_changelist"),
                        "permission": "core.superuser_permissions_callback",
                    },
                ]
            },
            {
                "title": _("Investment"),
                "separator":True,
                "items": [
                    {
                        "title": _("Pool"),
                        "icon": "savings",
                       "link": reverse_lazy("admin:invest_pool_changelist"),
                        "permission": "core.superuser_permissions_callback",
                    },
                    {
                        "title": _("Account"),
                        "icon": "admin_panel_settings",
                       "link": reverse_lazy("earnkraft:invest_account_changelist"),
                        "permission": "core.superuser_permissions_callback",
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
                        "permission": "core.superuser_permissions_callback",
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
            },
            {
                "title":_("Editor"),
                "separator":True,
                "items": [
                    {
                        "title": _("Writings"),
                        "icon": "article", # TODO add the write icon
                        "link": reverse_lazy("earnkraft:articles_article_changelist"),
                        "badge":"core.badge_articles_count_callback",
                        "permission": "core.staff_permissions_callback",
                    },
                    {
                        "title": _("AI Template"),
                        "icon": "highlight", # TODO add the write icon
                        "link": reverse_lazy("earnkraft:articles_templatecategory_changelist"),
                        # "badge":"core.badge_articles_count_callback",
                        "permission": "core.staff_permissions_callback",
                    },
                    {
                        "title": _("Templates"),
                        "icon": "connected_tv", # TODO add the write icon
                        "link": reverse_lazy("earnkraft:articles_template_changelist"),
                        # "badge":"core.badge_articles_count_callback",
                        "permission": "core.staff_permissions_callback",
                    },
                    {
                        "title": _("AI History"),
                        "icon": "history", # TODO add the write icon
                        "link": reverse_lazy("earnkraft:articles_aihistory_changelist"),
                        # "badge":"core.badge_articles_count_callback",
                        "permission": "core.staff_permissions_callback",
                    },
                ]
            },
            {
                "title":_("PROFILE KYC"),
                "separator":True,
                "items": [
                    {
                        "title": _("Address"),
                        "icon": "location_on", # TODO add the write icon
                        "link": reverse_lazy("earnkraft:users_address_changelist"),
                        
                        "permission": lambda request: request.user.is_superuser
                    },
                    {
                        "title": _("Documents"),
                        "icon": "app_registration", # TODO add the write icon
                        "link": reverse_lazy("earnkraft:users_document_changelist"),
                        "permission": lambda request: request.user.is_superuser
                    },
                ]
            },
            {
                "title":_("OPPOTUNITIES"),
                "separator":True,
                "items": [
                    {
                        "title": _("Job"),
                        "icon": "location_on", # TODO add the write icon
                        "link": reverse_lazy("earnkraft:jobs_job_changelist"),
                        
                        "permission": lambda request: request.user.is_superuser
                    },
                    
                ]
            },
            {
                "title":_("SERVICES"),
                "separator":True,
                "items": [
                    {
                        "title": _("Youtube Summarizer"),
                        "icon": "engineering", # TODO add the write icon
                        "link": reverse_lazy("earnkraft:articles_ytsummarizer_changelist"),
                        "permission": lambda request: request.user.is_superuser
                    },
                ]
            },
    ]
