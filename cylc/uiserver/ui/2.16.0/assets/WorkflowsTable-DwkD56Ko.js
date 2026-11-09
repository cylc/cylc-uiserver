import{i as e,r as t}from"./vuex.esm-bundler-DhFCIrIx.js";import{E as n,T as r,W as i,n as a,v as o,y as s}from"./index-_99OrTPv.js";import{kt as c}from"./mdi-DCsggE_y.js";import{n as l}from"./lib-BD1OgZUd.js";import{n as u,t as d}from"./datetime-B1UdshvC.js";import{Ct as f,D as p,E as m,St as h,Yt as g,b as _,et as v,mt as y,qt as b,tr as x,v as S,y as C}from"./runtime-core.esm-bundler-DZo3dYLJ.js";import{t as w}from"./_plugin-vue_export-helper-BDNMzG2s.js";import{n as T,t as E}from"./VDataTable-DDeuc6Qo.js";import{u as D}from"./router-Dc1DjKwM.js";import{t as O}from"./VContainer-zV-9GhTN.js";import{t as k}from"./VTooltip-usU9GFBN.js";var A=l`
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
`,j={name:`WorkflowsTable`,mixins:[n],components:{WorkflowIcon:i},setup(){return{formatDatetime:d,icons:{mdiTable:c}}},data:()=>({query:new r(A,{},`root`,[],!0,!0),now:null}),mounted(){this.updateDate(),this.interval=setInterval(this.updateDate,5e3)},beforeUnmount(){clearInterval(this.interval)},computed:{...e(`workflows`,[`cylcTree`]),...t(`workflows`,[`getNodes`]),workflows(){return this.getNodes(`workflow`)},workflowsTable(){return Object.values(this.workflows)}},methods:{viewWorkflow(e){this.$router.push({path:`/workspace/${e.tokens.workflow}`})},updateDate(){this.now=new Date},displayLastUpdate(e,t){if(e)return u(new Date(e*1e3))}},headers:[{sortable:!1,title:``,key:`icon`},{sortable:!0,title:a.global.t(`Workflows.tableColumnName`),key:`tokens.workflow`},{sortable:!0,title:`Status`,key:`node.status`},{sortable:!0,title:`Cylc Version`,key:`node.cylcVersion`},{sortable:!0,title:a.global.t(`Workflows.tableColumnOwner`),key:`node.owner`},{sortable:!0,title:a.global.t(`Workflows.tableColumnHost`),key:`node.host`},{sortable:!1,title:a.global.t(`Workflows.tableColumnPort`),key:`node.port`},{sortable:!0,title:`Last Activity`,key:`node.lastUpdated`}]},M={key:0};function N(e,t,n,r,i,a){let c=h(`WorkflowIcon`),l=f(`command-menu`);return y(),S(O,{"fill-height":``,fluid:``,class:`pa-0`},{default:b(()=>[p(o,{"no-gutters":``},{default:b(()=>[p(s,null,{default:b(()=>[p(E,{headers:e.$options.headers,items:a.workflowsTable,hover:``,"data-cy":`workflows-table`,style:{"font-size":`1rem`}},{item:b(({props:t,item:n})=>[p(D,{defaults:{VTooltip:{openDelay:200}}},{default:b(()=>[p(T,v(t,{onClick:e=>a.viewWorkflow(n),class:`cursor-pointer`}),{"item.icon":b(({item:e})=>[g(p(c,{status:e.node.status},null,8,[`status`]),[[l,e]])]),"item.node.lastUpdated":b(({value:t})=>[t?(y(),_(`span`,M,[m(x(r.formatDatetime(new Date(t*1e3)))+` `,1),p(k,null,{default:b(()=>[m(x(a.displayLastUpdate(t,e.now)),1)]),_:2},1024)])):C(``,!0)]),_:2},1040,[`onClick`])]),_:2},1024)]),_:1},8,[`headers`,`items`])]),_:1})]),_:1})]),_:1})}var P=w(j,[[`render`,N]]);export{P as default};