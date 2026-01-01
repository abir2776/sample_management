from django.db import models
from simple_history.models import HistoricalRecords

from common.choices import Status
from common.models import BaseModelWithUID

from .choices import (
    ActionTypes,
    MainCategoryChoices,
    ModifyRequestStatus,
    SampleStatus,
    SampleTypes,
    SizeRangeChoices,
    StorageType,
    SubCategoryChoices,
    WeightType,
)


class Project(BaseModelWithUID):
    company = models.ForeignKey("organizations.company", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    started_at = models.DateTimeField()
    will_finish_at = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name}_{self.started_at}"


class Storage(BaseModelWithUID):
    company = models.ForeignKey("organizations.Company", on_delete=models.CASCADE)
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


class GarmentSample(BaseModelWithUID):
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    sample_id = models.CharField(max_length=255)
    created_by = models.ForeignKey("core.User", on_delete=models.CASCADE)
    arrival_date = models.DateTimeField(null=True, blank=True)
    style_no = models.CharField(max_length=255, null=True, blank=True)
    sku_no = models.CharField(max_length=255, null=True, blank=True)
    item = models.CharField(max_length=255, null=True, blank=True)
    fabrication = models.CharField(max_length=255, null=True, blank=True)
    weight = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=0
    )
    weight_type = models.CharField(
        max_length=20,
        choices=WeightType.choices,
        default=WeightType.GM,
        null=True,
        blank=True,
    )
    color = models.CharField(max_length=255, null=True, blank=True)
    size_range_type = models.CharField(
        max_length=20, choices=SizeRangeChoices.choices, default=SizeRangeChoices.LETTER_RANGE
    )
    letter_range_max = models.IntegerField(null=True,blank=True)
    letter_range_min = models.IntegerField(null=True,blank=True)
    age_range_year_max = models.IntegerField(null=True,blank=True)
    age_range_year_min = models.IntegerField(null=True,blank=True)
    age_range_month_max = models.IntegerField(null=True,blank=True)
    age_range_month_min = models.IntegerField(null=True,blank=True)
    types = models.CharField(
        max_length=20, choices=SampleTypes.choices, null=True, blank=True
    )
    category = models.CharField(
        max_length=20, choices=MainCategoryChoices.choices, null=True, blank=True
    )
    sub_category = models.CharField(
        max_length=20, choices=SubCategoryChoices.choices, null=True, blank=True
    )
    comments = models.CharField(max_length=500, null=True, blank=True)
    company = models.ForeignKey("organizations.Company", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=SampleStatus.choices,
        default=SampleStatus.ACTIVE,
    )
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name}-{self.storage.name}"


class File(BaseModelWithUID):
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    file_id = models.CharField(max_length=255)
    created_by = models.ForeignKey("core.User", on_delete=models.CASCADE)
    company = models.ForeignKey("organizations.Company", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    comments = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name}-{self.storage.name}"


class Image(BaseModelWithUID):
    company = models.ForeignKey("organizations.Company", on_delete=models.CASCADE)
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


class Note(BaseModelWithUID):
    company = models.ForeignKey("organizations.Company", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=500)
    created_by = models.ForeignKey("core.User", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.title}-{self.status}"


class SampleImage(BaseModelWithUID):
    company = models.ForeignKey("organizations.Company", on_delete=models.CASCADE)
    sample = models.ForeignKey(GarmentSample, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        unique_together = ("sample", "image")

    def __str__(self):
        return f"{self.sample.name}-{self.image.file_name}"


class ProjectImage(BaseModelWithUID):
    company = models.ForeignKey("organizations.Company", on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        unique_together = ("project", "image")

    def __str__(self):
        return f"{self.project.name}-{self.image.file_name}"


class FileImage(BaseModelWithUID):
    company = models.ForeignKey("organizations.Company", on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        unique_together = ("file", "image")

    def __str__(self):
        return f"{self.file.name}-{self.image.file_name}"


class SampleNote(BaseModelWithUID):
    company = models.ForeignKey("organizations.Company", on_delete=models.CASCADE)
    sample = models.ForeignKey(GarmentSample, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        unique_together = ("sample", "note")

    def __str__(self):
        return f"{self.sample.name}-{self.note.title}"


class FileNote(BaseModelWithUID):
    company = models.ForeignKey("organizations.Company", on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        unique_together = ("file", "note")

    def __str__(self):
        return f"{self.file.name}-{self.note.title}"


class Buyer(BaseModelWithUID):
    created_by = models.ForeignKey("core.User", on_delete=models.CASCADE)
    company = models.ForeignKey("organizations.Company", on_delete=models.CASCADE)
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
    company = models.ForeignKey("organizations.Company", on_delete=models.CASCADE)
    sample = models.ForeignKey(GarmentSample, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    history = HistoricalRecords()

    class Meta:
        unique_together = ("sample", "buyer")

    def __str__(self):
        return f"{self.sample.name}-{self.buyer.name}"


class ProjectBuyerConnection(BaseModelWithUID):
    company = models.ForeignKey("organizations.Company", on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    history = HistoricalRecords()

    class Meta:
        unique_together = ("project", "buyer")

    def __str__(self):
        return f"{self.project.name}-{self.buyer.name}"


class FileBuyerConnection(BaseModelWithUID):
    company = models.ForeignKey("organizations.Company", on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    history = HistoricalRecords()

    class Meta:
        unique_together = ("file", "buyer")

    def __str__(self):
        return f"{self.file.name}-{self.buyer.name}"


class ProjectSample(BaseModelWithUID):
    company = models.ForeignKey("organizations.Company", on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sample = models.ForeignKey(GarmentSample, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    history = HistoricalRecords()

    class Meta:
        unique_together = ("project", "sample")

    def __str__(self):
        return f"{self.project.name}-{self.sample.name}"


class ProjectFile(BaseModelWithUID):
    company = models.ForeignKey("organizations.Company", on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    history = HistoricalRecords()

    class Meta:
        unique_together = ("project", "file")

    def __str__(self):
        return f"{self.project.name}-{self.file.name}"


class ModifyRequest(BaseModelWithUID):
    requested_user = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, related_name="requests"
    )
    responded_user = models.ForeignKey(
        "core.User", on_delete=models.SET_NULL, null=True, blank=True
    )
    company = models.ForeignKey("organizations.Company", on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    sample = models.ForeignKey(
        GarmentSample, on_delete=models.CASCADE, null=True, blank=True
    )
    file = models.ForeignKey(File, on_delete=models.CASCADE, null=True, blank=True)
    requested_from = models.CharField(max_length=20, choices=StorageType.choices)
    requested_action = models.CharField(max_length=20, choices=ActionTypes.choices)
    status = models.CharField(
        max_length=20,
        choices=ModifyRequestStatus.choices,
        default=ModifyRequestStatus.PENDING,
    )
    requested_data = models.JSONField()

    def __str__(self):
        return f"{self.requested_user.first_name}-{self.requested_from}-{self.status}"
