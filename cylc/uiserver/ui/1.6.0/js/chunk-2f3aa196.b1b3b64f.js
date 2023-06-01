(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2f3aa196"],{"1b43":function(e,n,t){"use strict";t.r(n);var a=function(){var e=this,n=e.$createElement,t=e._self._c||n;return t("div",{staticClass:"c-simple-tree"},e._l(e.workflows,(function(n){return t("ul",{key:n.id},[t("li",[t("b",[e._v(e._s(n.id))]),e._l(n.children,(function(n){return t("ul",{key:n.id},[t("li",[t("span",{staticClass:"name"},[e._v(e._s(n.name))]),t("span",{staticClass:"state"},[e._v(e._s(n.node.state))]),e._l(n.children,(function(n){return t("ul",{key:n.id},[t("li",[t("span",{staticClass:"name"},[e._v(e._s(n.name))]),t("span",{staticClass:"state"},[e._v(e._s(n.node.state))]),e._l(n.children,(function(n){return t("ul",{key:n.id},[t("li",[t("span",{staticClass:"name"},[e._v(e._s(n.name))]),t("span",{staticClass:"state"},[e._v(e._s(n.node.state))]),e._l(n.children,(function(n){return t("ul",{key:n.id},[t("li",[t("span",{staticClass:"name"},[e._v(e._s(n.name))]),t("span",{staticClass:"state"},[e._v(e._s(n.node.state))])])])}))],2)])}))],2)])}))],2)])}))],2)])})),0)},l=[],s=t("5184"),o=t("2f62"),i=t("1b62"),r=t("a254"),c=t("5982"),u=t("020d"),d=t("94ed");let m,f=e=>e;function w(){var e="/home/runner/work/cylc-ui/cylc-ui/src/views/SimpleTree.vue",n="6136fd14641ce710b4c694abec6ab2071fc9978d",t=new Function("return this")(),a="__coverage__",l={path:"/home/runner/work/cylc-ui/cylc-ui/src/views/SimpleTree.vue",statementMap:{0:{start:{line:119,column:14},end:{line:176,column:1}},1:{start:{line:191,column:4},end:{line:193,column:5}},2:{start:{line:198,column:4},end:{line:203,column:5}},3:{start:{line:218,column:6},end:{line:218,column:30}},4:{start:{line:225,column:6},end:{line:225,column:56}},5:{start:{line:232,column:6},end:{line:232,column:73}}},fnMap:{0:{name:"(anonymous_0)",decl:{start:{line:190,column:2},end:{line:190,column:3}},loc:{start:{line:190,column:14},end:{line:194,column:3}},line:190},1:{name:"(anonymous_1)",decl:{start:{line:197,column:2},end:{line:197,column:3}},loc:{start:{line:197,column:10},end:{line:204,column:3}},line:197},2:{name:"(anonymous_2)",decl:{start:{line:217,column:4},end:{line:217,column:5}},loc:{start:{line:217,column:19},end:{line:219,column:5}},line:217},3:{name:"(anonymous_3)",decl:{start:{line:222,column:4},end:{line:222,column:5}},loc:{start:{line:222,column:17},end:{line:226,column:5}},line:222},4:{name:"(anonymous_4)",decl:{start:{line:231,column:4},end:{line:231,column:5}},loc:{start:{line:231,column:13},end:{line:233,column:5}},line:231}},branchMap:{},s:{0:0,1:0,2:0,3:0,4:0,5:0},f:{0:0,1:0,2:0,3:0,4:0},b:{},_coverageSchema:"1a1c01bbd47fc00a2c39e90264f33305004495a9",hash:"6136fd14641ce710b4c694abec6ab2071fc9978d"},s=t[a]||(t[a]={});s[e]&&s[e].hash===n||(s[e]=l);var o=s[e];return w=function(){return o},o}w();const p=(w().s[0]++,Object(s["a"])(m||(m=f`
subscription SimpleTreeSubscription ($workflowId: ID) {
  deltas(workflows: [$workflowId]) {
    ...Deltas
  }
}

fragment Deltas on Deltas {
  added {
    ...AddedDelta
  }
  updated (stripNull: true) {
    ...UpdatedDelta
  }
  pruned {
    ...PrunedDelta
  }
}

fragment AddedDelta on Added {
  taskProxies {
    ...TaskProxyData
  }
  jobs {
    ...JobData
  }
}

fragment UpdatedDelta on Updated {
  taskProxies {
    ...TaskProxyData
  }
  jobs {
    ...JobData
  }
}

# We must list all of the types we request data for here to enable automatic
# hosekeeping.
fragment PrunedDelta on Pruned {
  workflow
  taskProxies
  jobs
}

# We must always request the "id" for ALL types.
# The only field this view requires beyond that is the status.
fragment TaskProxyData on TaskProxy {
  id
  state
}

# Same for jobs.
fragment JobData on Job {
  id
  state
}
`)));var _={mixins:[i["a"],r["a"],c["a"]],name:"SimpleTree",metaInfo(){return w().f[0]++,w().s[1]++,{title:this.getPageTitle("App.workflow",{name:this.workflowName})}},data(){return w().f[1]++,w().s[2]++,{widget:{title:"simple tree",icon:d["fb"]}}},computed:{...Object(o["e"])("workflows",["cylcTree"]),...Object(o["c"])("workflows",["getNodes"]),workflowIDs(){return w().f[2]++,w().s[3]++,[this.workflowId]},workflows(){return w().f[3]++,w().s[4]++,this.getNodes("workflow",this.workflowIDs)},query(){return w().f[4]++,w().s[5]++,new u["a"](p,this.variables,"workflow",[])}}},b=_,k=(t("c788"),t("2877")),h=Object(k["a"])(b,a,l,!1,null,null,null);n["default"]=h.exports},c788:function(e,n,t){"use strict";t("e09e")},e09e:function(e,n,t){}}]);