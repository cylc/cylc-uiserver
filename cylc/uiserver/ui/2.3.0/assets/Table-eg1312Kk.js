import{bz as I,db as $,cx as R,dE as A,dF as B,dG as f,dH as E,aM as c,aN as S,az as i,o as b,bs as l,z as n,bD as x,p as D,bE as J,bC as C,r as o,bu as h,a_ as r,b_ as O,al as U,c5 as z,q as g,aK as M,F as q,c7 as W,cf as Q,c8 as G,ch as H,ci as L,cg as j}from"./index-p5QwxXYb.js";import{g as K}from"./graphql-1_B3k2Rp.js";import{T as Y,m as X}from"./TaskFilter-HeF76y-C.js";function v(e,t){return e=(e??"")===""?1/0:new Date(e).getTime(),t=(t??"")===""?1/0:new Date(t).getTime(),e===t?0:e-t}const Z={name:"TableComponent",props:{tasks:{type:Array,required:!0},filterable:{type:Boolean,default:!0}},components:{Task:$,Job:R,TaskFilter:Y},data(){return{itemsPerPage:50,sortBy:[{key:"task.tokens.cycle",order:A().value?"desc":"asc"}],tasksFilter:{}}},computed:{filteredTasks(){return this.tasks.filter(({task:e})=>X(e,this.tasksFilter.id,this.tasksFilter.states))}},methods:{dtMean:B},headers:[{title:"Task",key:"task.name",sortable:!0,sort:f},{title:"Jobs",key:"data-table-expand",sortable:!1},{title:"Cycle Point",key:"task.tokens.cycle",sortable:!0,sort:(e,t)=>f(String(e??""),String(t??""))},{title:"Platform",key:"latestJob.node.platform",sortable:!0,sort:(e,t)=>f(e??"",t??"")},{title:"Job Runner",key:"latestJob.node.jobRunnerName",sortable:!0,sort:(e,t)=>f(e??"",t??"")},{title:"Job ID",key:"latestJob.node.jobId",sortable:!0,sort:(e,t)=>f(e??"",t??"")},{title:"Submit",key:"latestJob.node.submittedTime",sortable:!0,sort:(e,t)=>v(e??"",t??"")},{title:"Start",key:"latestJob.node.startedTime",sortable:!0,sort:(e,t)=>v(e??"",t??"")},{title:"Finish",key:"latestJob.node.finishedTime",sortable:!0,sort:(e,t)=>v(e??"",t??"")},{title:"Run Time",key:"task.node.task.meanElapsedTime",sortable:!0,sort:(e,t)=>parseInt(e??0)-parseInt(t??0)}],icons:{mdiChevronDown:E},itemsPerPageOptions:[{value:10,title:"10"},{value:20,title:"20"},{value:50,title:"50"},{value:100,title:"100"},{value:200,title:"200"},{value:-1,title:"All"}]},ee={class:"d-flex align-content-center flex-nowrap"},te={style:{width:"2em"}},se={style:{width:"2em"}},ae={colspan:3},oe={class:"d-flex align-content-center flex-nowrap"},le={class:"d-flex",style:{"margin-left":"2em"}},ne={class:"ml-2"},re=o("td",null,null,-1);function ie(e,t,k,m,d,p){const y=c("TaskFilter"),F=c("Task"),T=c("Job"),N=c("v-data-table-footer"),V=c("v-data-table"),w=S("cylc-object");return i(),b(C,{fluid:"",class:"c-table ma-0 pa-2 h-100 flex-column d-flex"},{default:l(()=>[n(J,{"no-gutters":"",class:"d-flex flex-wrap flex-grow-0"},{default:l(()=>[k.filterable?(i(),b(x,{key:0,class:""},{default:l(()=>[n(y,{modelValue:d.tasksFilter,"onUpdate:modelValue":t[0]||(t[0]=s=>d.tasksFilter=s)},null,8,["modelValue"])]),_:1})):D("",!0)]),_:1}),n(J,{"no-gutters":"",class:"flex-grow-1 position-relative"},{default:l(()=>[n(x,{cols:"12",class:"mh-100 position-relative"},{default:l(()=>[n(C,{fluid:"",class:"ma-0 pa-0 w-100 h-100 left-0 top-0 position-absolute pt-2"},{default:l(()=>[n(V,{headers:e.$options.headers,items:p.filteredTasks,"multi-sort":"","sort-by":d.sortBy,"show-expand":"",density:"compact","items-per-page":d.itemsPerPage,"onUpdate:itemsPerPage":t[1]||(t[1]=s=>d.itemsPerPage=s)},{"item.task.name":l(({item:s})=>{var a,u,_,P;return[o("div",ee,[o("div",te,[h(n(F,{task:s.value.task.node,startTime:(u=(a=s.value.latestJob)==null?void 0:a.node)==null?void 0:u.startedTime},null,8,["task","startTime"]),[[w,s.value.task]])]),o("div",se,[s.value.latestJob?h((i(),b(T,{key:0,status:s.value.latestJob.node.state,"previous-state":(P=(_=s.value.previousJob)==null?void 0:_.node)==null?void 0:P.state},null,8,["status","previous-state"])),[[w,s.value.latestJob]]):D("",!0)]),o("div",null,r(s.value.task.name),1)])]}),"item.task.node.task.meanElapsedTime":l(({item:s})=>[o("td",null,r(p.dtMean(s.value.task)),1)]),"item.data-table-expand":l(({item:s,toggleExpand:a,isExpanded:u})=>[n(O,{onClick:_=>a(s),icon:"",variant:"text",size:"small",style:U({visibility:(s.value.task.children||[]).length?null:"hidden",transform:u(s)?"rotate(180deg)":null})},{default:l(()=>[n(z,{icon:e.$options.icons.mdiChevronDown,size:"large"},null,8,["icon"])]),_:2},1032,["onClick","style"])]),"expanded-row":l(({item:s})=>[(i(!0),g(q,null,M(s.value.task.children,(a,u)=>(i(),g("tr",{key:a.id,class:"expanded-row bg-grey-lighten-5"},[o("td",ae,[o("div",oe,[o("div",le,[h((i(),b(T,{key:`${a.id}-summary-${u}`,status:a.node.state},null,8,["status"])),[[w,a]]),o("span",ne,"#"+r(a.node.submitNum),1)])])]),o("td",null,r(a.node.platform),1),o("td",null,r(a.node.jobRunnerName),1),o("td",null,r(a.node.jobId),1),o("td",null,r(a.node.submittedTime),1),o("td",null,r(a.node.startedTime),1),o("td",null,r(a.node.finishedTime),1),re]))),128))]),bottom:l(()=>[n(N,{itemsPerPageOptions:e.$options.itemsPerPageOptions},null,8,["itemsPerPageOptions"])]),_:1},8,["headers","items","sort-by","items-per-page"])]),_:1})]),_:1})]),_:1})]),_:1})}const de=I(Z,[["render",ie]]),ue=W`
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
  cyclePoints: familyProxies (ids: ["*/root"]) {
    ...CyclePointData
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
  cyclePoints: familyProxies (ids: ["*/root"]) {
    ...CyclePointData
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

fragment CyclePointData on FamilyProxy {
  __typename
  id
  state
  ancestors {
    name
  }
  childTasks {
    id
  }
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
`,ce={name:"Table",mixins:[K,Q],components:{TableComponent:de},head(){return{title:G("App.workflow",{name:this.workflowName})}},computed:{...H("workflows",["cylcTree"]),...L("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},tasks(){const e=[];for(const t of this.workflows)for(const k of t.children)for(const m of k.children)e.push({task:m,latestJob:m.children[0],previousJob:m.children[1]});return e},query(){return new j(ue,this.variables,"workflow",[],!0,!0)}}},me={class:"h-100"};function fe(e,t,k,m,d,p){const y=c("TableComponent");return i(),g("div",me,[n(y,{tasks:p.tasks,ref:"table0",key:"table0"},null,8,["tasks"])])}const ye=I(ce,[["render",fe]]);export{ye as default};
