from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Student)
admin.site.register(models.Teacher)
admin.site.register(models.Test_Questions)
admin.site.register(models.Paper)
admin.site.register(models.Score)
admin.site.register(models.Class)
