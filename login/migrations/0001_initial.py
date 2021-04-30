# Generated by Django 3.2 on 2021-04-30 09:42

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('sex', models.CharField(choices=[('secret', '保密'), ('male', '男'), ('female', '女')], default='secret', max_length=32)),
                ('rating', models.IntegerField(default=0)),
                ('c_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'ordering': [django.db.models.expressions.OrderBy(django.db.models.expressions.F('rating'), descending=True, nulls_last=True), django.db.models.expressions.OrderBy(django.db.models.expressions.F('c_time'), descending=True, nulls_last=True)],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('content', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True, max_length=1024, null=True)),
                ('c_time', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.user')),
            ],
            options={
                'verbose_name': '问题',
                'verbose_name_plural': '问题',
                'ordering': [django.db.models.expressions.OrderBy(django.db.models.expressions.F('c_time'), descending=True, nulls_last=True)],
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('content', models.TextField(max_length=1024)),
                ('c_time', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.user')),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.question')),
            ],
            options={
                'verbose_name': '回答',
                'verbose_name_plural': '回答',
                'ordering': [django.db.models.expressions.OrderBy(django.db.models.expressions.F('c_time'), descending=True, nulls_last=True)],
            },
        ),
    ]