import{_ as p,i as m,s as w,j as _,q as f,u as k,S as h,k as t,R as r,d as l,o as s,L as e,t as a}from"./index-4d6c7840.js";import{g as y}from"./graphql-c1d511dc.js";const D=m`
subscription SimpleTreeSubscription ($workflowId: ID) {
  deltas(workflows: [$workflowId]) {
    ...Deltas
  }
}

fragment Deltas on Deltas {
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

fragment AddedDelta on Added {
  taskProxies {
    ...TaskProxyData
  }
  jobs {
    ...JobData
  }
}

fragment UpdatedDelta on Updated {
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
`,g={name:"SimpleTree",mixins:[y,w],head(){return{title:_("App.workflow",{name:this.workflowName})}},computed:{...f("workflows",["cylcTree"]),...k("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},query(){return new h(D,this.variables,"workflow",[])}}},b={class:"c-simple-tree"},x={class:"name"},P={class:"state"},T={class:"name"},S={class:"state"},q={class:"name"},I={class:"state"},j={class:"name"},v={class:"state"};function A(N,$,J,L,U,c){return s(),t("div",b,[(s(!0),t(r,null,l(c.workflows,u=>(s(),t("ul",{key:u.id},[e("li",null,[e("b",null,a(u.id),1),(s(!0),t(r,null,l(u.children,o=>(s(),t("ul",{key:o.id},[e("li",null,[e("span",x,a(o.name),1),e("span",P,a(o.node.state),1),(s(!0),t(r,null,l(o.children,n=>(s(),t("ul",{key:n.id},[e("li",null,[e("span",T,a(n.name),1),e("span",S,a(n.node.state),1),(s(!0),t(r,null,l(n.children,i=>(s(),t("ul",{key:i.id},[e("li",null,[e("span",q,a(i.name),1),e("span",I,a(i.node.state),1),(s(!0),t(r,null,l(i.children,d=>(s(),t("ul",{key:d.id},[e("li",null,[e("span",j,a(d.name),1),e("span",v,a(d.node.state),1)])]))),128))])]))),128))])]))),128))])]))),128))])]))),128))])}const M=p(g,[["render",A]]);export{M as default};
