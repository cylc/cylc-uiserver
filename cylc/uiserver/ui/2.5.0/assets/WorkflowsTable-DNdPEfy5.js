import{_ as d,L as f,ef as u,eg as c,a2 as k,a3 as p,a4 as m,eh as a,Y as b,l as h,w as l,V as _,C as W,bN as g,k as y,m as r,q as C,E as e,t,cs as v,v as V}from"./index-DSRpE5Rv.js";import{V as T}from"./VAlert-DPLBpYWN.js";import{V as $}from"./VDataTable-DeJrdP8M.js";import"./VPagination-DeW5L5cH.js";const D=f`
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
  owner
  host
  port
}
`,N={name:"WorkflowsTable",mixins:[u],components:{WorkflowIcon:c},data:()=>({query:new k(D,{},"root",[],!0,!0)}),computed:{...p("workflows",["cylcTree"]),...m("workflows",["getNodes"]),workflows(){return this.getNodes("workflow")},workflowsTable(){return Object.values(this.workflows)}},methods:{viewWorkflow(s){this.$router.push({path:`/workspace/${s.tokens.workflow}`})}},headers:[{sortable:!1,title:"",key:"icon"},{sortable:!0,title:a.global.t("Workflows.tableColumnName"),key:"tokens.workflow"},{sortable:!0,title:"Status",key:"node.status"},{sortable:!0,title:a.global.t("Workflows.tableColumnOwner"),key:"node.owner"},{sortable:!0,title:a.global.t("Workflows.tableColumnHost"),key:"node.host"},{sortable:!1,title:a.global.t("Workflows.tableColumnPort"),key:"node.port"}],icons:{mdiTable:b}},x={class:"text-h5"},S=["onClick"],q={width:"1em"};function B(s,I,E,H,O,n){const i=W("WorkflowIcon"),w=g("command-menu");return y(),h(_,{"fill-height":"",fluid:"","grid-list-xl":""},{default:l(()=>[r(V,{class:"align-self-start"},{default:l(()=>[r(C,null,{default:l(()=>[r(T,{icon:s.$options.icons.mdiTable,prominent:"",color:"grey-lighten-3"},{default:l(()=>[e("h3",x,t(s.$t("Workflows.tableHeader")),1)]),_:1},8,["icon"]),r($,{headers:s.$options.headers,items:n.workflowsTable,"data-cy":"workflows-table",style:{"font-size":"1rem"}},{item:l(({item:o})=>[e("tr",{onClick:Q=>n.viewWorkflow(o),style:{cursor:"pointer"}},[e("td",q,[v(r(i,{status:o.node.status},null,8,["status"]),[[w,o]])]),e("td",null,t(o.tokens.workflow),1),e("td",null,t(o.node.status),1),e("td",null,t(o.node.owner),1),e("td",null,t(o.node.host),1),e("td",null,t(o.node.port),1)],8,S)]),_:1},8,["headers","items"])]),_:1})]),_:1})]),_:1})}const A=d(N,[["render",B]]);export{A as default};
