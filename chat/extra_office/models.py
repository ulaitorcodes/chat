from django.db import models

# Create your models here.

class Folder(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    icon = models.ImageField()
    #08092300022

class File(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True)
    doc = models.FileField(upload_to='media/files/', null=True)
    parent_folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='folder')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # created_by = models.OneToOneField(
    #     settings.AUTH_USER_MODEL,
    #     related_name='vendor',
    #     on_delete=models.CASCADE,
    #     unique=True)
  
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    # def get_balance(self):
    #     items = self.items.filter(
    #         vendor_paid=False,
    #         order__vendors__in=[
    #             self.id])
    #     return sum((item.product.price * item.quantity) for item in items)

    # def get_paid_amount(self):
    #     items = self.items.filter(
    #         vendor_paid=True,
    #         order__vendors__in=[
    #             self.id])
                
    #     return sum((item.product.price * item.quantity) for item in items)
