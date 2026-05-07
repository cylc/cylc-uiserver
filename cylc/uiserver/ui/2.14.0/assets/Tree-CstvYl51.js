import{_ as y,co as f,cp as c,cq as m,cr as k,a3 as g,a4 as b,cs as x,a6 as F,q as D,g as p,A as u,b8 as T,ad as P,H as _,o as A}from"./index-PqzDRcKR.js";import{g as S}from"./graphql-BSOF_UqA.js";import{i as I,a as w}from"./initialOptions-4bVsJsyJ.js";import{V as C}from"./ViewToolbar-iTqAo6Zf.js";import{g as M,b as N,c as R,a as v,u as E}from"./filter-vc3zbvID.js";const W=_`
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
  isHeld
  isQueued
  isRunahead
  isRetry
  isWallclock
  isXtriggered
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
`,j={name:"Tree",mixins:[S,F],components:{TreeComponent:x,ViewToolbar:C},props:{initialOptions:I},setup(t,{emit:e}){const l=w("tasksFilter",{props:t,emit:e},{id:null,states:null}),a=E(l),o=w("flat",{props:t,emit:e},!1);return{tasksFilter:l,filterState:a,flat:o}},data:()=>({expandAll:null}),computed:{...b("workflows",["cylcTree"]),...g("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},query(){return new P(W,this.variables,"workflow",[],!0,!0)},controlGroups(){return[{title:"Filter",controls:[{title:"Filter By ID",action:"taskIDFilter",key:"taskIDFilter",value:this.tasksFilter.id},{title:"Filter By State",action:"taskStateFilter",key:"taskStateFilter",value:this.tasksFilter.states}]},{title:"Tree",controls:[{title:"Toggle Families",icon:{true:k,false:m},action:"toggle",value:this.flat,key:"flat"},{title:"Expand All",key:"ExpandAll",icon:f,action:"callback",callback:this.treeExpandAll},{title:"Collapse All",key:"CollapseAll",icon:c,action:"callback",callback:this.treeCollapseAll}]}]}},methods:{setOption(t,e){t==="taskStateFilter"?this.tasksFilter.states=e:t==="taskIDFilter"?this.tasksFilter.id=e:this[t]=e},treeExpandAll(){this.expandAll=["workflow","cycle","family"]},treeCollapseAll(){this.expandAll=[]},filterNode(t,e,l=!1){if(t.type==="job")return!1;const[a,o,s]=M(this.tasksFilter.states?.length?this.tasksFilter.states:[]),n=N(t,a,o,s),r=l||R(t,v(this.tasksFilter.id));let i=n&&r,{children:d}=t;if(t.type==="cycle"&&(d=t.familyTree[0]?.children),d)for(const h of d)i=this.filterNode(h,e,r)||i;return e.set(t,!i),i}},icons:{mdiFormatAlignJustify:k,mdiFormatAlignRight:m,mdiMinus:c,mdiPlus:f}},q={class:"c-tree h-100 overflow-auto"};function J(t,e,l,a,o,s){const n=u("ViewToolbar"),r=u("TreeComponent");return A(),D("div",q,[p(n,{class:"toolbar",groups:s.controlGroups,onSetOption:s.setOption},null,8,["groups","onSetOption"]),p(r,T({class:"tree",workflows:s.workflows,hoverable:!1,autoStripTypes:["workflow"],"node-filter-func":s.filterNode,flat:a.flat},{expandAll:t.expandAll,filterState:a.filterState},{ref:"treeComponent"}),null,16,["workflows","node-filter-func","flat"])])}const G=y(j,[["render",J],["__scopeId","data-v-fddbdeab"]]);export{G as default};
