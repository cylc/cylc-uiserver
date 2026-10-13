import{H as e,R as t,Rt as n,_ as r,d as i,g as a,h as o,tt as s,u as c}from"./runtime-core.esm-bundler-CilEyzAc.js";import{O as l}from"./router-DOfkjfe2.js";import{c as u,d,t as f,u as p}from"./VList-BFF_Xe9J.js";import{t as m}from"./VDataTable-CY0zR2l-.js";import{t as h}from"./VDivider-Cm4helvI.js";import{H as g,S as _,a as v,kt as y,o as b,q as x,s as S}from"./mdi-DCsggE_y.js";import{n as C}from"./lib-CWAdvCqp.js";import{i as w,r as T}from"./vuex.esm-bundler-DiFTMXj2.js";import{r as E,t as D}from"./WorkflowState.model-BhCweRaB.js";import{t as O}from"./VTooltip-mBTL-h5c.js";import{t as k}from"./_plugin-vue_export-helper-BDNMzG2s.js";import{t as A}from"./EventChip-DgqouxyE.js";import{t as j}from"./VContainer-6R0NAAqg.js";import{E as M,F as N,T as P,et as F,v as I,y as L}from"./index-C9-ypOBE.js";var R=C`
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
`,z={name:`Dashboard`,mixins:[M],components:{EventChip:A},data(){return{query:new P(R,{},`root`,[],!0,!0)}},computed:{...w(`user`,[`user`]),...T(`workflows`,[`getNodes`]),workflows(){return this.getNodes(`workflow`)},workflowsTable(){let e=Object.values(this.workflows).map(e=>e.node.status).reduce((e,t)=>(e[t]=(e[t]||0)+1,e),{});return D.enumValues.sort((e,t)=>E.get(e)-E.get(t)).map(t=>({text:t.name.charAt(0).toUpperCase()+t.name.slice(1),count:e[t.name]||0}))},multiUserMode(){return this.user.mode!==`single user`},events(){let e=[];for(let t of this.workflows){let n=t.node?.logRecords||[];for(let r of n)e.push({workflow:t.tokens.workflow,...r})}return e.reverse()}},workflowsHeader:[{value:`count`},{value:`text`}],eventsHeader:[{value:`level`},{value:`workflow`},{value:`message`}],hubUrl:F(`/hub/home`,!1,!0),icons:{table:y,settings:_,hub:x,quickstart:v,workflow:S,documentation:b,jupyterLogo:N,mdiGraphql:g}};function B(g,_,v,y,b,x){let S=e(`EventChip`);return t(),i(j,{fluid:``,"grid-list":``,class:`c-dashboard mt-4 py-0 px-6`},{default:s(()=>[r(I,{wrap:``},{default:s(()=>[r(L,{md:`4`,lg:`3`},{default:s(()=>[_[2]||=c(`p`,{class:`text-headline-large my-2`},`Workflows`,-1),r(m,{headers:g.$options.workflowsHeader,items:x.workflowsTable,loading:g.isLoading,id:`dashboard-workflows`,"items-per-page":`-1`,style:{"font-size":`1rem`},density:`compact`},{headers:s(()=>[..._[0]||=[]]),bottom:s(()=>[..._[1]||=[]]),_:1},8,[`headers`,`items`,`loading`])]),_:1}),r(L,{md:`8`,lg:`9`},{default:s(()=>[_[4]||=c(`p`,{class:`text-headline-large my-2`},`Events`,-1),r(m,{headers:g.$options.eventsHeader,items:x.events,"items-per-page":8,density:`compact`,"data-cy":`events-table`},o({headers:s(()=>[]),"no-data":s(()=>[_[3]||=c(`td`,{class:`text-title-large text-disabled`},`No events`,-1)]),"item.level":s(({item:e})=>[r(S,{level:e.level},null,8,[`level`])]),_:2},[x.events.length?void 0:{name:`bottom`,fn:s(()=>[]),key:`0`}]),1032,[`headers`,`items`])]),_:1})]),_:1}),r(h),r(I,{wrap:``},{default:s(()=>[r(L,{md:`6`,lg:`6`},{default:s(()=>[r(f,{lines:`three`,class:`pa-0`},{default:s(()=>[r(u,{to:`/workflow-table`,"data-cy":`workflow-table-link`},{prepend:s(()=>[r(l,{size:`1.6em`},{default:s(()=>[a(n(g.$options.icons.table),1)]),_:1})]),default:s(()=>[r(p,null,{default:s(()=>[..._[5]||=[a(` Workflows Table `,-1)]]),_:1}),r(d,null,{default:s(()=>[..._[6]||=[a(` View name, host, version, etc. of your workflows `,-1)]]),_:1})]),_:1}),r(u,{to:`/user-profile`,"data-cy":`user-settings-link`},{prepend:s(()=>[r(l,{size:`1.6em`},{default:s(()=>[a(n(g.$options.icons.settings),1)]),_:1})]),default:s(()=>[r(p,null,{default:s(()=>[..._[7]||=[a(` Settings `,-1)]]),_:1}),r(d,null,{default:s(()=>[..._[8]||=[a(` View your Hub permissions, and alter user preferences `,-1)]]),_:1})]),_:1}),c(`div`,null,[r(u,{id:`cylc-hub-button`,disabled:!x.multiUserMode,href:g.$options.hubUrl},{prepend:s(()=>[r(l,{size:`1.6em`},{default:s(()=>[a(n(g.$options.icons.hub),1)]),_:1})]),default:s(()=>[r(p,null,{default:s(()=>[..._[9]||=[a(` Cylc Hub `,-1)]]),_:1}),r(d,null,{default:s(()=>[..._[10]||=[a(` Visit the Hub to manage your running UI Servers `,-1)]]),_:1})]),_:1},8,[`disabled`,`href`]),r(O,{disabled:x.multiUserMode},{default:s(()=>[..._[11]||=[a(` You are not running Cylc UI via Cylc Hub. `,-1)]]),_:1},8,[`disabled`])]),c(`div`,null,[r(u,{id:`jupyter-lab-button`,disabled:!g.user.extensions?.lab,href:g.user.extensions?.lab,target:`_blank`},{prepend:s(()=>[r(l,{size:`1.6em`},{default:s(()=>[a(n(g.$options.icons.jupyterLogo),1)]),_:1})]),default:s(()=>[r(p,null,{default:s(()=>[..._[12]||=[a(` Jupyter Lab `,-1)]]),_:1}),r(d,null,{default:s(()=>[..._[13]||=[a(` Open Jupyter Lab in a new browser tab. `,-1)]]),_:1})]),_:1},8,[`disabled`,`href`]),r(O,{disabled:g.user.extensions?.lab},{default:s(()=>[..._[14]||=[a(` Jupyter Lab is not installed. `,-1)]]),_:1},8,[`disabled`])])]),_:1})]),_:1}),r(L,{md:`6`,lg:`6`},{default:s(()=>[r(f,{lines:`three`,class:`pa-0`},{default:s(()=>[r(u,{to:`/guide`,"data-cy":`quickstart-link`},{prepend:s(()=>[r(l,{size:`1.6em`},{default:s(()=>[a(n(g.$options.icons.quickstart),1)]),_:1})]),default:s(()=>[r(p,null,{default:s(()=>[..._[15]||=[a(` Cylc UI Quickstart `,-1)]]),_:1}),r(d,null,{default:s(()=>[..._[16]||=[a(` Learn how to use the Cylc UI `,-1)]]),_:1})]),_:1}),r(u,{href:`https://cylc.github.io/cylc-doc/stable/html/workflow-design-guide/index.html`,target:`_blank`},{prepend:s(()=>[r(l,{size:`1.6em`},{default:s(()=>[a(n(g.$options.icons.workflow),1)]),_:1})]),default:s(()=>[r(p,null,{default:s(()=>[..._[17]||=[a(` Workflow Design Guide `,-1)]]),_:1}),r(d,null,{default:s(()=>[..._[18]||=[a(` How to make complex Cylc workflows and Rose suites simpler and easier to maintain `,-1)]]),_:1})]),_:1}),r(u,{href:`https://cylc.github.io/cylc-doc/stable/html/index.html`,target:`_blank`},{prepend:s(()=>[r(l,{size:`1.6em`},{default:s(()=>[a(n(g.$options.icons.documentation),1)]),_:1})]),default:s(()=>[r(p,null,{default:s(()=>[..._[19]||=[a(` Documentation `,-1)]]),_:1}),r(d,null,{default:s(()=>[..._[20]||=[a(` The complete Cylc documentation `,-1)]]),_:1})]),_:1}),r(u,{to:`/graphiql`},{prepend:s(()=>[r(l,{size:`1.6em`},{default:s(()=>[a(n(g.$options.icons.mdiGraphql),1)]),_:1})]),default:s(()=>[r(p,null,{default:s(()=>[..._[21]||=[a(` GraphiQL `,-1)]]),_:1}),r(d,null,{default:s(()=>[..._[22]||=[a(` Explore the Cylc GraphQL API `,-1)]]),_:1})]),_:1})]),_:1})]),_:1})]),_:1})]),_:1})}var V=k(z,[[`render`,B]]);export{V as default};