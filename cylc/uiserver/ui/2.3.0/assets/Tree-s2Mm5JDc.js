import{bz as P,c7 as h,cf as D,dI as g,c8 as b,ch as T,ci as _,cg as F,dJ as C,dK as V,aM as c,q as v,z as a,bs as s,bC as N,az as I,bE as p,bD as f,r as A,b_ as w,c5 as k,y as n,a_ as y,c6 as x,ah as M}from"./index-p5QwxXYb.js";import{g as S}from"./graphql-1_B3k2Rp.js";import{T as z,a as $,b as j}from"./TaskFilter-HeF76y-C.js";const E=h`
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
  cyclePoints: familyProxies (ids: ["*/root"]) {
    ...CyclePointData
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
`,J={name:"Tree",mixins:[S,D],components:{TaskFilter:z,TreeComponent:g},head(){return{title:b("App.workflow",{name:this.workflowName})}},data:()=>({expandAll:null,tasksFilter:{id:null,states:null}}),computed:{...T("workflows",["cylcTree"]),..._("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},query(){return new F(E,this.variables,"workflow",[],!0,!0)},filterState(){var e,t;return(e=this.tasksFilter.id)!=null&&e.trim()||(t=this.tasksFilter.states)!=null&&t.length?this.tasksFilter:null}},methods:{filterNode(e,t,m=!1){var i;if(e.type==="job")return!1;const u=$(e,this.tasksFilter.states),d=m||j(e,this.tasksFilter.id);let l=u&&d,{children:o}=e;if(e.type==="cycle"&&(o=(i=e.familyTree[0])==null?void 0:i.children),o)for(const r of o)l=this.filterNode(r,t,d)||l;return t.set(e,!l),l}},icons:{mdiPlus:C,mdiMinus:V}},U={class:"h-100"},W={class:"d-flex flex-nowrap ml-2"};function q(e,t,m,u,d,l){const o=c("TaskFilter"),i=c("TreeComponent");return I(),v("div",U,[a(N,{fluid:"",class:"c-tree pa-2","data-cy":"tree-view"},{default:s(()=>[a(p,{"no-gutters":"",class:"d-flex flex-wrap"},{default:s(()=>[a(f,null,{default:s(()=>[a(o,{modelValue:e.tasksFilter,"onUpdate:modelValue":t[0]||(t[0]=r=>e.tasksFilter=r)},null,8,["modelValue"])]),_:1}),a(f,{class:"flex-grow-0"},{default:s(()=>[A("div",W,[a(w,{onClick:t[1]||(t[1]=r=>e.expandAll=["workflow","cycle","family"]),icon:"",variant:"flat",size:"small","data-cy":"expand-all"},{default:s(()=>[a(k,{size:"x-large"},{default:s(()=>[n(y(e.$options.icons.mdiPlus),1)]),_:1}),a(x,null,{default:s(()=>[n("Expand all")]),_:1})]),_:1}),a(w,{onClick:t[2]||(t[2]=r=>e.expandAll=[]),icon:"",variant:"flat",size:"small","data-cy":"collapse-all"},{default:s(()=>[a(k,{size:"x-large"},{default:s(()=>[n(y(e.$options.icons.mdiMinus),1)]),_:1}),a(x,null,{default:s(()=>[n("Collapse all")]),_:1})]),_:1})])]),_:1})]),_:1}),a(p,{"no-gutters":"",class:"mt-2"},{default:s(()=>[a(f,{cols:"12",class:"mh-100 position-relative"},{default:s(()=>[a(i,M({workflows:l.workflows,hoverable:!1,autoStripTypes:["workflow"],"node-filter-func":l.filterNode},{expandAll:e.expandAll,filterState:l.filterState},{ref:"treeComponent"}),null,16,["workflows","node-filter-func"])]),_:1})]),_:1})]),_:1})])}const G=P(J,[["render",q]]);export{G as default};
