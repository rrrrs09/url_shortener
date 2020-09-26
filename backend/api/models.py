from django.db import models


class UrlItem(models.Model):
    original_url = models.URLField()

    def __str__(self):
        return self.original_url

    class Meta:
        db_table = 'urls'


class UrlSlug(models.Model):
    url = models.ForeignKey(to=UrlItem, on_delete=models.CASCADE,
                            related_name='slugs')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug

    class Meta:
        db_table = 'url_slugs'
