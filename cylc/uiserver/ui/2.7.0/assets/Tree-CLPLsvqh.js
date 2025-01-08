import{_ as h,J as D,$ as F,c8 as T,a1 as P,a2 as b,a0 as _,c9 as v,ca as A,cb as C,cc as V,B as I,k as e,w as l,V as N,A as y,h as S,p as g,n as c,C as J,G as p,E as w,m as r,t as m,F as k,bI as M}from"./index-Hyq34tSM.js";import{g as j}from"./graphql-D8b4q-7X.js";import{i as z,a as x}from"./initialOptions-BLDeg43d.js";import{T as R,a as B,b as E}from"./filter-gCYsvdqm.js";const U=D`
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
  messages
  taskProxy {
    outputs (satisfied: true) {
      label
      message
    }
  }
}
`,W={name:"Tree",mixins:[j,F],components:{TaskFilter:R,TreeComponent:T},props:{initialOptions:z},setup(a,{emit:t}){const d=x("tasksFilter",{props:a,emit:t},{id:null,states:null}),s=x("flat",{props:a,emit:t},!1);return{tasksFilter:d,flat:s}},data:()=>({expandAll:null}),computed:{...P("workflows",["cylcTree"]),...b("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},query(){return new _(U,this.variables,"workflow",[],!0,!0)},filterState(){var a,t;return(a=this.tasksFilter.id)!=null&&a.trim()||(t=this.tasksFilter.states)!=null&&t.length?this.tasksFilter:null}},methods:{filterNode(a,t,d=!1){var f;if(a.type==="job")return!1;const s=B(a,this.tasksFilter.states),u=d||E(a,this.tasksFilter.id);let o=s&&u,{children:n}=a;if(a.type==="cycle"&&(n=(f=a.familyTree[0])==null?void 0:f.children),n)for(const i of n)o=this.filterNode(i,t,u)||o;return t.set(a,!o),o}},icons:{mdiPlus:v,mdiMinus:A,mdiFormatAlignRight:C,mdiFormatAlignJustify:V}},$={class:"h-100"},q={class:"d-flex flex-nowrap ml-2"};function Q(a,t,d,s,u,o){const n=y("TaskFilter"),f=y("TreeComponent");return S(),I("div",$,[e(N,{fluid:"",class:"c-tree pa-2","data-cy":"tree-view"},{default:l(()=>[e(g,{"no-gutters":"",class:"d-flex flex-wrap"},{default:l(()=>[e(c,null,{default:l(()=>[e(n,{modelValue:s.tasksFilter,"onUpdate:modelValue":t[0]||(t[0]=i=>s.tasksFilter=i)},null,8,["modelValue"])]),_:1}),e(c,{class:"flex-grow-0"},{default:l(()=>[J("div",q,[e(p,{onClick:t[1]||(t[1]=i=>s.flat=!s.flat),icon:"",variant:"flat",size:"small","data-cy":"toggle-families"},{default:l(()=>[e(w,{size:"x-large"},{default:l(()=>[r(m(s.flat?a.$options.icons.mdiFormatAlignRight:a.$options.icons.mdiFormatAlignJustify),1)]),_:1}),e(k,null,{default:l(()=>[r(m(s.flat?"Show Families":"Hide Families"),1)]),_:1})]),_:1}),e(p,{onClick:t[2]||(t[2]=i=>a.expandAll=["workflow","cycle","family"]),icon:"",variant:"flat",size:"small","data-cy":"expand-all"},{default:l(()=>[e(w,{size:"x-large"},{default:l(()=>[r(m(a.$options.icons.mdiPlus),1)]),_:1}),e(k,null,{default:l(()=>[r("Expand all")]),_:1})]),_:1}),e(p,{onClick:t[3]||(t[3]=i=>a.expandAll=[]),icon:"",variant:"flat",size:"small","data-cy":"collapse-all"},{default:l(()=>[e(w,{size:"x-large"},{default:l(()=>[r(m(a.$options.icons.mdiMinus),1)]),_:1}),e(k,null,{default:l(()=>[r("Collapse all")]),_:1})]),_:1})])]),_:1})]),_:1}),e(g,{"no-gutters":"",class:"mt-2"},{default:l(()=>[e(c,{cols:"12",class:"mh-100 position-relative"},{default:l(()=>[e(f,M({workflows:o.workflows,hoverable:!1,autoStripTypes:["workflow"],"node-filter-func":o.filterNode,flat:s.flat},{expandAll:a.expandAll,filterState:o.filterState},{ref:"treeComponent"}),null,16,["workflows","node-filter-func","flat"])]),_:1})]),_:1})]),_:1})])}const K=h(W,[["render",Q]]);export{K as default};
