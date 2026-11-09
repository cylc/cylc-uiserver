import{D as e,St as t,b as n,et as r,mt as i,vn as a}from"./runtime-core.esm-bundler-DZo3dYLJ.js";import{i as o,r as s}from"./vuex.esm-bundler-DhFCIrIx.js";import{I as c,L as l,ht as u,nt as d}from"./mdi-DCsggE_y.js";import{n as f}from"./lib-BD1OgZUd.js";import{E as p,O as m,T as h,w as g}from"./index-_99OrTPv.js";import{r as _,t as v}from"./initialOptions-CHcgzlQU.js";import{t as y}from"./ViewToolbar-BCEZdBEB.js";import{a as b,n as x,o as S,r as C,t as w}from"./filter-D5prhhLM.js";import{t as T}from"./_plugin-vue_export-helper-BDNMzG2s.js";var E=f`
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
`,D={name:`Tree`,mixins:[p],components:{TreeComponent:m,ViewToolbar:y},props:{initialOptions:v},setup(e,{emit:t}){let{workflowIDs:n,variables:r}=g(),i=_(`tasksFilter`,{props:e,emit:t},{id:null,states:null}),o=S(i),s=_(`flat`,{props:e,emit:t},!1);return{expandAll:a(null),tasksFilter:i,filterState:o,flat:s,workflowIDs:n,variables:r}},computed:{...o(`workflows`,[`cylcTree`]),...s(`workflows`,[`getNodes`]),workflows(){return this.getNodes(`workflow`,this.workflowIDs)},query(){return new h(E,this.variables,`workflow`,[],!0,!0)},controlGroups(){return[{title:`Filter`,controls:[{title:`Filter By ID`,action:`taskIDFilter`,key:`taskIDFilter`,value:this.tasksFilter.id},{title:`Filter By State`,action:`taskStateFilter`,key:`taskStateFilter`,value:this.tasksFilter.states}]},{title:`Tree`,controls:[{title:`Toggle Families`,icon:{true:c,false:l},action:`toggle`,value:this.flat,key:`flat`},{title:`Expand All`,key:`ExpandAll`,icon:u,action:`callback`,callback:this.treeExpandAll},{title:`Collapse All`,key:`CollapseAll`,icon:d,action:`callback`,callback:this.treeCollapseAll}]}]}},methods:{setOption(e,t){e===`taskStateFilter`?this.tasksFilter.states=t:e===`taskIDFilter`?this.tasksFilter.id=t:this[e]=t},treeExpandAll(){this.expandAll=[`workflow`,`cycle`,`family`]},treeCollapseAll(){this.expandAll=[]},filterNode(e,t,n=!1){if(e.type===`job`)return!1;let[r,i,a]=x(this.tasksFilter.states?.length?this.tasksFilter.states:[]),o=b(e,r,i,a),s=n||C(e,w(this.tasksFilter.id)),c=o&&s,l=e.type===`cycle`?e.rootFamily?.children:e.children;if(l)for(let e of l)c=this.filterNode(e,t,s)||c;return t.set(e,!c),c}},icons:{mdiFormatAlignJustify:c,mdiFormatAlignRight:l,mdiMinus:d,mdiPlus:u}},O={class:`c-tree h-100 overflow-auto`};function k(a,o,s,c,l,u){let d=t(`ViewToolbar`),f=t(`TreeComponent`);return i(),n(`div`,O,[e(d,{class:`toolbar`,groups:u.controlGroups,onSetOption:u.setOption},null,8,[`groups`,`onSetOption`]),e(f,r({class:`tree`,workflows:u.workflows,hoverable:!1,autoStripTypes:[`workflow`],"node-filter-func":u.filterNode,flat:c.flat},{expandAll:c.expandAll,filterState:c.filterState},{ref:`treeComponent`}),null,16,[`workflows`,`node-filter-func`,`flat`])])}var A=T(D,[[`render`,k],[`__scopeId`,`data-v-80bc40c8`]]);export{A as default};