import{B as e,R as t,Rt as n,i as r,p as i,u as a}from"./runtime-core.esm-bundler-CilEyzAc.js";import{n as o}from"./lib-CWAdvCqp.js";import{i as s,r as c}from"./vuex.esm-bundler-DiFTMXj2.js";import{t as l}from"./_plugin-vue_export-helper-BDNMzG2s.js";import{E as u,T as d,w as f}from"./index-C9-ypOBE.js";var p=o`
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
`,m={name:`SimpleTree`,mixins:[u],setup(e){let{workflowIDs:t,variables:n}=f();return{workflowIDs:t,variables:n}},computed:{...s(`workflows`,[`cylcTree`]),...c(`workflows`,[`getNodes`]),workflows(){return this.getNodes(`workflow`,this.workflowIDs)},query(){return new d(p,this.variables,`workflow`,[])}}},h={class:`c-simple-tree`},g={class:`name`},_={class:`state`},v={class:`name`},y={class:`state`},b={class:`name`},x={class:`state`},S={class:`name`},C={class:`state`};function w(o,s,c,l,u,d){return t(),i(`div`,h,[(t(!0),i(r,null,e(d.workflows,o=>(t(),i(`ul`,{key:o.id},[a(`li`,null,[a(`b`,null,n(o.id),1),(t(!0),i(r,null,e(o.children,o=>(t(),i(`ul`,{key:o.id},[a(`li`,null,[a(`span`,g,n(o.name),1),a(`span`,_,n(o.node.state),1),(t(!0),i(r,null,e(o.children,o=>(t(),i(`ul`,{key:o.id},[a(`li`,null,[a(`span`,v,n(o.name),1),a(`span`,y,n(o.node.state),1),(t(!0),i(r,null,e(o.children,o=>(t(),i(`ul`,{key:o.id},[a(`li`,null,[a(`span`,b,n(o.name),1),a(`span`,x,n(o.node.state),1),(t(!0),i(r,null,e(o.children,e=>(t(),i(`ul`,{key:e.id},[a(`li`,null,[a(`span`,S,n(e.name),1),a(`span`,C,n(e.node.state),1)])]))),128))])]))),128))])]))),128))])]))),128))])]))),128))])}var T=l(m,[[`render`,w]]);export{T as default};