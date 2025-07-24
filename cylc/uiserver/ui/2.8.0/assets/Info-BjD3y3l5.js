import{_ as w,b6 as V,b7 as v,b8 as U,b9 as O,ba as S,bb as A,bc as R,bd as L,az as B,C,x as p,o,z as t,g as i,w as l,e as P,y as I,be as g,bf as h,l as m,bg as x,t as u,M as y,F as c,r as _,D as M,aA as D,bh as G,bi as J,a7 as z,ae as Q,bj as F,I as X,J as Y,af as q}from"./index-EpcknQ5m.js";import{g as H}from"./graphql-n5gzreXW.js";import{i as W,a as T}from"./initialOptions-CKJltX86.js";import{G as Z}from"./GraphNode-DyB56Gvt.js";import{V as K}from"./VTable-hoHcQV6C.js";function $(a,e){const n=[];let d=0,f="";for(let s of a.split(/(and|or|\(|\))/))if(s=s.trim(),!!s)if(s==="(")n.push([null,d,`${f}(`]),f="",d=d+1;else if(s===")")d=d-1,n.push([null,d,`${f})`]),f="";else if(s==="and"||s==="or")f=`${s} `;else{for(const b of e)if(b.label===s){n.push([b.satisfied,d,`${f}${s}`]);break}f=""}return n}const ee={name:"InfoComponent",components:{GraphNode:Z},props:{task:{required:!0},panelExpansion:{required:!1,default:[0]}},setup(a,{emit:e}){return{jobTheme:B()}},computed:{panelExpansionModel:{get(){return this.panelExpansion},set(a){this.$emit("update:panelExpansion",a)}},taskMetadata(){return this.task?.node?.task?.meta||{}},customMetadata(){return this.task?.node?.task?.meta.userDefined||{}},prerequisites(){return this.task?.node?.prerequisites||{}},outputs(){return this.task?.node?.outputs||{}},completion(){return this.task?.node?.runtime.completion},runModeIcon(){return this.task?.node?.runtime.runMode==="Skip"?O:this.task?.node?.runtime.runMode==="Live"?S:this.task?.node?.runtime.runMode==="Simulation"?A:this.task?.node?.runtime.runMode==="Dummy"?R:L},runMode(){return this.task?.node?.runtime.runMode},xtriggers(){const a=this.task?.node?.xtriggers?.map(e=>{const n=V(e);return n.satisfactionIcon=n.satisfied?v:U,n.id=n.id.replace(/trigger_time=(?<unixTime>[0-9.]+)/,(d,f)=>`trigger_time=${new Date(f*1e3).toISOString().slice(0,-5)}Z`),n});return a.sort(function(e,n){return e.label===n.label?e.id>n.id?1:-1:e.label>n.label?1:-1}),a}},methods:{formatCompletion:$}},te={class:"c-info"},se={style:{"overflow-x":"hidden"}},ae={preserveAspectRatio:"xMinYMin",viewBox:"-40 -40 99999 200",height:"6em"},ne={class:"markup"},ie=["href"],le={class:"markup"},re={style:{"margin-left":"0.5em",color:"rgb(0,0,0)"}};function oe(a,e,n,d,f,s){const b=C("GraphNode");return o(),p("div",te,[t("div",se,[(o(),p("svg",ae,[i(b,{task:n.task,jobs:n.task.children,jobTheme:d.jobTheme},null,8,["task","jobs","jobTheme"])]))]),i(J,{multiple:"",variant:"accordion",modelValue:s.panelExpansionModel,"onUpdate:modelValue":e[0]||(e[0]=r=>s.panelExpansionModel=r)},{default:l(()=>[i(g,{class:"metadata-panel"},{default:l(()=>[i(h,{color:"blue-grey-lighten-1"},{default:l(()=>e[1]||(e[1]=[m(" Metadata ",-1)])),_:1,__:[1]}),i(x,null,{default:l(()=>[t("dl",null,[e[2]||(e[2]=t("dt",null,"Title",-1)),t("dd",null,u(s.taskMetadata.title),1),i(y),e[3]||(e[3]=t("dt",null,"Description",-1)),t("dd",null,[t("span",ne,u(s.taskMetadata.description),1)]),i(y),e[4]||(e[4]=t("dt",null,"URL",-1)),t("dd",null,[s.taskMetadata.URL?(o(),p("a",{key:0,href:s.taskMetadata.URL,target:"_blank"},u(s.taskMetadata.URL),9,ie)):I("",!0)]),i(y),(o(!0),p(c,null,_(s.customMetadata,(r,k)=>(o(),p(c,{key:k},[t("dt",null,u(k),1),t("dd",null,[t("span",le,u(r),1)]),i(y)],64))),128))])]),_:1})]),_:1}),i(g,{class:"run-mode-panel"},{default:l(()=>[i(h,{color:"blue-grey-lighten-2"},{default:l(()=>e[5]||(e[5]=[m(" Run Mode ",-1)])),_:1,__:[5]}),i(x,null,{default:l(()=>[i(M,null,{default:l(()=>[m(u(s.runModeIcon),1)]),_:1}),m(" "+u(s.runMode),1)]),_:1})]),_:1}),s.xtriggers.length?(o(),P(g,{key:0,class:"xtriggers-panel"},{default:l(()=>[i(h,{color:"blue-grey-lighten-1"},{default:l(()=>e[6]||(e[6]=[m(" Xtriggers ",-1)])),_:1,__:[6]}),i(x,null,{default:l(()=>[i(K,{density:"compact"},{default:l(()=>[e[7]||(e[7]=t("thead",null,[t("tr",null,[t("th",null,"Label"),t("th",null,"ID"),t("th",null,"Is satisfied")])],-1)),t("tbody",null,[(o(!0),p(c,null,_(s.xtriggers,r=>(o(),p("tr",{key:r.id},[t("td",null,u(r.label),1),t("td",null,u(r.id),1),t("td",null,[i(M,null,{default:l(()=>[m(u(r.satisfactionIcon),1)]),_:2},1024)])]))),128))])]),_:1,__:[7]})]),_:1})]),_:1})):I("",!0),i(g,{class:"prerequisites-panel"},{default:l(()=>[i(h,{color:"blue-grey-lighten-2"},{default:l(()=>e[8]||(e[8]=[m(" Prerequisites ",-1)])),_:1,__:[8]}),i(x,null,{default:l(()=>[t("ul",null,[(o(!0),p(c,null,_(s.prerequisites,r=>(o(),p("li",{key:r.expression},[t("span",{class:D(["prerequisite-alias condition",{satisfied:r.satisfied}])},u(r.expression.replace(/c/g,"")),3),t("ul",null,[(o(!0),p(c,null,_(r.conditions,k=>(o(),p("li",{key:k.taskAlias},[t("span",{class:D(["prerequisite-alias condition",{satisfied:k.satisfied}])},[m(u(k.exprAlias.replace(/c/,""))+" ",1),t("span",re,u(k.taskId)+":"+u(k.reqState),1)],2)]))),128))])]))),128))])]),_:1})]),_:1}),i(g,{class:"outputs-panel"},{default:l(()=>[i(h,{color:"blue-grey-lighten-1"},{default:l(()=>e[9]||(e[9]=[m(" Outputs ",-1)])),_:1,__:[9]}),i(x,null,{default:l(()=>[t("ul",null,[(o(!0),p(c,null,_(s.outputs,r=>(o(),p("li",{key:r.label},[t("span",{class:D(["condition",{satisfied:r.satisfied}])},u(r.label),3)]))),128))])]),_:1})]),_:1}),i(g,{class:"completion-panel"},{default:l(()=>[i(h,{color:"blue-grey-lighten-2"},{default:l(()=>e[10]||(e[10]=[m(" Completion ",-1)])),_:1,__:[10]}),i(x,null,{default:l(()=>[t("ul",null,[(o(!0),p(c,null,_(s.formatCompletion(s.completion,s.outputs),([r,k,N],j)=>(o(),p("li",{key:j},[t("span",{class:D(["condition",{satisfied:r,blank:r===null}])},[t("span",{style:G(`margin-left: ${1*k}em;`)},null,4),m(" "+u(N),1)],2)]))),128))])]),_:1})]),_:1})]),_:1},8,["modelValue"])])}const de=w(ee,[["render",oe],["__scopeId","data-v-1882ac3a"]]),ue=X`
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
`;function pe(a){const e=new q(a.id);return{id:a.id,tokens:e,name:e.task,node:a,type:"task",children:[]}}function fe(a){const e=new q(a.id);return{id:a.id,name:e.job,tokens:e,node:a,type:"job"}}function E(a,e){a.children=[];for(const n of e.jobs)a.children.push(fe(n))}class me extends Y{constructor(e,n){super(),this.task=e,this.taskNode=n}onAdded(e,n,d){Object.assign(this.task,e.taskProxies[0]),Object.assign(this.taskNode,pe(this.task)),E(this.taskNode,this.task)}onUpdated(e,n,d){e?.taskProxies&&Object.assign(this.task,e.taskProxies[0]),E(this.taskNode,this.task)}onPruned(e){}}const ke={name:"InfoView",mixins:[H,z],components:{InfoComponent:de},head(){return{title:F("App.workflow",{name:this.workflowName})}},props:{initialOptions:W},setup(a,{emit:e}){const n=T("requestedTokens",{props:a,emit:e}),d=T("panelExpansion",{props:a,emit:e},[0]);return{requestedTokens:n,panelExpansion:d}},data(){return{requestedCycle:void 0,requestedTask:void 0,task:{},taskNode:{}}},computed:{query(){return new Q(ue,{...this.variables,taskID:this.requestedTokens?.relativeID},`info-query-${this._uid}`,[new me(this.task,this.taskNode)],!0,!1)}},methods:{updatePanelExpansion(a){this.panelExpansion=a}}};function ce(a,e,n,d,f,s){const b=C("InfoComponent");return f.taskNode.id?(o(),P(b,{key:0,task:f.taskNode,panelExpansion:d.panelExpansion,"onUpdate:panelExpansion":s.updatePanelExpansion},null,8,["task","panelExpansion","onUpdate:panelExpansion"])):I("",!0)}const ye=w(ke,[["render",ce]]);export{ye as default};
