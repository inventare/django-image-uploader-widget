"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[9585],{3905:(e,t,n)=>{n.d(t,{Zo:()=>c,kt:()=>u});var o=n(7294);function r(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);t&&(o=o.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,o)}return n}function a(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){r(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function s(e,t){if(null==e)return{};var n,o,r=function(e,t){if(null==e)return{};var n,o,r={},i=Object.keys(e);for(o=0;o<i.length;o++)n=i[o],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(o=0;o<i.length;o++)n=i[o],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}var l=o.createContext({}),d=function(e){var t=o.useContext(l),n=t;return e&&(n="function"==typeof e?e(t):a(a({},t),e)),n},c=function(e){var t=d(e.components);return o.createElement(l.Provider,{value:t},e.children)},p={inlineCode:"code",wrapper:function(e){var t=e.children;return o.createElement(o.Fragment,{},t)}},m=o.forwardRef((function(e,t){var n=e.components,r=e.mdxType,i=e.originalType,l=e.parentName,c=s(e,["components","mdxType","originalType","parentName"]),m=d(n),u=r,g=m["".concat(l,".").concat(u)]||m[u]||p[u]||i;return n?o.createElement(g,a(a({ref:t},c),{},{components:n})):o.createElement(g,a({ref:t},c))}));function u(e,t){var n=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var i=n.length,a=new Array(i);a[0]=m;var s={};for(var l in t)hasOwnProperty.call(t,l)&&(s[l]=t[l]);s.originalType=e,s.mdxType="string"==typeof e?e:r,a[1]=s;for(var d=2;d<i;d++)a[d]=n[d];return o.createElement.apply(null,a)}return o.createElement.apply(null,n)}m.displayName="MDXCreateElement"},7483:(e,t,n)=>{n.r(t),n.d(t,{contentTitle:()=>a,default:()=>c,frontMatter:()=>i,metadata:()=>s,toc:()=>l});var o=n(7462),r=(n(7294),n(3905));const i={sidebar_position:2},a="Text And Icons",s={unversionedId:"customization/text-and-icons",id:"customization/text-and-icons",title:"Text And Icons",description:"To customize the image uploader widget or inline you can set some variables (this feature is based on the issue #77). In this page we talk about how to, easy, change the texts and icons on that lib.",source:"@site/docs/customization/text-and-icons.md",sourceDirName:"customization",slug:"/customization/text-and-icons",permalink:"/django-image-uploader-widget/docs/next/customization/text-and-icons",editUrl:"https://github.com/inventare/django-image-uploader-widget/blob/main/docs/docs/customization/text-and-icons.md",tags:[],version:"current",sidebarPosition:2,frontMatter:{sidebar_position:2},sidebar:"tutorialSidebar",previous:{title:"Colors",permalink:"/django-image-uploader-widget/docs/next/customization/colors"},next:{title:"Tests",permalink:"/django-image-uploader-widget/docs/next/development/tests"}},l=[{value:"Widget",id:"widget",children:[],level:2},{value:"Inline Editor",id:"inline-editor",children:[],level:2}],d={toc:l};function c(e){let{components:t,...n}=e;return(0,r.kt)("wrapper",(0,o.Z)({},d,n,{components:t,mdxType:"MDXLayout"}),(0,r.kt)("h1",{id:"text-and-icons"},"Text And Icons"),(0,r.kt)("p",null,"To customize the image uploader widget or inline you can set some variables (this feature is based on the issue ",(0,r.kt)("a",{parentName:"p",href:"https://github.com/inventare/django-image-uploader-widget/issues/77"},"#77"),"). In this page we talk about how to, easy, change the texts and icons on that lib."),(0,r.kt)("h2",{id:"widget"},"Widget"),(0,r.kt)("p",null,"For the widget, to customize the icon and the text we need to set some variables in the ",(0,r.kt)("inlineCode",{parentName:"p"},"ImageUploaderWidget")," constructor, like it:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},'# ...\nclass TestCustomForm(forms.ModelForm):\n    class Meta:\n        model = CustomWidget\n        widgets = {\n            \'image\': ImageUploaderWidget(\n                drop_icon="<svg ...></svg>",\n                drop_text="Custom Drop Text",\n                empty_icon="<svg ...></svg>",\n                empty_text="Custom Empty Marker Text",\n            ),\n        }\n        fields = \'__all__\'\n')),(0,r.kt)("p",null,"In this example, we set all four properties (",(0,r.kt)("inlineCode",{parentName:"p"},"drop_icon"),", ",(0,r.kt)("inlineCode",{parentName:"p"},"drop_text"),", ",(0,r.kt)("inlineCode",{parentName:"p"},"empty_icon")," and ",(0,r.kt)("inlineCode",{parentName:"p"},"empty_text"),") for the widget. In the icons is possible to use the ",(0,r.kt)("inlineCode",{parentName:"p"},"django.shortcuts.render")," (",(0,r.kt)("a",{parentName:"p",href:"https://docs.djangoproject.com/en/4.1/topics/http/shortcuts/#render"},"REF"),") to renderize the icon from an HTML template."),(0,r.kt)("p",null,"Another way for customize it is create an new widget class based on that and use it for your forms:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class MyCustomWidget(ImageUploaderWidget):\n    drop_text = \"\"\n    empty_text = \"\"\n\n    def get_empty_icon(self):\n        return render(...)\n    \n    def get_drop_icon(self):\n        return render(...)\n\nclass TestCustomForm(forms.ModelForm):\n    class Meta:\n        model = CustomWidget\n        widgets = {\n            'image': MyCustomWidget()\n        }\n        fields = '__all__'\n")),(0,r.kt)("h2",{id:"inline-editor"},"Inline Editor"),(0,r.kt)("p",null,"To customize the text and the icons of the inline editor is a little bit faster too. We can set some variables on the ",(0,r.kt)("inlineCode",{parentName:"p"},"InlineAdmin")," of your model, like this:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},'class CustomInlineEditor(ImageUploaderInline):\n    model = models.CustomInlineItem\n    add_image_text = "add_image_text"\n    drop_text = "drop_text"\n    empty_text = "empty_text"\n\n    def get_empty_icon(self):\n        return render(...)\n\n    def get_add_icon(self):\n        return render(...)\n\n    def get_drop_icon(self):\n        return render(...)\n\n@admin.register(models.CustomInline)\nclass CustomInlineAdmin(admin.ModelAdmin):\n    inlines = [CustomInlineEditor]\n')))}c.isMDXComponent=!0}}]);