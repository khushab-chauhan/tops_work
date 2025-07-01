from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=255,blank=False,null=False)
    content = models.CharField(max_length=255,blank=False,null=False)
    create_at = models.DateTimeField(auto_created=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    