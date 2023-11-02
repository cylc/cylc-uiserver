import{bz as _,c6 as k,ce as y,c7 as v,cf as V,cg as C,ch as U,ci as x,cj as w,ck as D,ca as H,cl as T,cm as z,cn as S,co as W,cp as I,aM as N,o as $,bs as e,bC as q,az as A,z as t,bD as c,w as B,bE as b,cq as L,cr as g,cs as l,c4 as r,y as a,a_ as d,ct as i,cu as n,r as f,c5 as M}from"./index-3996a8d9.js";const E=k`
subscription App {
  deltas {
    id
    added {
      ...AddedDelta
    }
    updated (stripNull: true) {
      ...UpdatedDelta
    }
    pruned {
      workflow
    }
  }
}

fragment AddedDelta on Added {
  workflow {
    ...WorkflowData
  }
}

fragment UpdatedDelta on Updated {
  workflow {
    ...WorkflowData
  }
}

fragment WorkflowData on Workflow {
  # NOTE: do not request the "reloaded" event here
  # (it would cause a race condition with the workflow subscription)
  id
  status
}
`,O={name:"Dashboard",mixins:[y],head(){return{title:v("App.dashboard")}},data(){return{query:new V(E,{},"root",[],!0,!0),events:[]}},computed:{...C("user",["user"]),...U("workflows",["getNodes"]),workflows(){return this.getNodes("workflow")},workflowsTable(){const s=Object.values(this.workflows).map(o=>o.node.status).reduce((o,u)=>(o[u]=(o[u]||0)+1,o),{});return x.enumValues.sort((o,u)=>w.get(o)-w.get(u)).map(o=>({text:o.name.charAt(0).toUpperCase()+o.name.slice(1),count:s[o.name]||0}))},multiUserMode(){return this.user.mode!=="single user"}},workflowsHeader:[{value:"count"},{value:"text"}],eventsHeader:[{value:"id"},{value:"text"}],hubUrl:D("/hub/home",!1,!0),icons:{table:H,settings:T,hub:z,quickstart:S,workflow:W,documentation:I}},Q=f("p",{class:"text-h4 mb-2"},"Workflows",-1),R=f("p",{class:"text-h4 mb-2"},"Events",-1),j=f("td",{class:"text-h6 text-disabled"},"No events",-1);function G(s,o,u,Y,h,p){const m=N("v-data-table");return A(),$(q,{fluid:"","grid-list":"",class:"c-dashboard mt-4 py-0 px-6"},{default:e(()=>[t(b,{wrap:""},{default:e(()=>[t(c,{md:"6",lg:"6"},{default:e(()=>[Q,t(m,{headers:s.$options.workflowsHeader,items:p.workflowsTable,loading:s.isLoading,id:"dashboard-workflows","items-per-page":"-1"},{headers:e(()=>[]),bottom:e(()=>[]),_:1},8,["headers","items","loading"])]),_:1}),t(c,{md:"6",lg:"6"},{default:e(()=>[R,t(m,{headers:s.$options.eventsHeader,items:h.events},B({headers:e(()=>[]),"no-data":e(()=>[j]),_:2},[h.events.length?void 0:{name:"bottom",fn:e(()=>[]),key:"0"}]),1032,["headers","items"])]),_:1})]),_:1}),t(L),t(b,{wrap:""},{default:e(()=>[t(c,{md:"6",lg:"6"},{default:e(()=>[t(g,{lines:"three",class:"pa-0"},{default:e(()=>[t(l,{to:"/workflow-table","data-cy":"workflow-table-link"},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.table),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Workflows Table ")]),_:1}),t(n,null,{default:e(()=>[a(" View name, host, port, etc. of your workflows ")]),_:1})]),_:1}),t(l,{to:"/user-profile","data-cy":"user-settings-link"},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.settings),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Settings ")]),_:1}),t(n,null,{default:e(()=>[a(" View your Hub permissions, and alter user preferences ")]),_:1})]),_:1}),f("div",null,[t(l,{id:"cylc-hub-button",disabled:!p.multiUserMode,href:s.$options.hubUrl},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.hub),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Cylc Hub ")]),_:1}),t(n,null,{default:e(()=>[a(" Visit the Hub to manage your running UI Servers ")]),_:1})]),_:1},8,["disabled","href"]),t(M,{disabled:p.multiUserMode},{default:e(()=>[a(" You are not running Cylc UI via Cylc Hub. ")]),_:1},8,["disabled"])])]),_:1})]),_:1}),t(c,{md:"6",lg:"6"},{default:e(()=>[t(g,{lines:"three",class:"pa-0"},{default:e(()=>[t(l,{to:"/guide","data-cy":"quickstart-link"},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.quickstart),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Cylc UI Quickstart ")]),_:1}),t(n,null,{default:e(()=>[a(" Learn how to use the Cylc UI ")]),_:1})]),_:1}),t(l,{href:"https://cylc.github.io/cylc-doc/stable/html/workflow-design-guide/index.html",target:"_blank"},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.workflow),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Workflow Design Guide ")]),_:1}),t(n,null,{default:e(()=>[a(" How to make complex Cylc workflows and Rose suites simpler and easier to maintain ")]),_:1})]),_:1}),t(l,{href:"https://cylc.github.io/cylc-doc/stable/html/index.html",target:"_blank"},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.documentation),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Documentation ")]),_:1}),t(n,null,{default:e(()=>[a(" The complete Cylc documentation ")]),_:1})]),_:1})]),_:1})]),_:1})]),_:1})]),_:1})}const F=_(O,[["render",G]]);export{F as default};
