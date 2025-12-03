from django.contrib import admin

from .models import (
    Buyer,
    File,
    FileBuyerConnection,
    FileImage,
    FileNote,
    GarmentSample,
    Image,
    ModifyRequest,
    Project,
    ProjectBuyerConnection,
    ProjectFile,
    ProjectImage,
    ProjectSample,
    SampleBuyerConnection,
    SampleImage,
    SampleNote,
    Storage,
)

admin.site.register(Storage)
admin.site.register(GarmentSample)
admin.site.register(File)
admin.site.register(Buyer)
admin.site.register(SampleBuyerConnection)
admin.site.register(Image)
admin.site.register(Project)
admin.site.register(ProjectBuyerConnection)
admin.site.register(FileBuyerConnection)
admin.site.register(ProjectSample)
admin.site.register(ProjectFile)
admin.site.register(ProjectImage)
admin.site.register(SampleImage)
admin.site.register(FileImage)
admin.site.register(SampleNote)
admin.site.register(FileNote)
admin.site.register(ModifyRequest)
