import requests
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Image(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name="images_created", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to="images/%Y/%m/%d")
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    user_likes = models.ManyToManyField(
        get_user_model(), related_name="images_liked", blank=True
    )
    total_likes = models.PositiveIntegerField(db_index=True, default=0)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("images:image_detail", kwargs={"slug": self.slug})
