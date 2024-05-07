from django.db import models

# Create your models here.

class Agents(models.Model):
    id    = models.AutoField(primary_key=True)
    name  = models.CharField(max_length = 100) 
    info  = models.CharField(max_length = 100, default = '')
    ip_address = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
   

class Article(models.Model):
    title = models.CharField(max_length=256)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=ARTICLE_TYPES, default="UN")
    categories = models.ManyToManyField(to=Category, blank=True, related_name="categories")
    content = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    # new
    def type_to_string(self):
        if self.type == "UN":
            return "Unspecified"
        elif self.type == "TU":
            return "Tutorial"
        elif self.type == "RS":
            return "Research"
        elif self.type == "RW":
            return "Review"

    def __str__(self):
        return f"{self.author}: {self.title} ({self.created_datetime.date()})"