from django.db import models

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=264)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name_plural = 'Catagories'


class Product(models.Model):
    mainimage = models.ImageField(upload_to='product_pic')
    name = models.CharField(max_length=264)
    catagory = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='catagory')
    preview_text = models.TextField(max_length=200, verbose_name='Preview Text' )
    details = models.TextField(max_length=1000, verbose_name='Details')
    price = models.FloatField()
    old_price = models.FloatField(default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['-created']



