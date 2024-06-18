import{_ as k,L as _,a1 as y,a2 as V,a3 as v,a4 as U,a5 as x,a6 as h,a7 as D,Y as C,a8 as H,a9 as T,aa as S,ab as W,ac as I,l as N,w as e,V as $,k as q,m as t,q as f,n as z,v as w,Q as L,ad as g,ae as l,G as r,p as a,t as d,af as i,ag as n,E as c,H as B}from"./index-DSRpE5Rv.js";import{V as b}from"./VDataTable-DeJrdP8M.js";import"./VPagination-DeW5L5cH.js";const A=_`
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
`,M={name:"Dashboard",mixins:[y],data(){return{query:new V(A,{},"root",[],!0,!0),events:[]}},computed:{...v("user",["user"]),...U("workflows",["getNodes"]),workflows(){return this.getNodes("workflow")},workflowsTable(){const s=Object.values(this.workflows).map(o=>o.node.status).reduce((o,u)=>(o[u]=(o[u]||0)+1,o),{});return x.enumValues.sort((o,u)=>h.get(o)-h.get(u)).map(o=>({text:o.name.charAt(0).toUpperCase()+o.name.slice(1),count:s[o.name]||0}))},multiUserMode(){return this.user.mode!=="single user"}},workflowsHeader:[{value:"count"},{value:"text"}],eventsHeader:[{value:"id"},{value:"text"}],hubUrl:D("/hub/home",!1,!0),icons:{table:C,settings:H,hub:T,quickstart:S,workflow:W,documentation:I}},E=c("p",{class:"text-h4 mb-2"},"Workflows",-1),O=c("p",{class:"text-h4 mb-2"},"Events",-1),Q=c("td",{class:"text-h6 text-disabled"},"No events",-1);function G(s,o,u,R,p,m){return q(),N($,{fluid:"","grid-list":"",class:"c-dashboard mt-4 py-0 px-6"},{default:e(()=>[t(w,{wrap:""},{default:e(()=>[t(f,{md:"6",lg:"6"},{default:e(()=>[E,t(b,{headers:s.$options.workflowsHeader,items:m.workflowsTable,loading:s.isLoading,id:"dashboard-workflows","items-per-page":"-1",style:{"font-size":"1rem"}},{headers:e(()=>[]),bottom:e(()=>[]),_:1},8,["headers","items","loading"])]),_:1}),t(f,{md:"6",lg:"6"},{default:e(()=>[O,t(b,{headers:s.$options.eventsHeader,items:p.events},z({headers:e(()=>[]),"no-data":e(()=>[Q]),_:2},[p.events.length?void 0:{name:"bottom",fn:e(()=>[]),key:"0"}]),1032,["headers","items"])]),_:1})]),_:1}),t(L),t(w,{wrap:""},{default:e(()=>[t(f,{md:"6",lg:"6"},{default:e(()=>[t(g,{lines:"three",class:"pa-0"},{default:e(()=>[t(l,{to:"/workflow-table","data-cy":"workflow-table-link"},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.table),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Workflows Table ")]),_:1}),t(n,null,{default:e(()=>[a(" View name, host, port, etc. of your workflows ")]),_:1})]),_:1}),t(l,{to:"/user-profile","data-cy":"user-settings-link"},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.settings),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Settings ")]),_:1}),t(n,null,{default:e(()=>[a(" View your Hub permissions, and alter user preferences ")]),_:1})]),_:1}),c("div",null,[t(l,{id:"cylc-hub-button",disabled:!m.multiUserMode,href:s.$options.hubUrl},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.hub),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Cylc Hub ")]),_:1}),t(n,null,{default:e(()=>[a(" Visit the Hub to manage your running UI Servers ")]),_:1})]),_:1},8,["disabled","href"]),t(B,{disabled:m.multiUserMode},{default:e(()=>[a(" You are not running Cylc UI via Cylc Hub. ")]),_:1},8,["disabled"])])]),_:1})]),_:1}),t(f,{md:"6",lg:"6"},{default:e(()=>[t(g,{lines:"three",class:"pa-0"},{default:e(()=>[t(l,{to:"/guide","data-cy":"quickstart-link"},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.quickstart),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Cylc UI Quickstart ")]),_:1}),t(n,null,{default:e(()=>[a(" Learn how to use the Cylc UI ")]),_:1})]),_:1}),t(l,{href:"https://cylc.github.io/cylc-doc/stable/html/workflow-design-guide/index.html",target:"_blank"},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.workflow),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Workflow Design Guide ")]),_:1}),t(n,null,{default:e(()=>[a(" How to make complex Cylc workflows and Rose suites simpler and easier to maintain ")]),_:1})]),_:1}),t(l,{href:"https://cylc.github.io/cylc-doc/stable/html/index.html",target:"_blank"},{prepend:e(()=>[t(r,{size:"1.6em"},{default:e(()=>[a(d(s.$options.icons.documentation),1)]),_:1})]),default:e(()=>[t(i,{class:"text-h6 font-weight-light"},{default:e(()=>[a(" Documentation ")]),_:1}),t(n,null,{default:e(()=>[a(" The complete Cylc documentation ")]),_:1})]),_:1})]),_:1})]),_:1})]),_:1})]),_:1})}const J=k(M,[["render",G]]);export{J as default};
