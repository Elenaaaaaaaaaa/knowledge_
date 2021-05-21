from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Projects)
admin.site.register(Tags)
admin.site.register(Problems)
admin.site.register(Tasks)
admin.site.register(Jobs)
admin.site.register(Information)
admin.site.register(Comments)
admin.site.register(Messages)
admin.site.register(Calendar)
admin.site.register(Documents)

