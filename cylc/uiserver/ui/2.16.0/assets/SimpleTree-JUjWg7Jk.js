import{n as e}from"./lib-BD1OgZUd.js";import{i as t,r as n}from"./vuex.esm-bundler-DhFCIrIx.js";import{E as r,T as i,w as a}from"./index-_99OrTPv.js";import{_ as o,b as s,bt as c,mt as l,o as u,tr as d}from"./runtime-core.esm-bundler-DZo3dYLJ.js";import{t as f}from"./_plugin-vue_export-helper-BDNMzG2s.js";var p=e`
subscription SimpleTreeSubscription ($workflowID: ID) {
  deltas(workflows: [$workflowID]) {
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
  taskProxies {
    ...TaskProxyData
  }
  jobs {
    ...JobData
  }
}

# We must list all of the types we request data for here to enable automatic
# housekeeping.
fragment PrunedDelta on Pruned {
  workflow
  taskProxies
  jobs
}

# We must always request the reloaded field whenever we are requesting things
# within the workflow like tasks, cycles, etc as this is used to rebuild the
# store when a workflow is reloaded or restarted.
fragment WorkflowData on Workflow {
  id
  reloaded
}

# We must always request the "id" for ALL types.
# The only field this view requires beyond that is the status.
fragment TaskProxyData on TaskProxy {
  id
  state
}

# Same for jobs.
fragment JobData on Job {
  id
  state
}
`,m={name:`SimpleTree`,mixins:[r],setup(e){let{workflowIDs:t,variables:n}=a();return{workflowIDs:t,variables:n}},computed:{...t(`workflows`,[`cylcTree`]),...n(`workflows`,[`getNodes`]),workflows(){return this.getNodes(`workflow`,this.workflowIDs)},query(){return new i(p,this.variables,`workflow`,[])}}},h={class:`c-simple-tree`},g={class:`name`},_={class:`state`},v={class:`name`},y={class:`state`},b={class:`name`},x={class:`state`},S={class:`name`},C={class:`state`};function w(e,t,n,r,i,a){return l(),s(`div`,h,[(l(!0),s(u,null,c(a.workflows,e=>(l(),s(`ul`,{key:e.id},[o(`li`,null,[o(`b`,null,d(e.id),1),(l(!0),s(u,null,c(e.children,e=>(l(),s(`ul`,{key:e.id},[o(`li`,null,[o(`span`,g,d(e.name),1),o(`span`,_,d(e.node.state),1),(l(!0),s(u,null,c(e.children,e=>(l(),s(`ul`,{key:e.id},[o(`li`,null,[o(`span`,v,d(e.name),1),o(`span`,y,d(e.node.state),1),(l(!0),s(u,null,c(e.children,e=>(l(),s(`ul`,{key:e.id},[o(`li`,null,[o(`span`,b,d(e.name),1),o(`span`,x,d(e.node.state),1),(l(!0),s(u,null,c(e.children,e=>(l(),s(`ul`,{key:e.id},[o(`li`,null,[o(`span`,S,d(e.name),1),o(`span`,C,d(e.node.state),1)])]))),128))])]))),128))])]))),128))])]))),128))])]))),128))])}var T=f(m,[[`render`,w]]);export{T as default};