from csv import writer
from email.policy import default
from django.db import models
from django.core.files import File
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .utils import image_resize, barcode_gen
import uuid
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
# Create your models here.


def image_file_location(instance, filename):
    return "idimage/{0}/{1}".format(instance.id, filename)


class IdInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    id_number = models.CharField(max_length=13, blank=True, null=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    position = models.CharField(max_length=60)
    contact = models.CharField(max_length=13, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=120)
    contact_number = models.CharField(
        max_length=13, verbose_name="emergency contact number")
    address = models.TextField()
    blood_type = models.CharField(max_length=5, default="A")
    birth_date = models.DateField()
    image = models.ImageField(
        upload_to=image_file_location, help_text='Please upload square image')
    signature = models.ImageField(
        upload_to=image_file_location, help_text='Please upload square image', blank=True, null=True)
    barcode = models.ImageField(upload_to=image_file_location, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def full_name(self):
        fullname = "%s %s" % (self.first_name, self.last_name)
        return fullname

    def __str__(self):
        return self.full_name().title()

    def save(self, *args, **kwargs):
        # image_resize(self.image, 512, 512)
        # barcode
        # barcode_gen(self.id_number, self.barcode)
        return super().save(*args, **kwargs)


@receiver(post_save, sender=IdInfo)
def post_save_id_number(sender, instance, created, *args, **kwargs):
    if created:
        UUID = uuid.uuid1()
        ean = UUID.int
        text_id = str(ean)[:13]
        instance.id_number = int(text_id)
        # instance.save()
        barcode_gen(instance.id_number, instance.barcode)
        instance.save()


@receiver(pre_save, sender=IdInfo)
def pre_save_image(sender, instance, *args, **kwargs):
    image_resize(instance.image, 512, 512)
