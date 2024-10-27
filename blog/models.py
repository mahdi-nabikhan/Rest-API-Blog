from django.db import models
from account.models import User
from django.urls import reverse

# Create your models here.
class Posts(models.Model):
    """
    this is class to define for blog app
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='category')

    title = models.CharField(max_length=100)
    content = models.TextField()
    status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField()

    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_snippet(self):
        return self.content[:5]

    def get_absolute_api_url(self):
        return reverse('blog:api/v1:post-detail',kwargs={'pk':self.pk})


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
