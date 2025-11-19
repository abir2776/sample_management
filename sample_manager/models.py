from django.db import models
from simple_history.models import HistoricalRecords

from common.choices import Status
from common.models import BaseModelWithUID
from .choices import StorageType


class Storage(BaseModelWithUID):
    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE
    )
    created_by = models.ForeignKey("core.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    type = models.CharField(
        max_length=20, choices=StorageType, default=StorageType.SPACE
    )
    image = models.FileField(null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name}-{self.created_by.first_name}"


class Sample(BaseModelWithUID):
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    created_by = models.ForeignKey("core.User", on_delete=models.CASCADE)
    style_no = models.CharField(max_length=255)
    sku_no = models.CharField(max_length=255)
    item = models.CharField(max_length=255)
    fabrication = models.CharField(max_length=255)
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    color = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    sample_type = models.CharField(max_length=255)
    comments = models.CharField(max_length=500, null=True, blank=True)
    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name}-{self.bucket.name}"


class StorageFile(BaseModelWithUID):
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    created_by = models.ForeignKey("core.User", on_delete=models.CASCADE)
    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name}-{self.storage.name}"


class File(BaseModelWithUID):
    file = models.FileField()
    file_name = models.CharField(max_length=255)
    created_by = models.ForeignKey("core.User", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.file_name}"


class SampleFile(BaseModelWithUID):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("sample", "file")

    def __str__(self):
        return f"{self.sample.name}-{self.file.file_name}"


class StorageFileFile(BaseModelWithUID):
    storage_file = models.ForeignKey(StorageFile, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("storage_file", "file")

    def __str__(self):
        return f"{self.storage_file.name}-{self.file.file_name}"


class Buyer(BaseModelWithUID):
    created_by = models.ForeignKey("core.User", on_delete=models.CASCADE)
    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name}-{self.created_by.name}"


class SampleBuyerConnection(BaseModelWithUID):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.sample.name}-{self.buyer.name}"
