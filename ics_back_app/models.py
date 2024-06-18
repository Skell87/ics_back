from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    is_staff = models.BooleanField(default=False)

    def __str__ (self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


# class Warehouse(models.Model):
#     name = models.CharField(max_length=100)
    
#     def __str__(self):
#         return self.name
    
# class Division(models.Model):
#     warehouse = models.ForeignKey(Warehouse, related_name='divisions', on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     count = models.IntegerField(default=0)

#     def __str__(self):
#         return f'{self.name} ({self.count})'
    
# # i think i set this up incorrectly.
# # it gets the warehouse name
# # i want this to get the name, each division incremented by count.
# class WarehouseLocation(models.Model):
#     warehouse = models.ForeignKey(Warehouse, related_name='locations', on_delete=models.CASCADE)
#     location = models.CharField(max_length=255)

#     def __str__(self):
#         return f'{self.warehouse.name} - {self.location}'
    
# --------------------------------------------------------------------------------------

# models for inventory items and adding quantity to them.
    

    # def __str__(self):
    #     # do this...
        

# these are the models for the """WAREHOUSE"""
# grandaddy is section, then subSection, then SubSubSection. biggest to smallest. 


# +---------------------+          +---------------------+          +-------------------------+
# | WarehouseSection    |          | WarehouseSubSection |          | WarehouseSubSubSection  |
# +---------------------+          +---------------------+          +-------------------------+
# | - id: Integer (PK)  |1        *| - id: Integer (PK)  |1        *| - id: Integer (PK)      |
# | - name: String      |----------| - name: String      |----------| - name: String          |
# +---------------------+          | - section_id: FK    |          | - sub_section_id: FK    |
#                                  +---------------------+          +-------------------------+

class InventoryItems(models.Model):
    name = models.TextField(max_length=255)
    make = models.TextField(max_length=255)
    model = models.TextField(max_length=255)
    color = models.TextField(max_length=255)
    notes = models.TextField(max_length=255)

    def __str__(self):
        return f'name: {self.name}, make: {self.make}, model: {self.model}, color: {self.color}, notes: {self.notes}'

class WarehouseSection(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class WarehouseSubSection(models.Model):
    name = models.CharField(max_length=25)
    section = models.ForeignKey(WarehouseSection, on_delete=models.CASCADE, related_name='sub_sections')

    def __str__(self):
        return self.name

class WarehouseSubSubSection(models.Model):
    name = models.CharField(max_length=255)
    sub_section = models.ForeignKey(WarehouseSubSection, on_delete=models.CASCADE, related_name='sub_sub_sections')

    def __str__(self):
        return self.name

class InventoryDetails(models.Model):
    quantity = models.IntegerField(default=0)
    inventory_item = models.ForeignKey(InventoryItems, on_delete=models.CASCADE)
    sub_sub_section = models.ForeignKey(WarehouseSubSubSection, on_delete=models.CASCADE, related_name='inventory_details')

