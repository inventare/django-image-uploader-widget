#!/usr/bin/env python
import os
from setuptools import setup, find_packages

f = open(os.path.join(os.path.dirname(__file__), 'README.md'))
readme = f.read()
f.close()

setup(
    name='django-image-uploader-widget',
    version='0.0.4',
    description='Simple Image Uploader Widget for Django-Admin',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Eduardo Oliveira',
    author_email='eduardo_y05@outlook.com',
    url='https://github.com/EduardoJM/django-image-uploader-widget',
    license='MIT',
    packages=find_packages(
        exclude = ("image_uploader_widget_demo.*", "image_uploader_widget_demo", )
    ),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='django,admin,widget,image,uploader',
)