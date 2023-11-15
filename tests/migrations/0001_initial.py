# Generated by Django 3.2 on 2023-11-15 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomInline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Test Customized Inline',
            },
        ),
        migrations.CreateModel(
            name='CustomWidget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Image')),
            ],
            options={
                'verbose_name': 'Test Custom Widget',
            },
        ),
        migrations.CreateModel(
            name='Inline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Test With Inline',
            },
        ),
        migrations.CreateModel(
            name='TestNonRequired',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Image')),
            ],
            options={
                'verbose_name': 'Test Non Required',
            },
        ),
        migrations.CreateModel(
            name='TestNonRequiredInline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Test Non Required Inline',
            },
        ),
        migrations.CreateModel(
            name='TestNonRequiredTabularInline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Test Non Required Tabular Inline',
            },
        ),
        migrations.CreateModel(
            name='TestRequired',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Image')),
            ],
            options={
                'verbose_name': 'Test Required',
            },
        ),
        migrations.CreateModel(
            name='TestRequiredInline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Test Required Inline',
            },
        ),
        migrations.CreateModel(
            name='TestRequiredTabularInline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Test Non Required Tabular Inline',
            },
        ),
        migrations.CreateModel(
            name='TestRequiredTabularInlineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Image')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.testrequiredtabularinline')),
            ],
        ),
        migrations.CreateModel(
            name='TestRequiredInlineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Image')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.testrequiredinline')),
            ],
        ),
        migrations.CreateModel(
            name='TestNonRequiredTabularInlineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Image')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.testnonrequiredtabularinline')),
            ],
        ),
        migrations.CreateModel(
            name='TestNonRequiredInlineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Image')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.testnonrequiredinline')),
            ],
        ),
        migrations.CreateModel(
            name='InlineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Image')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='tests.inline')),
            ],
        ),
        migrations.CreateModel(
            name='CustomInlineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Image')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='tests.custominline')),
            ],
        ),
    ]
