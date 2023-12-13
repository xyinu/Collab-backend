from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    VMS = models.CharField(max_length=20) 
    name = models.CharField(max_length=255)
    program_year = models.CharField(max_length=15, null=True)
    student_type = models.CharField(max_length=20)
    course_type = models.CharField(max_length=10, null=True)
    nationality = models.CharField(max_length=5)

    def __str__(self):
        return self.VMS

class Course(models.Model):
    code = models.CharField(max_length=20, primary_key=True) 
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.code

class Group(models.Model):
    code = models.CharField(max_length=20) 
    type = models.CharField(max_length=20)
    course_code=models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('code', 'type',)

    def __str__(self):
        return self.code

class StudentGroup(models.Model):
    group=models.ForeignKey(Group, on_delete=models.CASCADE)
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    

class Task(models.Model):
    date=models.DateTimeField()
    TA = models.ForeignKey(
        User, related_name='Task_TA' ,on_delete=models.CASCADE, blank=True, null=True
    )
    prof = models.ForeignKey(
        User, related_name='Task_prof',on_delete=models.CASCADE, blank=True, null=True
    )
    title=models.CharField(max_length=50)
    details=models.TextField()
    dueDate=models.DateTimeField()
    status=models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Ticket(models.Model):
    date=models.DateTimeField()
    TA = models.ForeignKey(
        User, related_name='Ticket_TA',on_delete=models.CASCADE, blank=True, null=True
    )
    prof = models.ForeignKey(
        User,  related_name='Ticket_prof',on_delete=models.CASCADE, blank=True, null=True
    )
    details=models.TextField()
    title=models.CharField(max_length=50)
    status=models.CharField(max_length=20)
    category=models.CharField(max_length=20)
    severity=models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Thread(models.Model):
    date= models.DateTimeField()
    Ticket= models.ForeignKey(
        Ticket, on_delete=models.CASCADE, blank=True, null=True
    )
    details=models.TextField()
    by= models.ForeignKey(
        User,on_delete=models.CASCADE, blank=True, null=True
    )


class FAQ(models.Model):
    title=models.CharField(max_length=50)
    details=models.TextField()

    def __str__(self):
        return self.title
    
class UserAccess(models.Model):
    email=models.CharField(primary_key=True)
    access_type = (
        ('TA', 'TA'),
        ('Prof', 'Prof'),
    )
    access = models.CharField(max_length=40,
                              choices=access_type,
                              default='TA'
                              )

    def __str__(self):
        return self.email