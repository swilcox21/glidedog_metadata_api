from django.contrib import admin
from .models import Dataset, Table, Column

# will create a new instance of the selected record with an incremented version to be edited 
def duplicate_dataset(modeladmin, request, queryset):
    for obj in queryset:
        tables = Table.objects.filter(dataset = obj)
        obj.pk = None
        obj.version = obj.version + 1
        obj.save()
        for t in tables:
            columns = Column.objects.filter(table = t)
            t.pk = None
            t.dataset = obj
            t.save()
            for c in columns:
                c.pk = None
                c.table = t
                c.save()
duplicate_dataset.short_description = "Duplicate"

class ColumnInline(admin.StackedInline):
    model = Column
    extra = 0

# class TableInline(admin.TabularInline):
#     model = Table
#     fields = ['id','name','rows','version','deleted']
#     extra = 0
#     show_change_link = True
#     ordering = ['name','-version']

class DatasetAdmin(admin.ModelAdmin):
    list_display = ['name','id','owner','version','deleted']
    ordering = ['name','-version']
    filter_horizontal = ('table',)
    # inlines = [
    #     TableInline,
    # ]
    actions = [duplicate_dataset,]
admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Column)

class TableAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = ['name','id','rows','version']
    ordering = ['name','id','version']
    filter_horizontal = ('dataset',)
    inlines = [
        ColumnInline,
    ]
admin.site.register(Table, TableAdmin)


# def duplicate(data):
