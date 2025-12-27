from django.db import models


class StorageType(models.TextChoices):
    SPACE = "SPACE", "Space"
    DRAWER = "DRAWER", "Drawer"


class WeightType(models.TextChoices):
    GM = "GM", "Gm"
    KG = "KG", "Kg"
    GSM = "GSM", "GSM"


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


class ActionTypes(models.TextChoices):
    CREATE = "CREATE", "Create"
    UPDATE = "UPDATE", "Update"


class ModifyRequestStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ACCEPTED = "ACCEPTED", "Accepted"
    REJECTED = "REJECTED", "Rejected"


class MainCategoryChoices(models.TextChoices):
    CIRCULAR_KNIT = "CIRCULAR_KNIT", "Circular Knit"
    FLAT_KNIT = "FLAT_KNIT", "Flat Knit"
    WOVEN = "WOVEN", "Woven"


class SubCategoryChoices(models.TextChoices):
    MENS = "MENS", "Mens"
    JR_LADIES = "JR_LADIES", "Jr. Ladies"
    WOMEN = "WOMEN", "Women"
    JUNIOR_BOYS = "JUNIOR_BOYS", "Junior Boys"
    SENIOR_BOYS = "SENIOR_BOYS", "Senior Boys"
    TODDLER_BOYS = "TODDLER_BOYS", "Toddler Boys"
    JUNIOR_GIRLS = "JUNIOR_GIRLS", "Junior Girls"
    SENIOR_GIRLS = "SENIOR_GIRLS", "Senior Girls"
    TODDLER_GIRLS = "TODDLER_GIRLS", "Toddler Girls"
    KIDS = "KIDS", "Kids"
    DENIM = "DENIM", "Denim"
    NON_DENIM = "NON_DENIM", "Non Denim"
