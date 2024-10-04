# Register your models here.
from unfold.sites import UnfoldAdminSite


class CoreAdminInterface(UnfoldAdminSite):
    site_title = "Earnkraft Agencies"
    site_header = "Earnkraft administration"
    index_title = "Earnkraft Agencies"


earnkraft_site = CoreAdminInterface(name="earnkraft")

