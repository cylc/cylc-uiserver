import{bz as o,c6 as t,ce as s,dH as r,c7 as i,cg as n,ch as l,cf as d,aM as m,q as f,r as c,z as w,az as p}from"./index-3996a8d9.js";import{g as k}from"./graphql-7cda8b8d.js";const u=t`
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
`,y={name:"Tree",mixins:[k,s],components:{TreeComponent:r},head(){return{title:i("App.workflow",{name:this.workflowName})}},computed:{...n("workflows",["cylcTree"]),...l("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},query(){return new d(u,this.variables,"workflow",[],!0,!0)}}},P={class:"h-100"},x={class:"c-tree pa-2 h-100","data-cy":"tree-view"};function D(b,h,_,g,T,e){const a=m("tree-component");return p(),f("div",P,[c("div",x,[w(a,{workflows:e.workflows,hoverable:!1,activable:!1,"multiple-active":!1,"min-depth":1,autoStripTypes:["workflow"],ref:"tree0",key:"tree0"},null,8,["workflows"])])])}const I=o(y,[["render",D]]);export{I as default};
