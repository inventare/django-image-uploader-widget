# Generated by Django 5.0.3 on 2024-03-21 00:52

import django.db.models.deletion
import image_uploader_widget.postgres.fields
from django.db import migrations, models


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
            name='OrderedInline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Test With Ordered Inline',
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
            name='TestWithArrayField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', image_uploader_widget.postgres.fields.ImageListField(base_field=models.ImageField(max_length=150, upload_to='admin_test'), blank=True, max_length=None, null=True, size=None, upload_to='admin_test')),
            ],
            options={
                'verbose_name': 'Test With Array Field',
            },
        ),
        migrations.CreateModel(
            name='CustomInlineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Image')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='tests.custominline')),
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
            name='OrderedInlineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Image')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='Order')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='tests.orderedinline')),
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
            name='TestNonRequiredTabularInlineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Image')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.testnonrequiredtabularinline')),
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
            name='TestRequiredTabularInlineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Image')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.testrequiredtabularinline')),
            ],
        ),
    ]
