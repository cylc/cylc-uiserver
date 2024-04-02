import{bE as C,cR as F,ci as V,dw as N,aM as v,dx as R,dy as k,dz as $,aR as b,aS as O,aE as m,s as _,bx as l,v as o,bz as T,I as r,t as A,b3 as i,bR as S,aq as E,bT as U,u as P,aP as B,F as M,bU as q,c0 as z,bV as W,c2 as Q,c3 as H,c1 as L,bH as x,bJ as D,bI as J}from"./index-C2AHI-HK.js";import{g as j}from"./graphql-BScASb0Q.js";import{i as G,a as Y}from"./initialOptions-DCNtfDfN.js";import{T as K,m as X}from"./TaskFilter-Blo6nLre.js";import{a as Z,V as ee}from"./VDataTable-BEEIiNy3.js";function g(e,t){return e=(e??"")===""?1/0:new Date(e).getTime(),t=(t??"")===""?1/0:new Date(t).getTime(),e===t?0:e-t}const te={name:"TableComponent",props:{tasks:{type:Array,required:!0}},components:{Task:F,Job:V},setup(){const e=N();return{itemsPerPage:v(50),sortBy:v([{key:"task.tokens.cycle",order:e.value?"desc":"asc"}])}},methods:{dtMean:R},headers:[{title:"Task",key:"task.name",sortable:!0,sort:k},{title:"Jobs",key:"data-table-expand",sortable:!1},{title:"Cycle Point",key:"task.tokens.cycle",sortable:!0,sort:(e,t)=>k(String(e??""),String(t??""))},{title:"Platform",key:"latestJob.node.platform",sortable:!0,sort:(e,t)=>k(e??"",t??"")},{title:"Job Runner",key:"latestJob.node.jobRunnerName",sortable:!0,sort:(e,t)=>k(e??"",t??"")},{title:"Job ID",key:"latestJob.node.jobId",sortable:!0,sort:(e,t)=>k(e??"",t??"")},{title:"Submit",key:"latestJob.node.submittedTime",sortable:!0,sort:(e,t)=>g(e??"",t??"")},{title:"Start",key:"latestJob.node.startedTime",sortable:!0,sort:(e,t)=>g(e??"",t??"")},{title:"Finish",key:"latestJob.node.finishedTime",sortable:!0,sort:(e,t)=>g(e??"",t??"")},{title:"Run Time",key:"task.node.task.meanElapsedTime",sortable:!0,sort:(e,t)=>parseInt(e??0)-parseInt(t??0)}],icons:{mdiChevronDown:$},itemsPerPageOptions:[{value:10,title:"10"},{value:20,title:"20"},{value:50,title:"50"},{value:100,title:"100"},{value:200,title:"200"},{value:-1,title:"All"}]},se={class:"d-flex align-content-center flex-nowrap"},ae={style:{width:"2em"}},oe={style:{width:"2em"}},re={colspan:3},le={class:"d-flex align-content-center flex-nowrap"},ne={class:"d-flex",style:{"margin-left":"2em"}},ie={class:"ml-2"},de=o("td",null,null,-1);function me(e,t,u,n,I,w){const h=b("Task"),f=b("Job"),c=O("cylc-object");return m(),_(ee,{headers:e.$options.headers,items:u.tasks,"item-value":"task.id","multi-sort":"","sort-by":n.sortBy,"show-expand":"",density:"compact","items-per-page":n.itemsPerPage,"onUpdate:itemsPerPage":t[0]||(t[0]=a=>n.itemsPerPage=a)},{"item.task.name":l(({item:a})=>{var s,d,p,y;return[o("div",se,[o("div",ae,[T(r(h,{task:a.task.node,startTime:(d=(s=a.latestJob)==null?void 0:s.node)==null?void 0:d.startedTime},null,8,["task","startTime"]),[[c,a.task]])]),o("div",oe,[a.latestJob?T((m(),_(f,{key:0,status:a.latestJob.node.state,"previous-state":(y=(p=a.previousJob)==null?void 0:p.node)==null?void 0:y.state},null,8,["status","previous-state"])),[[c,a.latestJob]]):A("",!0)]),o("div",null,i(a.task.name),1)])]}),"item.task.node.task.meanElapsedTime":l(({item:a})=>[o("td",null,i(w.dtMean(a.task)),1)]),"item.data-table-expand":l(({item:a,internalItem:s,toggleExpand:d,isExpanded:p})=>[r(U,{onClick:y=>d(s),icon:"",variant:"text",size:"small",style:E({visibility:(a.task.children||[]).length?null:"hidden",transform:p(s)?"rotate(180deg)":null})},{default:l(()=>[r(S,{icon:e.$options.icons.mdiChevronDown,size:"large"},null,8,["icon"])]),_:2},1032,["onClick","style"])]),"expanded-row":l(({item:a})=>[(m(!0),P(M,null,B(a.task.children,(s,d)=>(m(),P("tr",{key:s.id,class:"expanded-row bg-grey-lighten-5"},[o("td",re,[o("div",le,[o("div",ne,[T((m(),_(f,{key:`${s.id}-summary-${d}`,status:s.node.state},null,8,["status"])),[[c,s]]),o("span",ie,"#"+i(s.node.submitNum),1)])])]),o("td",null,i(s.node.platform),1),o("td",null,i(s.node.jobRunnerName),1),o("td",null,i(s.node.jobId),1),o("td",null,i(s.node.submittedTime),1),o("td",null,i(s.node.startedTime),1),o("td",null,i(s.node.finishedTime),1),de]))),128))]),bottom:l(()=>[r(Z,{itemsPerPageOptions:e.$options.itemsPerPageOptions},null,8,["itemsPerPageOptions"])]),_:1},8,["headers","items","sort-by","items-per-page"])}const ue=C(te,[["render",me]]),ce=q`
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
`,ke={name:"Table",mixins:[j,z],components:{TableComponent:ue,TaskFilter:K},head(){return{title:W("App.workflow",{name:this.workflowName})}},props:{initialOptions:G},setup(e,{emit:t}){return{tasksFilter:Y("tasksFilter",{props:e,emit:t},{})}},computed:{...Q("workflows",["cylcTree"]),...H("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},tasks(){const e=[];for(const t of this.workflows)for(const u of t.children)for(const n of u.children)e.push({task:n,latestJob:n.children[0],previousJob:n.children[1]});return e},query(){return new L(ce,this.variables,"workflow",[],!0,!0)},filteredTasks(){return this.tasks.filter(({task:e})=>X(e,this.tasksFilter.id,this.tasksFilter.states))}}},fe={class:"h-100"};function pe(e,t,u,n,I,w){const h=b("TaskFilter"),f=b("TableComponent");return m(),P("div",fe,[r(x,{fluid:"",class:"c-table ma-0 pa-2 h-100 flex-column d-flex"},{default:l(()=>[r(D,{"no-gutters":"",class:"d-flex flex-wrap flex-grow-0"},{default:l(()=>[r(J,null,{default:l(()=>[r(h,{modelValue:n.tasksFilter,"onUpdate:modelValue":t[0]||(t[0]=c=>n.tasksFilter=c)},null,8,["modelValue"])]),_:1})]),_:1}),r(D,{"no-gutters":"",class:"flex-grow-1 position-relative"},{default:l(()=>[r(J,{cols:"12",class:"mh-100 position-relative"},{default:l(()=>[r(x,{fluid:"",class:"ma-0 pa-0 w-100 h-100 left-0 top-0 position-absolute pt-2"},{default:l(()=>[r(f,{tasks:w.filteredTasks},null,8,["tasks"])]),_:1})]),_:1})]),_:1})]),_:1})])}const Te=C(ke,[["render",pe]]);export{Te as default};
