import{_ as C,b1 as V,b2 as I,b$ as B,c0 as R,ak as U,aq as A,ay as E,c1 as S,c2 as W,e as h,w as l,C as w,bm as q,o as p,g as r,x as P,F as z,r as M,z as n,bl as _,t as i,B as Q,bh as L,D as $,aA as G,l as H,y as X,c3 as b,a4 as Y,a5 as j,a7 as K,j as v,ae as Z,I as ee,V as D,h as F}from"./index-EpcknQ5m.js";import{g as te}from"./graphql-n5gzreXW.js";import{i as J,u as N,a as y}from"./initialOptions-CKJltX86.js";import{T as se,m as ae}from"./filter-DgPx3Jyt.js";import{V as oe,a as ne}from"./VDataTable-BirqjyYH.js";import"./VPagination-KiduL2wZ.js";import"./VTable-hoHcQV6C.js";function x(o,e){return new Date(o)-new Date(e)}function re(o,e){return o-e}const le={name:"TableComponent",emits:[N],props:{tasks:{type:Array,required:!0},initialOptions:J},components:{FlowNumsChip:B,Task:I,Job:V},setup(o,{emit:e}){const d=R(),s=y("sortBy",{props:o,emit:e},[{key:"task.tokens.cycle",order:d.value?"desc":"asc"}]),T=y("page",{props:o,emit:e},1),g=y("itemsPerPage",{props:o,emit:e},50),c=U([{title:"Task",key:"task.name",sortable:!0,sortFunc:b},{title:"Jobs",key:"data-table-expand",sortable:!1},{title:"Cycle Point",key:"task.tokens.cycle",sortable:!0,sortFunc:b},{title:"Platform",key:"latestJob.node.platform",sortable:!0,sortFunc:b},{title:"Job Runner",key:"latestJob.node.jobRunnerName",sortable:!0,sortFunc:b},{title:"Job ID",key:"latestJob.node.jobId",sortable:!0,sortFunc:b},{title:"Submit",key:"latestJob.node.submittedTime",sortable:!0,sortFunc:x},{title:"Start",key:"latestJob.node.startedTime",sortable:!0,sortFunc:x},{title:"Finish",key:"latestJob.node.finishedTime",sortable:!0,sortFunc:x},{title:"Run Time",key:"task.node.task.meanElapsedTime",sortable:!0,sortFunc:re}]);return A(s,f=>{for(const{key:m,order:k}of f){const t=c.value.find(a=>a.key===m);t.sort=(a,u)=>!a&&!u?0:a?u?t.sortFunc(a,u):k==="asc"?-1:1:k==="asc"?1:-1}},{deep:!0,immediate:!0}),{dtMean:W,itemsPerPage:g,page:T,sortBy:s,headers:c,icons:{mdiChevronDown:S},isFlowNone:E,itemsPerPageOptions:[{value:10,title:"10"},{value:20,title:"20"},{value:50,title:"50"},{value:100,title:"100"},{value:200,title:"200"},{value:-1,title:"All"}]}}},ie=["data-cy-task-name"],de={style:{width:"2em"}},me={style:{width:"2em"}},ue={colspan:3},ce={class:"d-flex align-content-center flex-nowrap"},fe={class:"d-flex",style:{"margin-left":"2em"}},ke={class:"ml-2"};function pe(o,e,d,s,T,g){const c=w("Task"),f=w("Job"),m=w("FlowNumsChip"),k=q("command-menu");return p(),h(oe,{headers:s.headers,items:d.tasks,"item-value":"task.id","multi-sort":"","sort-by":s.sortBy,"onUpdate:sortBy":e[0]||(e[0]=t=>s.sortBy=t),"show-expand":"",density:"compact",page:s.page,"onUpdate:page":e[1]||(e[1]=t=>s.page=t),"items-per-page":s.itemsPerPage,"onUpdate:itemsPerPage":e[2]||(e[2]=t=>s.itemsPerPage=t)},{"item.task.name":l(({item:t})=>[n("div",{class:G(["d-flex align-center flex-nowrap",{"flow-none":s.isFlowNone(t.task.node.flowNums)}]),"data-cy-task-name":t.task.name},[n("div",de,[_(r(c,{task:t.task.node,startTime:t.latestJob?.node?.startedTime},null,8,["task","startTime"]),[[k,t.task]])]),n("div",me,[t.latestJob?_((p(),h(f,{key:0,status:t.latestJob.node.state,"previous-state":t.previousJob?.node?.state},null,8,["status","previous-state"])),[[k,t.latestJob]]):X("",!0)]),H(" "+i(t.task.name)+" ",1),r(m,{flowNums:t.task.node.flowNums,class:"ml-2"},null,8,["flowNums"])],10,ie)]),"item.task.node.task.meanElapsedTime":l(({item:t})=>[n("td",null,i(s.dtMean(t.task)),1)]),"item.data-table-expand":l(({item:t,internalItem:a,toggleExpand:u,isExpanded:O})=>[r(Q,{onClick:he=>u(a),icon:"",variant:"text",size:"small",style:L({visibility:(t.task.children||[]).length?null:"hidden",transform:O(a)?"rotate(180deg)":null})},{default:l(()=>[r($,{icon:s.icons.mdiChevronDown,size:"large"},null,8,["icon"])]),_:2},1032,["onClick","style"])]),"expanded-row":l(({item:t})=>[(p(!0),P(z,null,M(t.task.children,(a,u)=>(p(),P("tr",{key:a.id,class:"expanded-row bg-grey-lighten-5"},[n("td",ue,[n("div",ce,[n("div",fe,[_((p(),h(f,{key:`${a.id}-summary-${u}`,status:a.node.state},null,8,["status"])),[[k,a]]),n("span",ke,"#"+i(a.node.submitNum),1)])])]),n("td",null,i(a.node.platform),1),n("td",null,i(a.node.jobRunnerName),1),n("td",null,i(a.node.jobId),1),n("td",null,i(a.node.submittedTime),1),n("td",null,i(a.node.startedTime),1),n("td",null,i(a.node.finishedTime),1),e[3]||(e[3]=n("td",null,null,-1))]))),128))]),bottom:l(()=>[r(ne,{itemsPerPageOptions:s.itemsPerPageOptions},null,8,["itemsPerPageOptions"])]),_:1},8,["headers","items","sort-by","page","items-per-page"])}const be=C(le,[["render",pe]]),we=ee`
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
`,ye={name:"Table",mixins:[te,K],components:{TableComponent:be,TaskFilter:se},emits:[N],props:{initialOptions:J},setup(o,{emit:e}){const d=y("tasksFilter",{props:o,emit:e},{});return{dataTableOptions:y("dataTableOptions",{props:o,emit:e}),tasksFilter:d}},computed:{...j("workflows",["cylcTree"]),...Y("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},tasks(){const o=[];for(const e of this.workflows)for(const d of e.children)for(const s of d.children)o.push({task:s,latestJob:s.children[0],previousJob:s.children[1]});return o},query(){return new Z(we,this.variables,"workflow",[],!0,!0)},filteredTasks(){return this.tasks.filter(({task:o})=>ae(o,this.tasksFilter.id,this.tasksFilter.states))}}},ge={class:"h-100"};function Te(o,e,d,s,T,g){const c=w("TaskFilter"),f=w("TableComponent");return p(),P("div",ge,[r(v,{fluid:"",class:"c-table ma-0 pa-2 h-100 flex-column d-flex"},{default:l(()=>[r(D,{"no-gutters":"",class:"d-flex flex-wrap flex-grow-0"},{default:l(()=>[r(F,null,{default:l(()=>[r(c,{modelValue:s.tasksFilter,"onUpdate:modelValue":e[0]||(e[0]=m=>s.tasksFilter=m)},null,8,["modelValue"])]),_:1})]),_:1}),r(D,{"no-gutters":"",class:"flex-grow-1 position-relative"},{default:l(()=>[r(F,{cols:"12",class:"mh-100 position-relative"},{default:l(()=>[r(v,{fluid:"",class:"ma-0 pa-0 w-100 h-100 left-0 top-0 position-absolute pt-2"},{default:l(()=>[r(f,{tasks:g.filteredTasks,"initial-options":s.dataTableOptions,"onUpdate:initialOptions":e[1]||(e[1]=m=>s.dataTableOptions=m)},null,8,["tasks","initial-options"])]),_:1})]),_:1})]),_:1})]),_:1})])}const Je=C(ye,[["render",Te]]);export{Je as default};
