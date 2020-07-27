from django.db import models
from django.utils import timezone

# Create your models here.


class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    text = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])
