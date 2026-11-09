import{r as e}from"./vuex.esm-bundler-DhFCIrIx.js";import{H as t,S as n,a as r,kt as i,o as a,q as o,s}from"./mdi-DCsggE_y.js";import{E as c,F as l,G as u,T as d,v as f,y as p}from"./index-_99OrTPv.js";import{r as m,t as h}from"./WorkflowState.model-ThqSSWRC.js";import{n as g}from"./lib-BD1OgZUd.js";import{t as _}from"./EventChip-2Cak48wv.js";import{D as v,E as y,St as b,_ as x,mt as S,qt as C,tr as w,v as T,w as E,y as D}from"./runtime-core.esm-bundler-DZo3dYLJ.js";import{t as O}from"./_plugin-vue_export-helper-BDNMzG2s.js";import{t as k}from"./VDataTable-DDeuc6Qo.js";import{t as A}from"./VDivider-CM00VNx1.js";import{t as j}from"./VContainer-zV-9GhTN.js";import{_ as M}from"./router-Dc1DjKwM.js";import{c as N,d as P,t as F,u as I}from"./VList-CPNiY798.js";import{t as L}from"./VTooltip-usU9GFBN.js";var R=g`
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
`,z={name:`Dashboard`,mixins:[c],components:{EventChip:_},setup(){let{user:e,hubURL:t}=u();return{user:e,hubURL:t}},data(){return{query:new d(R,{},`root`,[],!0,!0)}},computed:{...e(`workflows`,[`getNodes`]),workflows(){return this.getNodes(`workflow`)},workflowsTable(){let e=Object.values(this.workflows).map(e=>e.node.status).reduce((e,t)=>(e[t]=(e[t]||0)+1,e),{});return h.enumValues.sort((e,t)=>m.get(e)-m.get(t)).map(t=>({text:t.name.charAt(0).toUpperCase()+t.name.slice(1),count:e[t.name]||0}))},events(){let e=[];for(let t of this.workflows){let n=t.node?.logRecords||[];for(let r of n)e.push({workflow:t.tokens.workflow,...r})}return e.reverse()}},workflowsHeader:[{value:`count`},{value:`text`}],eventsHeader:[{value:`level`},{value:`workflow`},{value:`message`}],icons:{table:i,settings:n,hub:o,quickstart:r,workflow:s,documentation:a,jupyterLogo:l,mdiGraphql:t}};function B(e,t,n,r,i,a){let o=b(`EventChip`);return S(),T(j,{fluid:``,"grid-list":``,class:`c-dashboard mt-4 py-0 px-6`},{default:C(()=>[v(f,{wrap:``},{default:C(()=>[v(p,{md:`4`,lg:`3`},{default:C(()=>[t[2]||=x(`p`,{class:`text-headline-large my-2`},`Workflows`,-1),v(k,{headers:e.$options.workflowsHeader,items:a.workflowsTable,loading:e.isLoading,id:`dashboard-workflows`,"items-per-page":`-1`,style:{"font-size":`1rem`},density:`compact`},{headers:C(()=>[...t[0]||=[]]),bottom:C(()=>[...t[1]||=[]]),_:1},8,[`headers`,`items`,`loading`])]),_:1}),v(p,{md:`8`,lg:`9`},{default:C(()=>[t[4]||=x(`p`,{class:`text-headline-large my-2`},`Events`,-1),v(k,{headers:e.$options.eventsHeader,items:a.events,"items-per-page":8,density:`compact`,"data-cy":`events-table`},E({headers:C(()=>[]),"no-data":C(()=>[t[3]||=x(`td`,{class:`text-title-large text-disabled`},`No events`,-1)]),"item.level":C(({item:e})=>[v(o,{level:e.level},null,8,[`level`])]),_:2},[a.events.length?void 0:{name:`bottom`,fn:C(()=>[]),key:`0`}]),1032,[`headers`,`items`])]),_:1})]),_:1}),v(A),v(f,{wrap:``},{default:C(()=>[v(p,{md:`6`,lg:`6`},{default:C(()=>[v(F,{lines:`three`,class:`pa-0`},{default:C(()=>[v(N,{to:`/workflow-table`,"data-cy":`workflow-table-link`},{prepend:C(()=>[v(M,{size:`1.6em`},{default:C(()=>[y(w(e.$options.icons.table),1)]),_:1})]),default:C(()=>[v(I,null,{default:C(()=>[...t[5]||=[y(` Workflows Table `,-1)]]),_:1}),v(P,null,{default:C(()=>[...t[6]||=[y(` View name, host, version, etc. of your workflows `,-1)]]),_:1})]),_:1}),v(N,{to:`/user-profile`,"data-cy":`user-settings-link`},{prepend:C(()=>[v(M,{size:`1.6em`},{default:C(()=>[y(w(e.$options.icons.settings),1)]),_:1})]),default:C(()=>[v(I,null,{default:C(()=>[...t[7]||=[y(` Settings `,-1)]]),_:1}),v(P,null,{default:C(()=>[...t[8]||=[y(` View your Hub permissions, and alter user preferences `,-1)]]),_:1})]),_:1}),x(`div`,null,[v(N,{id:`cylc-hub-button`,disabled:!r.hubURL,href:r.hubURL},{prepend:C(()=>[v(M,{size:`1.6em`},{default:C(()=>[y(w(e.$options.icons.hub),1)]),_:1})]),default:C(()=>[v(I,null,{default:C(()=>[...t[9]||=[y(` Cylc Hub `,-1)]]),_:1}),v(P,null,{default:C(()=>[...t[10]||=[y(` Visit the Hub to manage your running UI Servers `,-1)]]),_:1})]),_:1},8,[`disabled`,`href`]),r.hubURL?D(``,!0):(S(),T(L,{key:0},{default:C(()=>[...t[11]||=[y(` You are not running Cylc UI via Cylc Hub. `,-1)]]),_:1}))]),x(`div`,null,[v(N,{id:`jupyter-lab-button`,disabled:!r.user.extensions?.lab,href:r.user.extensions?.lab,target:`_blank`},{prepend:C(()=>[v(M,{size:`1.6em`},{default:C(()=>[y(w(e.$options.icons.jupyterLogo),1)]),_:1})]),default:C(()=>[v(I,null,{default:C(()=>[...t[12]||=[y(` Jupyter Lab `,-1)]]),_:1}),v(P,null,{default:C(()=>[...t[13]||=[y(` Open Jupyter Lab in a new browser tab. `,-1)]]),_:1})]),_:1},8,[`disabled`,`href`]),v(L,{disabled:r.user.extensions?.lab},{default:C(()=>[...t[14]||=[y(` Jupyter Lab is not installed. `,-1)]]),_:1},8,[`disabled`])])]),_:1})]),_:1}),v(p,{md:`6`,lg:`6`},{default:C(()=>[v(F,{lines:`three`,class:`pa-0`},{default:C(()=>[v(N,{to:`/guide`,"data-cy":`quickstart-link`},{prepend:C(()=>[v(M,{size:`1.6em`},{default:C(()=>[y(w(e.$options.icons.quickstart),1)]),_:1})]),default:C(()=>[v(I,null,{default:C(()=>[...t[15]||=[y(` Cylc UI Quickstart `,-1)]]),_:1}),v(P,null,{default:C(()=>[...t[16]||=[y(` Learn how to use the Cylc UI `,-1)]]),_:1})]),_:1}),v(N,{href:`https://cylc.github.io/cylc-doc/stable/html/workflow-design-guide/index.html`,target:`_blank`},{prepend:C(()=>[v(M,{size:`1.6em`},{default:C(()=>[y(w(e.$options.icons.workflow),1)]),_:1})]),default:C(()=>[v(I,null,{default:C(()=>[...t[17]||=[y(` Workflow Design Guide `,-1)]]),_:1}),v(P,null,{default:C(()=>[...t[18]||=[y(` How to make complex Cylc workflows and Rose suites simpler and easier to maintain `,-1)]]),_:1})]),_:1}),v(N,{href:`https://cylc.github.io/cylc-doc/stable/html/index.html`,target:`_blank`},{prepend:C(()=>[v(M,{size:`1.6em`},{default:C(()=>[y(w(e.$options.icons.documentation),1)]),_:1})]),default:C(()=>[v(I,null,{default:C(()=>[...t[19]||=[y(` Documentation `,-1)]]),_:1}),v(P,null,{default:C(()=>[...t[20]||=[y(` The complete Cylc documentation `,-1)]]),_:1})]),_:1}),v(N,{to:`/graphiql`},{prepend:C(()=>[v(M,{size:`1.6em`},{default:C(()=>[y(w(e.$options.icons.mdiGraphql),1)]),_:1})]),default:C(()=>[v(I,null,{default:C(()=>[...t[21]||=[y(` GraphiQL `,-1)]]),_:1}),v(P,null,{default:C(()=>[...t[22]||=[y(` Explore the Cylc GraphQL API `,-1)]]),_:1})]),_:1})]),_:1})]),_:1})]),_:1})]),_:1})}var V=O(z,[[`render`,B]]);export{V as default};