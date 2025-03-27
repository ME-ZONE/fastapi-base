# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class PcsUserDetails(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey('PcsUsers', models.CASCADE)
    fullname = models.CharField(unique=True, max_length=50)
    gender = models.TextField()  # This field type is a guess.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pcs_user_details'
