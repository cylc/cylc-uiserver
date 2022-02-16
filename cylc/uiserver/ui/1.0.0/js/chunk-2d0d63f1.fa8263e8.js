(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d0d63f1"],{7277:function(t,e,n){"use strict";n.r(e);var l=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("v-container",{staticClass:"c-dashboard mt-4",attrs:{fluid:"","grid-list":""}},[n("v-layout",{attrs:{wrap:""}},[n("v-flex",{attrs:{xs12:"",md6:"",lg6:""}},[n("p",{staticClass:"display-1"},[t._v("Workflows")]),n("v-data-table",{attrs:{headers:t.workflowsHeader,items:t.workflowsTable,loading:t.isLoading,"hide-default-footer":"","hide-default-header":"",id:"dashboard-workflows"},scopedSlots:t._u([{key:"item.count",fn:function(e){var l=e.item;return[n("v-skeleton-loader",{attrs:{loading:t.isLoading,"max-width":50,type:"table-cell",tile:""}},[n("span",{staticClass:"headline font-weight-light"},[t._v(t._s(l.count))])])]}},{key:"item.text",fn:function(e){var l=e.item;return[n("span",{staticClass:"title font-weight-light"},[t._v(t._s(l.text))])]}}])},[n("v-progress-linear",{attrs:{slot:"progress",color:"grey",indeterminate:""},slot:"progress"})],1)],1),n("v-flex",{attrs:{xs12:"",md6:"",lg6:""}},[n("p",{staticClass:"display-1"},[t._v("Events")]),n("v-data-table",{attrs:{headers:t.eventsHeader,items:t.events,"hide-default-footer":"","hide-default-header":""},scopedSlots:t._u([{key:"item.id",fn:function(e){var l=e.item;return[n("span",{staticClass:"title font-weight-light"},[t._v(t._s(l.id))])]}},{key:"item.text",fn:function(e){var l=e.item;return[n("span",{staticClass:"title font-weight-light"},[t._v(t._s(l.text))])]}},{key:"no-data",fn:function(){return[n("td",{staticClass:"title"},[t._v("No events")])]},proxy:!0}])})],1)],1),n("v-divider"),n("v-layout",{attrs:{wrap:""}},[n("v-flex",{attrs:{xs12:"",md6:"",lg6:""}},[n("v-list",{attrs:{"three-line":""}},[n("v-list-item",{attrs:{to:"/workflows"}},[n("v-list-item-avatar",{staticStyle:{"font-size":"2em"},attrs:{size:"60"}},[n("v-icon",{attrs:{large:""}},[t._v(t._s(t.svgPaths.table))])],1),n("v-list-item-content",[n("v-list-item-title",{staticClass:"title font-weight-light"},[t._v(" Workflows Table ")]),n("v-list-item-subtitle",[t._v(" View name, host, port, etc. of your workflows ")])],1)],1),n("v-list-item",{attrs:{to:"/user-profile"}},[n("v-list-item-avatar",{staticStyle:{"font-size":"2em"},attrs:{size:"60"}},[n("v-icon",{attrs:{large:""}},[t._v(t._s(t.svgPaths.settings))])],1),n("v-list-item-content",[n("v-list-item-title",{staticClass:"title font-weight-light"},[t._v(" Settings ")]),n("v-list-item-subtitle",[t._v(" View your Hub permissions, and alter user preferences ")])],1)],1),n("v-list-item",{attrs:{href:t.hubUrl}},[n("v-list-item-avatar",{staticStyle:{"font-size":"2em"},attrs:{size:"60"}},[n("v-icon",{attrs:{large:""}},[t._v(t._s(t.svgPaths.hub))])],1),n("v-list-item-content",[n("v-list-item-title",{staticClass:"title font-weight-light"},[t._v(" Cylc Hub ")]),n("v-list-item-subtitle",[t._v(" Visit the Hub to manage your running UI Servers ")])],1)],1)],1)],1),n("v-flex",{attrs:{xs12:"",md6:"",lg6:""}},[n("v-list",{attrs:{"three-line":""}},[n("v-list-item",{attrs:{href:"#/guide"}},[n("v-list-item-avatar",{staticStyle:{"font-size":"2em"},attrs:{size:"60"}},[n("v-icon",{attrs:{large:""}},[t._v(t._s(t.svgPaths.quickstart))])],1),n("v-list-item-content",[n("v-list-item-title",{staticClass:"title font-weight-light"},[t._v(" Cylc UI Quickstart ")]),n("v-list-item-subtitle",[t._v(" Learn how to use the Cylc UI ")])],1)],1),n("v-list-item",{attrs:{href:"https://cylc.github.io/cylc-doc/latest/html/workflow-design-guide/index.html"}},[n("v-list-item-avatar",{staticStyle:{"font-size":"2em"},attrs:{size:"60"}},[n("v-icon",{attrs:{large:""}},[t._v(t._s(t.svgPaths.workflow))])],1),n("v-list-item-content",[n("v-list-item-title",{staticClass:"title font-weight-light"},[t._v(" Workflow Design Guide ")]),n("v-list-item-subtitle",[t._v(" How to make complex Cylc workflows and Rose suites simpler and easier to maintain ")])],1)],1),n("v-list-item",{attrs:{href:"https://cylc.github.io/cylc-doc/latest/html/index.html"}},[n("v-list-item-avatar",{staticStyle:{"font-size":"2em"},attrs:{size:"60"}},[n("v-icon",{attrs:{large:""}},[t._v(t._s(t.svgPaths.documentation))])],1),n("v-list-item-content",[n("v-list-item-title",{staticClass:"title font-weight-light"},[t._v(" Documentation ")]),n("v-list-item-subtitle",[t._v(" The complete Cylc documentation ")])],1)],1)],1)],1)],1)],1)},i=[],s=n("5530"),a=(n("d81d"),n("07ac"),n("4e827"),n("b0c0"),n("fb6a"),n("2f62")),o=n("94ed"),r=n("1b62"),c=n("ebc4"),u=n("5982"),m=n("700d"),d=n("e2db"),v=n("020d"),f=n("b4d2"),h=n("0306");function b(){var t="/home/runner/work/cylc-ui/cylc-ui/src/views/Dashboard.vue",e="89ed54e148152e8f90485d99fa4445f8bd4587d6",n=new Function("return this")(),l="__coverage__",i={path:"/home/runner/work/cylc-ui/cylc-ui/src/views/Dashboard.vue",statementMap:{0:{start:{line:193,column:4},end:{line:195,column:5}},1:{start:{line:198,column:4},end:{line:241,column:5}},2:{start:{line:246,column:20},end:{line:251,column:14}},3:{start:{line:247,column:25},end:{line:247,column:40}},4:{start:{line:249,column:10},end:{line:249,column:44}},5:{start:{line:250,column:10},end:{line:250,column:20}},6:{start:{line:252,column:6},end:{line:259,column:10}},7:{start:{line:253,column:31},end:{line:253,column:91}},8:{start:{line:255,column:10},end:{line:258,column:11}}},fnMap:{0:{name:"(anonymous_0)",decl:{start:{line:192,column:2},end:{line:192,column:3}},loc:{start:{line:192,column:14},end:{line:196,column:3}},line:192},1:{name:"(anonymous_1)",decl:{start:{line:197,column:2},end:{line:197,column:3}},loc:{start:{line:197,column:10},end:{line:242,column:3}},line:197},2:{name:"(anonymous_2)",decl:{start:{line:245,column:4},end:{line:245,column:5}},loc:{start:{line:245,column:22},end:{line:260,column:5}},line:245},3:{name:"(anonymous_3)",decl:{start:{line:247,column:13},end:{line:247,column:14}},loc:{start:{line:247,column:25},end:{line:247,column:40}},line:247},4:{name:"(anonymous_4)",decl:{start:{line:248,column:16},end:{line:248,column:17}},loc:{start:{line:248,column:32},end:{line:251,column:9}},line:248},5:{name:"(anonymous_5)",decl:{start:{line:253,column:14},end:{line:253,column:15}},loc:{start:{line:253,column:31},end:{line:253,column:91}},line:253},6:{name:"(anonymous_6)",decl:{start:{line:254,column:13},end:{line:254,column:14}},loc:{start:{line:254,column:22},end:{line:259,column:9}},line:254}},branchMap:{0:{loc:{start:{line:249,column:24},end:{line:249,column:39}},type:"binary-expr",locations:[{start:{line:249,column:24},end:{line:249,column:34}},{start:{line:249,column:38},end:{line:249,column:39}}],line:249},1:{loc:{start:{line:257,column:19},end:{line:257,column:41}},type:"binary-expr",locations:[{start:{line:257,column:19},end:{line:257,column:36}},{start:{line:257,column:40},end:{line:257,column:41}}],line:257}},s:{0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0},f:{0:0,1:0,2:0,3:0,4:0,5:0,6:0},b:{0:[0,0],1:[0,0]},_coverageSchema:"1a1c01bbd47fc00a2c39e90264f33305004495a9",hash:"89ed54e148152e8f90485d99fa4445f8bd4587d6"},s=n[l]||(n[l]={});s[t]&&s[t].hash===e||(s[t]=i);var a=s[t];return b=function(){return a},a}b();var g={name:"Dashboard",mixins:[r["a"],u["a"],c["a"]],metaInfo:function(){return b().f[0]++,b().s[0]++,{title:this.getPageTitle("App.dashboard")}},data:function(){return b().f[1]++,b().s[1]++,{query:new v["a"](h["a"],{},"root",[new f["a"]]),workflowsHeader:[{text:"Count",sortable:!1,value:"count"},{text:"Text",sortable:!1,value:"text"}],eventsHeader:[{text:"ID",sortable:!1,value:"id"},{text:"Event",sortable:!1,value:"text"}],events:[],svgPaths:{table:o["Q"],settings:o["k"],hub:o["x"],quickstart:o["c"],workflow:o["e"],documentation:o["d"]},hubUrl:Object(m["a"])("/hub/home",!1,!0)}},computed:Object(s["a"])(Object(s["a"])({},Object(a["e"])("workflows",["workflows"])),{},{workflowsTable:function(){b().f[2]++;var t=(b().s[2]++,Object.values(this.workflows).map((function(t){return b().f[3]++,b().s[3]++,t.status})).reduce((function(t,e){return b().f[4]++,b().s[4]++,t[e]=(b().b[0][0]++,(t[e]||(b().b[0][1]++,0))+1),b().s[5]++,t}),{}));return b().s[6]++,d["a"].enumValues.sort((function(t,e){return b().f[5]++,b().s[7]++,d["b"].get(t)-d["b"].get(e)})).map((function(e){return b().f[6]++,b().s[8]++,{text:e.name.charAt(0).toUpperCase()+e.name.slice(1),count:(b().b[1][0]++,t[e.name]||(b().b[1][1]++,0))}}))}})},w=g,_=n("2877"),p=n("6544"),y=n.n(p),k=n("a523"),x=n("8fea"),C=n("ce7e"),V=n("0e8f"),S=n("132d"),z=n("a722"),L=n("8860"),I=n("da13"),P=n("8270"),D=n("5d23"),H=n("8e36"),T=n("3129"),j=Object(_["a"])(w,l,i,!1,null,null,null);e["default"]=j.exports;y()(j,{VContainer:k["a"],VDataTable:x["a"],VDivider:C["a"],VFlex:V["a"],VIcon:S["a"],VLayout:z["a"],VList:L["a"],VListItem:I["a"],VListItemAvatar:P["a"],VListItemContent:D["b"],VListItemSubtitle:D["c"],VListItemTitle:D["d"],VProgressLinear:H["a"],VSkeletonLoader:T["a"]})}}]);