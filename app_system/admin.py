from django.contrib import admin

# Register your models here.
from app_system.models import Tbl_FieldTask_Purpose_Master, Tbl_Tasks

admin.site.register(Tbl_FieldTask_Purpose_Master)
admin.site.register(Tbl_Tasks)
