"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[344],{3905:(e,t,n)=>{n.d(t,{Zo:()=>l,kt:()=>m});var r=n(7294);function i(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function a(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?o(Object(n),!0).forEach((function(t){i(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function d(e,t){if(null==e)return{};var n,r,i=function(e,t){if(null==e)return{};var n,r,i={},o=Object.keys(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||(i[n]=e[n]);return i}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(i[n]=e[n])}return i}var s=r.createContext({}),c=function(e){var t=r.useContext(s),n=t;return e&&(n="function"==typeof e?e(t):a(a({},t),e)),n},l=function(e){var t=c(e.components);return r.createElement(s.Provider,{value:t},e.children)},p={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},u=r.forwardRef((function(e,t){var n=e.components,i=e.mdxType,o=e.originalType,s=e.parentName,l=d(e,["components","mdxType","originalType","parentName"]),u=c(n),m=i,h=u["".concat(s,".").concat(m)]||u[m]||p[m]||o;return n?r.createElement(h,a(a({ref:t},l),{},{components:n})):r.createElement(h,a({ref:t},l))}));function m(e,t){var n=arguments,i=t&&t.mdxType;if("string"==typeof e||i){var o=n.length,a=new Array(o);a[0]=u;var d={};for(var s in t)hasOwnProperty.call(t,s)&&(d[s]=t[s]);d.originalType=e,d.mdxType="string"==typeof e?e:i,a[1]=d;for(var c=2;c<o;c++)a[c]=n[c];return r.createElement.apply(null,a)}return r.createElement.apply(null,n)}u.displayName="MDXCreateElement"},6006:(e,t,n)=>{n.r(t),n.d(t,{contentTitle:()=>a,default:()=>l,frontMatter:()=>o,metadata:()=>d,toc:()=>s});var r=n(7462),i=(n(7294),n(3905));const o={},a="ADR 0000: Why jQuery?",d={unversionedId:"development/architecture-decision-records/why-jquery",id:"version-0.4.1/development/architecture-decision-records/why-jquery",title:"ADR 0000: Why jQuery?",description:"November 2023 . Eduardo Oliveira",source:"@site/versioned_docs/version-0.4.1/development/architecture-decision-records/0000-why-jquery.md",sourceDirName:"development/architecture-decision-records",slug:"/development/architecture-decision-records/why-jquery",permalink:"/django-image-uploader-widget/docs/development/architecture-decision-records/why-jquery",editUrl:"https://github.com/inventare/django-image-uploader-widget/blob/main/docs/versioned_docs/version-0.4.1/development/architecture-decision-records/0000-why-jquery.md",tags:[],version:"0.4.1",sidebarPosition:0,frontMatter:{},sidebar:"tutorialSidebar",previous:{title:"Tests",permalink:"/django-image-uploader-widget/docs/development/tests"},next:{title:"ADR 0001: Why functional tests?",permalink:"/django-image-uploader-widget/docs/development/architecture-decision-records/why-functional-tests"}},s=[{value:"Context",id:"context",children:[],level:2},{value:"Decision Drivers",id:"decision-drivers",children:[],level:2},{value:"Decision",id:"decision",children:[],level:2}],c={toc:s};function l(e){let{components:t,...n}=e;return(0,i.kt)("wrapper",(0,r.Z)({},c,n,{components:t,mdxType:"MDXLayout"}),(0,i.kt)("h1",{id:"adr-0000-why-jquery"},"ADR 0000: Why jQuery?"),(0,i.kt)("p",null,"November 2023 . ",(0,i.kt)("a",{parentName:"p",href:"https://github.com/EduardoJM"},"Eduardo Oliveira")),(0,i.kt)("h2",{id:"context"},"Context"),(0,i.kt)("p",null,"Some of the ",(0,i.kt)("inlineCode",{parentName:"p"},"django-admin")," scripts uses jQuery and we need to decide if we will use jQuery or not."),(0,i.kt)("h2",{id:"decision-drivers"},"Decision Drivers"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},"We need to maintain retrocompatibility with ",(0,i.kt)("inlineCode",{parentName:"li"},"Django 3.2")," and new versions of ",(0,i.kt)("inlineCode",{parentName:"li"},"Django 4.x"),"."),(0,i.kt)("li",{parentName:"ul"},"Our code don't have any dependencies to jQuery.")),(0,i.kt)("h2",{id:"decision"},"Decision"),(0,i.kt)("p",null,"At the ",(0,i.kt)("inlineCode",{parentName:"p"},"Django 3.2")," and ",(0,i.kt)("inlineCode",{parentName:"p"},"Django 4.0")," version, the ",(0,i.kt)("inlineCode",{parentName:"p"},"inlines.js")," script (a script to control the inlines form inside the ",(0,i.kt)("inlineCode",{parentName:"p"},"django-admin"),") dispatch ",(0,i.kt)("inlineCode",{parentName:"p"},"formset:added")," event as jQuery ",(0,i.kt)("inlineCode",{parentName:"p"},"trigger()")," event. This event can't be catched using native event handlers [",(0,i.kt)("a",{parentName:"p",href:"https://github.com/django/django/blob/stable/3.2.x/django/contrib/admin/static/admin/js/inlines.js#L91"},"inlines.js#L91"),"]."),(0,i.kt)("p",null,"At ",(0,i.kt)("inlineCode",{parentName:"p"},"Django 4.1.x")," version, this event dispatch was transformed to use native browser ",(0,i.kt)("inlineCode",{parentName:"p"},"CustomEvent")," [",(0,i.kt)("a",{parentName:"p",href:"https://github.com/django/django/blob/stable/4.1.x/django/contrib/admin/static/admin/js/inlines.js#L91"},"inlines.js#L91"),"]. The other side way is valid: if we dispatched the event using native ",(0,i.kt)("inlineCode",{parentName:"p"},"CustomEvent")," can be catched by the jQuery ",(0,i.kt)("inlineCode",{parentName:"p"},"on()")," method. Then, to maintain compatibility with ",(0,i.kt)("inlineCode",{parentName:"p"},"Django 4.0.x")," and ",(0,i.kt)("inlineCode",{parentName:"p"},"Django 3.2.x"),", we decided to use jQuery at this project with one restriction:"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},"jQuery is used, and your use is alowed only in this case, to start the widget inside inlines formset.")))}l.isMDXComponent=!0}}]);