# Generated by Django 4.1.7 on 2023-05-05 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ADAUGDB', '0002_btgradepoints'),
        ('BTco_ordinator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BTGradesThreshold',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Threshold_Mark', models.FloatField()),
                ('Section', models.CharField(default='NA', max_length=2)),
                ('Exam_Mode', models.BooleanField()),
                ('Grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ADAUGDB.btgradepoints')),
                ('RegEventId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ADAUGDB.btregistrationstatus')),
                ('Subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BTco_ordinator.btsubjects')),
            ],
            options={
                'db_table': 'BTGradesThreshold',
                'managed': True,
                'unique_together': {('Grade', 'Subject', 'RegEventId', 'Section', 'Exam_Mode')},
            },
        ),
    ]
