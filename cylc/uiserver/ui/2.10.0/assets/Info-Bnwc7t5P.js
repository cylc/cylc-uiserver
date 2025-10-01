import{_ as w,b5 as V,b6 as v,b7 as U,b8 as O,b9 as R,ba as A,bb as L,bc as S,bd as B,ay as G,C,x as p,o,z as t,g as i,w as l,e as P,y as I,be as g,bf as h,l as m,bg as x,t as u,L as y,F as c,r as _,D as T,bh as J,az as D,bi as z,bj as Q,a6 as F,ad as X,bk as Y,I as H,J as W,ae as q}from"./index-jbzX_AXb.js";import{g as K}from"./graphql-o3z6-itG.js";import{i as Z,a as M}from"./initialOptions-Ceh0265h.js";import{G as $}from"./GraphNode-CjrYIu24.js";function ee(a,e){const n=[];let d=0,f="";for(let s of a.split(/(and|or|\(|\))/))if(s=s.trim(),!!s)if(s==="(")n.push([null,d,`${f}(`]),f="",d=d+1;else if(s===")")d=d-1,n.push([null,d,`${f})`]),f="";else if(s==="and"||s==="or")f=`${s} `;else{for(const b of e)if(b.label===s){n.push([b.satisfied,d,`${f}${s}`]);break}f=""}return n}const te={name:"InfoComponent",components:{GraphNode:$},props:{task:{required:!0},panelExpansion:{required:!1,default:[0]}},setup(a,{emit:e}){return{jobTheme:G()}},computed:{panelExpansionModel:{get(){return this.panelExpansion},set(a){this.$emit("update:panelExpansion",a)}},taskMetadata(){return this.task?.node?.task?.meta||{}},customMetadata(){return this.task?.node?.task?.meta.userDefined||{}},prerequisites(){return this.task?.node?.prerequisites||{}},outputs(){return this.task?.node?.outputs||{}},completion(){return this.task?.node?.runtime.completion},runModeIcon(){return this.task?.node?.runtime.runMode==="Skip"?R:this.task?.node?.runtime.runMode==="Live"?A:this.task?.node?.runtime.runMode==="Simulation"?L:this.task?.node?.runtime.runMode==="Dummy"?S:B},runMode(){return this.task?.node?.runtime.runMode},xtriggers(){const a=this.task?.node?.xtriggers?.map(e=>{const n=V(e);return n.satisfactionIcon=n.satisfied?v:U,n.id=n.id.replace(/trigger_time=(?<unixTime>[0-9.]+)/,(d,f)=>`trigger_time=${O(new Date(f*1e3))}`),n});return a.sort(function(e,n){return e.label===n.label?e.id>n.id?1:-1:e.label>n.label?1:-1}),a}},methods:{formatCompletion:ee}},se={class:"c-info"},ae={style:{"overflow-x":"hidden"}},ne={preserveAspectRatio:"xMinYMin",viewBox:"-40 -40 99999 200",height:"6em"},ie={class:"markup"},le=["href"],re={class:"markup"},oe={style:{"margin-left":"0.5em",color:"rgb(0,0,0)"}};function de(a,e,n,d,f,s){const b=C("GraphNode");return o(),p("div",se,[t("div",ae,[(o(),p("svg",ne,[i(b,{task:n.task,jobs:n.task.children,jobTheme:d.jobTheme},null,8,["task","jobs","jobTheme"])]))]),i(Q,{multiple:"",variant:"accordion",modelValue:s.panelExpansionModel,"onUpdate:modelValue":e[0]||(e[0]=r=>s.panelExpansionModel=r)},{default:l(()=>[i(g,{class:"metadata-panel"},{default:l(()=>[i(h,{color:"blue-grey-lighten-1"},{default:l(()=>[...e[1]||(e[1]=[m(" Metadata ",-1)])]),_:1}),i(x,null,{default:l(()=>[t("dl",null,[e[2]||(e[2]=t("dt",null,"Title",-1)),t("dd",null,u(s.taskMetadata.title),1),i(y),e[3]||(e[3]=t("dt",null,"Description",-1)),t("dd",null,[t("span",ie,u(s.taskMetadata.description),1)]),i(y),e[4]||(e[4]=t("dt",null,"URL",-1)),t("dd",null,[s.taskMetadata.URL?(o(),p("a",{key:0,href:s.taskMetadata.URL,target:"_blank"},u(s.taskMetadata.URL),9,le)):I("",!0)]),i(y),(o(!0),p(c,null,_(s.customMetadata,(r,k)=>(o(),p(c,{key:k},[t("dt",null,u(k),1),t("dd",null,[t("span",re,u(r),1)]),i(y)],64))),128))])]),_:1})]),_:1}),i(g,{class:"run-mode-panel"},{default:l(()=>[i(h,{color:"blue-grey-lighten-2"},{default:l(()=>[...e[5]||(e[5]=[m(" Run Mode ",-1)])]),_:1}),i(x,null,{default:l(()=>[i(T,null,{default:l(()=>[m(u(s.runModeIcon),1)]),_:1}),m(" "+u(s.runMode),1)]),_:1})]),_:1}),s.xtriggers.length?(o(),P(g,{key:0,class:"xtriggers-panel"},{default:l(()=>[i(h,{color:"blue-grey-lighten-1"},{default:l(()=>[...e[6]||(e[6]=[m(" Xtriggers ",-1)])]),_:1}),i(x,null,{default:l(()=>[i(J,{density:"compact"},{default:l(()=>[e[7]||(e[7]=t("thead",null,[t("tr",null,[t("th",null,"Label"),t("th",null,"ID"),t("th",null,"Is satisfied")])],-1)),t("tbody",null,[(o(!0),p(c,null,_(s.xtriggers,r=>(o(),p("tr",{key:r.id},[t("td",null,u(r.label),1),t("td",null,u(r.id),1),t("td",null,[i(T,null,{default:l(()=>[m(u(r.satisfactionIcon),1)]),_:2},1024)])]))),128))])]),_:1})]),_:1})]),_:1})):I("",!0),i(g,{class:"prerequisites-panel"},{default:l(()=>[i(h,{color:"blue-grey-lighten-2"},{default:l(()=>[...e[8]||(e[8]=[m(" Prerequisites ",-1)])]),_:1}),i(x,null,{default:l(()=>[t("ul",null,[(o(!0),p(c,null,_(s.prerequisites,r=>(o(),p("li",{key:r.expression},[t("span",{class:D(["prerequisite-alias condition",{satisfied:r.satisfied}])},u(r.expression.replace(/c/g,"")),3),t("ul",null,[(o(!0),p(c,null,_(r.conditions,k=>(o(),p("li",{key:k.taskAlias},[t("span",{class:D(["prerequisite-alias condition",{satisfied:k.satisfied}])},[m(u(k.exprAlias.replace(/c/,""))+" ",1),t("span",oe,u(k.taskId)+":"+u(k.reqState),1)],2)]))),128))])]))),128))])]),_:1})]),_:1}),i(g,{class:"outputs-panel"},{default:l(()=>[i(h,{color:"blue-grey-lighten-1"},{default:l(()=>[...e[9]||(e[9]=[m(" Outputs ",-1)])]),_:1}),i(x,null,{default:l(()=>[t("ul",null,[(o(!0),p(c,null,_(s.outputs,r=>(o(),p("li",{key:r.label},[t("span",{class:D(["condition",{satisfied:r.satisfied}])},u(r.label),3)]))),128))])]),_:1})]),_:1}),i(g,{class:"completion-panel"},{default:l(()=>[i(h,{color:"blue-grey-lighten-2"},{default:l(()=>[...e[10]||(e[10]=[m(" Completion ",-1)])]),_:1}),i(x,null,{default:l(()=>[t("ul",null,[(o(!0),p(c,null,_(s.formatCompletion(s.completion,s.outputs),([r,k,N],j)=>(o(),p("li",{key:j},[t("span",{class:D(["condition",{satisfied:r,blank:r===null}])},[t("span",{style:z(`margin-left: ${1*k}em;`)},null,4),m(" "+u(N),1)],2)]))),128))])]),_:1})]),_:1})]),_:1},8,["modelValue"])])}const ue=w(te,[["render",de],["__scopeId","data-v-7b186a8d"]]),pe=H`
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
`;function fe(a){const e=new q(a.id);return{id:a.id,tokens:e,name:e.task,node:a,type:"task",children:[]}}function me(a){const e=new q(a.id);return{id:a.id,name:e.job,tokens:e,node:a,type:"job"}}function E(a,e){a.children=[];for(const n of e.jobs)a.children.push(me(n))}class ke extends W{constructor(e,n){super(),this.task=e,this.taskNode=n}onAdded(e,n,d){Object.assign(this.task,e.taskProxies[0]),Object.assign(this.taskNode,fe(this.task)),E(this.taskNode,this.task)}onUpdated(e,n,d){e?.taskProxies&&Object.assign(this.task,e.taskProxies[0]),E(this.taskNode,this.task)}onPruned(e){}}const ce={name:"InfoView",mixins:[K,F],components:{InfoComponent:ue},head(){return{title:Y("App.workflow",{name:this.workflowName})}},props:{initialOptions:Z},setup(a,{emit:e}){const n=M("requestedTokens",{props:a,emit:e}),d=M("panelExpansion",{props:a,emit:e},[0]);return{requestedTokens:n,panelExpansion:d}},data(){return{requestedCycle:void 0,requestedTask:void 0,task:{},taskNode:{}}},computed:{query(){return new X(pe,{...this.variables,taskID:this.requestedTokens?.relativeID},`info-query-${this._uid}`,[new ke(this.task,this.taskNode)],!0,!1)}},methods:{updatePanelExpansion(a){this.panelExpansion=a}}};function be(a,e,n,d,f,s){const b=C("InfoComponent");return f.taskNode.id?(o(),P(b,{key:0,task:f.taskNode,panelExpansion:d.panelExpansion,"onUpdate:panelExpansion":s.updatePanelExpansion},null,8,["task","panelExpansion","onUpdate:panelExpansion"])):I("",!0)}const ye=w(ce,[["render",be]]);export{ye as default};
