(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-481cbb56"],{"1b62":function(e,n,t){"use strict";t("99af");var i=t("12cb");function o(){var e="/home/runner/work/cylc-ui/cylc-ui/src/mixins/index.js",n="00c13a517ad5fe31b7978da6442a2c9ccbbd80ac",t=new Function("return this")(),i="__coverage__",a={path:"/home/runner/work/cylc-ui/cylc-ui/src/mixins/index.js",statementMap:{0:{start:{line:37,column:6},end:{line:37,column:61}}},fnMap:{0:{name:"(anonymous_0)",decl:{start:{line:36,column:18},end:{line:36,column:19}},loc:{start:{line:36,column:46},end:{line:38,column:5}},line:36}},branchMap:{0:{loc:{start:{line:36,column:33},end:{line:36,column:44}},type:"default-arg",locations:[{start:{line:36,column:42},end:{line:36,column:44}}],line:36}},s:{0:0},f:{0:0},b:{0:[0]},_coverageSchema:"1a1c01bbd47fc00a2c39e90264f33305004495a9",hash:"00c13a517ad5fe31b7978da6442a2c9ccbbd80ac"},l=t[i]||(t[i]={});l[e]&&l[e].hash===n||(l[e]=a);var s=l[e];return o=function(){return s},s}o(),n["a"]={methods:{getPageTitle:function(e){var n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:(o().b[0][0]++,{});return o().f[0]++,o().s[0]++,"".concat(i["a"].t("App.name")," | ").concat(i["a"].t(e,n))}}}},"2c64":function(e,n,t){},"3d86":function(e,n,t){},"4a39":function(e,n,t){"use strict";t.r(n);var i=function(){var e=this,n=e.$createElement,t=e._self._c||n;return t("v-container",{staticClass:"c-user-profile"},[t("v-layout",{attrs:{wrap:""}},[t("v-flex",{attrs:{xs12:"",md12:""}},[t("v-alert",{attrs:{icon:e.svgPaths.settings,prominent:"",color:"grey lighten-3"}},[t("h3",{staticClass:"headline"},[e._v(e._s(e.$t("UserProfile.tableHeader")))]),t("p",{staticClass:"body-1"},[e._v(e._s(e.$t("UserProfile.tableSubHeader")))])]),null!==e.user?t("v-form",[t("v-container",{attrs:{"py-0":""}},[t("v-layout",{attrs:{row:"","align-center":"",wrap:""}},[t("v-flex",{attrs:{xs3:""}},[t("span",[e._v(e._s(e.$t("UserProfile.username")))])]),t("v-flex",{attrs:{xs9:""}},[t("v-text-field",{staticClass:"body-1",attrs:{value:e.user.username,disabled:"",id:"profile-username","aria-disabled":"true"}})],1)],1),t("v-layout",{attrs:{row:"","align-center":"",wrap:""}},[t("v-flex",{attrs:{xs3:""}},[t("span",[e._v(e._s(e.$t("UserProfile.administrator")))])]),t("v-flex",{attrs:{xs9:""}},[t("v-checkbox",{staticClass:"body-1",attrs:{disabled:"",id:"profile-admin","aria-disabled":"true"},model:{value:e.user.admin,callback:function(n){e.$set(e.user,"admin",n)},expression:"user.admin"}})],1)],1),t("v-layout",{attrs:{row:"","align-center":"",wrap:""}},[t("v-flex",{attrs:{xs3:""}},[t("span",[e._v(e._s(e.$t("UserProfile.groups")))])]),t("v-flex",{attrs:{xs9:""}},[t("v-select",{staticClass:"body-1",attrs:{items:e.user.groups,attach:"",multiple:"",disabled:"",id:"profile-groups","aria-disabled":"true"},model:{value:e.user.groups,callback:function(n){e.$set(e.user,"groups",n)},expression:"user.groups"}})],1)],1),t("v-layout",{attrs:{row:"","align-center":"",wrap:""}},[t("v-flex",{attrs:{xs3:""}},[t("span",[e._v(e._s(e.$t("UserProfile.created")))])]),t("v-flex",{attrs:{xs9:""}},[t("v-text-field",{staticClass:"body-1",attrs:{value:e.user.created,disabled:"",id:"profile-created","aria-disabled":"true"}})],1)],1),t("v-row",{attrs:{"mt-4":""}},[t("v-flex",{attrs:{xs12:""}},[t("p",{staticClass:"title"},[e._v("Preferences")])])],1),t("v-layout",{attrs:{row:"","align-center":"",wrap:""}},[t("v-flex",{attrs:{xs3:""}},[t("span",[e._v("Font size")])]),t("v-flex",{attrs:{xs9:""}},[t("v-btn",{staticClass:"mr-2",attrs:{depressed:"",id:"font-size-reset-button"},on:{click:function(n){return e.resetFontSize()}}},[e._v(" Reset ")]),t("v-btn",{staticClass:"mx-2",attrs:{depressed:"",id:"font-size-decrease-button"},on:{click:function(n){return e.decreaseFontSize()}}},[t("v-icon",[e._v(e._s(e.svgPaths.decrease))])],1),t("v-btn",{staticClass:"ml-2",attrs:{depressed:"",id:"font-size-increase-button"},on:{click:function(n){return e.increaseFontSize()}}},[t("v-icon",[e._v(e._s(e.svgPaths.increase))])],1)],1)],1),t("v-layout",{attrs:{row:"","align-center":"",wrap:""}},[t("v-flex",{attrs:{xs3:""}},[t("span",[e._v("Colour Theme")])]),t("v-radio-group",{attrs:{column:""},model:{value:e.jobTheme,callback:function(n){e.jobTheme=n},expression:"jobTheme"}},[t("table",{staticClass:"c-job-state-table"},[t("tr",[t("th",[e._v("State")]),e._l(e.jobThemes,(function(n){return t("th",{key:n},[e._v(" "+e._s(n)+" ")])}))],2),t("tr",[t("td"),e._l(e.jobThemes,(function(e){return t("td",{key:e},[t("v-radio",{attrs:{value:e,id:"input-job-theme-"+e}})],1)}))],2),e._l(e.jobStates,(function(n){return t("tr",{key:n},[t("td",[e._v(e._s(n))]),e._l(e.jobThemes,(function(e){return t("td",{key:e,class:["job_theme--"+e,"job_theme_override"]},[t("job",{attrs:{status:n}})],1)}))],2)}))],2)]),t("v-flex",{attrs:{xs9:""}})],1),t("v-layout",{attrs:{row:"","align-center":"",wrap:""}},[t("v-flex",{attrs:{xs3:""}},[t("span",[e._v("Latest cycle point at top")])]),t("v-checkbox",{attrs:{id:"input-cyclepoints-order"},model:{value:e.cyclePointsOrderDesc,callback:function(n){e.cyclePointsOrderDesc=n},expression:"cyclePointsOrderDesc"}})],1)],1)],1):t("v-progress-linear",{attrs:{indeterminate:!0}})],1)],1)],1)},o=[],a=t("f3f3"),l=(t("d81d"),t("b0c0"),t("2f62")),s=t("1b62"),r=t("b20f"),c=t.n(r);function u(){var e="/home/runner/work/cylc-ui/cylc-ui/src/utils/font-size.js",n="2d1c5782fa988d3527e0c1278fb7e73837a103a7",t=new Function("return this")(),i="__coverage__",o={path:"/home/runner/work/cylc-ui/cylc-ui/src/utils/font-size.js",statementMap:{0:{start:{line:25,column:26},end:{line:25,column:45}},1:{start:{line:34,column:2},end:{line:34,column:41}},2:{start:{line:35,column:2},end:{line:35,column:75}},3:{start:{line:42,column:26},end:{line:42,column:51}},4:{start:{line:43,column:22},end:{line:43,column:50}},5:{start:{line:44,column:2},end:{line:44,column:37}},6:{start:{line:45,column:2},end:{line:45,column:71}},7:{start:{line:52,column:26},end:{line:52,column:51}},8:{start:{line:53,column:22},end:{line:53,column:50}},9:{start:{line:54,column:2},end:{line:54,column:37}},10:{start:{line:55,column:2},end:{line:55,column:71}},11:{start:{line:64,column:2},end:{line:66,column:3}},12:{start:{line:65,column:4},end:{line:65,column:44}},13:{start:{line:67,column:15},end:{line:67,column:55}},14:{start:{line:68,column:20},end:{line:68,column:49}},15:{start:{line:69,column:2},end:{line:69,column:39}},16:{start:{line:85,column:16},end:{line:85,column:36}},17:{start:{line:86,column:2},end:{line:86,column:52}}},fnMap:{0:{name:"resetFontSize",decl:{start:{line:33,column:9},end:{line:33,column:22}},loc:{start:{line:33,column:61},end:{line:36,column:1}},line:33},1:{name:"decreaseFontSize",decl:{start:{line:41,column:9},end:{line:41,column:25}},loc:{start:{line:41,column:29},end:{line:46,column:1}},line:41},2:{name:"increaseFontSize",decl:{start:{line:51,column:9},end:{line:51,column:25}},loc:{start:{line:51,column:29},end:{line:56,column:1}},line:51},3:{name:"getCurrentFontSize",decl:{start:{line:63,column:9},end:{line:63,column:27}},loc:{start:{line:63,column:31},end:{line:70,column:1}},line:63},4:{name:"expectedFontSize",decl:{start:{line:84,column:9},end:{line:84,column:25}},loc:{start:{line:84,column:94},end:{line:87,column:1}},line:84}},branchMap:{0:{loc:{start:{line:33,column:24},end:{line:33,column:59}},type:"default-arg",locations:[{start:{line:33,column:42},end:{line:33,column:59}}],line:33},1:{loc:{start:{line:64,column:2},end:{line:66,column:3}},type:"if",locations:[{start:{line:64,column:2},end:{line:66,column:3}},{start:{line:64,column:2},end:{line:66,column:3}}],line:64},2:{loc:{start:{line:84,column:45},end:{line:84,column:92}},type:"default-arg",locations:[{start:{line:84,column:63},end:{line:84,column:92}}],line:84},3:{loc:{start:{line:85,column:16},end:{line:85,column:36}},type:"cond-expr",locations:[{start:{line:85,column:27},end:{line:85,column:30}},{start:{line:85,column:33},end:{line:85,column:36}}],line:85}},s:{0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0},f:{0:0,1:0,2:0,3:0,4:0},b:{0:[0],1:[0,0],2:[0],3:[0,0]},_coverageSchema:"1a1c01bbd47fc00a2c39e90264f33305004495a9",hash:"2d1c5782fa988d3527e0c1278fb7e73837a103a7"},a=t[i]||(t[i]={});a[e]&&a[e].hash===n||(a[e]=o);var l=a[e];return u=function(){return l},l}u();var d=(u().s[0]++,c.a.fontRootSize);function m(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:(u().b[0][0]++,d);u().f[0]++,u().s[1]++,localStorage.fontSize=e,u().s[2]++,document.getElementsByTagName("html")[0].style.fontSize=e}function f(){u().f[1]++;var e=(u().s[3]++,this.getCurrentFontSize()),n=(u().s[4]++,"".concat(.8*e,"px"));u().s[5]++,localStorage.fontSize=n,u().s[6]++,document.getElementsByTagName("html")[0].style.fontSize=n}function h(){u().f[2]++;var e=(u().s[7]++,this.getCurrentFontSize()),n=(u().s[8]++,"".concat(1.2*e,"px"));u().s[9]++,localStorage.fontSize=n,u().s[10]++,document.getElementsByTagName("html")[0].style.fontSize=n}function p(){if(u().f[3]++,u().s[11]++,localStorage.fontSize)return u().b[1][0]++,u().s[12]++,parseFloat(localStorage.fontSize);u().b[1][1]++;var e=(u().s[13]++,document.getElementsByTagName("html")[0]),n=(u().s[14]++,window.getComputedStyle(e));return u().s[15]++,parseFloat(n.fontSize)}var b=t("94ed"),v=t("9070"),g=t("c743"),y=t("adf6"),_=t("ebc4");function S(){var e="/home/runner/work/cylc-ui/cylc-ui/src/views/UserProfile.vue",n="cf74f123072b047cfe465ef5458d55d363d25f4c",t=new Function("return this")(),i="__coverage__",o={path:"/home/runner/work/cylc-ui/cylc-ui/src/views/UserProfile.vue",statementMap:{0:{start:{line:217,column:4},end:{line:231,column:5}},1:{start:{line:224,column:50},end:{line:224,column:60}},2:{start:{line:237,column:4},end:{line:239,column:5}},3:{start:{line:242,column:4},end:{line:244,column:5}},4:{start:{line:243,column:6},end:{line:243,column:79}},5:{start:{line:255,column:6},end:{line:255,column:29}},6:{start:{line:258,column:6},end:{line:258,column:60}},7:{start:{line:259,column:6},end:{line:259,column:42}}},fnMap:{0:{name:"(anonymous_0)",decl:{start:{line:216,column:2},end:{line:216,column:3}},loc:{start:{line:216,column:10},end:{line:232,column:3}},line:216},1:{name:"(anonymous_1)",decl:{start:{line:224,column:41},end:{line:224,column:42}},loc:{start:{line:224,column:50},end:{line:224,column:60}},line:224},2:{name:"(anonymous_2)",decl:{start:{line:236,column:2},end:{line:236,column:3}},loc:{start:{line:236,column:14},end:{line:240,column:3}},line:236},3:{name:"(anonymous_3)",decl:{start:{line:241,column:2},end:{line:241,column:3}},loc:{start:{line:241,column:13},end:{line:245,column:3}},line:241},4:{name:"(anonymous_4)",decl:{start:{line:254,column:14},end:{line:254,column:15}},loc:{start:{line:254,column:31},end:{line:256,column:5}},line:254},5:{name:"(anonymous_5)",decl:{start:{line:257,column:4},end:{line:257,column:5}},loc:{start:{line:257,column:36},end:{line:260,column:5}},line:257}},branchMap:{0:{loc:{start:{line:230,column:16},end:{line:230,column:50}},type:"binary-expr",locations:[{start:{line:230,column:16},end:{line:230,column:37}},{start:{line:230,column:41},end:{line:230,column:50}}],line:230},1:{loc:{start:{line:242,column:4},end:{line:244,column:5}},type:"if",locations:[{start:{line:242,column:4},end:{line:244,column:5}},{start:{line:242,column:4},end:{line:244,column:5}}],line:242}},s:{0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0},f:{0:0,1:0,2:0,3:0,4:0,5:0},b:{0:[0,0],1:[0,0]},_coverageSchema:"1a1c01bbd47fc00a2c39e90264f33305004495a9",hash:"cf74f123072b047cfe465ef5458d55d363d25f4c"},a=t[i]||(t[i]={});a[e]&&a[e].hash===n||(a[e]=o);var l=a[e];return S=function(){return l},l}S();var x={name:"UserProfile",mixins:[s["a"],_["a"]],components:{Job:v["a"]},data:function(){return S().f[0]++,S().s[0]++,{cyclePointsOrderDesc:y["DEFAULT_CYCLE_POINTS_ORDER_DESC"],svgPaths:{settings:b["h"],increase:b["p"],decrease:b["o"]},jobStates:g["a"].enumValues.map((function(e){return S().f[1]++,S().s[1]++,e.name})),jobThemes:["default","greyscale","colour_blind"],jobTheme:(S().b[0][0]++,localStorage.jobTheme||(S().b[0][1]++,"default"))}},computed:Object(a["a"])({},Object(l["e"])("user",["user"])),metaInfo:function(){return S().f[2]++,S().s[2]++,{title:this.getPageTitle("App.userProfile")}},mounted:function(){S().f[3]++,S().s[3]++,localStorage.cyclePointsOrderDesc?(S().b[1][0]++,S().s[4]++,this.cyclePointsOrderDesc=JSON.parse(localStorage.cyclePointsOrderDesc)):S().b[1][1]++},methods:Object(a["a"])({resetFontSize:m,decreaseFontSize:f,increaseFontSize:h,getCurrentFontSize:p},Object(l["d"])("app",["setJobTheme"])),watch:{jobTheme:function(e){S().f[4]++,S().s[5]++,this.setJobTheme(e)},cyclePointsOrderDesc:function(e){S().f[5]++,S().s[6]++,localStorage.setItem("cyclePointsOrderDesc",e),S().s[7]++,this.cyclePointsOrderDesc=e}}},w=x,j=t("2877"),C=t("6544"),O=t.n(C),z=t("0798"),k=t("8336"),F=t("ac7c"),P=t("a523"),$=t("0e8f"),V=t("4bd4"),T=t("132d"),B=t("a722"),I=t("8e36"),E=t("c9e9"),D=(t("2c64"),t("ba87")),R=t("9d26"),G=t("c37a"),L=t("7e2b"),M=t("a9ad"),U=t("4e82"),N=t("5311"),A=t("7560"),J=t("fe09"),H=t("80d2"),K=t("58df"),Y=t("d9f7"),q=["title"],Q=Object(K["a"])(L["a"],M["a"],N["a"],Object(U["a"])("radioGroup"),A["a"]),W=Q.extend().extend({name:"v-radio",inheritAttrs:!1,props:{disabled:Boolean,id:String,label:String,name:String,offIcon:{type:String,default:"$radioOff"},onIcon:{type:String,default:"$radioOn"},readonly:Boolean,value:{default:null}},data:function(){return{isFocused:!1}},computed:{classes:function(){return Object(a["a"])(Object(a["a"])({"v-radio--is-disabled":this.isDisabled,"v-radio--is-focused":this.isFocused},this.themeClasses),this.groupClasses)},computedColor:function(){return J["a"].options.computed.computedColor.call(this)},computedIcon:function(){return this.isActive?this.onIcon:this.offIcon},computedId:function(){return G["a"].options.computed.computedId.call(this)},hasLabel:G["a"].options.computed.hasLabel,hasState:function(){return(this.radioGroup||{}).hasState},isDisabled:function(){return this.disabled||!!this.radioGroup&&this.radioGroup.isDisabled},isReadonly:function(){return this.readonly||!!this.radioGroup&&this.radioGroup.isReadonly},computedName:function(){return this.name||!this.radioGroup?this.name:this.radioGroup.name||"radio-".concat(this.radioGroup._uid)},rippleState:function(){return J["a"].options.computed.rippleState.call(this)},validationState:function(){return(this.radioGroup||{}).validationState||this.computedColor}},methods:{genInput:function(e){return J["a"].options.methods.genInput.call(this,"radio",e)},genLabel:function(){return this.hasLabel?this.$createElement(D["a"],{on:{click:J["b"]},attrs:{for:this.computedId},props:{color:this.validationState,focused:this.hasState}},Object(H["r"])(this,"label")||this.label):null},genRadio:function(){var e=this.attrs$,n=(e.title,Object(E["a"])(e,q));return this.$createElement("div",{staticClass:"v-input--selection-controls__input"},[this.$createElement(R["a"],this.setTextColor(this.validationState,{props:{dense:this.radioGroup&&this.radioGroup.dense}}),this.computedIcon),this.genInput(Object(a["a"])({name:this.computedName,value:this.value},n)),this.genRipple(this.setTextColor(this.rippleState))])},onFocus:function(e){this.isFocused=!0,this.$emit("focus",e)},onBlur:function(e){this.isFocused=!1,this.$emit("blur",e)},onChange:function(){this.isDisabled||this.isReadonly||this.isActive||this.toggle()},onKeydown:function(){}},render:function(e){var n={staticClass:"v-radio",class:this.classes,on:Object(Y["c"])({click:this.onChange},this.listeners$),attrs:{title:this.attrs$.title}};return e("div",n,[this.genRadio(),this.genLabel()])}}),X=(t("a9e3"),t("ec29"),t("3d86"),t("604c")),Z=t("8547"),ee=Object(K["a"])(Z["a"],X["a"],G["a"]),ne=ee.extend({name:"v-radio-group",provide:function(){return{radioGroup:this}},props:{column:{type:Boolean,default:!0},height:{type:[Number,String],default:"auto"},name:String,row:Boolean,value:null},computed:{classes:function(){return Object(a["a"])(Object(a["a"])({},G["a"].options.computed.classes.call(this)),{},{"v-input--selection-controls v-input--radio-group":!0,"v-input--radio-group--column":this.column&&!this.row,"v-input--radio-group--row":this.row})}},methods:{genDefaultSlot:function(){return this.$createElement("div",{staticClass:"v-input--radio-group__input",attrs:{id:this.id,role:"radiogroup","aria-labelledby":this.computedId}},G["a"].options.methods.genDefaultSlot.call(this))},genInputSlot:function(){var e=G["a"].options.methods.genInputSlot.call(this);return delete e.data.on.click,e},genLabel:function(){var e=G["a"].options.methods.genLabel.call(this);return e?(e.data.attrs.id=this.computedId,delete e.data.attrs.for,e.tag="legend",e):null},onClick:X["a"].options.methods.onClick}}),te=t("0fd9"),ie=t("b974"),oe=t("8654"),ae=Object(j["a"])(w,i,o,!1,null,null,null);n["default"]=ae.exports;O()(ae,{VAlert:z["a"],VBtn:k["a"],VCheckbox:F["a"],VContainer:P["a"],VFlex:$["a"],VForm:V["a"],VIcon:T["a"],VLayout:B["a"],VProgressLinear:I["a"],VRadio:W,VRadioGroup:ne,VRow:te["a"],VSelect:ie["a"],VTextField:oe["a"]})},"4bd4":function(e,n,t){"use strict";var i=t("f3f3"),o=(t("caad"),t("2532"),t("07ac"),t("4de4"),t("159b"),t("7db0"),t("58df")),a=t("7e2b"),l=t("3206");n["a"]=Object(o["a"])(a["a"],Object(l["b"])("form")).extend({name:"v-form",provide:function(){return{form:this}},inheritAttrs:!1,props:{disabled:Boolean,lazyValidation:Boolean,readonly:Boolean,value:Boolean},data:function(){return{inputs:[],watchers:[],errorBag:{}}},watch:{errorBag:{handler:function(e){var n=Object.values(e).includes(!0);this.$emit("input",!n)},deep:!0,immediate:!0}},methods:{watchInput:function(e){var n=this,t=function(e){return e.$watch("hasError",(function(t){n.$set(n.errorBag,e._uid,t)}),{immediate:!0})},i={_uid:e._uid,valid:function(){},shouldValidate:function(){}};return this.lazyValidation?i.shouldValidate=e.$watch("shouldValidate",(function(o){o&&(n.errorBag.hasOwnProperty(e._uid)||(i.valid=t(e)))})):i.valid=t(e),i},validate:function(){return 0===this.inputs.filter((function(e){return!e.validate(!0)})).length},reset:function(){this.inputs.forEach((function(e){return e.reset()})),this.resetErrorBag()},resetErrorBag:function(){var e=this;this.lazyValidation&&setTimeout((function(){e.errorBag={}}),0)},resetValidation:function(){this.inputs.forEach((function(e){return e.resetValidation()})),this.resetErrorBag()},register:function(e){this.inputs.push(e),this.watchers.push(this.watchInput(e))},unregister:function(e){var n=this.inputs.find((function(n){return n._uid===e._uid}));if(n){var t=this.watchers.find((function(e){return e._uid===n._uid}));t&&(t.valid(),t.shouldValidate()),this.watchers=this.watchers.filter((function(e){return e._uid!==n._uid})),this.inputs=this.inputs.filter((function(e){return e._uid!==n._uid})),this.$delete(this.errorBag,n._uid)}}},render:function(e){var n=this;return e("form",{staticClass:"v-form",attrs:Object(i["a"])({novalidate:!0},this.attrs$),on:{submit:function(e){return n.$emit("submit",e)}}},this.$slots.default)}})},b20f:function(e,n,t){e.exports={fontRootSize:"16px"}},ebc4:function(e,n,t){"use strict";var i=t("d981");function o(){var e="/home/runner/work/cylc-ui/cylc-ui/src/mixins/subscriptionView.js",n="66ec013f03155a2e098a883987b91415d8deabe4",t=new Function("return this")(),i="__coverage__",a={path:"/home/runner/work/cylc-ui/cylc-ui/src/mixins/subscriptionView.js",statementMap:{0:{start:{line:36,column:4},end:{line:38,column:6}},1:{start:{line:37,column:6},end:{line:37,column:46}},2:{start:{line:41,column:4},end:{line:43,column:6}},3:{start:{line:42,column:6},end:{line:42,column:46}}},fnMap:{0:{name:"(anonymous_0)",decl:{start:{line:35,column:2},end:{line:35,column:3}},loc:{start:{line:35,column:36},end:{line:39,column:3}},line:35},1:{name:"(anonymous_1)",decl:{start:{line:36,column:9},end:{line:36,column:10}},loc:{start:{line:36,column:15},end:{line:38,column:5}},line:36},2:{name:"(anonymous_2)",decl:{start:{line:40,column:2},end:{line:40,column:3}},loc:{start:{line:40,column:37},end:{line:44,column:3}},line:40},3:{name:"(anonymous_3)",decl:{start:{line:41,column:9},end:{line:41,column:10}},loc:{start:{line:41,column:15},end:{line:43,column:5}},line:41}},branchMap:{},s:{0:0,1:0,2:0,3:0},f:{0:0,1:0,2:0,3:0},b:{},_coverageSchema:"1a1c01bbd47fc00a2c39e90264f33305004495a9",hash:"66ec013f03155a2e098a883987b91415d8deabe4"},l=t[i]||(t[i]={});l[e]&&l[e].hash===n||(l[e]=a);var s=l[e];return o=function(){return s},s}o(),n["a"]={mixins:[i["a"]],beforeRouteEnter:function(e,n,t){o().f[0]++,o().s[0]++,t((function(e){o().f[1]++,o().s[1]++,e.$workflowService.startSubscriptions()}))},beforeRouteUpdate:function(e,n,t){o().f[2]++,o().s[2]++,t((function(e){o().f[3]++,o().s[3]++,e.$workflowService.startSubscriptions()}))}}}}]);