from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create user by email, name, password"""
        
        if not email:
            raise ValueError('User must have an email!')
        user = self.model(email=self.normalize_email(
            email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password):
        """Create superuser by email, name, password"""
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self.db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model"""
    USERNAME_FIELD = 'email'

    email = models.EmailField(unique=True)
    send = models.EmailField(null=True)
    name = models.CharField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    User_Type = (
        ('TA', 'TA'),
        ('Prof', 'Prof'),
    )
    user_type = models.CharField(max_length=40,
                                 choices=User_Type,
                                 default='TA'
                                 )
    created_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    def __str__(self):
        return self.email

    def __repr__(self):
        return f"{self.email!r}, {self.is_staff!r}, {self.is_active!r}, "

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
    name = models.CharField(max_length=255,default='')
    course_code=models.ForeignKey(Course, related_name="course_group",on_delete=models.CASCADE)

    class Meta:
        unique_together = ('code', 'type','course_code')

    def __str__(self):
        return self.code

class TAGroup(models.Model):
    TA = models.ForeignKey(
        User, related_name='group_TA' ,on_delete=models.CASCADE
    )
    group=models.ForeignKey(Group,related_name='group_Ta', on_delete=models.CASCADE)

class StudentGroup(models.Model):
    group=models.ForeignKey(Group,related_name='group_student', on_delete=models.CASCADE)
    student=models.ForeignKey(Student, related_name='student_group',on_delete=models.CASCADE)
    

class Task(models.Model):
    date=models.DateTimeField()
    TA = models.ForeignKey(
        User, related_name='Task_TA' ,on_delete=models.SET_NULL, blank=True, null=True
    )
    prof = models.ForeignKey(
        User, related_name='Task_prof',on_delete=models.SET_NULL, blank=True, null=True
    )
    group=models.ForeignKey(Group,related_name='Task_group',on_delete=models.SET_NULL, blank=True, null=True)
    title=models.CharField(max_length=50)
    details=models.TextField()
    dueDate=models.DateTimeField()
    status=models.CharField(max_length=20)
    url = models.URLField(null=True)
    file_name=models.CharField(max_length=200, blank=True,null=True)

    def __str__(self):
        return self.title

class TaskThread(models.Model):
    date= models.DateTimeField()
    Task= models.ForeignKey(
        Task, related_name='task_thread',on_delete=models.CASCADE
    )
    details=models.TextField()
    by= models.ForeignKey(
        User,on_delete=models.SET_NULL, blank=True, null=True
    )
    url = models.URLField(null=True,blank=True)
    file_name=models.CharField(max_length=200, blank=True,null=True)

class Ticket(models.Model):
    id = models.UUIDField( 
         primary_key = True, 
         default = uuid.uuid4, 
         editable = False) 
    date=models.DateTimeField()
    TA = models.ForeignKey(
        User, related_name='Ticket_TA',on_delete=models.SET_NULL, blank=True, null=True
    )
    prof = models.ForeignKey(
        User,  related_name='Ticket_prof',on_delete=models.SET_NULL, blank=True, null=True
    )
    student = models.ForeignKey(
        Student,  related_name='Ticket_student',on_delete=models.CASCADE, blank=True, null=True
    )
    details=models.TextField()
    group=models.ForeignKey(Group,related_name='Ticket_group',on_delete=models.SET_NULL, blank=True, null=True)
    title=models.CharField(max_length=50)
    status=models.CharField(max_length=80)
    category=models.CharField(max_length=50)
    severity=models.CharField(max_length=20)
    url = models.URLField(null=True)
    file_name=models.CharField(max_length=200, blank=True,null=True)

    def __str__(self):
        return self.title

class Thread(models.Model):
    date= models.DateTimeField()
    Ticket= models.ForeignKey(
        Ticket, related_name='ticket_thread',on_delete=models.CASCADE, blank=True, null=True
    )
    details=models.TextField()
    by= models.ForeignKey(
        User,on_delete=models.SET_NULL, blank=True, null=True
    )
    url = models.URLField(null=True,blank=True)
    file_name=models.CharField(max_length=200, blank=True,null=True)


class FAQ(models.Model):
    title=models.CharField(max_length=50)
    details=models.TextField()
    date= models.DateField(default=timezone.now)
    category=models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title
    
class TicketCategory(models.Model):
    category=models.CharField(max_length=50)

class FAQCategory(models.Model):
    category=models.CharField(max_length=50)