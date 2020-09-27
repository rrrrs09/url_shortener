from django.db import models


class LongUrl(models.Model):
    '''User posted long url'''
    url = models.URLField(db_index=True)

    def __str__(self):
        return self.url

    class Meta:
        db_table = 'urls'


class UrlSlug(models.Model):
    '''Urls custom slugs posted by users'''
    long_url = models.ForeignKey(to=LongUrl, on_delete=models.CASCADE,
                            related_name='slugs')
    slug = models.SlugField(unique=True, db_index=True, max_length=50)

    def __str__(self):
        return self.slug

    class Meta:
        db_table = 'url_slugs'
