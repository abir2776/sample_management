from django.db import models


class StorageType(models.TextChoices):
    SPACE = "SPACE", "Space"
    DRAWER = "DRAWER", "Drawer"
