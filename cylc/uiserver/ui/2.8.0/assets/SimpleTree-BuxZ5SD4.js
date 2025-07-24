import{_ as w,a4 as f,a5 as p,a7 as k,x as t,o as s,F as r,r as o,z as e,t as a,ae as m,I as h}from"./index-EpcknQ5m.js";import{g as _}from"./graphql-n5gzreXW.js";const y=h`
subscription SimpleTreeSubscription ($workflowId: ID) {
  deltas(workflows: [$workflowId]) {
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
`,D={name:"SimpleTree",mixins:[_,k],computed:{...p("workflows",["cylcTree"]),...f("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},query(){return new m(y,this.variables,"workflow",[])}}},b={class:"c-simple-tree"},g={class:"name"},x={class:"state"},P={class:"name"},T={class:"state"},q={class:"name"},S={class:"state"},I={class:"name"},W={class:"state"};function $(j,v,A,J,N,c){return s(),t("div",b,[(s(!0),t(r,null,o(c.workflows,d=>(s(),t("ul",{key:d.id},[e("li",null,[e("b",null,a(d.id),1),(s(!0),t(r,null,o(d.children,l=>(s(),t("ul",{key:l.id},[e("li",null,[e("span",g,a(l.name),1),e("span",x,a(l.node.state),1),(s(!0),t(r,null,o(l.children,n=>(s(),t("ul",{key:n.id},[e("li",null,[e("span",P,a(n.name),1),e("span",T,a(n.node.state),1),(s(!0),t(r,null,o(n.children,i=>(s(),t("ul",{key:i.id},[e("li",null,[e("span",q,a(i.name),1),e("span",S,a(i.node.state),1),(s(!0),t(r,null,o(i.children,u=>(s(),t("ul",{key:u.id},[e("li",null,[e("span",I,a(u.name),1),e("span",W,a(u.node.state),1)])]))),128))])]))),128))])]))),128))])]))),128))])]))),128))])}const L=w(D,[["render",$]]);export{L as default};
