from django.db import models
from django.contrib.auth.models import User

class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

class Blog(models.Model):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)  #添加创建时间
    last_updated_time = models.DateTimeField(auto_now=True)  #添加修改时间

    def __str__(self):
        return "<Blog: %s>" % self.title
