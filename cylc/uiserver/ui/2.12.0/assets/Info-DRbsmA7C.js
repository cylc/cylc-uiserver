import{_ as w,b9 as j,ba as v,bb as U,bc as O,bd as R,be as A,bf as S,bg as L,ay as B,B as P,v as u,o as r,y as t,g as l,w as i,R as G,e as C,x as T,bh as x,bi as h,k,bj as g,t as p,K as D,F as c,r as _,C as I,bk as J,az as y,bl as Q,bm as z,a6 as F,ad as H,bn as X,H as Y,I as K,ae as V}from"./index-Dk_oQcLS.js";import{g as W}from"./graphql-Dr9bN1Q1.js";import{i as Z,a as M}from"./initialOptions-BnNLz-ak.js";import{G as $}from"./GraphNode-BFYupDpf.js";import{f as ee}from"./datetime-BTQ3cuKI.js";function te(a,e){const n=[];let d=0,f="";for(let s of a.split(/(and|or|\(|\))/))if(s=s.trim(),!!s)if(s==="(")n.push([null,d,`${f}(`]),f="",d=d+1;else if(s===")")d=d-1,n.push([null,d,`${f})`]),f="";else if(s==="and"||s==="or")f=`${s} `;else{for(const b of e)if(b.label===s){n.push([b.satisfied,d,`${f}${s}`]);break}f=""}return n}const se={name:"InfoComponent",components:{GraphNode:$},props:{task:{required:!0},panelExpansion:{required:!1,default:[0]}},setup(a,{emit:e}){return{jobTheme:B()}},computed:{panelExpansionModel:{get(){return this.panelExpansion},set(a){this.$emit("update:panelExpansion",a)}},taskMetadata(){return this.task?.node?.task?.meta||{}},customMetadata(){return this.task?.node?.task?.meta.userDefined||{}},prerequisites(){return this.task?.node?.prerequisites||{}},outputs(){return this.task?.node?.outputs||{}},completion(){return this.task?.node?.runtime.completion},runModeIcon(){return this.task?.node?.runtime.runMode==="Skip"?O:this.task?.node?.runtime.runMode==="Live"?R:this.task?.node?.runtime.runMode==="Simulation"?A:this.task?.node?.runtime.runMode==="Dummy"?S:L},runMode(){return this.task?.node?.runtime.runMode},xtriggers(){const a=this.task?.node?.xtriggers?.map(e=>{const n=j(e);return n.satisfactionIcon=n.satisfied?v:U,n.id=n.id.replace(/trigger_time=(?<unixTime>[0-9.]+)/,(d,f)=>`trigger_time=${ee(new Date(f*1e3))}`),n});return a.sort(function(e,n){return e.label===n.label?e.id>n.id?1:-1:e.label>n.label?1:-1}),a}},methods:{formatCompletion:te}},ae={class:"c-info"},ne={style:{"overflow-x":"hidden"}},le={preserveAspectRatio:"xMinYMin",viewBox:"-40 -40 99999 200",height:"6em"},ie={class:"markup"},oe=["href"],re={class:"markup"},de={class:"d-flex align-center gap-2"},ue={class:"text-mono"},pe={style:{"margin-left":"0.5em",color:"rgb(0,0,0)"}};function fe(a,e,n,d,f,s){const b=P("GraphNode");return r(),u("div",ae,[t("div",ne,[(r(),u("svg",le,[l(b,{task:n.task,jobs:n.task.children,jobTheme:d.jobTheme},null,8,["task","jobs","jobTheme"])]))]),l(z,{multiple:"",modelValue:s.panelExpansionModel,"onUpdate:modelValue":e[0]||(e[0]=o=>s.panelExpansionModel=o),flat:"",static:"",color:"blue-grey-lighten-3","bg-color":"grey-lighten-4",rounded:"lg"},{default:i(()=>[l(G,{defaults:{VExpansionPanelTitle:{class:"text-button py-2"},VExpansionPanelText:{class:"mt-2"},VTable:{density:"compact",class:"bg-transparent"}}},{default:i(()=>[l(x,{class:"metadata-panel"},{default:i(()=>[l(h,null,{default:i(()=>[...e[1]||(e[1]=[k(" Metadata ",-1)])]),_:1}),l(g,null,{default:i(()=>[t("dl",null,[e[3]||(e[3]=t("dt",null,"Title",-1)),t("dd",null,p(s.taskMetadata.title),1),l(D),e[4]||(e[4]=t("dt",null,"Description",-1)),t("dd",null,[t("span",ie,p(s.taskMetadata.description),1)]),s.taskMetadata.URL?(r(),u(c,{key:0},[l(D),e[2]||(e[2]=t("dt",null,"URL",-1)),t("dd",null,[t("a",{href:s.taskMetadata.URL,target:"_blank"},p(s.taskMetadata.URL),9,oe)])],64)):T("",!0),(r(!0),u(c,null,_(s.customMetadata,(o,m)=>(r(),u(c,{key:m},[l(D),t("dt",null,p(m),1),t("dd",null,[t("span",re,p(o),1)])],64))),128))])]),_:1})]),_:1}),l(x,{class:"run-mode-panel"},{default:i(()=>[l(h,null,{default:i(()=>[...e[5]||(e[5]=[k(" Run Mode ",-1)])]),_:1}),l(g,null,{default:i(()=>[t("div",de,[l(I,{icon:s.runModeIcon},null,8,["icon"]),k(p(s.runMode),1)])]),_:1})]),_:1}),s.xtriggers.length?(r(),C(x,{key:0,class:"xtriggers-panel"},{default:i(()=>[l(h,null,{default:i(()=>[...e[6]||(e[6]=[k(" Xtriggers ",-1)])]),_:1}),l(g,null,{default:i(()=>[l(J,null,{default:i(()=>[e[7]||(e[7]=t("thead",null,[t("tr",null,[t("th",null,"Label"),t("th",null,"ID"),t("th",null,"Is satisfied")])],-1)),t("tbody",null,[(r(!0),u(c,null,_(s.xtriggers,o=>(r(),u("tr",{key:o.id},[t("td",null,p(o.label),1),t("td",ue,p(o.id),1),t("td",null,[l(I,null,{default:i(()=>[k(p(o.satisfactionIcon),1)]),_:2},1024)])]))),128))])]),_:1})]),_:1})]),_:1})):T("",!0),l(x,{class:"prerequisites-panel"},{default:i(()=>[l(h,null,{default:i(()=>[...e[8]||(e[8]=[k(" Prerequisites ",-1)])]),_:1}),l(g,null,{default:i(()=>[t("ul",null,[(r(!0),u(c,null,_(s.prerequisites,o=>(r(),u("li",{key:o.expression},[t("span",{class:y(["prerequisite-alias condition",{satisfied:o.satisfied}])},p(o.expression.replace(/c/g,"")),3),t("ul",null,[(r(!0),u(c,null,_(o.conditions,m=>(r(),u("li",{key:m.taskAlias},[t("span",{class:y(["prerequisite-alias condition",{satisfied:m.satisfied}])},[k(p(m.exprAlias.replace(/c/,""))+" ",1),t("span",pe,p(m.taskId)+":"+p(m.reqState),1)],2)]))),128))])]))),128))])]),_:1})]),_:1}),l(x,{class:"outputs-panel"},{default:i(()=>[l(h,null,{default:i(()=>[...e[9]||(e[9]=[k(" Outputs ",-1)])]),_:1}),l(g,null,{default:i(()=>[t("ul",null,[(r(!0),u(c,null,_(s.outputs,o=>(r(),u("li",{key:o.label},[t("span",{class:y(["condition",{satisfied:o.satisfied}])},p(o.label),3)]))),128))])]),_:1})]),_:1}),l(x,{class:"completion-panel"},{default:i(()=>[l(h,null,{default:i(()=>[...e[10]||(e[10]=[k(" Completion ",-1)])]),_:1}),l(g,null,{default:i(()=>[t("ul",null,[(r(!0),u(c,null,_(s.formatCompletion(s.completion,s.outputs),([o,m,q],N)=>(r(),u("li",{key:N},[t("span",{class:y(["condition",{satisfied:o,blank:o===null}])},[t("span",{style:Q(`margin-left: ${1*m}em;`)},null,4),k(" "+p(q),1)],2)]))),128))])]),_:1})]),_:1})]),_:1})]),_:1},8,["modelValue"])])}const me=w(se,[["render",fe],["__scopeId","data-v-8bf9d9dc"]]),ke=Y`
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
`;function ce(a){const e=new V(a.id);return{id:a.id,tokens:e,name:e.task,node:a,type:"task",children:[]}}function be(a){const e=new V(a.id);return{id:a.id,name:e.job,tokens:e,node:a,type:"job"}}function E(a,e){a.children=[];for(const n of e.jobs)a.children.push(be(n))}class xe extends K{constructor(e,n){super(),this.task=e,this.taskNode=n}onAdded(e,n,d){Object.assign(this.task,e.taskProxies[0]),Object.assign(this.taskNode,ce(this.task)),E(this.taskNode,this.task)}onUpdated(e,n,d){e?.taskProxies&&Object.assign(this.task,e.taskProxies[0]),E(this.taskNode,this.task)}onPruned(e){}}const he={name:"InfoView",mixins:[W,F],components:{InfoComponent:me},head(){return{title:X("App.workflow",{name:this.workflowName})}},props:{initialOptions:Z},setup(a,{emit:e}){const n=M("requestedTokens",{props:a,emit:e}),d=M("panelExpansion",{props:a,emit:e},[0]);return{requestedTokens:n,panelExpansion:d}},data(){return{requestedCycle:void 0,requestedTask:void 0,task:{},taskNode:{}}},computed:{query(){return new H(ke,{...this.variables,taskID:this.requestedTokens?.relativeID},`info-query-${this._uid}`,[new xe(this.task,this.taskNode)],!0,!1)}},methods:{updatePanelExpansion(a){this.panelExpansion=a}}};function ge(a,e,n,d,f,s){const b=P("InfoComponent");return f.taskNode.id?(r(),C(b,{key:0,task:f.taskNode,panelExpansion:d.panelExpansion,"onUpdate:panelExpansion":s.updatePanelExpansion},null,8,["task","panelExpansion","onUpdate:panelExpansion"])):T("",!0)}const Me=w(he,[["render",ge]]);export{Me as default};
