from django.db import models


class Plane(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    passengers_amount = models.PositiveIntegerField()

    @property
    def fuel_capacity(self):
        return 200 * self.id
