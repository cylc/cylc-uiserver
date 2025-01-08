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
`,J={name:"Dashboard",mixins:[k],data(){return{query:new S(K,{},"root",[],!0,!0),events:[]}},computed:{...F("user",["user"]),...f("workflows",["getNodes"]),workflows(){return this.getNodes("workflow")},workflowsTable(){const s=Object.values(this.workflows).map(e=>e.node.status).reduce((e,h)=>(e[h]=(e[h]||0)+1,e),{});return y.enumValues.sort((e,h)=>M.get(e)-M.get(h)).map(e=>({text:e.name.charAt(0).toUpperCase()+e.name.slice(1),count:s[e.name]||0}))},multiUserMode(){return this.user.mode!=="single user"}},workflowsHeader:[{value:"count"},{value:"text"}],eventsHeader:[{value:"id"},{value:"text"}],hubUrl:D("/hub/home",!1,!0),icons:{table:E,settings:P,hub:Z,quickstart:q,workflow:T,documentation:G,jupyterLogo:U,mdiGraphql:_}},X=r("p",{class:"text-h4 mb-2"},"Workflows",-1),Y=r("p",{class:"text-h4 mb-2"},"Events",-1),$=r("td",{class:"text-h6 text-disabled"},"No events",-1);function t0(s,e,h,z,a,p){return R(),I(O,{fluid:"","grid-list":"",class:"c-dashboard mt-4 py-0 px-6"},{default:t(()=>[c(C,{wrap:""},{default:t(()=>[c(w,{md:"6",lg:"6"},{default:t(()=>[X,c(B,{headers:s.$options.workflowsHeader,items:p.workflowsTable,loading:s.isLoading,id:"dashboard-workflows","items-per-page":"-1",style:{"font-size":"1rem"}},{headers:t(()=>[]),bottom:t(()=>[]),_:1},8,["headers","items","loading"])]),_:1}),c(w,{md:"6",lg:"6"},{default:t(()=>[Y,c(B,{headers:s.$options.eventsHeader,items:a.events},N({headers:t(()=>[]),"no-data":t(()=>[$]),_:2},[a.events.length?void 0:{name:"bottom",fn:t(()=>[]),key:"0"}]),1032,["headers","items"])]),_:1})]),_:1}),c(W),c(C,{wrap:""},{default:t(()=>[c(w,{md:"6",lg:"6"},{default:t(()=>[c(H,{lines:"three",class:"pa-0"},{default:t(()=>{var u,d,x;return[c(v,{to:"/workflow-table","data-cy":"workflow-table-link"},{prepend:t(()=>[c(i,{size:"1.6em"},{default:t(()=>[l(g(s.$options.icons.table),1)]),_:1})]),default:t(()=>[c(o,{class:"text-h6 font-weight-light"},{default:t(()=>[l(" Workflows Table ")]),_:1}),c(m,null,{default:t(()=>[l(" View name, host, port, etc. of your workflows ")]),_:1})]),_:1}),c(v,{to:"/user-profile","data-cy":"user-settings-link"},{prepend:t(()=>[c(i,{size:"1.6em"},{default:t(()=>[l(g(s.$options.icons.settings),1)]),_:1})]),default:t(()=>[c(o,{class:"text-h6 font-weight-light"},{default:t(()=>[l(" Settings ")]),_:1}),c(m,null,{default:t(()=>[l(" View your Hub permissions, and alter user preferences ")]),_:1})]),_:1}),r("div",null,[c(v,{id:"cylc-hub-button",disabled:!p.multiUserMode,href:s.$options.hubUrl},{prepend:t(()=>[c(i,{size:"1.6em"},{default:t(()=>[l(g(s.$options.icons.hub),1)]),_:1})]),default:t(()=>[c(o,{class:"text-h6 font-weight-light"},{default:t(()=>[l(" Cylc Hub ")]),_:1}),c(m,null,{default:t(()=>[l(" Visit the Hub to manage your running UI Servers ")]),_:1})]),_:1},8,["disabled","href"]),c(L,{disabled:p.multiUserMode},{default:t(()=>[l(" You are not running Cylc UI via Cylc Hub. ")]),_:1},8,["disabled"])]),r("div",null,[c(v,{id:"jupyter-lab-button",disabled:!((u=s.user.extensions)!=null&&u.lab),href:(d=s.user.extensions)==null?void 0:d.lab,target:"_blank"},{prepend:t(()=>[c(i,{size:"1.6em"},{default:t(()=>[l(g(s.$options.icons.jupyterLogo),1)]),_:1})]),default:t(()=>[c(o,{class:"text-h6 font-weight-light"},{default:t(()=>[l(" Jupyter Lab ")]),_:1}),c(m,null,{default:t(()=>[l(" Open Jupyter Lab in a new browser tab. ")]),_:1})]),_:1},8,["disabled","href"]),c(L,{disabled:(x=s.user.extensions)==null?void 0:x.lab},{default:t(()=>[l(" Jupyter Lab is not installed. ")]),_:1},8,["disabled"])])]}),_:1})]),_:1}),c(w,{md:"6",lg:"6"},{default:t(()=>[c(H,{lines:"three",class:"pa-0"},{default:t(()=>[c(v,{to:"/guide","data-cy":"quickstart-link"},{prepend:t(()=>[c(i,{size:"1.6em"},{default:t(()=>[l(g(s.$options.icons.quickstart),1)]),_:1})]),default:t(()=>[c(o,{class:"text-h6 font-weight-light"},{default:t(()=>[l(" Cylc UI Quickstart ")]),_:1}),c(m,null,{default:t(()=>[l(" Learn how to use the Cylc UI ")]),_:1})]),_:1}),c(v,{href:"https://cylc.github.io/cylc-doc/stable/html/workflow-design-guide/index.html",target:"_blank"},{prepend:t(()=>[c(i,{size:"1.6em"},{default:t(()=>[l(g(s.$options.icons.workflow),1)]),_:1})]),default:t(()=>[c(o,{class:"text-h6 font-weight-light"},{default:t(()=>[l(" Workflow Design Guide ")]),_:1}),c(m,null,{default:t(()=>[l(" How to make complex Cylc workflows and Rose suites simpler and easier to maintain ")]),_:1})]),_:1}),c(v,{href:"https://cylc.github.io/cylc-doc/stable/html/index.html",target:"_blank"},{prepend:t(()=>[c(i,{size:"1.6em"},{default:t(()=>[l(g(s.$options.icons.documentation),1)]),_:1})]),default:t(()=>[c(o,{class:"text-h6 font-weight-light"},{default:t(()=>[l(" Documentation ")]),_:1}),c(m,null,{default:t(()=>[l(" The complete Cylc documentation ")]),_:1})]),_:1}),c(v,{to:"/graphiql"},{prepend:t(()=>[c(i,{size:"1.6em"},{default:t(()=>[l(g(s.$options.icons.mdiGraphql),1)]),_:1})]),default:t(()=>[c(o,{class:"text-h6 font-weight-light"},{default:t(()=>[l(" GraphiQL ")]),_:1}),c(m,null,{default:t(()=>[l(" Explore the Cylc GraphQL API ")]),_:1})]),_:1})]),_:1})]),_:1})]),_:1})]),_:1})}const e0=b(J,[["render",t0]]);export{e0 as default};