import{_ as d,J as u,cz as c,cA as f,a0 as k,a1 as p,a2 as m,cB as a,W as b,j as h,w as l,V as _,A as W,bw as g,h as y,k as r,n as C,C as t,t as e,bx as V,p as v}from"./index-Hyq34tSM.js";import{V as T}from"./VAlert-CLAKnZDH.js";import{V as $}from"./VDataTable-D1WRK44R.js";import"./VPagination-D6i7DgtD.js";const D=u`
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
`,x={name:"WorkflowsTable",mixins:[c],components:{WorkflowIcon:f},data:()=>({query:new k(D,{},"root",[],!0,!0)}),computed:{...p("workflows",["cylcTree"]),...m("workflows",["getNodes"]),workflows(){return this.getNodes("workflow")},workflowsTable(){return Object.values(this.workflows)}},methods:{viewWorkflow(s){this.$router.push({path:`/workspace/${s.tokens.workflow}`})}},headers:[{sortable:!1,title:"",key:"icon"},{sortable:!0,title:a.global.t("Workflows.tableColumnName"),key:"tokens.workflow"},{sortable:!0,title:"Status",key:"node.status"},{sortable:!0,title:a.global.t("Workflows.tableColumnOwner"),key:"node.owner"},{sortable:!0,title:a.global.t("Workflows.tableColumnHost"),key:"node.host"},{sortable:!1,title:a.global.t("Workflows.tableColumnPort"),key:"node.port"}],icons:{mdiTable:b}},N={class:"text-h5"},B=["onClick"],S={width:"1em"};function A(s,I,j,q,z,n){const i=W("WorkflowIcon"),w=g("command-menu");return y(),h(_,{"fill-height":"",fluid:"","grid-list-xl":""},{default:l(()=>[r(v,{class:"align-self-start"},{default:l(()=>[r(C,null,{default:l(()=>[r(T,{icon:s.$options.icons.mdiTable,prominent:"",color:"grey-lighten-3"},{default:l(()=>[t("h3",N,e(s.$t("Workflows.tableHeader")),1)]),_:1},8,["icon"]),r($,{headers:s.$options.headers,items:n.workflowsTable,"data-cy":"workflows-table",style:{"font-size":"1rem"}},{item:l(({item:o})=>[t("tr",{onClick:H=>n.viewWorkflow(o),style:{cursor:"pointer"}},[t("td",S,[V(r(i,{status:o.node.status},null,8,["status"]),[[w,o]])]),t("td",null,e(o.tokens.workflow),1),t("td",null,e(o.node.status),1),t("td",null,e(o.node.owner),1),t("td",null,e(o.node.host),1),t("td",null,e(o.node.port),1)],8,B)]),_:1},8,["headers","items"])]),_:1})]),_:1})]),_:1})}const G=d(x,[["render",A]]);export{G as default};
