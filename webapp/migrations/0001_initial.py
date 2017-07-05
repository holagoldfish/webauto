# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('date', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Business_stp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('case_id', models.CharField(max_length=200)),
                ('date', models.DateTimeField(auto_now=True)),
                ('case_nature', models.CharField(max_length=200)),
                ('business', models.ForeignKey(to='webapp.Business')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('browser', models.CharField(max_length=500)),
                ('date', models.DateTimeField(auto_now=True)),
                ('case_nature', models.CharField(max_length=500)),
                ('category', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='case_process',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('desc', models.CharField(max_length=500)),
                ('action', models.CharField(max_length=200)),
                ('value', models.CharField(max_length=200)),
                ('ele_id', models.CharField(max_length=20)),
                ('ele_name', models.CharField(max_length=200)),
                ('case', models.ForeignKey(to='webapp.Case')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DbDiff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uName', models.CharField(max_length=20)),
                ('pWord', models.CharField(max_length=20)),
                ('dbAddress', models.CharField(max_length=200)),
                ('sql', models.CharField(max_length=500)),
                ('key1', models.CharField(max_length=20)),
                ('key2', models.CharField(max_length=20, null=True)),
                ('key3', models.CharField(max_length=20, null=True)),
                ('dbkey1', models.CharField(max_length=20)),
                ('dbkey2', models.CharField(max_length=20, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='element',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('fun', models.CharField(max_length=200)),
                ('values', models.CharField(max_length=500)),
                ('desc', models.CharField(max_length=500)),
                ('page_url', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Execution_detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('case_nature', models.CharField(max_length=500)),
                ('category', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now=True)),
                ('case_id', models.CharField(max_length=200)),
                ('business_id', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InCaseDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key1', models.CharField(max_length=40)),
                ('key2', models.CharField(max_length=40, null=True)),
                ('keyValue', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InCaseList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caseName', models.CharField(unique=True, max_length=200)),
                ('caseType', models.CharField(max_length=10)),
                ('diffType', models.CharField(max_length=10)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('modifyDate', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InterMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MessageObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('objName', models.CharField(max_length=40, null=True)),
                ('key1', models.CharField(max_length=40, null=True)),
                ('key2', models.CharField(max_length=40, null=True)),
                ('key3', models.CharField(max_length=40, null=True)),
                ('type', models.CharField(max_length=40, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Method',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ObjDiff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key1', models.CharField(max_length=40)),
                ('key2', models.CharField(max_length=40, null=True)),
                ('key3', models.CharField(max_length=40, null=True)),
                ('key4', models.CharField(max_length=40, null=True)),
                ('execeptValue', models.CharField(max_length=200)),
                ('caseName', models.ForeignKey(to='webapp.InCaseList')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('pro_user', models.CharField(max_length=200)),
                ('pro_status', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('envName', models.CharField(max_length=200, null=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('userName', models.CharField(max_length=30, null=True)),
                ('passWord', models.CharField(max_length=30, null=True)),
                ('interfaceType', models.CharField(max_length=20, null=True)),
                ('is_used', models.BooleanField(default=False)),
                ('proName', models.ForeignKey(to='webapp.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Test_execution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Test_report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('Execution_id', models.CharField(max_length=20)),
                ('date', models.CharField(max_length=200)),
                ('path', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='messageobject',
            name='proName',
            field=models.ForeignKey(to='webapp.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incaselist',
            name='project',
            field=models.ForeignKey(to='webapp.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incasedetail',
            name='caseName',
            field=models.ForeignKey(to='webapp.InCaseList'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='execution_detail',
            name='perform',
            field=models.ForeignKey(to='webapp.Test_execution'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='element',
            name='project',
            field=models.ForeignKey(to='webapp.Project', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dbdiff',
            name='caseName',
            field=models.ForeignKey(to='webapp.InCaseList'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='case',
            name='project',
            field=models.ForeignKey(to='webapp.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='business',
            name='Project',
            field=models.ForeignKey(to='webapp.Project'),
            preserve_default=True,
        ),
    ]
