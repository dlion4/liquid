from django.contrib import admin

# Register your models here.
from django.contrib import admin
from unfold.sites import UnfoldAdminSite


class CoreAdminInterface(UnfoldAdminSite):
    
    site_title = "Earnkraft Agencies"
    site_header = "Earnkraft administration"
    index_title = "Earnkraft Agencies"
    index_title = "Welcome to the Earnkraft Agencies Admin Portal"


earnkraft_site = CoreAdminInterface(name="earnkraft",)

