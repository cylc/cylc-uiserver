import{D as e,H as t,R as n,_ as r,dt as i,p as a}from"./runtime-core.esm-bundler-CilEyzAc.js";import{t as o}from"./ViewToolbar-DFsrpfa5.js";import{I as s,L as c,ht as l,nt as u}from"./mdi-DCsggE_y.js";import{n as d}from"./lib-CWAdvCqp.js";import{i as f,r as p}from"./vuex.esm-bundler-DiFTMXj2.js";import{a as m,n as h,o as g,r as _,t as v}from"./filter-FSggriUT.js";import{t as y}from"./_plugin-vue_export-helper-BDNMzG2s.js";import{E as b,O as x,T as S,w as C}from"./index-C9-ypOBE.js";import{r as w,t as T}from"./initialOptions-Bou6yVjH.js";var E=d`
subscription Workflow ($workflowID: ID) {
  deltas (workflows: [$workflowID]) {
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
  graphDepth
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
  graphDepth
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
`,D={name:`Tree`,mixins:[b],components:{TreeComponent:x,ViewToolbar:o},props:{initialOptions:T},setup(e,{emit:t}){let{workflowIDs:n,variables:r}=C(),a=w(`tasksFilter`,{props:e,emit:t},{id:null,states:null}),o=g(a),s=w(`flat`,{props:e,emit:t},!1);return{expandAll:i(null),tasksFilter:a,filterState:o,flat:s,workflowIDs:n,variables:r}},computed:{...f(`workflows`,[`cylcTree`]),...p(`workflows`,[`getNodes`]),workflows(){return this.getNodes(`workflow`,this.workflowIDs)},query(){return new S(E,this.variables,`workflow`,[],!0,!0)},controlGroups(){return[{title:`Filter`,controls:[{title:`Filter By ID`,action:`taskIDFilter`,key:`taskIDFilter`,value:this.tasksFilter.id},{title:`Filter By State`,action:`taskStateFilter`,key:`taskStateFilter`,value:this.tasksFilter.states}]},{title:`Tree`,controls:[{title:`Toggle Families`,icon:{true:s,false:c},action:`toggle`,value:this.flat,key:`flat`},{title:`Expand All`,key:`ExpandAll`,icon:l,action:`callback`,callback:this.treeExpandAll},{title:`Collapse All`,key:`CollapseAll`,icon:u,action:`callback`,callback:this.treeCollapseAll}]}]}},methods:{setOption(e,t){e===`taskStateFilter`?this.tasksFilter.states=t:e===`taskIDFilter`?this.tasksFilter.id=t:this[e]=t},treeExpandAll(){this.expandAll=[`workflow`,`cycle`,`family`]},treeCollapseAll(){this.expandAll=[]},filterNode(e,t,n=!1){if(e.type===`job`)return!1;let[r,i,a]=h(this.tasksFilter.states?.length?this.tasksFilter.states:[]),o=m(e,r,i,a),s=n||_(e,v(this.tasksFilter.id)),c=o&&s,{children:l}=e;if(e.type===`cycle`&&(l=e.familyTree[0]?.children),l)for(let e of l)c=this.filterNode(e,t,s)||c;return t.set(e,!c),c}},icons:{mdiFormatAlignJustify:s,mdiFormatAlignRight:c,mdiMinus:u,mdiPlus:l}},O={class:`c-tree h-100 overflow-auto`};function k(i,o,s,c,l,u){let d=t(`ViewToolbar`),f=t(`TreeComponent`);return n(),a(`div`,O,[r(d,{class:`toolbar`,groups:u.controlGroups,onSetOption:u.setOption},null,8,[`groups`,`onSetOption`]),r(f,e({class:`tree`,workflows:u.workflows,hoverable:!1,autoStripTypes:[`workflow`],"node-filter-func":u.filterNode,flat:c.flat},{expandAll:c.expandAll,filterState:c.filterState},{ref:`treeComponent`}),null,16,[`workflows`,`node-filter-func`,`flat`])])}var A=y(D,[[`render`,k],[`__scopeId`,`data-v-594f1db0`]]);export{A as default};