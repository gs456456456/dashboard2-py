from django.contrib import admin
from .models import line,Profile
# Register your models here.
class lineAdmin(admin.ModelAdmin):
    list_display = ['num','line']

class lineInline(admin.StackedInline):
    model = line



class AAdmin(admin.ModelAdmin):
    inlines = [lineInline, ]

admin.site.register(line)
admin.site.register(Profile)

# Register your models here.
