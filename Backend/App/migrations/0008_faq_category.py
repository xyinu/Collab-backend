# Generated by Django 4.2.3 on 2024-01-12 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0007_faqcategory_ticketcategory_alter_studentgroup_group_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='category',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]