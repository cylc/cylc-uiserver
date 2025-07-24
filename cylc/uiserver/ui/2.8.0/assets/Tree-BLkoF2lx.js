import{_ as D,c4 as T,c5 as h,c6 as F,c7 as P,a4 as b,a5 as _,c8 as v,a7 as C,x as V,g as e,w as l,j as A,ae as I,I as N,C as y,o as S,V as g,h as p,z as j,B as w,D as k,l as i,t as f,E as c,bG as z}from"./index-EpcknQ5m.js";import{g as M}from"./graphql-n5gzreXW.js";import{i as R,a as x}from"./initialOptions-CKJltX86.js";import{T as J,a as W,b as B}from"./filter-DgPx3Jyt.js";const E=N`
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
  isXtriggered
  isRetry
  isWallclock
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
`,U={name:"Tree",mixins:[M,C],components:{TaskFilter:J,TreeComponent:v},props:{initialOptions:R},setup(t,{emit:a}){const n=x("tasksFilter",{props:t,emit:a},{id:null,states:null}),s=x("flat",{props:t,emit:a},!1);return{tasksFilter:n,flat:s}},data:()=>({expandAll:null}),computed:{..._("workflows",["cylcTree"]),...b("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},query(){return new I(E,this.variables,"workflow",[],!0,!0)},filterState(){return this.tasksFilter.id?.trim()||this.tasksFilter.states?.length?this.tasksFilter:null}},methods:{filterNode(t,a,n=!1){if(t.type==="job")return!1;const s=W(t,this.tasksFilter.states),m=n||B(t,this.tasksFilter.id);let o=s&&m,{children:r}=t;if(t.type==="cycle"&&(r=t.familyTree[0]?.children),r)for(const u of r)o=this.filterNode(u,a,m)||o;return a.set(t,!o),o}},icons:{mdiPlus:P,mdiMinus:F,mdiFormatAlignRight:h,mdiFormatAlignJustify:T}},q={class:"h-100"},Q={class:"d-flex flex-nowrap ml-2"};function $(t,a,n,s,m,o){const r=y("TaskFilter"),u=y("TreeComponent");return S(),V("div",q,[e(A,{fluid:"",class:"c-tree pa-2","data-cy":"tree-view"},{default:l(()=>[e(g,{"no-gutters":"",class:"d-flex flex-wrap"},{default:l(()=>[e(p,null,{default:l(()=>[e(r,{modelValue:s.tasksFilter,"onUpdate:modelValue":a[0]||(a[0]=d=>s.tasksFilter=d)},null,8,["modelValue"])]),_:1}),e(p,{class:"flex-grow-0"},{default:l(()=>[j("div",Q,[e(w,{onClick:a[1]||(a[1]=d=>s.flat=!s.flat),icon:"",variant:"flat",size:"small","data-cy":"toggle-families"},{default:l(()=>[e(k,{size:"x-large"},{default:l(()=>[i(f(s.flat?t.$options.icons.mdiFormatAlignRight:t.$options.icons.mdiFormatAlignJustify),1)]),_:1}),e(c,null,{default:l(()=>[i(f(s.flat?"Show Families":"Hide Families"),1)]),_:1})]),_:1}),e(w,{onClick:a[2]||(a[2]=d=>t.expandAll=["workflow","cycle","family"]),icon:"",variant:"flat",size:"small","data-cy":"expand-all"},{default:l(()=>[e(k,{size:"x-large"},{default:l(()=>[i(f(t.$options.icons.mdiPlus),1)]),_:1}),e(c,null,{default:l(()=>a[4]||(a[4]=[i("Expand all",-1)])),_:1,__:[4]})]),_:1}),e(w,{onClick:a[3]||(a[3]=d=>t.expandAll=[]),icon:"",variant:"flat",size:"small","data-cy":"collapse-all"},{default:l(()=>[e(k,{size:"x-large"},{default:l(()=>[i(f(t.$options.icons.mdiMinus),1)]),_:1}),e(c,null,{default:l(()=>a[5]||(a[5]=[i("Collapse all",-1)])),_:1,__:[5]})]),_:1})])]),_:1})]),_:1}),e(g,{"no-gutters":"",class:"mt-2"},{default:l(()=>[e(p,{cols:"12",class:"mh-100 position-relative"},{default:l(()=>[e(u,z({workflows:o.workflows,hoverable:!1,autoStripTypes:["workflow"],"node-filter-func":o.filterNode,flat:s.flat},{expandAll:t.expandAll,filterState:o.filterState},{ref:"treeComponent"}),null,16,["workflows","node-filter-func","flat"])]),_:1})]),_:1})]),_:1})])}const Y=D(U,[["render",$]]);export{Y as default};
