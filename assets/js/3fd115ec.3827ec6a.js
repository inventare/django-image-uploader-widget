"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[4562],{3905:(e,t,n)=>{n.d(t,{Zo:()=>c,kt:()=>m});var o=n(7294);function i(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function r(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);t&&(o=o.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,o)}return n}function s(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?r(Object(n),!0).forEach((function(t){i(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):r(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function a(e,t){if(null==e)return{};var n,o,i=function(e,t){if(null==e)return{};var n,o,i={},r=Object.keys(e);for(o=0;o<r.length;o++)n=r[o],t.indexOf(n)>=0||(i[n]=e[n]);return i}(e,t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);for(o=0;o<r.length;o++)n=r[o],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(i[n]=e[n])}return i}var d=o.createContext({}),l=function(e){var t=o.useContext(d),n=t;return e&&(n="function"==typeof e?e(t):s(s({},t),e)),n},c=function(e){var t=l(e.components);return o.createElement(d.Provider,{value:t},e.children)},p={inlineCode:"code",wrapper:function(e){var t=e.children;return o.createElement(o.Fragment,{},t)}},u=o.forwardRef((function(e,t){var n=e.components,i=e.mdxType,r=e.originalType,d=e.parentName,c=a(e,["components","mdxType","originalType","parentName"]),u=l(n),m=i,h=u["".concat(d,".").concat(m)]||u[m]||p[m]||r;return n?o.createElement(h,s(s({ref:t},c),{},{components:n})):o.createElement(h,s({ref:t},c))}));function m(e,t){var n=arguments,i=t&&t.mdxType;if("string"==typeof e||i){var r=n.length,s=new Array(r);s[0]=u;var a={};for(var d in t)hasOwnProperty.call(t,d)&&(a[d]=t[d]);a.originalType=e,a.mdxType="string"==typeof e?e:i,s[1]=a;for(var l=2;l<r;l++)s[l]=n[l];return o.createElement.apply(null,s)}return o.createElement.apply(null,n)}u.displayName="MDXCreateElement"},6865:(e,t,n)=>{n.r(t),n.d(t,{contentTitle:()=>s,default:()=>c,frontMatter:()=>r,metadata:()=>a,toc:()=>d});var o=n(7462),i=(n(7294),n(3905));const r={sidebar_position:1},s="Tests",a={unversionedId:"development/tests",id:"version-0.4.1/development/tests",title:"Tests",description:"To maintain the integrity of the features of this project we have written some integration tests to grant that main features of the widget and inline admin is really good.",source:"@site/versioned_docs/version-0.4.1/development/tests.md",sourceDirName:"development",slug:"/development/tests",permalink:"/django-image-uploader-widget/docs/development/tests",editUrl:"https://github.com/inventare/django-image-uploader-widget/blob/main/docs/versioned_docs/version-0.4.1/development/tests.md",tags:[],version:"0.4.1",sidebarPosition:1,frontMatter:{sidebar_position:1},sidebar:"tutorialSidebar",previous:{title:"Text And Icons",permalink:"/django-image-uploader-widget/docs/customization/text-and-icons"},next:{title:"ADR 0000: Why jQuery?",permalink:"/django-image-uploader-widget/docs/development/architecture-decision-records/why-jquery"}},d=[{value:"Functional Tests",id:"functional-tests",children:[],level:2},{value:"Some unit tests",id:"some-unit-tests",children:[],level:2},{value:"UI Regression Tests",id:"ui-regression-tests",children:[],level:2},{value:"Some Tests Decisions and Workarounds",id:"some-tests-decisions-and-workarounds",children:[{value:"An test project",id:"an-test-project",children:[],level:3}],level:2},{value:"Test Cases",id:"test-cases",children:[],level:2}],l={toc:d};function c(e){let{components:t,...n}=e;return(0,i.kt)("wrapper",(0,o.Z)({},l,n,{components:t,mdxType:"MDXLayout"}),(0,i.kt)("h1",{id:"tests"},"Tests"),(0,i.kt)("p",null,"To maintain the integrity of the features of this project we have written some integration tests to grant that main features of the widget and inline admin is really good."),(0,i.kt)("h2",{id:"functional-tests"},"Functional Tests"),(0,i.kt)("p",null,"In the decision to write the tests we opted for writing only integration tests using the selenium. And the reason for it is: our project uses much more JavaScript for web browser than Python code for back-end and runs in high coupling with the django-admin. In this context, unit tests are expendable."),(0,i.kt)("h2",{id:"some-unit-tests"},"Some unit tests"),(0,i.kt)("p",null,"In the note block above i talked about not using unit test cases, and in the decisions of the issue ",(0,i.kt)("a",{parentName:"p",href:"https://github.com/inventare/django-image-uploader-widget/issues/77"},"#77")," we decided to add one unit test for the translation of the widget (",(0,i.kt)("a",{parentName:"p",href:"https://github.com/inventare/django-image-uploader-widget/blob/main/tests/widget/functional/tests_functional_widget_custom.py#L5"},"tests/widget/functional/tests_functional_widget_custom.py"),")."),(0,i.kt)("h2",{id:"ui-regression-tests"},"UI Regression Tests"),(0,i.kt)("p",null,"In some versions of django, specially in some django 4.x versions, the style of the widget was broken. The behaviour is described in the issue ",(0,i.kt)("a",{parentName:"p",href:"https://github.com/inventare/django-image-uploader-widget/issues/96#issuecomment-1690740705"},"#96"),". Due this behaviour, we decided to implements some ",(0,i.kt)("strong",{parentName:"p"},"UI Regression Tests")," and make some fixes to solve this problem."),(0,i.kt)("h2",{id:"some-tests-decisions-and-workarounds"},"Some Tests Decisions and Workarounds"),(0,i.kt)("p",null,"When testing with selenium is not possible to hack the file picker to choose some file. And in this project, in some moments we use an ",(0,i.kt)("em",{parentName:"p"},"temporary file input")," for choosing files without compromise the current choosed file. Based on those context, to test correctly fires to onClick event of the ",(0,i.kt)("em",{parentName:"p"},"temporary file input"),", we added an JavaScript to add an onClick event showing an alert and test for this alert into the screen."),(0,i.kt)("h3",{id:"an-test-project"},"An test project"),(0,i.kt)("p",null,"For easy testing, we used the ",(0,i.kt)("strong",{parentName:"p"},"demo")," project ",(0,i.kt)("inlineCode",{parentName:"p"},"image_uploader_widget_demo")," for writing base models for test add the tests for this project instead of the main component project."),(0,i.kt)("h2",{id:"test-cases"},"Test Cases"),(0,i.kt)("p",null,"You can read (or contribute, if you want to improve this project) the test cases inside the ",(0,i.kt)("inlineCode",{parentName:"p"},"/tests")," path inside the github repository ",(0,i.kt)("a",{parentName:"p",href:"https://github.com/inventare/django-image-uploader-widget/tree/main/tests"},"here"),"."))}c.isMDXComponent=!0}}]);