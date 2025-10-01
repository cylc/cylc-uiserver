import{_ as D,cb as h,cc as F,cd as T,ce as P,a3 as b,a4 as _,cf as v,a6 as C,x as V,g as e,w as s,j as A,ad as I,I as N,C as y,o as S,V as g,h as p,z as M,B as c,D as w,l as i,t as f,E as k,bJ as j}from"./index-jbzX_AXb.js";import{g as z}from"./graphql-o3z6-itG.js";import{i as J,a as x}from"./initialOptions-Ceh0265h.js";import{_ as R,a as W,b as B}from"./filter-E7bBrTct.js";const E=N`
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
  isRetry
  isWallclock
  isXtriggered
  task {
    meanElapsedTime
  }
  firstParent {
    id
  }
  runtime {
    runMode
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
  estimatedFinishTime
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
`,U={name:"Tree",mixins:[z,C],components:{TaskFilter:R,TreeComponent:v},props:{initialOptions:J},setup(t,{emit:a}){const n=x("tasksFilter",{props:t,emit:a},{id:null,states:null}),l=x("flat",{props:t,emit:a},!1);return{tasksFilter:n,flat:l}},data:()=>({expandAll:null}),computed:{..._("workflows",["cylcTree"]),...b("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},query(){return new I(E,this.variables,"workflow",[],!0,!0)},filterState(){return this.tasksFilter.id?.trim()||this.tasksFilter.states?.length?this.tasksFilter:null}},methods:{filterNode(t,a,n=!1){if(t.type==="job")return!1;const l=W(t,this.tasksFilter.states),m=n||B(t,this.tasksFilter.id);let o=l&&m,{children:r}=t;if(t.type==="cycle"&&(r=t.familyTree[0]?.children),r)for(const u of r)o=this.filterNode(u,a,m)||o;return a.set(t,!o),o}},icons:{mdiPlus:P,mdiMinus:T,mdiFormatAlignRight:F,mdiFormatAlignJustify:h}},$={class:"h-100"},q={class:"d-flex flex-nowrap ml-2"};function Q(t,a,n,l,m,o){const r=y("TaskFilter"),u=y("TreeComponent");return S(),V("div",$,[e(A,{fluid:"",class:"c-tree pa-2","data-cy":"tree-view"},{default:s(()=>[e(g,{"no-gutters":"",class:"d-flex flex-wrap"},{default:s(()=>[e(p,null,{default:s(()=>[e(r,{modelValue:l.tasksFilter,"onUpdate:modelValue":a[0]||(a[0]=d=>l.tasksFilter=d)},null,8,["modelValue"])]),_:1}),e(p,{class:"flex-grow-0"},{default:s(()=>[M("div",q,[e(c,{onClick:a[1]||(a[1]=d=>l.flat=!l.flat),icon:"",variant:"flat",size:"small","data-cy":"toggle-families"},{default:s(()=>[e(w,{size:"x-large"},{default:s(()=>[i(f(l.flat?t.$options.icons.mdiFormatAlignRight:t.$options.icons.mdiFormatAlignJustify),1)]),_:1}),e(k,null,{default:s(()=>[i(f(l.flat?"Show Families":"Hide Families"),1)]),_:1})]),_:1}),e(c,{onClick:a[2]||(a[2]=d=>t.expandAll=["workflow","cycle","family"]),icon:"",variant:"flat",size:"small","data-cy":"expand-all"},{default:s(()=>[e(w,{size:"x-large"},{default:s(()=>[i(f(t.$options.icons.mdiPlus),1)]),_:1}),e(k,null,{default:s(()=>[...a[4]||(a[4]=[i("Expand all",-1)])]),_:1})]),_:1}),e(c,{onClick:a[3]||(a[3]=d=>t.expandAll=[]),icon:"",variant:"flat",size:"small","data-cy":"collapse-all"},{default:s(()=>[e(w,{size:"x-large"},{default:s(()=>[i(f(t.$options.icons.mdiMinus),1)]),_:1}),e(k,null,{default:s(()=>[...a[5]||(a[5]=[i("Collapse all",-1)])]),_:1})]),_:1})])]),_:1})]),_:1}),e(g,{"no-gutters":"",class:"mt-2"},{default:s(()=>[e(p,{cols:"12",class:"mh-100 position-relative"},{default:s(()=>[e(u,j({workflows:o.workflows,hoverable:!1,autoStripTypes:["workflow"],"node-filter-func":o.filterNode,flat:l.flat},{expandAll:t.expandAll,filterState:o.filterState},{ref:"treeComponent"}),null,16,["workflows","node-filter-func","flat"])]),_:1})]),_:1})]),_:1})])}const Y=D(U,[["render",Q]]);export{Y as default};
