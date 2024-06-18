import{_ as h,L as D,a1 as T,dQ as g,a3 as P,a4 as b,a2 as _,dR as F,dS as V,D as v,m as a,w as s,V as C,C as p,k as I,v as c,q as u,E as N,I as k,G as w,p as d,t as x,H as y,bl as S}from"./index-DSRpE5Rv.js";import{g as A}from"./graphql-B2keRYja.js";import{i as M,a as j}from"./initialOptions-qpNtWc_g.js";import{T as E,a as R,b as U}from"./filter-DyjY8Bu5.js";const W=D`
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
  familyProxies {
    ...FamilyProxyData
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
  familyProxies {
    ...FamilyProxyData
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

fragment FamilyProxyData on FamilyProxy {
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
  messages
  taskProxy {
    outputs (satisfied: true) {
      label
      message
    }
  }
}
`,$={name:"Tree",mixins:[A,T],components:{TaskFilter:E,TreeComponent:g},props:{initialOptions:M},setup(e,{emit:t}){return{tasksFilter:j("tasksFilter",{props:e,emit:t},{id:null,states:null})}},data:()=>({expandAll:null}),computed:{...P("workflows",["cylcTree"]),...b("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},query(){return new _(W,this.variables,"workflow",[],!0,!0)},filterState(){var e,t;return(e=this.tasksFilter.id)!=null&&e.trim()||(t=this.tasksFilter.states)!=null&&t.length?this.tasksFilter:null}},methods:{filterNode(e,t,f=!1){var n;if(e.type==="job")return!1;const i=R(e,this.tasksFilter.states),m=f||U(e,this.tasksFilter.id);let l=i&&m,{children:o}=e;if(e.type==="cycle"&&(o=(n=e.familyTree[0])==null?void 0:n.children),o)for(const r of o)l=this.filterNode(r,t,m)||l;return t.set(e,!l),l}},icons:{mdiPlus:F,mdiMinus:V}},q={class:"h-100"},z={class:"d-flex flex-nowrap ml-2"};function B(e,t,f,i,m,l){const o=p("TaskFilter"),n=p("TreeComponent");return I(),v("div",q,[a(C,{fluid:"",class:"c-tree pa-2","data-cy":"tree-view"},{default:s(()=>[a(c,{"no-gutters":"",class:"d-flex flex-wrap"},{default:s(()=>[a(u,null,{default:s(()=>[a(o,{modelValue:i.tasksFilter,"onUpdate:modelValue":t[0]||(t[0]=r=>i.tasksFilter=r)},null,8,["modelValue"])]),_:1}),a(u,{class:"flex-grow-0"},{default:s(()=>[N("div",z,[a(k,{onClick:t[1]||(t[1]=r=>e.expandAll=["workflow","cycle","family"]),icon:"",variant:"flat",size:"small","data-cy":"expand-all"},{default:s(()=>[a(w,{size:"x-large"},{default:s(()=>[d(x(e.$options.icons.mdiPlus),1)]),_:1}),a(y,null,{default:s(()=>[d("Expand all")]),_:1})]),_:1}),a(k,{onClick:t[2]||(t[2]=r=>e.expandAll=[]),icon:"",variant:"flat",size:"small","data-cy":"collapse-all"},{default:s(()=>[a(w,{size:"x-large"},{default:s(()=>[d(x(e.$options.icons.mdiMinus),1)]),_:1}),a(y,null,{default:s(()=>[d("Collapse all")]),_:1})]),_:1})])]),_:1})]),_:1}),a(c,{"no-gutters":"",class:"mt-2"},{default:s(()=>[a(u,{cols:"12",class:"mh-100 position-relative"},{default:s(()=>[a(n,S({workflows:l.workflows,hoverable:!1,autoStripTypes:["workflow"],"node-filter-func":l.filterNode},{expandAll:e.expandAll,filterState:l.filterState},{ref:"treeComponent"}),null,16,["workflows","node-filter-func"])]),_:1})]),_:1})]),_:1})])}const L=h($,[["render",B]]);export{L as default};
