from django.contrib import admin
from mainapp.models import *
# Register your models here.

admin.site.register(Task)
admin.site.register(Status)
admin.site.register(TaskHistry)
admin.site.register(TaskDetail)
admin.site.register(TaskFiles)
admin.site.register(TaskCodes)



admin.site.register(MileStone)
admin.site.register(SubTask)
admin.site.register(SubTaskWork)
admin.site.register(Sprint)
