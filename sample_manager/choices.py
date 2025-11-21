from django.db import models


class StorageType(models.TextChoices):
    SPACE = "SPACE", "Space"
    DRAWER = "DRAWER", "Drawer"


class WeightType(models.TextChoices):
    GM = "GM", "Gm"
    KG = "KG", "Kg"


class SizeType(models.TextChoices):
    CENTIMETER = "CENTIMETER", "Centimeter"
    LETTER = "LETTER", "Letter"


class SampleTypes(models.TextChoices):
    DEVELOPMENT = "DEVELOPMENT", "Development"
    SALESMAN = "SALESMAN", "Salesman"
    STYLING = "STYLING", "Styling"
    SHIPPING = "SHIPPING", "Shipping"
    FIT = "FIT", "Fit"
    PRODUCTION = "PRODUCTION", "Production"
    PRE_PRODUCTION = "PRE_PRODUCTION", "Pre_Production"
    COUNTER = "COUNTER", "Counter"
    SIZE_SET = "SIZE_SET", "Size_set"
    ORIGINAL = "ORIGINAL", "Original"


class SampleStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    OUT_OF_STOCK = "OUT_OF_STOCK", "Out_of_stock"
    DELETED = "Deleted"
