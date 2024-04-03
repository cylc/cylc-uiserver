import{bE as k,bU as _,c0 as y,bV as V,c1 as v,c2 as U,c3 as x,c4 as D,c5 as m,c6 as C,bY as H,c7 as T,c8 as I,c9 as S,ca as W,cb as N,s as $,bx as e,bH as z,aE as A,I as t,bI as c,A as q,bJ as w,cc as B,cd as b,ce as l,bR as r,H as a,b3 as d,cf as i,cg as n,v as f,bS as L}from"./index-C2AHI-HK.js";import{V as g}from"./VDataTable-BEEIiNy3.js";const E=_`
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
`,M={name:"Dashboard",mixins:[y],head(){return{title:V("App.dashboard")}},data(){return{query:new v(E,{},"root",[],!0,!0),events:[]}},computed:{...U("user",["user"]),...x("workflows",["getNodes"]),workflows(){return this.getNodes("workflow")},workflowsTable(){const s=Object.values(this.workflows).map(o=>o.node.status).reduce((o,u)=>(o[u]=(o[u]||0)+1,o),{});return D.enumValues.sort((o,u)=>m.get(o)-m.get(u)).map(o=>({text:o.name.charAt(0).toUpperCase()+o.name.slice(1),count:s[o.name]||0}))},multiUserMode(){return this.user.mode!=="single user"}},workflowsHeader:[{value:"count"},{value:"text"}],eventsHeader:[{value:"id"},{value:"text"}],hubUrl:C("/hub/home",!1,!0),icons:{table:H,settings:T,hub:I,quickstart:S,workflow:W,documentation:N}},O=f("p",{class:"text-h4 mb-2"},"Workflows",-1),R=f("p",{class:"text-h4 mb-2"},"Events",-1),Q=f("td",{class:"text-h6 text-disabled"},"No events",-1);function Y(s,o,u,G,p,h){return A(),$(z,{fluid:"","grid-list":"",class:"c-dashboard mt-4 py-0 px-6"},{default:e(()=>[t(w,{wrap:""},{default:e(()=>[t(c,{md:"6",lg:"6"},{default:e(()=>[O,t(g,{headers:s.$options.workflowsHeader,items:h.workflowsTable,loading:s.isLoading,id:"dashboard-workflows","items-per-page":"-1",style:{"font-size":"1rem"}},{headers:e(()=>[]),bottom:e(()=>[]),_:1},8,["headers","items","loading"])]),_:1}),t(c,{md:"6",lg:"6"},{default:e(()=>[R,t(g,{headers:s.$options.eventsHeader,items:p.events},q({headers:e(()=>[]),"no-data":e(()=>[Q]),_:2},[p.events.length?void 0:{name:"bottom",fn:e(()=>[]),key:"0"}]),1032,["headers","items"])]),_:1})]),_:1}),t(B),t(w,{wrap:""},{default:e(()=>[t(c,{md:"6",lg:"6"},{default:e(()=>[t(b,{lines:"three",class:"pa-0"},{default:e(()=>[t(l,{to:"/workflow-table","data-cy":"workflow-table-link"},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.table),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Workflows Table ")]),_:1}),t(n,null,{default:e(()=>[a(" View name, host, port, etc. of your workflows ")]),_:1})]),_:1}),t(l,{to:"/user-profile","data-cy":"user-settings-link"},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.settings),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Settings ")]),_:1}),t(n,null,{default:e(()=>[a(" View your Hub permissions, and alter user preferences ")]),_:1})]),_:1}),f("div",null,[t(l,{id:"cylc-hub-button",disabled:!h.multiUserMode,href:s.$options.hubUrl},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.hub),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Cylc Hub ")]),_:1}),t(n,null,{default:e(()=>[a(" Visit the Hub to manage your running UI Servers ")]),_:1})]),_:1},8,["disabled","href"]),t(L,{disabled:h.multiUserMode},{default:e(()=>[a(" You are not running Cylc UI via Cylc Hub. ")]),_:1},8,["disabled"])])]),_:1})]),_:1}),t(c,{md:"6",lg:"6"},{default:e(()=>[t(b,{lines:"three",class:"pa-0"},{default:e(()=>[t(l,{to:"/guide","data-cy":"quickstart-link"},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.quickstart),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Cylc UI Quickstart ")]),_:1}),t(n,null,{default:e(()=>[a(" Learn how to use the Cylc UI ")]),_:1})]),_:1}),t(l,{href:"https://cylc.github.io/cylc-doc/stable/html/workflow-design-guide/index.html",target:"_blank"},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.workflow),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Workflow Design Guide ")]),_:1}),t(n,null,{default:e(()=>[a(" How to make complex Cylc workflows and Rose suites simpler and easier to maintain ")]),_:1})]),_:1}),t(l,{href:"https://cylc.github.io/cylc-doc/stable/html/index.html",target:"_blank"},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.documentation),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Documentation ")]),_:1}),t(n,null,{default:e(()=>[a(" The complete Cylc documentation ")]),_:1})]),_:1})]),_:1})]),_:1})]),_:1})]),_:1})}const P=k(M,[["render",Y]]);export{P as default};
