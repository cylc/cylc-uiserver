import{_ as y,co as d,cp as c,cq as m,cr as k,a3 as g,a4 as b,cs as x,a6 as F,q as D,g as p,A as u,b8 as T,ad as P,H as _,o as A}from"./index-BxIX773T.js";import{g as S}from"./graphql-LLAnEp44.js";import{i as I,a as w}from"./initialOptions-Cwf6VhRd.js";import{V as C}from"./ViewToolbar-Ue7t8UtL.js";import{g as M,b as N,c as v,a as E,u as j}from"./filter-BKMXLKHk.js";const R=_`
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
`,W={name:"Tree",mixins:[S,F],components:{TreeComponent:x,ViewToolbar:C},props:{initialOptions:I},setup(t,{emit:e}){const o=w("tasksFilter",{props:t,emit:e},{id:null,states:null}),a=j(o),l=w("flat",{props:t,emit:e},!1);return{tasksFilter:o,filterState:a,flat:l}},data:()=>({expandAll:null}),computed:{...b("workflows",["cylcTree"]),...g("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},query(){return new P(R,this.variables,"workflow",[],!0,!0)},controlGroups(){return[{title:"Filter",controls:[{title:"Filter By ID",action:"taskIDFilter",key:"taskIDFilter",value:this.tasksFilter.id},{title:"Filter By State",action:"taskStateFilter",key:"taskStateFilter",value:this.tasksFilter.states}]},{title:"Tree",controls:[{title:"Toggle Families",icon:{true:k,false:m},action:"toggle",value:this.flat,key:"flat"},{title:"Expand All",key:"ExpandAll",icon:d,action:"callback",callback:this.treeExpandAll},{title:"Collapse All",key:"CollapseAll",icon:c,action:"callback",callback:this.treeCollapseAll}]}]}},methods:{setOption(t,e){t==="taskStateFilter"?this.tasksFilter.states=e:t==="taskIDFilter"?this.tasksFilter.id=e:this[t]=e},treeExpandAll(){this.expandAll=["workflow","cycle","family"]},treeCollapseAll(){this.expandAll=[]},filterNode(t,e,o=!1){if(t.type==="job")return!1;const[a,l,s]=M(this.tasksFilter.states?.length?this.tasksFilter.states:[]),n=N(t,a,l,s),r=o||v(t,E(this.tasksFilter.id));let i=n&&r,{children:f}=t;if(t.type==="cycle"&&(f=t.familyTree[0]?.children),f)for(const h of f)i=this.filterNode(h,e,r)||i;return e.set(t,!i),i}},icons:{mdiFormatAlignJustify:k,mdiFormatAlignRight:m,mdiMinus:c,mdiPlus:d}},q={class:"c-tree h-100 overflow-auto"};function J(t,e,o,a,l,s){const n=u("ViewToolbar"),r=u("TreeComponent");return A(),D("div",q,[p(n,{class:"toolbar",groups:s.controlGroups,onSetOption:s.setOption},null,8,["groups","onSetOption"]),p(r,T({class:"tree",workflows:s.workflows,hoverable:!1,autoStripTypes:["workflow"],"node-filter-func":s.filterNode,flat:a.flat},{expandAll:t.expandAll,filterState:a.filterState},{ref:"treeComponent"}),null,16,["workflows","node-filter-func","flat"])])}const Q=y(W,[["render",J],["__scopeId","data-v-b247f6c0"]]);export{Q as default};
