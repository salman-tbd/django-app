from django.contrib import admin

# Register your models here.
from app_system.models import Tbl_FieldTask_Purpose_Master, Tbl_Tasks, Tbl_FieldTask, Tbl_TaskTemplate, Tbl_Salman

admin.site.register(Tbl_FieldTask_Purpose_Master)
admin.site.register(Tbl_Tasks)
admin.site.register(Tbl_FieldTask)
admin.site.register(Tbl_TaskTemplate)
admin.site.register(Tbl_Salman)
