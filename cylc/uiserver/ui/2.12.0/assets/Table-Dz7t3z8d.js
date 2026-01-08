import{c6 as G,aj as L,p as Q,c7 as R,e as D,w as f,c8 as J,bS as c,c9 as S,bq as Z,o as w,g as d,v as V,F as H,r as X,y as n,b8 as B,bp as O,b2 as E,t as p,ca as x,f as A,A as Y,bl as K,C as j,cb as tt,az as et,ax as at,k as st,cc as M,cd as U,b3 as ot,x as nt,ce as it,cf as h,_ as rt,a3 as lt,a4 as dt,a6 as ut,ad as mt,H as ct,B as $}from"./index-Dk_oQcLS.js";import{g as ft}from"./graphql-Dr9bN1Q1.js";import{u as z,i as W,a as g}from"./initialOptions-BnNLz-ak.js";import{g as kt,m as pt,a as bt}from"./filter-DRtrMOfy.js";import{V as wt}from"./ViewToolbar-Ben90_oc.js";import{V as Tt,a as yt}from"./VDataTable-CLZT2yA6.js";import{V as ht}from"./VContainer-COcUMfSR.js";import"./VPagination-CxvzufF_.js";function N(a,s){return new Date(a)-new Date(s)}function gt(a,s){return a-s}const vt=["data-cy-task-name"],Ft={colspan:3},xt={class:"d-flex align-content-center flex-nowrap"},Dt={__name:"Table",props:{tasks:{type:Array,required:!0},initialOptions:W},emits:[z],setup(a,{emit:s}){const u=s,i=a,C=G(),m=g("sortBy",{props:i,emit:u},[{key:"task.tokens.cycle",order:C.value?"desc":"asc"}]),T=g("page",{props:i,emit:u},1),y=g("itemsPerPage",{props:i,emit:u},50),v=L([{title:"Task",key:"task.name",sortFunc:h},{title:"Jobs",key:"data-table-expand"},{title:"Cycle Point",key:"task.tokens.cycle",sortFunc:h},{title:"Platform",key:"latestJob.node.platform",sortFunc:h},{title:"Job Runner",key:"latestJob.node.jobRunnerName",sortFunc:h},{title:"Job ID",key:"latestJob.node.jobId",sortFunc:h},{title:"Submit",key:"latestJob.node.submittedTime",sortFunc:N},{title:"Start",key:"latestJob.node.startedTime",sortFunc:N},{title:"Finish",key:"latestJob.node.finishedTime",sortRaw(r,o){const l=r.latestJob?.node,t=o.latestJob?.node;return P("latestJob.node.finishedTime",N,l?.finishedTime||l?.estimatedFinishTime,t?.finishedTime||t?.estimatedFinishTime)}},{title:"Run Time",key:"task.node.task.meanElapsedTime",sortRaw(r,o){const l=_.value.get(r.task.id),t=_.value.get(o.task.id);return P("task.node.task.meanElapsedTime",gt,l?.actual||l?.estimate,t?.actual||t?.estimate)}}]);function P(r,o,l,t){const e=S(l),k=S(t);if(e&&k)return o(l,t);if(!e&&!k)return 0;const{order:b}=m.value.find(I=>I.key===r);if(!e)return b==="asc"?1:-1;if(!k)return b==="asc"?-1:1}for(const r of v.value)r.sortFunc&&(r.sort=(o,l)=>P(r.key,r.sortFunc,o,l));const _=Q(()=>new Map(i.tasks.map(({task:r,latestJob:o})=>[r.id,{actual:R(o?.node),estimate:r.node?.task?.meanElapsedTime}]))),F={class:["d-flex","align-center"],style:{width:"2em"}},q=[{value:10,title:"10"},{value:20,title:"20"},{value:50,title:"50"},{value:100,title:"100"},{value:200,title:"200"},{value:-1,title:"All"}];return(r,o)=>{const l=Z("command-menu");return w(),D(Tt,{headers:v.value,items:a.tasks,"item-value":"task.id","multi-sort":"","sort-by":c(m),"onUpdate:sortBy":o[0]||(o[0]=t=>J(m)?m.value=t:null),"show-expand":"",density:"compact",page:c(T),"onUpdate:page":o[1]||(o[1]=t=>J(T)?T.value=t:null),"items-per-page":c(y),"onUpdate:itemsPerPage":o[2]||(o[2]=t=>J(y)?y.value=t:null),"fixed-header":""},{"item.task.name":f(({item:t})=>[n("div",{class:et(["d-flex align-center flex-nowrap",{"flow-none":c(at)(t.task.node.flowNums)}]),"data-cy-task-name":t.task.name},[n("div",M(U(F)),[O(d(ot,{task:t.task.node,startTime:t.latestJob?.node?.startedTime},null,8,["task","startTime"]),[[l,t.task]])],16),n("div",M(U(F)),[t.latestJob?O((w(),D(E,{key:0,status:t.latestJob.node.state,"previous-state":t.previousJob?.node?.state},null,8,["status","previous-state"])),[[l,t.latestJob]]):nt("",!0)],16),st(" "+p(t.task.name)+" ",1),d(it,{flowNums:t.task.node.flowNums,class:"ml-2"},null,8,["flowNums"])],10,vt)]),"item.latestJob.node.finishedTime":f(({item:t,value:e})=>[d(x,{actual:e,estimate:t.latestJob?.node.estimatedFinishTime},null,8,["actual","estimate"])]),"item.task.node.task.meanElapsedTime":f(({item:t})=>[d(x,B(_.value.get(t.task.id),{formatter:e=>c(A)(e,{allowZeros:!0}),tooltip:"Mean for this task"}),null,16,["formatter"])]),"item.data-table-expand":f(({item:t,internalItem:e,toggleExpand:k,isExpanded:b})=>[d(Y,{onClick:I=>k(e),icon:"",variant:"text",size:"small",style:K({visibility:(t.task.children||[]).length?null:"hidden",transform:b(e)?"rotate(180deg)":null})},{default:f(()=>[d(j,{icon:c(tt),size:"large"},null,8,["icon"])]),_:1},8,["onClick","style"])]),"expanded-row":f(({item:t})=>[(w(!0),V(H,null,X(t.task.children,(e,k)=>(w(),V("tr",{key:e.id,class:"expanded-row bg-grey-lighten-5"},[n("td",Ft,[n("div",xt,[n("div",B({ref_for:!0},F,{style:{marginLeft:F.style.width}}),[O((w(),D(E,{key:`${e.id}-summary-${k}`,status:e.node.state},null,8,["status"])),[[l,e]])],16),n("span",null,"#"+p(e.node.submitNum),1)])]),n("td",null,p(e.node.platform),1),n("td",null,p(e.node.jobRunnerName),1),n("td",null,p(e.node.jobId),1),n("td",null,p(e.node.submittedTime),1),n("td",null,p(e.node.startedTime),1),n("td",null,[d(x,{actual:e.node.finishedTime,estimate:e.node.estimatedFinishTime},null,8,["actual","estimate"])]),n("td",null,[d(x,{actual:c(R)(e.node),estimate:t.task.node?.task.meanElapsedTime,formatter:b=>c(A)(b,{allowZeros:!0}),tooltip:"Mean"},null,8,["actual","estimate","formatter"])])]))),128))]),bottom:f(()=>[d(yt,{itemsPerPageOptions:q})]),_:1},8,["headers","items","sort-by","page","items-per-page"])}}},Pt=ct`
subscription Workflow ($workflowId: ID) {
  deltas (workflows: [$workflowId]) {
    id
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
}

fragment AddedDelta on Added {
  workflow {
    ...WorkflowData
  }
  taskProxies {
    ...TaskProxyData
  }
  jobs {
    ...JobData
  }
}

fragment UpdatedDelta on Updated {
  workflow {
    ...WorkflowData
  }
  taskProxies {
    ...TaskProxyData
  }
  jobs {
    ...JobData
  }
}

fragment PrunedDelta on Pruned {
  workflow
  familyProxies
  taskProxies
  jobs
}

fragment WorkflowData on Workflow {
  id
  reloaded
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
    meanElapsedTime
  }
  firstParent {
    id
  }
  runtime {
    runMode
  }
  flowNums
}

fragment JobData on Job {
  id
  jobRunnerName
  jobId
  platform
  startedTime
  submittedTime
  finishedTime
  estimatedFinishTime
  state
  submitNum
}
`,_t={name:"Table",mixins:[ft,ut],components:{TableComponent:Dt,ViewToolbar:wt},emits:[z],props:{initialOptions:W},setup(a,{emit:s}){const u=g("tasksFilter",{props:a,emit:s},{});return{dataTableOptions:g("dataTableOptions",{props:a,emit:s}),tasksFilter:u}},computed:{...dt("workflows",["cylcTree"]),...lt("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},tasks(){const a=[];for(const s of this.workflows)for(const u of s.children)for(const i of u.children)a.push({task:i,latestJob:i.children[0],previousJob:i.children[1]});return a},query(){return new mt(Pt,this.variables,"workflow",[],!0,!0)},filteredTasks(){const[a,s,u]=kt(this.tasksFilter.states?.length?this.tasksFilter.states:[]);return this.tasks.filter(({task:i})=>pt(i,bt(this.tasksFilter.id),a,s,u))},controlGroups(){return[{title:"Filter",controls:[{title:"Filter By ID",action:"taskIDFilter",key:"taskIDFilter",value:this.tasksFilter.id},{title:"Filter By State",action:"taskStateFilter",key:"taskStateFilter",value:this.tasksFilter.states}]}]}},methods:{setOption(a,s){a==="taskStateFilter"?this.tasksFilter.states=s:a==="taskIDFilter"?this.tasksFilter.id=s:this[a]=s}}},Jt={class:"overflow-hidden"};function Ot(a,s,u,i,C,m){const T=$("ViewToolbar"),y=$("TableComponent");return w(),D(ht,{fluid:"",class:"c-table pa-2 pb-0 h-100 flex-column d-flex"},{default:f(()=>[d(T,{groups:m.controlGroups,onSetOption:m.setOption},null,8,["groups","onSetOption"]),n("div",Jt,[d(y,{tasks:m.filteredTasks,"initial-options":i.dataTableOptions,"onUpdate:initialOptions":s[0]||(s[0]=v=>i.dataTableOptions=v),class:"mh-100"},null,8,["tasks","initial-options"])])]),_:1})}const At=rt(_t,[["render",Ot]]);export{At as default};
