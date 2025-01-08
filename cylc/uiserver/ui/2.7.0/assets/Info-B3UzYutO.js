import{_ as w,aI as M,A as q,h as r,B as d,C as n,k as o,w as u,bn as b,bo as x,m,bp as g,t as c,O as I,H as N,I as h,r as _,aQ as T,bq as V,br as v,bs as U,bt as A,J as O,$ as S,bu as R,a0 as L,j as B,L as J,ag as P}from"./index-Hyq34tSM.js";import{g as G}from"./graphql-D8b4q-7X.js";import{i as Q,a as y}from"./initialOptions-BLDeg43d.js";import{G as $}from"./GraphNode-DQwCPFhY.js";function z(e,t){const a=[];let i=0,p="";for(let s of e.split(/(and|or|\(|\))/))if(s=s.trim(),!!s)if(s==="(")a.push([null,i,`${p}(`]),p="",i=i+1;else if(s===")")i=i-1,a.push([null,i,`${p})`]),p="";else if(s==="and"||s==="or")p=`${s} `;else{for(const k of t)if(k.label===s){a.push([k.satisfied,i,`${p}${s}`]);break}p=""}return a}const H={name:"InfoComponent",components:{GraphNode:$},props:{task:{required:!0},panelExpansion:{required:!1,default:[0]}},setup(e,{emit:t}){return{jobTheme:M()}},computed:{panelExpansionModel:{get(){return this.panelExpansion},set(e){this.$emit("update:panelExpansion",e)}},taskMetadata(){var e,t,a;return((a=(t=(e=this.task)==null?void 0:e.node)==null?void 0:t.task)==null?void 0:a.meta)||{}},customMetadata(){var e,t,a;return((a=(t=(e=this.task)==null?void 0:e.node)==null?void 0:t.task)==null?void 0:a.meta.userDefined)||{}},prerequisites(){var e,t;return((t=(e=this.task)==null?void 0:e.node)==null?void 0:t.prerequisites)||{}},outputs(){var e,t;return((t=(e=this.task)==null?void 0:e.node)==null?void 0:t.outputs)||{}},completion(){var e,t;return(t=(e=this.task)==null?void 0:e.node)==null?void 0:t.runtime.completion}},methods:{formatCompletion:z}},D=e=>(U("data-v-d103a99f"),e=e(),A(),e),Y={class:"c-info"},F={style:{"overflow-x":"hidden"}},K={preserveAspectRatio:"xMinYMin",viewBox:"-40 -40 99999 200",height:"6em"},W=D(()=>n("dt",null,"Title",-1)),X=D(()=>n("dt",null,"Description",-1)),Z={class:"markup"},ee=D(()=>n("dt",null,"URL",-1)),te=["href"],se={class:"markup"},ae={style:{"margin-left":"0.5em",color:"rgb(0,0,0)"}};function ne(e,t,a,i,p,s){const k=q("GraphNode");return r(),d("div",Y,[n("div",F,[(r(),d("svg",K,[o(k,{task:a.task,jobs:a.task.children,jobTheme:i.jobTheme},null,8,["task","jobs","jobTheme"])]))]),o(v,{multiple:"",variant:"accordion",modelValue:s.panelExpansionModel,"onUpdate:modelValue":t[0]||(t[0]=l=>s.panelExpansionModel=l)},{default:u(()=>[o(b,{class:"metadata-panel"},{default:u(()=>[o(x,{color:"blue-grey-lighten-1"},{default:u(()=>[m(" Metadata ")]),_:1}),o(g,null,{default:u(()=>[n("dl",null,[W,n("dd",null,c(s.taskMetadata.title),1),o(I),X,n("dd",null,[n("span",Z,c(s.taskMetadata.description),1)]),o(I),ee,n("dd",null,[s.taskMetadata.URL?(r(),d("a",{key:0,href:s.taskMetadata.URL,target:"_blank"},c(s.taskMetadata.URL),9,te)):N("",!0)]),o(I),(r(!0),d(h,null,_(s.customMetadata,(l,f)=>(r(),d(h,{key:f},[n("dt",null,c(f),1),n("dd",null,[n("span",se,c(l),1)]),o(I)],64))),128))])]),_:1})]),_:1}),o(b,{class:"prerequisites-panel"},{default:u(()=>[o(x,{color:"blue-grey-lighten-2"},{default:u(()=>[m(" Prerequisites ")]),_:1}),o(g,null,{default:u(()=>[n("ul",null,[(r(!0),d(h,null,_(s.prerequisites,l=>(r(),d("li",{key:l.expression},[n("span",{class:T(["prerequisite-alias condition",{satisfied:l.satisfied}])},c(l.expression.replace(/c/g,"")),3),n("ul",null,[(r(!0),d(h,null,_(l.conditions,f=>(r(),d("li",{key:f.taskAlias},[n("span",{class:T(["prerequisite-alias condition",{satisfied:f.satisfied}])},[m(c(f.exprAlias.replace(/c/,""))+" ",1),n("span",ae,c(f.taskId)+":"+c(f.reqState),1)],2)]))),128))])]))),128))])]),_:1})]),_:1}),o(b,{class:"outputs-panel"},{default:u(()=>[o(x,{color:"blue-grey-lighten-1"},{default:u(()=>[m(" Outputs ")]),_:1}),o(g,null,{default:u(()=>[n("ul",null,[(r(!0),d(h,null,_(s.outputs,l=>(r(),d("li",{key:l.label},[n("span",{class:T(["condition",{satisfied:l.satisfied}])},c(l.label),3)]))),128))])]),_:1})]),_:1}),o(b,{class:"completion-panel"},{default:u(()=>[o(x,{color:"blue-grey-lighten-2"},{default:u(()=>[m(" Completion ")]),_:1}),o(g,null,{default:u(()=>[n("ul",null,[(r(!0),d(h,null,_(s.formatCompletion(s.completion,s.outputs),([l,f,j],C)=>(r(),d("li",{key:C},[n("span",{class:T(["condition",{satisfied:l,blank:l===null}])},[n("span",{style:V(`margin-left: ${1*f}em;`)},null,4),m(" "+c(j),1)],2)]))),128))])]),_:1})]),_:1})]),_:1},8,["modelValue"])])}const oe=w(H,[["render",ne],["__scopeId","data-v-d103a99f"]]),ie=O`
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
`;function le(e){const t=new P(e.id);return{id:e.id,tokens:t,name:t.task,node:e,type:"task",children:[]}}function re(e){const t=new P(e.id);return{id:e.id,name:t.job,tokens:t,node:e,type:"job"}}function E(e,t){e.children=[];for(const a of t.jobs)e.children.push(re(a))}class de extends J{constructor(t,a){super(),this.task=t,this.taskNode=a}onAdded(t,a,i){Object.assign(this.task,t.taskProxies[0]),Object.assign(this.taskNode,le(this.task)),E(this.taskNode,this.task)}onUpdated(t,a,i){t!=null&&t.taskProxies&&Object.assign(this.task,t.taskProxies[0]),E(this.taskNode,this.task)}onPruned(t){}}const ue={name:"InfoView",mixins:[G,S],components:{InfoComponent:oe},head(){return{title:R("App.workflow",{name:this.workflowName})}},props:{initialOptions:Q},setup(e,{emit:t}){const a=y("requestedTokens",{props:e,emit:t}),i=y("panelExpansion",{props:e,emit:t},[0]);return{requestedTokens:a,panelExpansion:i}},data(){return{requestedCycle:void 0,requestedTask:void 0,task:{},taskNode:{}}},computed:{query(){var e;return new L(ie,{...this.variables,taskID:(e=this.requestedTokens)==null?void 0:e.relativeID},`info-query-${this._uid}`,[new de(this.task,this.taskNode)],!0,!1)}},methods:{updatePanelExpansion(e){this.panelExpansion=e}}};function pe(e,t,a,i,p,s){const k=q("InfoComponent");return p.taskNode.id?(r(),B(k,{key:0,task:p.taskNode,panelExpansion:i.panelExpansion,"onUpdate:panelExpansion":s.updatePanelExpansion},null,8,["task","panelExpansion","onUpdate:panelExpansion"])):N("",!0)}const he=w(ue,[["render",pe]]);export{he as default};
