import{b9 as B,ba as E,bb as S,x as s,bc as P,az as y,bd as q,be as z,bf as Q,g as i,b8 as O,p as N,bg as W,bh as U,bi as X,bj as Y,bk as K,bl as Z,bm as $,bn as ee,bo as te,bp as ae,bq as se,br as ne,bs as D,B as T,R as L,F as k,_ as G,bt as ie,bu as le,bv as re,bw as oe,bx as de,by as ue,bz as ce,bA as me,bB as fe,ay as pe,A as F,q as m,o as c,w as r,e as V,v as I,bC as h,bD as v,k as p,bE as x,t as f,K as M,r as C,bF as be,bG as ke,bH as ge,bI as he,a6 as ve,ad as xe,bJ as ye,H as Ce,I as _e,ae as H}from"./index-PqzDRcKR.js";import{g as De}from"./graphql-BSOF_UqA.js";import{i as Ie,a as R}from"./initialOptions-4bVsJsyJ.js";import{G as Te}from"./GraphNode-DA0LB_Gz.js";import{f as Ve}from"./datetime-BTQ3cuKI.js";function Pe(e,t){const a=[];let o=0,d="";for(let n of e.split(/(and|or|\(|\))/))if(n=n.trim().replace("_","-"),!!n)if(n==="(")a.push([null,o,`${d}(`]),d="",o=o+1;else if(n===")")o=o-1,a.push([null,o,`${d})`]),d="";else if(n==="and"||n==="or")d=`${n} `;else{for(const b of t)if(b.label===n){a.push([b.satisfied,o,`${d}${n}`]);break}d=""}return a}const we=E({divider:[Number,String],...q()},"VBreadcrumbsDivider"),Me=B()({name:"VBreadcrumbsDivider",props:we(),setup(e,t){let{slots:a}=t;return S(()=>s("li",{"aria-hidden":"true",class:y(["v-breadcrumbs-divider",e.class]),style:P(e.style)},[a?.default?.()??e.divider])),{}}}),Be=E({active:Boolean,activeClass:String,activeColor:String,color:String,disabled:Boolean,title:String,...q(),...Y(K(),["width","maxWidth"]),...X(),...U({tag:"li"})},"VBreadcrumbsItem"),Ee=B()({name:"VBreadcrumbsItem",props:Be(),setup(e,t){let{slots:a,attrs:o}=t;const d=z(e,o),n=N(()=>e.active||d.isActive?.value),{dimensionStyles:b}=W(e),{textColorClasses:l,textColorStyles:u}=Q(()=>n.value?e.activeColor:e.color);return S(()=>i(e.tag,{class:y(["v-breadcrumbs-item",{"v-breadcrumbs-item--active":n.value,"v-breadcrumbs-item--disabled":e.disabled,[`${e.activeClass}`]:n.value&&e.activeClass},l.value,e.class]),style:P([u.value,b.value,e.style]),"aria-current":n.value?"page":void 0},{default:()=>[d.isLink.value?s("a",O({class:"v-breadcrumbs-item--link",onClick:d.navigate},d.linkProps),[a.default?.()??e.title]):a.default?.()??e.title]})),{}}}),Se=E({activeClass:String,activeColor:String,bgColor:String,color:String,disabled:Boolean,divider:{type:String,default:"/"},icon:ne,items:{type:Array,default:()=>[]},...q(),...se(),...ae(),...U({tag:"ul"})},"VBreadcrumbs"),qe=B()({name:"VBreadcrumbs",props:Se(),setup(e,t){let{slots:a}=t;const{backgroundColorClasses:o,backgroundColorStyles:d}=Z(()=>e.bgColor),{densityClasses:n}=$(e),{roundedClasses:b}=ee(e);te({VBreadcrumbsDivider:{divider:D(()=>e.divider)},VBreadcrumbsItem:{activeClass:D(()=>e.activeClass),activeColor:D(()=>e.activeColor),color:D(()=>e.color),disabled:D(()=>e.disabled)}});const l=N(()=>e.items.map(u=>typeof u=="string"?{item:{title:u},raw:u}:{item:u,raw:u}));return S(()=>{const u=!!(a.prepend||e.icon);return i(e.tag,{class:y(["v-breadcrumbs",o.value,n.value,b.value,e.class]),style:P([d.value,e.style])},{default:()=>[u&&s("li",{key:"prepend",class:"v-breadcrumbs__prepend"},[a.prepend?i(L,{key:"prepend-defaults",disabled:!e.icon,defaults:{VIcon:{icon:e.icon,start:!0}}},a.prepend):i(T,{key:"prepend-icon",start:!0,icon:e.icon},null)]),l.value.map((w,g,j)=>{let{item:_,raw:J}=w;return s(k,null,[a.item?.({item:_,index:g})??i(Ee,O({key:g,disabled:g>=j.length-1},typeof _=="string"?{title:_}:_),{default:a.title?()=>a.title?.({item:_,index:g}):void 0}),g<j.length-1&&i(Me,null,{default:a.divider?()=>a.divider?.({item:J,index:g}):void 0})])}),a.default?.()]})}),{}}}),Ne={name:"InfoComponent",components:{GraphNode:Te},props:{task:{required:!0},panelExpansion:{required:!1,default:["metadata"]}},setup(e,{emit:t}){return{inheritance:N(()=>e.task?.node?.namespace?.slice(1)??[]),jobTheme:pe(),icons:{mdiHelpCircleOutline:fe}}},computed:{panelExpansionModel:{get(){return this.panelExpansion},set(e){this.$emit("update:panelExpansion",e)}},taskMetadata(){return this.task?.node?.task?.meta||{}},customMetadata(){return this.task?.node?.task?.meta.userDefined||{}},prerequisites(){return this.task?.node?.prerequisites||{}},outputs(){return this.task?.node?.outputs||{}},completion(){return this.task?.node?.runtime.completion},runModeIcon(){return this.task?.node?.runtime.runMode==="Skip"?oe:this.task?.node?.runtime.runMode==="Live"?de:this.task?.node?.runtime.runMode==="Simulation"?ue:this.task?.node?.runtime.runMode==="Dummy"?ce:me},runMode(){return this.task?.node?.runtime.runMode},xtriggers(){const e=this.task?.node?.xtriggers?.map(t=>{const a=ie(t);return a.satisfactionIcon=a.satisfied?le:re,a.id=a.id.replace(/trigger_time=(?<unixTime>[0-9.]+)/,(o,d)=>`trigger_time=${Ve(new Date(d*1e3))}`),a});return e.sort(function(t,a){return t.label===a.label?t.id>a.id?1:-1:t.label>a.label?1:-1}),e}},methods:{formatCompletion:Pe}},je={class:"c-info"},Re={style:{"overflow-x":"hidden"}},Ae={preserveAspectRatio:"xMinYMin",viewBox:"-40 -40 99999 200",height:"6em"},Oe={class:"markup"},Ue=["href"],Le={class:"markup"},Ge={class:"d-flex align-center gap-2"},Fe={class:"text-mono"},He={style:{"margin-left":"0.5em",color:"rgb(0,0,0)"}};function Je(e,t,a,o,d,n){const b=F("GraphNode");return c(),m("div",je,[s("div",Re,[(c(),m("svg",Ae,[i(b,{task:a.task,jobs:a.task.children,jobTheme:o.jobTheme},null,8,["task","jobs","jobTheme"])]))]),i(he,{multiple:"",modelValue:n.panelExpansionModel,"onUpdate:modelValue":t[0]||(t[0]=l=>n.panelExpansionModel=l),flat:"",static:"",color:"blue-grey-lighten-3","bg-color":"grey-lighten-4",rounded:"lg"},{default:r(()=>[i(L,{defaults:{VExpansionPanelTitle:{class:"text-button py-2"},VExpansionPanelText:{class:"mt-2"},VTable:{density:"compact",class:"bg-transparent"}}},{default:r(()=>[i(h,{value:"metadata",class:"metadata-panel"},{default:r(()=>[i(v,null,{default:r(()=>[...t[1]||(t[1]=[p(" Metadata ",-1)])]),_:1}),i(x,null,{default:r(()=>[s("dl",null,[t[3]||(t[3]=s("dt",null,"Title",-1)),s("dd",null,f(n.taskMetadata.title),1),i(M),t[4]||(t[4]=s("dt",null,"Description",-1)),s("dd",null,[s("span",Oe,f(n.taskMetadata.description),1)]),n.taskMetadata.URL?(c(),m(k,{key:0},[i(M),t[2]||(t[2]=s("dt",null,"URL",-1)),s("dd",null,[s("a",{href:n.taskMetadata.URL,target:"_blank"},f(n.taskMetadata.URL),9,Ue)])],64)):I("",!0),(c(!0),m(k,null,C(n.customMetadata,(l,u)=>(c(),m(k,{key:u},[i(M),s("dt",null,f(u),1),s("dd",null,[s("span",Le,f(l),1)])],64))),128))])]),_:1})]),_:1}),i(h,{value:"runMode",class:"run-mode-panel"},{default:r(()=>[i(v,null,{default:r(()=>[...t[5]||(t[5]=[p(" Run Mode ",-1)])]),_:1}),i(x,null,{default:r(()=>[s("div",Ge,[i(T,{icon:n.runModeIcon},null,8,["icon"]),p(f(n.runMode),1)])]),_:1})]),_:1}),o.inheritance?.length>1?(c(),V(h,{key:0,value:"inheritance","data-cy":"inheritance-panel"},{default:r(()=>[i(v,null,{default:r(({expanded:l})=>[t[6]||(t[6]=p(" Inheritance ",-1)),l?be((c(),V(T,{key:0,icon:o.icons.mdiHelpCircleOutline,class:"ml-2"},null,8,["icon"])),[[ke,{text:"Shows the linearised family inheritance hierarchy for this task. The order of precedence is determined by the C3 algorithm used in Python.",location:"top"}]]):I("",!0)]),_:1}),i(x,null,{default:r(()=>[i(qe,{items:o.inheritance},{divider:r(()=>[...t[7]||(t[7]=[s("span",null,"::",-1)])]),_:1},8,["items"])]),_:1})]),_:1})):I("",!0),n.xtriggers.length?(c(),V(h,{key:1,value:"xtriggers",class:"xtriggers-panel"},{default:r(()=>[i(v,null,{default:r(()=>[...t[8]||(t[8]=[p(" Xtriggers ",-1)])]),_:1}),i(x,null,{default:r(()=>[i(ge,null,{default:r(()=>[t[9]||(t[9]=s("thead",null,[s("tr",null,[s("th",null,"Label"),s("th",null,"ID"),s("th",null,"Is satisfied")])],-1)),s("tbody",null,[(c(!0),m(k,null,C(n.xtriggers,l=>(c(),m("tr",{key:l.id},[s("td",null,f(l.label),1),s("td",Fe,f(l.id),1),s("td",null,[i(T,null,{default:r(()=>[p(f(l.satisfactionIcon),1)]),_:2},1024)])]))),128))])]),_:1})]),_:1})]),_:1})):I("",!0),i(h,{value:"prereqs",class:"prerequisites-panel"},{default:r(()=>[i(v,null,{default:r(()=>[...t[10]||(t[10]=[p(" Prerequisites ",-1)])]),_:1}),i(x,null,{default:r(()=>[s("ul",null,[(c(!0),m(k,null,C(n.prerequisites,l=>(c(),m("li",{key:l.expression},[s("span",{class:y(["prerequisite-alias condition",{satisfied:l.satisfied}])},f(l.expression.replace(/c/g,"")),3),s("ul",null,[(c(!0),m(k,null,C(l.conditions,u=>(c(),m("li",{key:u.taskAlias},[s("span",{class:y(["prerequisite-alias condition",{satisfied:u.satisfied}])},[p(f(u.exprAlias.replace(/c/,""))+" ",1),s("span",He,f(u.taskId)+":"+f(u.reqState),1)],2)]))),128))])]))),128))])]),_:1})]),_:1}),i(h,{value:"outputs",class:"outputs-panel"},{default:r(()=>[i(v,null,{default:r(()=>[...t[11]||(t[11]=[p(" Outputs ",-1)])]),_:1}),i(x,null,{default:r(()=>[s("ul",null,[(c(!0),m(k,null,C(n.outputs,l=>(c(),m("li",{key:l.label},[s("span",{class:y(["condition",{satisfied:l.satisfied}])},f(l.label),3)]))),128))])]),_:1})]),_:1}),i(h,{value:"completion",class:"completion-panel"},{default:r(()=>[i(v,null,{default:r(()=>[...t[12]||(t[12]=[p(" Completion ",-1)])]),_:1}),i(x,null,{default:r(()=>[s("ul",null,[(c(!0),m(k,null,C(n.formatCompletion(n.completion,n.outputs),([l,u,w],g)=>(c(),m("li",{key:g},[s("span",{class:y(["condition",{satisfied:l,blank:l===null}])},[s("span",{style:P(`margin-left: ${1*u}em;`)},null,4),p(" "+f(w),1)],2)]))),128))])]),_:1})]),_:1})]),_:1})]),_:1},8,["modelValue"])])}const ze=G(Ne,[["render",Je],["__scopeId","data-v-4fd0edb1"]]),Qe=Ce`
subscription InfoViewSubscription ($workflowId: ID, $taskID: ID) {
  deltas(workflows: [$workflowId]) {
    added {
      ...AddedDelta
    }
    updated (stripNull: true) {
      ...UpdatedDelta
    }
  }
}

fragment AddedDelta on Added {
  taskProxies(ids: [$taskID]) {
    ...TaskProxyData
  }
}

fragment UpdatedDelta on Updated {
  taskProxies(ids: [$taskID]) {
    ...TaskProxyData
  }
}

fragment TaskProxyData on TaskProxy {
  id
  namespace
  state
  isHeld
  isQueued
  isRunahead
  isRetry
  isWallclock
  isXtriggered

  task {
    ...TaskDefinitionData
  }

  jobs {
    ...JobData
  }

  prerequisites {
    satisfied
    expression
    conditions {
      taskId
      reqState
      exprAlias
      satisfied
    }
  }

  outputs {
    label
    satisfied
  }

  runtime {
    completion
    runMode
  }

  xtriggers {
    label
    id
    satisfied
  }
}

fragment TaskDefinitionData on Task {
  meanElapsedTime

  meta {
    title
    description
    URL
    userDefined
  }
}

fragment JobData on Job {
  id
  jobId
  startedTime
  state
}
`;function We(e){const t=new H(e.id);return{id:e.id,tokens:t,name:t.task,node:e,type:"task",children:[]}}function Xe(e){const t=new H(e.id);return{id:e.id,name:t.job,tokens:t,node:e,type:"job"}}function A(e,t){e.children=[];for(const a of t.jobs)e.children.push(Xe(a))}class Ye extends _e{constructor(t,a){super(),this.task=t,this.taskNode=a}onAdded(t,a,o){Object.assign(this.task,t.taskProxies[0]),Object.assign(this.taskNode,We(this.task)),A(this.taskNode,this.task)}onUpdated(t,a,o){t?.taskProxies&&Object.assign(this.task,t.taskProxies[0]),A(this.taskNode,this.task)}onPruned(t){}}const Ke={name:"InfoView",mixins:[De,ve],components:{InfoComponent:ze},head(){return{title:ye("App.workflow",{name:this.workflowName})}},props:{initialOptions:Ie},setup(e,{emit:t}){const a=R("requestedTokens",{props:e,emit:t}),o=R("panelExpansion",{props:e,emit:t},["metadata"]);return{requestedTokens:a,panelExpansion:o}},data(){return{requestedCycle:void 0,requestedTask:void 0,task:{},taskNode:{}}},computed:{query(){return new xe(Qe,{...this.variables,taskID:this.requestedTokens?.relativeID},`info-query-${this._uid}`,[new Ye(this.task,this.taskNode)],!0,!1)}},methods:{updatePanelExpansion(e){this.panelExpansion=e}}};function Ze(e,t,a,o,d,n){const b=F("InfoComponent");return d.taskNode.id?(c(),V(b,{key:0,task:d.taskNode,panelExpansion:o.panelExpansion,"onUpdate:panelExpansion":n.updatePanelExpansion},null,8,["task","panelExpansion","onUpdate:panelExpansion"])):I("",!0)}const nt=G(Ke,[["render",Ze]]);export{nt as default};
