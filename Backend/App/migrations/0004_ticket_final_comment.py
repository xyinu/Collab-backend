# Generated by Django 4.2.3 on 2024-01-05 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0003_alter_faq_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='final_comment',
            field=models.CharField(blank=True, null=True),
        ),
    ]