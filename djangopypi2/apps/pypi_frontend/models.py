#######################
from __future__ import unicode_literals, print_function
from django.utils.encoding import python_2_unicode_compatible
#######################
from django.db import models
from django.utils.translation import ugettext_lazy as _

@python_2_unicode_compatible
class MirrorSite(models.Model):
    enabled = models.BooleanField(default=False)
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class MirrorLog(models.Model):
    mirror_site = models.ForeignKey(MirrorSite, related_name='logs')
    created = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=256)
    
    def __str__(self):
        return self.action
    
    class Meta:
        get_latest_by = 'created'
