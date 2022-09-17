from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
#from django.utils.text import slugify
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
#from .utils import unique_slug_generator
# Create your models here.


class UserRegi(models.Model):
    name=models.CharField( max_length=50,blank=False)
    flat=models.CharField( max_length=10,blank=False)
    phone=models.CharField( max_length=50,blank=True)
    email=models.EmailField( max_length=50,blank=True)
    #slug=models.SlugField(unique=True)
    image=models.ImageField(null=True,blank=True, upload_to="")


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('user_details', args=[str(self.id)]) #kwargs={'slug': self.slug})



    def save(self, *args, **kwargs):
        super(UserRegi, self).save(*args, **kwargs)

        image = Image.open(self.image.path)
        if image.height > 300 or image.width > 300:
            output_size = (300, 300)
            image.thumbnail(output_size)
            image.save(self.image.path)
