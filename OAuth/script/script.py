import sys, os
import django
sys.path.append(os.path.abspath(".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OAuth.settings")
django.setup()
from quickstart.models import Student, Course, Group, StudentGroup
import pandas as pd 


Student.objects.all().delete()
Course.objects.all().delete()
Group.objects.all().delete()
StudentGroup.objects.all().delete()

# test= pd.read_excel('../class_attendance_tut.xls',header=None)
# course_code=test.iloc[2][0].split()[1]
# print(course_code)
# class_type=test.iloc[3][0].split()[2]
# print(class_type)
# [current_course, created]=Course.objects.get_or_create(code=course_code,name=course_code)

# i=0
# tempgroup=''
# while(i<len(test)):
#     if(isinstance(test.iloc[i][0], str) and test.iloc[i][0].startswith('Class Group:')):
#         [tempgroup,created]=Group.objects.get_or_create(code=test.iloc[i][0].split()[2],type=class_type,course_code=current_course)
#     if(isinstance(test.iloc[i][0], str) and test.iloc[i][0].startswith('No.')):
#         i+=1
#         while(i<len(test) and not pd.isna(test.iloc[i][0])):
#             value=test.iloc[i]
#             student_type='Exchange'
#             program_year=None
            
#             if('Exchange' not in value[2]):
#                 program_year=value[2].split()[0]
#                 student_type=value[2].split()[1]
#             [student, created]=Student.objects.get_or_create(
#                 VMS=value[5],
#                 name=value[1],
#                 program_year=program_year,
#                 student_type=student_type,
#                 course_type=value[3],
#                 nationality=value[4]
#                 )
#             StudentGroup.objects.get_or_create(
#                 group=tempgroup,
#                 student=student
#             )
#             i+=1
#     i+=1