import{D as e,H as t,R as n,Rt as r,U as i,_ as a,d as o,f as s,g as c,nt as l,p as u,tt as d}from"./runtime-core.esm-bundler-CilEyzAc.js";import{h as f}from"./router-DOfkjfe2.js";import{n as p,t as m}from"./VDataTable-CY0zR2l-.js";import{kt as h}from"./mdi-DCsggE_y.js";import{n as g}from"./lib-CWAdvCqp.js";import{i as _,r as v}from"./vuex.esm-bundler-DiFTMXj2.js";import{t as y}from"./VTooltip-mBTL-h5c.js";import{t as b}from"./_plugin-vue_export-helper-BDNMzG2s.js";import{t as x}from"./VContainer-6R0NAAqg.js";import{E as S,T as C,W as w,n as T,v as E,y as D}from"./index-C9-ypOBE.js";import{n as O,t as k}from"./datetime-B1UdshvC.js";var A=g`
subscription Workflow {
  deltas {
    id
    added {
      workflow {
        ...WorkflowData
      }
    }
    updated (stripNull: true) {
      workflow {
        ...WorkflowData
      }
    }
    pruned {
      workflow
    }
  }
}

fragment WorkflowData on Workflow {
  id
  status
  cylcVersion
  owner
  host
  port
  lastUpdated
}
`,j={name:`WorkflowsTable`,mixins:[S],components:{WorkflowIcon:w},setup(){return{formatDatetime:k,icons:{mdiTable:h}}},data:()=>({query:new C(A,{},`root`,[],!0,!0),now:null}),mounted(){this.updateDate(),this.interval=setInterval(this.updateDate,5e3)},beforeUnmount(){clearInterval(this.interval)},computed:{..._(`workflows`,[`cylcTree`]),...v(`workflows`,[`getNodes`]),workflows(){return this.getNodes(`workflow`)},workflowsTable(){return Object.values(this.workflows)}},methods:{viewWorkflow(e){this.$router.push({path:`/workspace/${e.tokens.workflow}`})},updateDate(){this.now=new Date},displayLastUpdate(e,t){if(e)return O(new Date(e*1e3))}},headers:[{sortable:!1,title:``,key:`icon`},{sortable:!0,title:T.global.t(`Workflows.tableColumnName`),key:`tokens.workflow`},{sortable:!0,title:`Status`,key:`node.status`},{sortable:!0,title:`Cylc Version`,key:`node.cylcVersion`},{sortable:!0,title:T.global.t(`Workflows.tableColumnOwner`),key:`node.owner`},{sortable:!0,title:T.global.t(`Workflows.tableColumnHost`),key:`node.host`},{sortable:!1,title:T.global.t(`Workflows.tableColumnPort`),key:`node.port`},{sortable:!0,title:`Last Activity`,key:`node.lastUpdated`}]},M={key:0};function N(h,g,_,v,b,S){let C=t(`WorkflowIcon`),w=i(`command-menu`);return n(),o(x,{"fill-height":``,fluid:``,class:`pa-0`},{default:d(()=>[a(E,{"no-gutters":``},{default:d(()=>[a(D,null,{default:d(()=>[a(m,{headers:h.$options.headers,items:S.workflowsTable,hover:``,"data-cy":`workflows-table`,style:{"font-size":`1rem`}},{item:d(({props:t,item:i})=>[a(f,{defaults:{VTooltip:{openDelay:200}}},{default:d(()=>[a(p,e(t,{onClick:e=>S.viewWorkflow(i),class:`cursor-pointer`}),{"item.icon":d(({item:e})=>[l(a(C,{status:e.node.status},null,8,[`status`]),[[w,e]])]),"item.node.lastUpdated":d(({value:e})=>[e?(n(),u(`span`,M,[c(r(v.formatDatetime(new Date(e*1e3)))+` `,1),a(y,null,{default:d(()=>[c(r(S.displayLastUpdate(e,h.now)),1)]),_:2},1024)])):s(``,!0)]),_:2},1040,[`onClick`])]),_:2},1024)]),_:1},8,[`headers`,`items`])]),_:1})]),_:1})]),_:1})}var P=b(j,[[`render`,N]]);export{P as default};