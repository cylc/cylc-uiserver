import{_ as w,O as c,cy as a,a4 as u,a5 as f,ae as k,cz as p,a7 as m,C as b,bm as h,e as _,o as y,w as l,g as r,V as W,h as g,z as e,t,bl as V,j as C,I as v}from"./index-EpcknQ5m.js";import{V as T}from"./VAlert-CtG1z_R3.js";import{V as $}from"./VDataTable-BirqjyYH.js";import"./VPagination-KiduL2wZ.js";import"./VTable-hoHcQV6C.js";const D=v`
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
}
`,N={name:"WorkflowsTable",mixins:[m],components:{WorkflowIcon:p},data:()=>({query:new k(D,{},"root",[],!0,!0)}),computed:{...f("workflows",["cylcTree"]),...u("workflows",["getNodes"]),workflows(){return this.getNodes("workflow")},workflowsTable(){return Object.values(this.workflows)}},methods:{viewWorkflow(s){this.$router.push({path:`/workspace/${s.tokens.workflow}`})}},headers:[{sortable:!1,title:"",key:"icon"},{sortable:!0,title:a.global.t("Workflows.tableColumnName"),key:"tokens.workflow"},{sortable:!0,title:"Status",key:"node.status"},{sortable:!0,title:"Cylc Version",key:"node.cylcVersion"},{sortable:!0,title:a.global.t("Workflows.tableColumnOwner"),key:"node.owner"},{sortable:!0,title:a.global.t("Workflows.tableColumnHost"),key:"node.host"},{sortable:!1,title:a.global.t("Workflows.tableColumnPort"),key:"node.port"}],icons:{mdiTable:c}},x={class:"text-h5"},I=["onClick"],S={width:"1em"};function z(s,B,O,j,q,n){const i=b("WorkflowIcon"),d=h("command-menu");return y(),_(C,{"fill-height":"",fluid:"","grid-list-xl":""},{default:l(()=>[r(W,{class:"align-self-start"},{default:l(()=>[r(g,null,{default:l(()=>[r(T,{icon:s.$options.icons.mdiTable,prominent:"",color:"grey-lighten-3"},{default:l(()=>[e("h3",x,t(s.$t("Workflows.tableHeader")),1)]),_:1},8,["icon"]),r($,{headers:s.$options.headers,items:n.workflowsTable,"data-cy":"workflows-table",style:{"font-size":"1rem"}},{item:l(({item:o})=>[e("tr",{onClick:H=>n.viewWorkflow(o),style:{cursor:"pointer"}},[e("td",S,[V(r(i,{status:o.node.status},null,8,["status"]),[[d,o]])]),e("td",null,t(o.tokens.workflow),1),e("td",null,t(o.node.status),1),e("td",null,t(o.node.cylcVersion),1),e("td",null,t(o.node.owner),1),e("td",null,t(o.node.host),1),e("td",null,t(o.node.port),1)],8,I)]),_:1},8,["headers","items"])]),_:1})]),_:1})]),_:1})}const M=w(N,[["render",z]]);export{M as default};
