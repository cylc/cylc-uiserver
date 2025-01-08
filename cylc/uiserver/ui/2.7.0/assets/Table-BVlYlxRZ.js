import{_ as N,c2 as I,bh as B,bi as R,c3 as U,Q as A,c4 as w,c5 as E,c6 as S,c7 as q,aJ as M,A as b,bw as Q,h as p,j as x,w as l,C as n,bx as P,k as r,H as W,m as z,t as d,aQ as G,E as H,bq as L,G as $,B as D,r as Y,I as j,J as K,$ as X,a1 as Z,a2 as ee,a0 as te,V as F,p as J,n as C}from"./index-Hyq34tSM.js";import{g as se}from"./graphql-D8b4q-7X.js";import{u as O,i as V,a as y}from"./initialOptions-BLDeg43d.js";import{T as ae,m as oe}from"./filter-gCYsvdqm.js";import{a as ne,V as re}from"./VDataTable-D1WRK44R.js";import"./VPagination-D6i7DgtD.js";function v(o,t){return new Date(o)-new Date(t)}function le(o,t){return o-t}const ie={name:"TableComponent",emits:[O],props:{tasks:{type:Array,required:!0},initialOptions:V},components:{FlowNumsChip:I,Task:B,Job:R},setup(o,{emit:t}){const u=U(),s=y("sortBy",{props:o,emit:t},[{key:"task.tokens.cycle",order:u.value?"desc":"asc"}]),T=y("page",{props:o,emit:t},1),_=y("itemsPerPage",{props:o,emit:t},50),c=A([{title:"Task",key:"task.name",sortable:!0,sortFunc:w},{title:"Jobs",key:"data-table-expand",sortable:!1},{title:"Cycle Point",key:"task.tokens.cycle",sortable:!0,sortFunc:w},{title:"Platform",key:"latestJob.node.platform",sortable:!0,sortFunc:w},{title:"Job Runner",key:"latestJob.node.jobRunnerName",sortable:!0,sortFunc:w},{title:"Job ID",key:"latestJob.node.jobId",sortable:!0,sortFunc:w},{title:"Submit",key:"latestJob.node.submittedTime",sortable:!0,sortFunc:v},{title:"Start",key:"latestJob.node.startedTime",sortable:!0,sortFunc:v},{title:"Finish",key:"latestJob.node.finishedTime",sortable:!0,sortFunc:v},{title:"Run Time",key:"task.node.task.meanElapsedTime",sortable:!0,sortFunc:le}]);return E(s,f=>{for(const{key:m,order:k}of f){const e=c.value.find(a=>a.key===m);e.sort=(a,i)=>!a&&!i?0:a?i?e.sortFunc(a,i):k==="asc"?-1:1:k==="asc"?1:-1}},{deep:!0,immediate:!0}),{dtMean:S,itemsPerPage:_,page:T,sortBy:s,headers:c,icons:{mdiChevronDown:q},isFlowNone:M,itemsPerPageOptions:[{value:10,title:"10"},{value:20,title:"20"},{value:50,title:"50"},{value:100,title:"100"},{value:200,title:"200"},{value:-1,title:"All"}]}}},de=["data-cy-task-name"],ue={style:{width:"2em"}},me={style:{width:"2em"}},ce={colspan:3},fe={class:"d-flex align-content-center flex-nowrap"},ke={class:"d-flex",style:{"margin-left":"2em"}},pe={class:"ml-2"},we=n("td",null,null,-1);function be(o,t,u,s,T,_){const c=b("Task"),f=b("Job"),m=b("FlowNumsChip"),k=Q("command-menu");return p(),x(re,{headers:s.headers,items:u.tasks,"item-value":"task.id","multi-sort":"","sort-by":s.sortBy,"onUpdate:sortBy":t[0]||(t[0]=e=>s.sortBy=e),"show-expand":"",density:"compact",page:s.page,"onUpdate:page":t[1]||(t[1]=e=>s.page=e),"items-per-page":s.itemsPerPage,"onUpdate:itemsPerPage":t[2]||(t[2]=e=>s.itemsPerPage=e)},{"item.task.name":l(({item:e})=>{var a,i,h,g;return[n("div",{class:G(["d-flex align-center flex-nowrap",{"flow-none":s.isFlowNone(e.task.node.flowNums)}]),"data-cy-task-name":e.task.name},[n("div",ue,[P(r(c,{task:e.task.node,startTime:(i=(a=e.latestJob)==null?void 0:a.node)==null?void 0:i.startedTime},null,8,["task","startTime"]),[[k,e.task]])]),n("div",me,[e.latestJob?P((p(),x(f,{key:0,status:e.latestJob.node.state,"previous-state":(g=(h=e.previousJob)==null?void 0:h.node)==null?void 0:g.state},null,8,["status","previous-state"])),[[k,e.latestJob]]):W("",!0)]),z(" "+d(e.task.name)+" ",1),r(m,{flowNums:e.task.node.flowNums,class:"ml-2"},null,8,["flowNums"])],10,de)]}),"item.task.node.task.meanElapsedTime":l(({item:e})=>[n("td",null,d(s.dtMean(e.task)),1)]),"item.data-table-expand":l(({item:e,internalItem:a,toggleExpand:i,isExpanded:h})=>[r($,{onClick:g=>i(a),icon:"",variant:"text",size:"small",style:L({visibility:(e.task.children||[]).length?null:"hidden",transform:h(a)?"rotate(180deg)":null})},{default:l(()=>[r(H,{icon:s.icons.mdiChevronDown,size:"large"},null,8,["icon"])]),_:2},1032,["onClick","style"])]),"expanded-row":l(({item:e})=>[(p(!0),D(j,null,Y(e.task.children,(a,i)=>(p(),D("tr",{key:a.id,class:"expanded-row bg-grey-lighten-5"},[n("td",ce,[n("div",fe,[n("div",ke,[P((p(),x(f,{key:`${a.id}-summary-${i}`,status:a.node.state},null,8,["status"])),[[k,a]]),n("span",pe,"#"+d(a.node.submitNum),1)])])]),n("td",null,d(a.node.platform),1),n("td",null,d(a.node.jobRunnerName),1),n("td",null,d(a.node.jobId),1),n("td",null,d(a.node.submittedTime),1),n("td",null,d(a.node.startedTime),1),n("td",null,d(a.node.finishedTime),1),we]))),128))]),bottom:l(()=>[r(ne,{itemsPerPageOptions:s.itemsPerPageOptions},null,8,["itemsPerPageOptions"])]),_:1},8,["headers","items","sort-by","page","items-per-page"])}const ye=N(ie,[["render",be]]),_e=K`
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
  task {
    meanElapsedTime
  }
  firstParent {
    id
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
  state
  submitNum
}
`,he={name:"Table",mixins:[se,X],components:{TableComponent:ye,TaskFilter:ae},emits:[O],props:{initialOptions:V},setup(o,{emit:t}){const u=y("tasksFilter",{props:o,emit:t},{});return{dataTableOptions:y("dataTableOptions",{props:o,emit:t}),tasksFilter:u}},computed:{...Z("workflows",["cylcTree"]),...ee("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},tasks(){const o=[];for(const t of this.workflows)for(const u of t.children)for(const s of u.children)o.push({task:s,latestJob:s.children[0],previousJob:s.children[1]});return o},query(){return new te(_e,this.variables,"workflow",[],!0,!0)},filteredTasks(){return this.tasks.filter(({task:o})=>oe(o,this.tasksFilter.id,this.tasksFilter.states))}}},Te={class:"h-100"};function ge(o,t,u,s,T,_){const c=b("TaskFilter"),f=b("TableComponent");return p(),D("div",Te,[r(F,{fluid:"",class:"c-table ma-0 pa-2 h-100 flex-column d-flex"},{default:l(()=>[r(J,{"no-gutters":"",class:"d-flex flex-wrap flex-grow-0"},{default:l(()=>[r(C,null,{default:l(()=>[r(c,{modelValue:s.tasksFilter,"onUpdate:modelValue":t[0]||(t[0]=m=>s.tasksFilter=m)},null,8,["modelValue"])]),_:1})]),_:1}),r(J,{"no-gutters":"",class:"flex-grow-1 position-relative"},{default:l(()=>[r(C,{cols:"12",class:"mh-100 position-relative"},{default:l(()=>[r(F,{fluid:"",class:"ma-0 pa-0 w-100 h-100 left-0 top-0 position-absolute pt-2"},{default:l(()=>[r(f,{tasks:_.filteredTasks,"initial-options":s.dataTableOptions,"onUpdate:initialOptions":t[1]||(t[1]=m=>s.dataTableOptions=m)},null,8,["tasks","initial-options"])]),_:1})]),_:1})]),_:1})]),_:1})])}const Ce=N(he,[["render",ge]]);export{Ce as default};
