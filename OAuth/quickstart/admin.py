from django.contrib import admin

# Register your models here.
from . import models

myModels = [models.Student, models.Course, models.Group,
            models.StudentGroup, models.FAQ, models.Task, models.Ticket, models.Thread,models.User,models.FAQCategory,models.TicketCategory]
admin.site.register(myModels)

