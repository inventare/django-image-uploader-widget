"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[671],{3905:function(e,t,n){n.d(t,{Zo:function(){return u},kt:function(){return g}});var r=n(7294);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function o(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var d=r.createContext({}),s=function(e){var t=r.useContext(d),n=t;return e&&(n="function"==typeof e?e(t):o(o({},t),e)),n},u=function(e){var t=s(e.components);return r.createElement(d.Provider,{value:t},e.children)},c={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},p=r.forwardRef((function(e,t){var n=e.components,a=e.mdxType,i=e.originalType,d=e.parentName,u=l(e,["components","mdxType","originalType","parentName"]),p=s(n),g=a,m=p["".concat(d,".").concat(g)]||p[g]||c[g]||i;return n?r.createElement(m,o(o({ref:t},u),{},{components:n})):r.createElement(m,o({ref:t},u))}));function g(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var i=n.length,o=new Array(i);o[0]=p;var l={};for(var d in t)hasOwnProperty.call(t,d)&&(l[d]=t[d]);l.originalType=e,l.mdxType="string"==typeof e?e:a,o[1]=l;for(var s=2;s<i;s++)o[s]=n[s];return r.createElement.apply(null,o)}return r.createElement.apply(null,n)}p.displayName="MDXCreateElement"},9881:function(e,t,n){n.r(t),n.d(t,{frontMatter:function(){return l},contentTitle:function(){return d},metadata:function(){return s},toc:function(){return u},default:function(){return p}});var r=n(7462),a=n(3366),i=(n(7294),n(3905)),o=["components"],l={sidebar_position:1},d="Introduction",s={unversionedId:"intro",id:"intro",title:"Introduction",description:"The django-image-uploader-widget is a widget to django, specially django-admin to handle better image uploads with a modern and beautiful user interface.",source:"@site/docs/intro.md",sourceDirName:".",slug:"/intro",permalink:"/django-image-uploader-widget/docs/next/intro",editUrl:"https://github.com/inventare/django-image-uploader-widget/blob/main/docs/docs/intro.md",tags:[],version:"current",sidebarPosition:1,frontMatter:{sidebar_position:1},sidebar:"tutorialSidebar",next:{title:"Comming",permalink:"/django-image-uploader-widget/docs/next/widget/comming"}},u=[{value:"Features",id:"features",children:[],level:2},{value:"Getting Started",id:"getting-started",children:[],level:2},{value:"Using",id:"using",children:[],level:2},{value:"Advanced Use Cases",id:"advanced-use-cases",children:[],level:2}],c={toc:u};function p(e){var t=e.components,l=(0,a.Z)(e,o);return(0,i.kt)("wrapper",(0,r.Z)({},c,l,{components:t,mdxType:"MDXLayout"}),(0,i.kt)("h1",{id:"introduction"},"Introduction"),(0,i.kt)("p",null,"The ",(0,i.kt)("strong",{parentName:"p"},"django-image-uploader-widget")," is a widget to ",(0,i.kt)("strong",{parentName:"p"},"django"),", specially ",(0,i.kt)("strong",{parentName:"p"},"django-admin")," to handle better image uploads with a modern and beautiful user interface."),(0,i.kt)("h2",{id:"features"},"Features"),(0,i.kt)("p",null,"Some of the features of this widget is:"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},"Beautiful user interface."),(0,i.kt)("li",{parentName:"ul"},"Handle drop files from your file manager."),(0,i.kt)("li",{parentName:"ul"},"Handle select file by click in the widget or by droping the image (previous item)."),(0,i.kt)("li",{parentName:"ul"},"Inline editor provided to work with multiple images."),(0,i.kt)("li",{parentName:"ul"},"Modal to view the full image (The images are adjusted as cover in the preview box, then, in some cases, that is very useful).")),(0,i.kt)("p",null,(0,i.kt)("img",{alt:"Drag and Drop Image",src:n(7782).Z})),(0,i.kt)("p",null,(0,i.kt)("img",{alt:"Select by click",src:n(4248).Z})),(0,i.kt)("p",null,(0,i.kt)("img",{alt:"Inline handle",src:n(1319).Z})),(0,i.kt)("h2",{id:"getting-started"},"Getting Started"),(0,i.kt)("p",null,"To get started, install this plugin with the pip package manager:"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-sh"},"pip install django-image-uploader-widget\n")),(0,i.kt)("p",null,"then, go to the ",(0,i.kt)("inlineCode",{parentName:"p"},"settings.py")," file and add the ",(0,i.kt)("inlineCode",{parentName:"p"},"image_uploader_widget")," to the installed apps:"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"INSTALLED_APPS = [\n    'my_app.apps.MyAppConfig',\n    'django.contrib.admin',\n    'django.contrib.auth',\n    'django.contrib.contenttypes',\n    'django.contrib.sessions',\n    'django.contrib.messages',\n    'django.contrib.staticfiles',\n    'django.forms',\n    'image_uploader_widget',\n]\n")),(0,i.kt)("h2",{id:"using"},"Using"),(0,i.kt)("p",null,"Now, you must be able to use the widget in your forms:"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"# forms.py\nfrom django import forms\nfrom image_uploader_widget.widgets import ImageUploaderWidget\n\nclass ExampleForm(forms.ModelForm):\n    class Meta:\n        widgets = {\n            'image': ImageUploaderWidget(),\n        }\n        fields = '__all__'\n")),(0,i.kt)("h2",{id:"advanced-use-cases"},"Advanced Use Cases"),(0,i.kt)("p",null,"Better writed widget use cases and more effective examples is comming. Other examples with the inline is comming. For now, check the ",(0,i.kt)("inlineCode",{parentName:"p"},"image_uploader_widget_demo")," folder in the Github ",(0,i.kt)("a",{parentName:"p",href:"https://github.com/inventare/django-image-uploader-widget"},"repository"),"."))}p.isMDXComponent=!0},7782:function(e,t,n){t.Z=n.p+"assets/images/beautiful-c07b6f77d2fbbb6dc35342bd71104a16.gif"},4248:function(e,t,n){t.Z=n.p+"assets/images/click-21c35a5a66e89cb8243fc8d7aa3b9bea.gif"},1319:function(e,t,n){t.Z=n.p+"assets/images/inline_multiple-85388833bbd84e120201fee4d36a1108.gif"}}]);