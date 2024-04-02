import{bE as d,bU as c,dZ as f,bV as u,d_ as k,c1 as b,c2 as p,c3 as h,d$ as a,bY as m,s as _,bx as l,bH as W,aR as g,aS as y,aE as v,I as r,bI as C,v as e,b3 as t,bz as V,bJ as T}from"./index-C2AHI-HK.js";import{V as $}from"./VAlert-DabNp_ty.js";import{V as D}from"./VDataTable-BEEIiNy3.js";const x=c`
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
`,N={name:"WorkflowsTable",mixins:[f],head(){return{title:u("App.workflows")}},components:{WorkflowIcon:k},data:()=>({query:new b(x,{},"root",[],!0,!0)}),computed:{...p("workflows",["cylcTree"]),...h("workflows",["getNodes"]),workflows(){return this.getNodes("workflow")},workflowsTable(){return Object.values(this.workflows)}},methods:{viewWorkflow(s){this.$router.push({path:`/workspace/${s.tokens.workflow}`})}},headers:[{sortable:!1,title:"",key:"icon"},{sortable:!0,title:a.global.t("Workflows.tableColumnName"),key:"tokens.workflow"},{sortable:!0,title:"Status",key:"node.status"},{sortable:!0,title:a.global.t("Workflows.tableColumnOwner"),key:"node.owner"},{sortable:!0,title:a.global.t("Workflows.tableColumnHost"),key:"node.host"},{sortable:!1,title:a.global.t("Workflows.tableColumnPort"),key:"node.port"}],icons:{mdiTable:m}},I={class:"text-h5"},S=["onClick"],j={width:"1em"};function B(s,E,H,R,q,n){const i=g("WorkflowIcon"),w=y("cylc-object");return v(),_(W,{"fill-height":"",fluid:"","grid-list-xl":""},{default:l(()=>[r(T,{class:"align-self-start"},{default:l(()=>[r(C,null,{default:l(()=>[r($,{icon:s.$options.icons.mdiTable,prominent:"",color:"grey-lighten-3"},{default:l(()=>[e("h3",I,t(s.$t("Workflows.tableHeader")),1)]),_:1},8,["icon"]),r(D,{headers:s.$options.headers,items:n.workflowsTable,"data-cy":"workflows-table",style:{"font-size":"1rem"}},{item:l(({item:o})=>[e("tr",{onClick:z=>n.viewWorkflow(o),style:{cursor:"pointer"}},[e("td",j,[V(r(i,{status:o.node.status},null,8,["status"]),[[w,o]])]),e("td",null,t(o.tokens.workflow),1),e("td",null,t(o.node.status),1),e("td",null,t(o.node.owner),1),e("td",null,t(o.node.host),1),e("td",null,t(o.node.port),1)],8,S)]),_:1},8,["headers","items"])]),_:1})]),_:1})]),_:1})}const Q=d(N,[["render",B]]);export{Q as default};
