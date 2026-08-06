import{_ as C,W as x,X as U,Y as D,Z as L,$ as H,a0 as $,a1 as T,M as W,a2 as q,a3 as z,a4 as I,a5 as S,a6 as N,A,e as B,o as E,w as t,g as s,V as b,h as m,x as p,j as G,K as M,a7 as g,a8 as a,a9 as r,k as o,aa as n,B as d,t as i,C as k,ab as j,ac as h,ad as O,H as Q}from"./index-PqzDRcKR.js";import{V as y}from"./VDataTable-B4DpBnek.js";import{V as R}from"./VContainer-f0cvaE61.js";import"./VPagination-CkT2um5K.js";const J=Q`
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
`,Y={name:"Dashboard",mixins:[N],components:{EventChip:S},data(){return{query:new O(J,{},"root",[],!0,!0)}},computed:{...I("user",["user"]),...z("workflows",["getNodes"]),workflows(){return this.getNodes("workflow")},workflowsTable(){const l=Object.values(this.workflows).map(e=>e.node.status).reduce((e,u)=>(e[u]=(e[u]||0)+1,e),{});return j.enumValues.sort((e,u)=>h.get(e)-h.get(u)).map(e=>({text:e.name.charAt(0).toUpperCase()+e.name.slice(1),count:l[e.name]||0}))},multiUserMode(){return this.user.mode!=="single user"},events(){const l=[];for(const e of this.workflows){const u=e.node?.logRecords||[];for(const w of u)l.push({workflow:e.tokens.workflow,...w})}return l.reverse()}},workflowsHeader:[{value:"count"},{value:"text"}],eventsHeader:[{value:"level"},{value:"workflow"},{value:"message"}],hubUrl:q("/hub/home",!1,!0),icons:{table:W,settings:T,hub:$,quickstart:H,workflow:L,documentation:D,jupyterLogo:U,mdiGraphql:x}};function K(l,e,u,w,P,f){const v=A("EventChip");return E(),B(R,{fluid:"","grid-list":"",class:"c-dashboard mt-4 py-0 px-6"},{default:t(()=>[s(b,{wrap:""},{default:t(()=>[s(m,{md:"4",lg:"3"},{default:t(()=>[e[2]||(e[2]=p("p",{class:"text-h4 mb-2"},"Workflows",-1)),s(y,{headers:l.$options.workflowsHeader,items:f.workflowsTable,loading:l.isLoading,id:"dashboard-workflows","items-per-page":"-1",style:{"font-size":"1rem"},density:"compact"},{headers:t(()=>[...e[0]||(e[0]=[])]),bottom:t(()=>[...e[1]||(e[1]=[])]),_:1},8,["headers","items","loading"])]),_:1}),s(m,{md:"8",lg:"9"},{default:t(()=>[e[4]||(e[4]=p("p",{class:"text-h4 mb-2"},"Events",-1)),s(y,{headers:l.$options.eventsHeader,items:f.events,"items-per-page":8,density:"compact","data-cy":"events-table"},G({headers:t(()=>[]),"no-data":t(()=>[e[3]||(e[3]=p("td",{class:"text-h6 text-disabled"},"No events",-1))]),"item.level":t(({item:V})=>[s(v,{level:V.level},null,8,["level"])]),_:2},[f.events.length?void 0:{name:"bottom",fn:t(()=>[]),key:"0"}]),1032,["headers","items"])]),_:1})]),_:1}),s(M),s(b,{wrap:""},{default:t(()=>[s(m,{md:"6",lg:"6"},{default:t(()=>[s(g,{lines:"three",class:"pa-0"},{default:t(()=>[s(a,{to:"/workflow-table","data-cy":"workflow-table-link"},{prepend:t(()=>[s(d,{size:"1.6em"},{default:t(()=>[o(i(l.$options.icons.table),1)]),_:1})]),default:t(()=>[s(r,{class:"text-h6 font-weight-light"},{default:t(()=>[...e[5]||(e[5]=[o(" Workflows Table ",-1)])]),_:1}),s(n,null,{default:t(()=>[...e[6]||(e[6]=[o(" View name, host, version, etc. of your workflows ",-1)])]),_:1})]),_:1}),s(a,{to:"/user-profile","data-cy":"user-settings-link"},{prepend:t(()=>[s(d,{size:"1.6em"},{default:t(()=>[o(i(l.$options.icons.settings),1)]),_:1})]),default:t(()=>[s(r,{class:"text-h6 font-weight-light"},{default:t(()=>[...e[7]||(e[7]=[o(" Settings ",-1)])]),_:1}),s(n,null,{default:t(()=>[...e[8]||(e[8]=[o(" View your Hub permissions, and alter user preferences ",-1)])]),_:1})]),_:1}),p("div",null,[s(a,{id:"cylc-hub-button",disabled:!f.multiUserMode,href:l.$options.hubUrl},{prepend:t(()=>[s(d,{size:"1.6em"},{default:t(()=>[o(i(l.$options.icons.hub),1)]),_:1})]),default:t(()=>[s(r,{class:"text-h6 font-weight-light"},{default:t(()=>[...e[9]||(e[9]=[o(" Cylc Hub ",-1)])]),_:1}),s(n,null,{default:t(()=>[...e[10]||(e[10]=[o(" Visit the Hub to manage your running UI Servers ",-1)])]),_:1})]),_:1},8,["disabled","href"]),s(k,{disabled:f.multiUserMode},{default:t(()=>[...e[11]||(e[11]=[o(" You are not running Cylc UI via Cylc Hub. ",-1)])]),_:1},8,["disabled"])]),p("div",null,[s(a,{id:"jupyter-lab-button",disabled:!l.user.extensions?.lab,href:l.user.extensions?.lab,target:"_blank"},{prepend:t(()=>[s(d,{size:"1.6em"},{default:t(()=>[o(i(l.$options.icons.jupyterLogo),1)]),_:1})]),default:t(()=>[s(r,{class:"text-h6 font-weight-light"},{default:t(()=>[...e[12]||(e[12]=[o(" Jupyter Lab ",-1)])]),_:1}),s(n,null,{default:t(()=>[...e[13]||(e[13]=[o(" Open Jupyter Lab in a new browser tab. ",-1)])]),_:1})]),_:1},8,["disabled","href"]),s(k,{disabled:l.user.extensions?.lab},{default:t(()=>[...e[14]||(e[14]=[o(" Jupyter Lab is not installed. ",-1)])]),_:1},8,["disabled"])])]),_:1})]),_:1}),s(m,{md:"6",lg:"6"},{default:t(()=>[s(g,{lines:"three",class:"pa-0"},{default:t(()=>[s(a,{to:"/guide","data-cy":"quickstart-link"},{prepend:t(()=>[s(d,{size:"1.6em"},{default:t(()=>[o(i(l.$options.icons.quickstart),1)]),_:1})]),default:t(()=>[s(r,{class:"text-h6 font-weight-light"},{default:t(()=>[...e[15]||(e[15]=[o(" Cylc UI Quickstart ",-1)])]),_:1}),s(n,null,{default:t(()=>[...e[16]||(e[16]=[o(" Learn how to use the Cylc UI ",-1)])]),_:1})]),_:1}),s(a,{href:"https://cylc.github.io/cylc-doc/stable/html/workflow-design-guide/index.html",target:"_blank"},{prepend:t(()=>[s(d,{size:"1.6em"},{default:t(()=>[o(i(l.$options.icons.workflow),1)]),_:1})]),default:t(()=>[s(r,{class:"text-h6 font-weight-light"},{default:t(()=>[...e[17]||(e[17]=[o(" Workflow Design Guide ",-1)])]),_:1}),s(n,null,{default:t(()=>[...e[18]||(e[18]=[o(" How to make complex Cylc workflows and Rose suites simpler and easier to maintain ",-1)])]),_:1})]),_:1}),s(a,{href:"https://cylc.github.io/cylc-doc/stable/html/index.html",target:"_blank"},{prepend:t(()=>[s(d,{size:"1.6em"},{default:t(()=>[o(i(l.$options.icons.documentation),1)]),_:1})]),default:t(()=>[s(r,{class:"text-h6 font-weight-light"},{default:t(()=>[...e[19]||(e[19]=[o(" Documentation ",-1)])]),_:1}),s(n,null,{default:t(()=>[...e[20]||(e[20]=[o(" The complete Cylc documentation ",-1)])]),_:1})]),_:1}),s(a,{to:"/graphiql"},{prepend:t(()=>[s(d,{size:"1.6em"},{default:t(()=>[o(i(l.$options.icons.mdiGraphql),1)]),_:1})]),default:t(()=>[s(r,{class:"text-h6 font-weight-light"},{default:t(()=>[...e[21]||(e[21]=[o(" GraphiQL ",-1)])]),_:1}),s(n,null,{default:t(()=>[...e[22]||(e[22]=[o(" Explore the Cylc GraphQL API ",-1)])]),_:1})]),_:1})]),_:1})]),_:1})]),_:1})]),_:1})}const _=C(Y,[["render",K]]);export{_ as default};
