import{bE as b,bU as h,c0 as T,dA as g,bV as D,c2 as P,c3 as _,c1 as F,dB as V,dC as v,u as C,I as a,bx as s,bH as I,aR as p,aE as N,bJ as c,bI as u,v as A,bT as w,bR as k,H as d,b3 as x,bS as y,am as S}from"./index-C2AHI-HK.js";import{g as M}from"./graphql-BScASb0Q.js";import{i as j,a as E}from"./initialOptions-DCNtfDfN.js";import{T as R,a as U,b as B}from"./TaskFilter-Blo6nLre.js";const J=h`
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
`,W={name:"Tree",mixins:[M,T],components:{TaskFilter:R,TreeComponent:g},head(){return{title:D("App.workflow",{name:this.workflowName})}},props:{initialOptions:j},setup(e,{emit:t}){return{tasksFilter:E("tasksFilter",{props:e,emit:t},{id:null,states:null})}},data:()=>({expandAll:null}),computed:{...P("workflows",["cylcTree"]),..._("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},query(){return new F(J,this.variables,"workflow",[],!0,!0)},filterState(){var e,t;return(e=this.tasksFilter.id)!=null&&e.trim()||(t=this.tasksFilter.states)!=null&&t.length?this.tasksFilter:null}},methods:{filterNode(e,t,f=!1){var n;if(e.type==="job")return!1;const i=U(e,this.tasksFilter.states),m=f||B(e,this.tasksFilter.id);let l=i&&m,{children:o}=e;if(e.type==="cycle"&&(o=(n=e.familyTree[0])==null?void 0:n.children),o)for(const r of o)l=this.filterNode(r,t,m)||l;return t.set(e,!l),l}},icons:{mdiPlus:V,mdiMinus:v}},$={class:"h-100"},z={class:"d-flex flex-nowrap ml-2"};function q(e,t,f,i,m,l){const o=p("TaskFilter"),n=p("TreeComponent");return N(),C("div",$,[a(I,{fluid:"",class:"c-tree pa-2","data-cy":"tree-view"},{default:s(()=>[a(c,{"no-gutters":"",class:"d-flex flex-wrap"},{default:s(()=>[a(u,null,{default:s(()=>[a(o,{modelValue:i.tasksFilter,"onUpdate:modelValue":t[0]||(t[0]=r=>i.tasksFilter=r)},null,8,["modelValue"])]),_:1}),a(u,{class:"flex-grow-0"},{default:s(()=>[A("div",z,[a(w,{onClick:t[1]||(t[1]=r=>e.expandAll=["workflow","cycle","family"]),icon:"",variant:"flat",size:"small","data-cy":"expand-all"},{default:s(()=>[a(k,{size:"x-large"},{default:s(()=>[d(x(e.$options.icons.mdiPlus),1)]),_:1}),a(y,null,{default:s(()=>[d("Expand all")]),_:1})]),_:1}),a(w,{onClick:t[2]||(t[2]=r=>e.expandAll=[]),icon:"",variant:"flat",size:"small","data-cy":"collapse-all"},{default:s(()=>[a(k,{size:"x-large"},{default:s(()=>[d(x(e.$options.icons.mdiMinus),1)]),_:1}),a(y,null,{default:s(()=>[d("Collapse all")]),_:1})]),_:1})])]),_:1})]),_:1}),a(c,{"no-gutters":"",class:"mt-2"},{default:s(()=>[a(u,{cols:"12",class:"mh-100 position-relative"},{default:s(()=>[a(n,S({workflows:l.workflows,hoverable:!1,autoStripTypes:["workflow"],"node-filter-func":l.filterNode},{expandAll:e.expandAll,filterState:l.filterState},{ref:"treeComponent"}),null,16,["workflows","node-filter-func"])]),_:1})]),_:1})]),_:1})])}const Y=b(W,[["render",q]]);export{Y as default};
