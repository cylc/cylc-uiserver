import{_ as k,J as _,$ as y,a0 as V,a1 as v,a2 as U,a3 as x,a4 as h,a5 as C,W as D,a6 as H,a7 as T,a8 as W,a9 as S,aa as $,j as I,w as e,V as N,h as z,k as t,n as f,l as q,p as w,O as B,ab as g,ac as l,E as r,m as a,t as d,ad as i,ae as n,C as c,F as L}from"./index-CQRaJAEP.js";import{V as b}from"./VDataTable-CgfMuQhE.js";import"./VPagination-C1Is40ky.js";const A=_`
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
`,M={name:"Dashboard",mixins:[y],data(){return{query:new V(A,{},"root",[],!0,!0),events:[]}},computed:{...v("user",["user"]),...U("workflows",["getNodes"]),workflows(){return this.getNodes("workflow")},workflowsTable(){const s=Object.values(this.workflows).map(o=>o.node.status).reduce((o,u)=>(o[u]=(o[u]||0)+1,o),{});return x.enumValues.sort((o,u)=>h.get(o)-h.get(u)).map(o=>({text:o.name.charAt(0).toUpperCase()+o.name.slice(1),count:s[o.name]||0}))},multiUserMode(){return this.user.mode!=="single user"}},workflowsHeader:[{value:"count"},{value:"text"}],eventsHeader:[{value:"id"},{value:"text"}],hubUrl:C("/hub/home",!1,!0),icons:{table:D,settings:H,hub:T,quickstart:W,workflow:S,documentation:$}},O=c("p",{class:"text-h4 mb-2"},"Workflows",-1),E=c("p",{class:"text-h4 mb-2"},"Events",-1),Q=c("td",{class:"text-h6 text-disabled"},"No events",-1);function R(s,o,u,j,p,m){return z(),I(N,{fluid:"","grid-list":"",class:"c-dashboard mt-4 py-0 px-6"},{default:e(()=>[t(w,{wrap:""},{default:e(()=>[t(f,{md:"6",lg:"6"},{default:e(()=>[O,t(b,{headers:s.$options.workflowsHeader,items:m.workflowsTable,loading:s.isLoading,id:"dashboard-workflows","items-per-page":"-1",style:{"font-size":"1rem"}},{headers:e(()=>[]),bottom:e(()=>[]),_:1},8,["headers","items","loading"])]),_:1}),t(f,{md:"6",lg:"6"},{default:e(()=>[E,t(b,{headers:s.$options.eventsHeader,items:p.events},q({headers:e(()=>[]),"no-data":e(()=>[Q]),_:2},[p.events.length?void 0:{name:"bottom",fn:e(()=>[]),key:"0"}]),1032,["headers","items"])]),_:1})]),_:1}),t(B),t(w,{wrap:""},{default:e(()=>[t(f,{md:"6",lg:"6"},{default:e(()=>[t(g,{lines:"three",class:"pa-0"},{default:e(()=>[t(l,{to:"/workflow-table","data-cy":"workflow-table-link"},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.table),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Workflows Table ")]),_:1}),t(n,null,{default:e(()=>[a(" View name, host, port, etc. of your workflows ")]),_:1})]),_:1}),t(l,{to:"/user-profile","data-cy":"user-settings-link"},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.settings),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Settings ")]),_:1}),t(n,null,{default:e(()=>[a(" View your Hub permissions, and alter user preferences ")]),_:1})]),_:1}),c("div",null,[t(l,{id:"cylc-hub-button",disabled:!m.multiUserMode,href:s.$options.hubUrl},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.hub),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Cylc Hub ")]),_:1}),t(n,null,{default:e(()=>[a(" Visit the Hub to manage your running UI Servers ")]),_:1})]),_:1},8,["disabled","href"]),t(L,{disabled:m.multiUserMode},{default:e(()=>[a(" You are not running Cylc UI via Cylc Hub. ")]),_:1},8,["disabled"])])]),_:1})]),_:1}),t(f,{md:"6",lg:"6"},{default:e(()=>[t(g,{lines:"three",class:"pa-0"},{default:e(()=>[t(l,{to:"/guide","data-cy":"quickstart-link"},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.quickstart),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Cylc UI Quickstart ")]),_:1}),t(n,null,{default:e(()=>[a(" Learn how to use the Cylc UI ")]),_:1})]),_:1}),t(l,{href:"https://cylc.github.io/cylc-doc/stable/html/workflow-design-guide/index.html",target:"_blank"},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.workflow),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Workflow Design Guide ")]),_:1}),t(n,null,{default:e(()=>[a(" How to make complex Cylc workflows and Rose suites simpler and easier to maintain ")]),_:1})]),_:1}),t(l,{href:"https://cylc.github.io/cylc-doc/stable/html/index.html",target:"_blank"},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.documentation),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Documentation ")]),_:1}),t(n,null,{default:e(()=>[a(" The complete Cylc documentation ")]),_:1})]),_:1})]),_:1})]),_:1})]),_:1})]),_:1})}const J=k(M,[["render",R]]);export{J as default};
