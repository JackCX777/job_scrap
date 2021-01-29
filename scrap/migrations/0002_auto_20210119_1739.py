# Generated by Django 3.1.4 on 2021-01-19 17:39

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import scrap.models


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateField(auto_now=True)),
                ('data', jsonfield.fields.JSONField(default=dict)),
            ],
        ),
        migrations.AlterModelOptions(
            name='vacancy',
            options={'ordering': ['-timestamp'], 'verbose_name': 'Вакансия', 'verbose_name_plural': 'Вакансии'},
        ),
        migrations.AddField(
            model_name='vacancy',
            name='conditions',
            field=models.CharField(default=0, max_length=250, verbose_name='Условия'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_data', jsonfield.fields.JSONField(default=scrap.models.default_urls)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrap.city', verbose_name='Город')),
                ('programming_language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrap.programminglanguage', verbose_name='Язык программирования')),
            ],
            options={
                'unique_together': {('city', 'programming_language')},
            },
        ),
    ]