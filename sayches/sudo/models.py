from django.db import models
from users.models import BaseModel


class CloseWebsite(BaseModel):
    close_site = models.BooleanField(default=False)
    closing_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.closing_text

    def delete(self):
        self.close_site = False
        self.save()

    class Meta:
        verbose_name_plural = "Close Website"


class VersionNumber(BaseModel):
    version_no = models.CharField(max_length=25, null=True, blank=True)
    show_beta_icon = models.BooleanField(default=False)
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Versioning"


class CloseRegistration(BaseModel):
    close_registration = models.BooleanField(default=False)
    custom_error_message = models.TextField(null=True, blank=False)

    class Meta:
        verbose_name_plural = "Close Registration"

class BitcoinAddress(BaseModel):
    address = models.CharField(null=True, blank=False, max_length=45, unique=True)
    expired = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name_plural = "Bitcoin Addresses"