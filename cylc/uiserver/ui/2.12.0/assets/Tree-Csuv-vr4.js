import{_ as g,cg as f,ch as c,ci as m,cj as k,a3 as y,a4 as F,ck as x,a6 as b,v as D,g as p,B as u,b8 as T,ad as P,H as A,o as _}from"./index-Dk_oQcLS.js";import{g as S}from"./graphql-Dr9bN1Q1.js";import{i as I,a as w}from"./initialOptions-BnNLz-ak.js";import{V as C}from"./ViewToolbar-Ben90_oc.js";import{g as M,b as N,c as v,a as j}from"./filter-DRtrMOfy.js";const E=A`
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
`,R={name:"Tree",mixins:[S,b],components:{TreeComponent:x,ViewToolbar:C},props:{initialOptions:I},setup(t,{emit:e}){const l=w("tasksFilter",{props:t,emit:e},{id:null,states:null}),s=w("flat",{props:t,emit:e},!1);return{tasksFilter:l,flat:s}},data:()=>({expandAll:null}),computed:{...F("workflows",["cylcTree"]),...y("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},query(){return new P(E,this.variables,"workflow",[],!0,!0)},filterState(){return this.tasksFilter.id?.trim()||this.tasksFilter.states?.length?[this.tasksFilter.id,this.tasksFilter.states,this.flat]:null},controlGroups(){return[{title:"Filter",controls:[{title:"Filter By ID",action:"taskIDFilter",key:"taskIDFilter",value:this.tasksFilter.id},{title:"Filter By State",action:"taskStateFilter",key:"taskStateFilter",value:this.tasksFilter.states}]},{title:"Tree",controls:[{title:"Toggle Families",icon:{true:k,false:m},action:"toggle",value:this.flat,key:"flat"},{title:"Expand All",key:"ExpandAll",icon:f,action:"callback",callback:this.treeExpandAll},{title:"Collapse All",key:"CollapseAll",icon:c,action:"callback",callback:this.treeCollapseAll}]}]}},methods:{setOption(t,e){t==="taskStateFilter"?this.tasksFilter.states=e:t==="taskIDFilter"?this.tasksFilter.id=e:this[t]=e},treeExpandAll(){this.expandAll=["workflow","cycle","family"]},treeCollapseAll(){this.expandAll=[]},filterNode(t,e,l=!1){if(t.type==="job")return!1;const[s,d,a]=M(this.tasksFilter.states?.length?this.tasksFilter.states:[]),i=N(t,s,d,a),o=l||v(t,j(this.tasksFilter.id));let r=i&&o,{children:n}=t;if(t.type==="cycle"&&(n=t.familyTree[0]?.children),!this.flat&&n)for(const h of n)r=this.filterNode(h,e,o)||r;return e.set(t,!r),r}},icons:{mdiFormatAlignJustify:k,mdiFormatAlignRight:m,mdiMinus:c,mdiPlus:f}},W={class:"c-tree h-100 overflow-auto"};function B(t,e,l,s,d,a){const i=u("ViewToolbar"),o=u("TreeComponent");return _(),D("div",W,[p(i,{class:"toolbar",groups:a.controlGroups,onSetOption:a.setOption},null,8,["groups","onSetOption"]),p(o,T({class:"tree",workflows:a.workflows,hoverable:!1,autoStripTypes:["workflow"],"node-filter-func":a.filterNode,flat:s.flat},{expandAll:t.expandAll,filterState:a.filterState},{ref:"treeComponent"}),null,16,["workflows","node-filter-func","flat"])])}const G=g(R,[["render",B],["__scopeId","data-v-90851896"]]);export{G as default};
