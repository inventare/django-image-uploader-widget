"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[8099],{3905:(e,t,r)=>{r.d(t,{Zo:()=>p,kt:()=>m});var o=r(7294);function n(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function a(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);t&&(o=o.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,o)}return r}function i(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?a(Object(r),!0).forEach((function(t){n(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):a(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function c(e,t){if(null==e)return{};var r,o,n=function(e,t){if(null==e)return{};var r,o,n={},a=Object.keys(e);for(o=0;o<a.length;o++)r=a[o],t.indexOf(r)>=0||(n[r]=e[r]);return n}(e,t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(o=0;o<a.length;o++)r=a[o],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(n[r]=e[r])}return n}var s=o.createContext({}),l=function(e){var t=o.useContext(s),r=t;return e&&(r="function"==typeof e?e(t):i(i({},t),e)),r},p=function(e){var t=l(e.components);return o.createElement(s.Provider,{value:t},e.children)},d={inlineCode:"code",wrapper:function(e){var t=e.children;return o.createElement(o.Fragment,{},t)}},u=o.forwardRef((function(e,t){var r=e.components,n=e.mdxType,a=e.originalType,s=e.parentName,p=c(e,["components","mdxType","originalType","parentName"]),u=l(r),m=n,g=u["".concat(s,".").concat(m)]||u[m]||d[m]||a;return r?o.createElement(g,i(i({ref:t},p),{},{components:r})):o.createElement(g,i({ref:t},p))}));function m(e,t){var r=arguments,n=t&&t.mdxType;if("string"==typeof e||n){var a=r.length,i=new Array(a);i[0]=u;var c={};for(var s in t)hasOwnProperty.call(t,s)&&(c[s]=t[s]);c.originalType=e,c.mdxType="string"==typeof e?e:n,i[1]=c;for(var l=2;l<a;l++)i[l]=r[l];return o.createElement.apply(null,i)}return o.createElement.apply(null,r)}u.displayName="MDXCreateElement"},2571:(e,t,r)=>{r.r(t),r.d(t,{contentTitle:()=>i,default:()=>p,frontMatter:()=>a,metadata:()=>c,toc:()=>s});var o=r(7462),n=(r(7294),r(3905));const a={sidebar_position:1},i="Colors",c={unversionedId:"customization/colors",id:"customization/colors",title:"Colors",description:"To customize the image uploader widget colors you can use your own css file to override the css variables defined by the image-uploader-inline.css and image-uploader-widget.css. See an example, taken from another personal private project:",source:"@site/docs/customization/colors.md",sourceDirName:"customization",slug:"/customization/colors",permalink:"/django-image-uploader-widget/docs/next/customization/colors",editUrl:"https://github.com/inventare/django-image-uploader-widget/blob/main/docs/docs/customization/colors.md",tags:[],version:"current",sidebarPosition:1,frontMatter:{sidebar_position:1},sidebar:"tutorialSidebar",previous:{title:"Accept Input Attribute",permalink:"/django-image-uploader-widget/docs/next/inline_admin/accept"},next:{title:"Text And Icons",permalink:"/django-image-uploader-widget/docs/next/customization/text-and-icons"}},s=[],l={toc:s};function p(e){let{components:t,...r}=e;return(0,n.kt)("wrapper",(0,o.Z)({},l,r,{components:t,mdxType:"MDXLayout"}),(0,n.kt)("h1",{id:"colors"},"Colors"),(0,n.kt)("p",null,"To customize the image uploader widget colors you can use your own css file to override the css variables defined by the ",(0,n.kt)("inlineCode",{parentName:"p"},"image-uploader-inline.css")," and ",(0,n.kt)("inlineCode",{parentName:"p"},"image-uploader-widget.css"),". See an example, taken from another personal private project:"),(0,n.kt)("pre",null,(0,n.kt)("code",{parentName:"pre",className:"language-scss"},"body {\n    --iuw-background: #{$dashdark} !important;\n    --iuw-border-color: #{$dashborder} !important;\n    --iuw-color: #{$dashgray} !important;\n    --iuw-placeholder-text-color: #{$dashgray} !important;\n    --iuw-dropzone-background: #{$dashlight} !important;\n    --iuw-image-preview-border: #{$dashborder} !important;\n    --iuw-image-preview-shadow: rgba(0, 0, 0, 0.3);\n    --iuw-add-image-background: #{$dashlight} !important;\n    --iuw-add-image-color: #{$dashgray} !important;\n}\n")),(0,n.kt)("p",null,(0,n.kt)("strong",{parentName:"p"},"Observation"),": To see better the variables name, check the css file at the GitHub repository: ",(0,n.kt)("a",{parentName:"p",href:"https://github.com/inventare/django-image-uploader-widget/blob/main/image_uploader_widget/static/admin/css/image-uploader-inline.css"},"here")," or ",(0,n.kt)("a",{parentName:"p",href:"https://github.com/inventare/django-image-uploader-widget/blob/main/image_uploader_widget/static/admin/css/image-uploader-widget.css"},"here"),"."))}p.isMDXComponent=!0}}]);