import{_ as h,J as D,$ as T,dJ as g,a1 as P,a2 as b,a0 as _,dK as F,dL as V,B as C,k as a,w as s,V as v,A as p,h as I,p as c,n as u,C as N,G as k,E as w,m as d,t as x,F as y,bj as A}from"./index-CQRaJAEP.js";import{g as S}from"./graphql-i5tnMPnl.js";import{i as j,a as M}from"./initialOptions-Bp4vgjqV.js";import{T as J,a as $,b as B}from"./filter-aZNna_Ju.js";const E=D`
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
`,U={name:"Tree",mixins:[S,T],components:{TaskFilter:J,TreeComponent:g},props:{initialOptions:j},setup(e,{emit:t}){return{tasksFilter:M("tasksFilter",{props:e,emit:t},{id:null,states:null})}},data:()=>({expandAll:null}),computed:{...P("workflows",["cylcTree"]),...b("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},query(){return new _(E,this.variables,"workflow",[],!0,!0)},filterState(){var e,t;return(e=this.tasksFilter.id)!=null&&e.trim()||(t=this.tasksFilter.states)!=null&&t.length?this.tasksFilter:null}},methods:{filterNode(e,t,f=!1){var n;if(e.type==="job")return!1;const i=$(e,this.tasksFilter.states),m=f||B(e,this.tasksFilter.id);let l=i&&m,{children:o}=e;if(e.type==="cycle"&&(o=(n=e.familyTree[0])==null?void 0:n.children),o)for(const r of o)l=this.filterNode(r,t,m)||l;return t.set(e,!l),l}},icons:{mdiPlus:F,mdiMinus:V}},W={class:"h-100"},z={class:"d-flex flex-nowrap ml-2"};function R(e,t,f,i,m,l){const o=p("TaskFilter"),n=p("TreeComponent");return I(),C("div",W,[a(v,{fluid:"",class:"c-tree pa-2","data-cy":"tree-view"},{default:s(()=>[a(c,{"no-gutters":"",class:"d-flex flex-wrap"},{default:s(()=>[a(u,null,{default:s(()=>[a(o,{modelValue:i.tasksFilter,"onUpdate:modelValue":t[0]||(t[0]=r=>i.tasksFilter=r)},null,8,["modelValue"])]),_:1}),a(u,{class:"flex-grow-0"},{default:s(()=>[N("div",z,[a(k,{onClick:t[1]||(t[1]=r=>e.expandAll=["workflow","cycle","family"]),icon:"",variant:"flat",size:"small","data-cy":"expand-all"},{default:s(()=>[a(w,{size:"x-large"},{default:s(()=>[d(x(e.$options.icons.mdiPlus),1)]),_:1}),a(y,null,{default:s(()=>[d("Expand all")]),_:1})]),_:1}),a(k,{onClick:t[2]||(t[2]=r=>e.expandAll=[]),icon:"",variant:"flat",size:"small","data-cy":"collapse-all"},{default:s(()=>[a(w,{size:"x-large"},{default:s(()=>[d(x(e.$options.icons.mdiMinus),1)]),_:1}),a(y,null,{default:s(()=>[d("Collapse all")]),_:1})]),_:1})])]),_:1})]),_:1}),a(c,{"no-gutters":"",class:"mt-2"},{default:s(()=>[a(u,{cols:"12",class:"mh-100 position-relative"},{default:s(()=>[a(n,A({workflows:l.workflows,hoverable:!1,autoStripTypes:["workflow"],"node-filter-func":l.filterNode},{expandAll:e.expandAll,filterState:l.filterState},{ref:"treeComponent"}),null,16,["workflows","node-filter-func"])]),_:1})]),_:1})]),_:1})])}const K=h(U,[["render",R]]);export{K as default};
