import{bE as w,bU as f,c0 as p,bV as k,c2 as m,c3 as h,c1 as _,u as t,F as r,aP as o,aE as s,v as e,b3 as a}from"./index-C2AHI-HK.js";import{g as b}from"./graphql-BScASb0Q.js";const y=f`
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
`,D={name:"SimpleTree",mixins:[b,p],head(){return{title:k("App.workflow",{name:this.workflowName})}},computed:{...m("workflows",["cylcTree"]),...h("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},query(){return new _(y,this.variables,"workflow",[])}}},g={class:"c-simple-tree"},x={class:"name"},P={class:"state"},T={class:"name"},q={class:"state"},S={class:"name"},W={class:"state"},I={class:"name"},v={class:"state"};function A(N,U,$,j,E,c){return s(),t("div",g,[(s(!0),t(r,null,o(c.workflows,d=>(s(),t("ul",{key:d.id},[e("li",null,[e("b",null,a(d.id),1),(s(!0),t(r,null,o(d.children,l=>(s(),t("ul",{key:l.id},[e("li",null,[e("span",x,a(l.name),1),e("span",P,a(l.node.state),1),(s(!0),t(r,null,o(l.children,n=>(s(),t("ul",{key:n.id},[e("li",null,[e("span",T,a(n.name),1),e("span",q,a(n.node.state),1),(s(!0),t(r,null,o(n.children,i=>(s(),t("ul",{key:i.id},[e("li",null,[e("span",S,a(i.name),1),e("span",W,a(i.node.state),1),(s(!0),t(r,null,o(i.children,u=>(s(),t("ul",{key:u.id},[e("li",null,[e("span",I,a(u.name),1),e("span",v,a(u.node.state),1)])]))),128))])]))),128))])]))),128))])]))),128))])]))),128))])}const L=w(D,[["render",A]]);export{L as default};
