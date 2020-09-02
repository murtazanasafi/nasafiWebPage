from __future__ import unicode_literals
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings



class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        print(instance)
        content_type = ContentType.objects.get_for_model(instance.__class__)

        qs = super(CommentManager, self).filter(content_type=content_type, object_id = instance.pk).filter(parent=None)
        return qs




# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type','object_id')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    approve_comment = models.BooleanField(default=True)

    objects = CommentManager()


    def approve(self):
        self.approve_comment = True
        self.save()

    def childern(self):
        return Comment.objects.filter(parent=self)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        ordering = ['-timestamp']

