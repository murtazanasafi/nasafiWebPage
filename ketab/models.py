from django.db import models
from django.conf import settings
from django.utils import timezone
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from django.utils.text import slugify
from django.urls import reverse
from account.models import Account
from django.db.models import Q

# Create your models here.


def upload_location(instance, filename):
    KetabModel = instance.__class__
    print(KetabModel)
    try:
        obj = KetabModel.objects.order_by('id').last()
        new_id = int(obj.id)+1
    except:
        new_id = 9999
        print(new_id)

    if new_id is None:
        new_id = 1

    return f'user-img-upload/obj-{new_id}/{filename}'


class TaggedKetab(TaggedItemBase):
    content_object = models.ForeignKey('Ketab', on_delete=models.CASCADE)





class KetabManager(models.Manager):



    def active(self, *args, **kwargs):
        return super(KetabManager, self).filter(draft=False).filter(publish__lte=timezone.now())

    def search(self, query=None, *args, **kwargs):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (
                    Q(title__icontains=query) |
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query) |
                    Q(content__icontains=query) |
                    Q(tags__name__icontains = query)
                        )
            qs = qs.filter(or_lookup).distinct()
            print(qs)
        else:
            qs = qs.all()

        return qs

    def search_tags(self, query=None, *args, **kwargs):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (
                    Q(tags__name__icontains = query)
                        )
            qs = qs.filter(or_lookup).distinct()

        return qs




class Ketab(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=250)
    content = models.TextField()
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    publish_date = models.DateTimeField(blank=True, null=True)
    draft = models.BooleanField(default=False)
    slug = models.SlugField(max_length=300, unique=False, editable=False)
    tags = TaggableManager(through=TaggedKetab)

    objects = KetabManager()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super(Ketab, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ketab_detail', kwargs={'slug': self.slug, 'pk': self.pk})

    class Meta:
        ordering = ['-created_date']
