import{_ as C,d7 as I,cy as N,dF as B,Q as R,dG as b,ck as U,dH as A,dI as E,A as T,bL as S,h as p,j as h,w as i,C as n,cq as P,k as l,H as q,t as u,E as M,bn as W,G as Q,B as x,r as z,I as G,J as H,$ as L,a1 as $,a2 as Y,a0 as j,V as D,p as F,n as J}from"./index-CQRaJAEP.js";import{g as K}from"./graphql-i5tnMPnl.js";import{u as O,i as V,a as w}from"./initialOptions-Bp4vgjqV.js";import{T as X,m as Z}from"./filter-aZNna_Ju.js";import{a as ee,V as te}from"./VDataTable-CgfMuQhE.js";import"./VPagination-C1Is40ky.js";function v(o,e){return new Date(o)-new Date(e)}function se(o,e){return o-e}const ae={name:"TableComponent",emits:[O],props:{tasks:{type:Array,required:!0},initialOptions:V},components:{Task:I,Job:N},setup(o,{emit:e}){const m=B(),t=w("sortBy",{props:o,emit:e},[{key:"task.tokens.cycle",order:m.value?"desc":"asc"}]),_=w("page",{props:o,emit:e},1),y=w("itemsPerPage",{props:o,emit:e},50),k=R([{title:"Task",key:"task.name",sortable:!0,sortFunc:b},{title:"Jobs",key:"data-table-expand",sortable:!1},{title:"Cycle Point",key:"task.tokens.cycle",sortable:!0,sortFunc:b},{title:"Platform",key:"latestJob.node.platform",sortable:!0,sortFunc:b},{title:"Job Runner",key:"latestJob.node.jobRunnerName",sortable:!0,sortFunc:b},{title:"Job ID",key:"latestJob.node.jobId",sortable:!0,sortFunc:b},{title:"Submit",key:"latestJob.node.submittedTime",sortable:!0,sortFunc:v},{title:"Start",key:"latestJob.node.startedTime",sortable:!0,sortFunc:v},{title:"Finish",key:"latestJob.node.finishedTime",sortable:!0,sortFunc:v},{title:"Run Time",key:"task.node.task.meanElapsedTime",sortable:!0,sortFunc:se}]);return U(t,f=>{for(const{key:d,order:s}of f){const a=k.value.find(r=>r.key===d);a.sort=(r,c)=>!r&&!c?0:r?c?a.sortFunc(r,c):s==="asc"?-1:1:s==="asc"?1:-1}},{deep:!0,immediate:!0}),{dtMean:A,itemsPerPage:y,page:_,sortBy:t,headers:k,icons:{mdiChevronDown:E},itemsPerPageOptions:[{value:10,title:"10"},{value:20,title:"20"},{value:50,title:"50"},{value:100,title:"100"},{value:200,title:"200"},{value:-1,title:"All"}]}}},oe={class:"d-flex align-content-center flex-nowrap"},ne={style:{width:"2em"}},re={style:{width:"2em"}},le={colspan:3},ie={class:"d-flex align-content-center flex-nowrap"},de={class:"d-flex",style:{"margin-left":"2em"}},ue={class:"ml-2"},me=n("td",null,null,-1);function ce(o,e,m,t,_,y){const k=T("Task"),f=T("Job"),d=S("command-menu");return p(),h(te,{headers:t.headers,items:m.tasks,"item-value":"task.id","multi-sort":"","sort-by":t.sortBy,"onUpdate:sortBy":e[0]||(e[0]=s=>t.sortBy=s),"show-expand":"",density:"compact",page:t.page,"onUpdate:page":e[1]||(e[1]=s=>t.page=s),"items-per-page":t.itemsPerPage,"onUpdate:itemsPerPage":e[2]||(e[2]=s=>t.itemsPerPage=s)},{"item.task.name":i(({item:s})=>{var a,r,c,g;return[n("div",oe,[n("div",ne,[P(l(k,{task:s.task.node,startTime:(r=(a=s.latestJob)==null?void 0:a.node)==null?void 0:r.startedTime},null,8,["task","startTime"]),[[d,s.task]])]),n("div",re,[s.latestJob?P((p(),h(f,{key:0,status:s.latestJob.node.state,"previous-state":(g=(c=s.previousJob)==null?void 0:c.node)==null?void 0:g.state},null,8,["status","previous-state"])),[[d,s.latestJob]]):q("",!0)]),n("div",null,u(s.task.name),1)])]}),"item.task.node.task.meanElapsedTime":i(({item:s})=>[n("td",null,u(t.dtMean(s.task)),1)]),"item.data-table-expand":i(({item:s,internalItem:a,toggleExpand:r,isExpanded:c})=>[l(Q,{onClick:g=>r(a),icon:"",variant:"text",size:"small",style:W({visibility:(s.task.children||[]).length?null:"hidden",transform:c(a)?"rotate(180deg)":null})},{default:i(()=>[l(M,{icon:t.icons.mdiChevronDown,size:"large"},null,8,["icon"])]),_:2},1032,["onClick","style"])]),"expanded-row":i(({item:s})=>[(p(!0),x(G,null,z(s.task.children,(a,r)=>(p(),x("tr",{key:a.id,class:"expanded-row bg-grey-lighten-5"},[n("td",le,[n("div",ie,[n("div",de,[P((p(),h(f,{key:`${a.id}-summary-${r}`,status:a.node.state},null,8,["status"])),[[d,a]]),n("span",ue,"#"+u(a.node.submitNum),1)])])]),n("td",null,u(a.node.platform),1),n("td",null,u(a.node.jobRunnerName),1),n("td",null,u(a.node.jobId),1),n("td",null,u(a.node.submittedTime),1),n("td",null,u(a.node.startedTime),1),n("td",null,u(a.node.finishedTime),1),me]))),128))]),bottom:i(()=>[l(ee,{itemsPerPageOptions:t.itemsPerPageOptions},null,8,["itemsPerPageOptions"])]),_:1},8,["headers","items","sort-by","page","items-per-page"])}const ke=C(ae,[["render",ce]]),fe=H`
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
`,pe={name:"Table",mixins:[K,L],components:{TableComponent:ke,TaskFilter:X},emits:[O],props:{initialOptions:V},setup(o,{emit:e}){const m=w("tasksFilter",{props:o,emit:e},{});return{dataTableOptions:w("dataTableOptions",{props:o,emit:e}),tasksFilter:m}},computed:{...$("workflows",["cylcTree"]),...Y("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},tasks(){const o=[];for(const e of this.workflows)for(const m of e.children)for(const t of m.children)o.push({task:t,latestJob:t.children[0],previousJob:t.children[1]});return o},query(){return new j(fe,this.variables,"workflow",[],!0,!0)},filteredTasks(){return this.tasks.filter(({task:o})=>Z(o,this.tasksFilter.id,this.tasksFilter.states))}}},be={class:"h-100"};function we(o,e,m,t,_,y){const k=T("TaskFilter"),f=T("TableComponent");return p(),x("div",be,[l(D,{fluid:"",class:"c-table ma-0 pa-2 h-100 flex-column d-flex"},{default:i(()=>[l(F,{"no-gutters":"",class:"d-flex flex-wrap flex-grow-0"},{default:i(()=>[l(J,null,{default:i(()=>[l(k,{modelValue:t.tasksFilter,"onUpdate:modelValue":e[0]||(e[0]=d=>t.tasksFilter=d)},null,8,["modelValue"])]),_:1})]),_:1}),l(F,{"no-gutters":"",class:"flex-grow-1 position-relative"},{default:i(()=>[l(J,{cols:"12",class:"mh-100 position-relative"},{default:i(()=>[l(D,{fluid:"",class:"ma-0 pa-0 w-100 h-100 left-0 top-0 position-absolute pt-2"},{default:i(()=>[l(f,{tasks:y.filteredTasks,"initial-options":t.dataTableOptions,"onUpdate:initialOptions":e[1]||(e[1]=d=>t.dataTableOptions=d)},null,8,["tasks","initial-options"])]),_:1})]),_:1})]),_:1})]),_:1})])}const ve=C(pe,[["render",we]]);export{ve as default};
