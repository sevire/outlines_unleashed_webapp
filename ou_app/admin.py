from django.contrib import admin

from ou_app.models import TransformationInstance, DescriptorCategory, DataNodeDescriptor

admin.site.register(TransformationInstance)
admin.site.register(DescriptorCategory)
admin.site.register(DataNodeDescriptor)