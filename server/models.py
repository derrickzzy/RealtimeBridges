from __future__ import unicode_literals

from django.db import models

# Create your models here.

# define bridge conditions
BRIDGE_CONDITIONS = (
    ('g', 'Green'),
    ('y', 'Yellow'),
    ('r', 'Red'),
)

# Bridge Information
class Bridge(models.Model):
    name = models.CharField(
        max_length = 40,
        verbose_name = 'Bridge Name',
    )
    number = models.CharField(
        max_length = 40,
        verbose_name='Bridge Number',
    )
    photo = models.ImageField(
        upload_to='static',
    )
    year = models.CharField(
        max_length = 4,
        verbose_name='Built Year',
    )
    inspection = models.DateField(
        max_length = 4,
        verbose_name='Last Inspection Date',
    )
    town = models.CharField(
        max_length = 40,
        verbose_name='Town',
    )
    state = models.CharField(
        max_length = 20,
        verbose_name='State',
    )
    conditions = models.CharField(
        max_length=1,
        choices=BRIDGE_CONDITIONS,
        verbose_name='Bridge Condition',
    )

    def __str__(self):
        return self.name
