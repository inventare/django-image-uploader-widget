"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[4863],{3905:(e,t,n)=>{n.d(t,{Zo:()=>p,kt:()=>g});var a=n(7294);function o(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function r(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function i(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?r(Object(n),!0).forEach((function(t){o(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):r(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,a,o=function(e,t){if(null==e)return{};var n,a,o={},r=Object.keys(e);for(a=0;a<r.length;a++)n=r[a],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);for(a=0;a<r.length;a++)n=r[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}var d=a.createContext({}),m=function(e){var t=a.useContext(d),n=t;return e&&(n="function"==typeof e?e(t):i(i({},t),e)),n},p=function(e){var t=m(e.components);return a.createElement(d.Provider,{value:t},e.children)},s={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},c=a.forwardRef((function(e,t){var n=e.components,o=e.mdxType,r=e.originalType,d=e.parentName,p=l(e,["components","mdxType","originalType","parentName"]),c=m(n),g=o,u=c["".concat(d,".").concat(g)]||c[g]||s[g]||r;return n?a.createElement(u,i(i({ref:t},p),{},{components:n})):a.createElement(u,i({ref:t},p))}));function g(e,t){var n=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var r=n.length,i=new Array(r);i[0]=c;var l={};for(var d in t)hasOwnProperty.call(t,d)&&(l[d]=t[d]);l.originalType=e,l.mdxType="string"==typeof e?e:o,i[1]=l;for(var m=2;m<r;m++)i[m]=n[m];return a.createElement.apply(null,i)}return a.createElement.apply(null,n)}c.displayName="MDXCreateElement"},14:(e,t,n)=>{n.r(t),n.d(t,{contentTitle:()=>i,default:()=>p,frontMatter:()=>r,metadata:()=>l,toc:()=>d});var a=n(7462),o=(n(7294),n(3905));const r={sidebar_position:1},i="Tutorial",l={unversionedId:"widget/tutorial",id:"widget/tutorial",title:"Tutorial",description:"First, we need of some context: the image uploader widget is a widget to handle image uploading with a beautiful interface with click to select file and a drop file behaviour handler. It is used with django forms.",source:"@site/docs/widget/tutorial.md",sourceDirName:"widget",slug:"/widget/tutorial",permalink:"/django-image-uploader-widget/docs/next/widget/tutorial",editUrl:"https://github.com/inventare/django-image-uploader-widget/blob/main/docs/docs/widget/tutorial.md",tags:[],version:"current",sidebarPosition:1,frontMatter:{sidebar_position:1},sidebar:"tutorialSidebar",previous:{title:"Introduction",permalink:"/django-image-uploader-widget/docs/next/intro"},next:{title:"Resumed",permalink:"/django-image-uploader-widget/docs/next/widget/resumed"}},d=[{value:"Creating a django project",id:"creating-a-django-project",children:[],level:2},{value:"Installing the widget",id:"installing-the-widget",children:[{value:"Warning",id:"warning",children:[],level:3}],level:2},{value:"Using the widget",id:"using-the-widget",children:[{value:"With ModelForm",id:"with-modelform",children:[{value:"Creating and applying migrations",id:"creating-and-applying-migrations",children:[],level:4},{value:"See it in the action",id:"see-it-in-the-action",children:[],level:4}],level:3},{value:"With Form and custom behaviour",id:"with-form-and-custom-behaviour",children:[],level:3},{value:"Comments about using with django-admin",id:"comments-about-using-with-django-admin",children:[],level:3}],level:2}],m={toc:d};function p(e){let{components:t,...r}=e;return(0,o.kt)("wrapper",(0,a.Z)({},m,r,{components:t,mdxType:"MDXLayout"}),(0,o.kt)("h1",{id:"tutorial"},"Tutorial"),(0,o.kt)("p",null,"First, we need of some context: the image uploader widget is a widget to handle image uploading with a beautiful interface with click to select file and a drop file behaviour handler. It is used with django forms."),(0,o.kt)("p",null,"This is a more long and for newbies tutorial of how to use this widget. If you is an advanced user, see the ",(0,o.kt)("a",{parentName:"p",href:"/django-image-uploader-widget/docs/next/widget/resumed"},"Resumed")," version."),(0,o.kt)("p",null,"To write this tutorial of this documentation we go to create an empty django project, then if you don't want to see this part, skip to ",(0,o.kt)("a",{parentName:"p",href:"#installing-the-widget"},"using the widget section"),". Another information is: we're assuming you already know the basics of ",(0,o.kt)("strong",{parentName:"p"},"django")," and already have it installed in your machine."),(0,o.kt)("h2",{id:"creating-a-django-project"},"Creating a django project"),(0,o.kt)("p",null,"First, create a project folder. Here we call it as ",(0,o.kt)("inlineCode",{parentName:"p"},"my-ecommerce"),":"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"mkdir my-ecommerce\ncd my-ecommerce\n")),(0,o.kt)("p",null,"And, now, create a django project in this folder:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"django-admin startproject core .\n")),(0,o.kt)("p",null,"And, then, we have the folder structure:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre"},"| - my-ecommerce\n  | - core\n    | - asgi.py\n    | - __init__.py\n    | - settings.py\n    | - urls.py\n    | - wsgi.py\n  | - manage.py\n")),(0,o.kt)("p",null,"Create our ",(0,o.kt)("strong",{parentName:"p"},"django")," application by running the command:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre"},"python manage.py startapp ecommerce\n")),(0,o.kt)("p",null,"And, now, we have a new, and more complex, folder structure:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre"},"| - my-ecommerce\n  | - core\n    | - asgi.py\n    | - __init__.py\n    | - settings.py\n    | - urls.py\n    | - wsgi.py\n  | - ecommerce\n    | - migrations\n      | - __init__.py\n    | - admin.py\n    | - apps.py\n    | - __init__.py\n    | - models.py\n    | - tests.py\n    | - views.py\n  | - manage.py\n")),(0,o.kt)("h2",{id:"installing-the-widget"},"Installing the widget"),(0,o.kt)("p",null,"To install the widget, is possible to use the same instructions of the ",(0,o.kt)("a",{parentName:"p",href:"/django-image-uploader-widget/docs/next/intro"},"Introduction"),", and the first step is to install the package with pip:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"pip install django-image-uploader-widget\n")),(0,o.kt)("p",null,"then, add it to the ",(0,o.kt)("inlineCode",{parentName:"p"},"INSTALLED_APPS")," on the ",(0,o.kt)("inlineCode",{parentName:"p"},"settings.py"),", in the case of this example: ",(0,o.kt)("inlineCode",{parentName:"p"},"core/settings.py")," file. To understand better the Applications, see the django documentation: ",(0,o.kt)("a",{parentName:"p",href:"https://docs.djangoproject.com/en/3.2/ref/applications/"},"Applications"),"."),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"# core/settings.py\n# ...\n\nINSTALLED_APPS = [\n    'django.contrib.admin',\n    'django.contrib.auth',\n    'django.contrib.contenttypes',\n    'django.contrib.sessions',\n    'django.contrib.messages',\n    'django.contrib.staticfiles',\n    'image_uploader_widget',\n]\n\n# ...\n")),(0,o.kt)("h3",{id:"warning"},"Warning"),(0,o.kt)("p",null,(0,o.kt)("strong",{parentName:"p"},"Observation"),": note that the application name to be added on the ",(0,o.kt)("inlineCode",{parentName:"p"},"INSTALLED_APPS")," are not equals to the pip package name / install name."),(0,o.kt)("h2",{id:"using-the-widget"},"Using the widget"),(0,o.kt)("p",null,"We have two basic modes to use this widget:"),(0,o.kt)("ol",null,(0,o.kt)("li",{parentName:"ol"},(0,o.kt)("p",{parentName:"li"},"creating a ORM ",(0,o.kt)("inlineCode",{parentName:"p"},"Model")," and using an ",(0,o.kt)("inlineCode",{parentName:"p"},"ModelForm")," to it setting the widget.")),(0,o.kt)("li",{parentName:"ol"},(0,o.kt)("p",{parentName:"li"},"creating an custom ",(0,o.kt)("inlineCode",{parentName:"p"},"Form")," with any other behaviour."))),(0,o.kt)("h3",{id:"with-modelform"},"With ModelForm"),(0,o.kt)("p",null,"First, go to our ecommerce app models ",(0,o.kt)("inlineCode",{parentName:"p"},"ecommerce/models.py")," and create a basic django model with an ",(0,o.kt)("inlineCode",{parentName:"p"},"ImageField"),":"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"# ecommerce/models.py\nfrom django.db import models\n\nclass Product(models.Model):\n    name = models.CharField(max_length=100)\n    image = models.ImageField()\n\n    def __str__(self):\n        return self.name\n    \n    class Meta:\n        verbose_name = 'Product'\n        verbose_name_plural = 'Products'\n")),(0,o.kt)("p",null,"Now, we go to create our ",(0,o.kt)("inlineCode",{parentName:"p"},"ModelForm"),". Create a empty file on ",(0,o.kt)("inlineCode",{parentName:"p"},"ecommerce/forms.py")," to store our django forms. And create our own ",(0,o.kt)("inlineCode",{parentName:"p"},"ProductForm"),":"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"# ecommerce/forms.py\nfrom django.forms import ModelForm\nfrom ecommerce.models import Product\n\nclass ProductForm(ModelForm):\n    class Meta:\n        model = Product\n        fields = ['name', 'image']\n")),(0,o.kt)("p",null,"And, here, we can declare the widget that our ",(0,o.kt)("inlineCode",{parentName:"p"},"image")," field uses:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"# ecommerce/forms.py\nfrom django.forms import ModelForm\nfrom ecommerce.models import Product\nfrom image_uploader_widget.widgets import ImageUploaderWidget\n\nclass ProductForm(ModelForm):\n    class Meta:\n        model = Product\n        fields = ['name', 'image']\n        widgets = {\n            'image': ImageUploaderWidget()\n        }\n")),(0,o.kt)("h4",{id:"creating-and-applying-migrations"},"Creating and applying migrations"),(0,o.kt)("p",null,"Our Model, declared in the above section, needs to be inserted on our database using the ",(0,o.kt)("a",{parentName:"p",href:"https://docs.djangoproject.com/en/3.2/topics/migrations/"},"migrations"),". To create our migrations, we need to add our ",(0,o.kt)("inlineCode",{parentName:"p"},"ecommerce")," app to ",(0,o.kt)("inlineCode",{parentName:"p"},"INSTALLED_APPS")," on the ",(0,o.kt)("inlineCode",{parentName:"p"},"settings.py"),":"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"# core/settings.py\n# ...\n\nINSTALLED_APPS = [\n    'django.contrib.admin',\n    'django.contrib.auth',\n    'django.contrib.contenttypes',\n    'django.contrib.sessions',\n    'django.contrib.messages',\n    'django.contrib.staticfiles',\n    'image_uploader_widget',\n    'ecommerce',\n]\n\n# ...\n")),(0,o.kt)("p",null,"Now, we go to create the migrations using the command:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"python manage.py makemigrations\n")),(0,o.kt)("p",null,"If you found an ",(0,o.kt)("inlineCode",{parentName:"p"},"ecommerce.Product.image: (fields.E210) Cannot use ImageField because Pillow is not installed.")," error, just run an:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"pip install Pillow\n")),(0,o.kt)("p",null,"and re-run the makemigrations command. Now, we go to apply the migrations with:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"python manage.py migrate\n")),(0,o.kt)("p",null,"And, now, we can run the development server to see our next steps coding:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"python manage.py runserver\n")),(0,o.kt)("h4",{id:"see-it-in-the-action"},"See it in the action"),(0,o.kt)("p",null,"To see the widget in action, just go to the ecommerce app and create, in the ",(0,o.kt)("inlineCode",{parentName:"p"},"views.py"),", an view that renders an form:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"# ecommerce/views.py\nfrom django.shortcuts import render\nfrom ecommerce.forms import ProductForm\n\ndef test_widget(request):\n    context = { 'form': ProductForm() }\n    return render(request, 'test_widget.html', context)\n")),(0,o.kt)("p",null,"Now, we can create an ",(0,o.kt)("inlineCode",{parentName:"p"},"templates")," folder in the ",(0,o.kt)("inlineCode",{parentName:"p"},"ecommerce")," application and inside it we need to create a ",(0,o.kt)("inlineCode",{parentName:"p"},"test_widget.html"),":"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-html"},'\x3c!-- ecommerce/templates/test_widget.html --\x3e\n<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta http-equiv="X-UA-Compatible" content="IE=edge">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n    <title>Document</title>\n    {{ form.media }}\n</head>\n<body>\n\n    {{ form.as_p }}\n    \n</body>\n</html>\n')),(0,o.kt)("p",null,"And register this view in the ",(0,o.kt)("inlineCode",{parentName:"p"},"core/urls.py"),":"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"# core/urls.py\nfrom django.contrib import admin\nfrom django.urls import path\nfrom ecommerce.views import test_widget\n\nurlpatterns = [\n    path('admin/', admin.site.urls),\n    path('test_widget/', test_widget),\n]\n")),(0,o.kt)("p",null,"And go to the browser in ",(0,o.kt)("inlineCode",{parentName:"p"},"http://localhost:8000/test_widget/")," and see the result:"),(0,o.kt)("p",null,(0,o.kt)("img",{alt:"Image Uploader Widget",src:n(4811).Z})),(0,o.kt)("h3",{id:"with-form-and-custom-behaviour"},"With Form and custom behaviour"),(0,o.kt)("p",null,"It's very like the above item and we need only to change some things in the ",(0,o.kt)("inlineCode",{parentName:"p"},"forms.py"),":"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"from django import forms\nfrom ecommerce.models import Product\nfrom image_uploader_widget.widgets import ImageUploaderWidget\n\nclass ProductForm(forms.Form):\n    image = forms.ImageField(widget=ImageUploaderWidget())\n\n    class Meta:\n        fields = ['image']\n")),(0,o.kt)("p",null,"And we not need to change nothing more. It works."),(0,o.kt)("h3",{id:"comments-about-using-with-django-admin"},"Comments about using with django-admin"),(0,o.kt)("p",null,"The use with ",(0,o.kt)("strong",{parentName:"p"},"django-admin")," is very like it: we only needs to create ",(0,o.kt)("inlineCode",{parentName:"p"},"ModelForm")," for our models and in the ",(0,o.kt)("inlineCode",{parentName:"p"},"ModelAdmin")," (",(0,o.kt)("a",{parentName:"p",href:"https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin"},"django documentation"),") we set our form (",(0,o.kt)("a",{parentName:"p",href:"https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.form"},"here is an example"),")."))}p.isMDXComponent=!0},4811:(e,t,n)=>{n.d(t,{Z:()=>a});const a=n.p+"assets/images/form_demo-0d860345aab1bf3659448af668000f00.png"}}]);