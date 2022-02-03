from django.contrib import admin
from .models import Dataset, Table, Column

class ColumnInline(admin.StackedInline):
    model = Column
    extra = 0

class DatasetAdmin(admin.ModelAdmin):
    list_display = ['name','id','owner','version','current']
    ordering = ['name','-version']
    filter_horizontal = ('table',)

class TableAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = ['name','id','rows','version']
    ordering = ['name','id','version']
    filter_horizontal = ('dataset',)
    inlines = [
        ColumnInline,
    ]

admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(Column)
