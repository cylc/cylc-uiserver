import{_ as k,db as s,a3 as p,a4 as b,ad as h,dc as y,a6 as _,B as D,bq as V,e as W,o as i,w as e,g as o,V as g,h as v,y as C,t as l,R as T,b8 as N,v as x,x as U,k as d,D as B,bp as I,M as R,H as S}from"./index-Dk_oQcLS.js";import{h as $,f as q}from"./datetime-BTQ3cuKI.js";import{V as H}from"./VAlert-DL-eSlg8.js";import{V as L,b as P}from"./VDataTable-CLZT2yA6.js";import{V as A}from"./VContainer-COcUMfSR.js";import"./VPagination-CxvzufF_.js";const E=S`
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
`,M={name:"WorkflowsTable",mixins:[_],components:{WorkflowIcon:y},setup(){return{formatDatetime:q,icons:{mdiTable:R}}},data:()=>({query:new h(E,{},"root",[],!0,!0),now:null}),mounted(){this.updateDate(),this.interval=setInterval(this.updateDate,5e3)},beforeUnmount(){clearInterval(this.interval)},computed:{...b("workflows",["cylcTree"]),...p("workflows",["getNodes"]),workflows(){return this.getNodes("workflow")},workflowsTable(){return Object.values(this.workflows)}},methods:{viewWorkflow(t){this.$router.push({path:`/workspace/${t.tokens.workflow}`})},updateDate(){this.now=new Date},displayLastUpdate(t,w){if(t)return $(new Date(t*1e3))}},headers:[{sortable:!1,title:"",key:"icon"},{sortable:!0,title:s.global.t("Workflows.tableColumnName"),key:"tokens.workflow"},{sortable:!0,title:"Status",key:"node.status"},{sortable:!0,title:"Cylc Version",key:"node.cylcVersion"},{sortable:!0,title:s.global.t("Workflows.tableColumnOwner"),key:"node.owner"},{sortable:!0,title:s.global.t("Workflows.tableColumnHost"),key:"node.host"},{sortable:!1,title:s.global.t("Workflows.tableColumnPort"),key:"node.port"},{sortable:!0,title:"Last Activity",key:"node.lastUpdated"}]},O={class:"text-h5"},Q={key:0};function j(t,w,z,n,G,r){const c=D("WorkflowIcon"),f=V("command-menu");return i(),W(A,{"fill-height":"",fluid:"","grid-list-xl":""},{default:e(()=>[o(g,{class:"align-self-start"},{default:e(()=>[o(v,null,{default:e(()=>[o(H,{icon:n.icons.mdiTable,prominent:"",color:"grey-lighten-3"},{default:e(()=>[C("h3",O,l(t.$t("Workflows.tableHeader")),1)]),_:1},8,["icon"]),o(L,{headers:t.$options.headers,items:r.workflowsTable,hover:"","data-cy":"workflows-table",style:{"font-size":"1rem"}},{item:e(({props:u,item:m})=>[o(T,{defaults:{VTooltip:{openDelay:200}}},{default:e(()=>[o(P,N(u,{onClick:a=>r.viewWorkflow(m),class:"cursor-pointer"}),{"item.icon":e(({item:a})=>[I(o(c,{status:a.node.status},null,8,["status"]),[[f,a]])]),"item.node.lastUpdated":e(({value:a})=>[a?(i(),x("span",Q,[d(l(n.formatDatetime(new Date(a*1e3)))+" ",1),o(B,null,{default:e(()=>[d(l(r.displayLastUpdate(a,t.now)),1)]),_:2},1024)])):U("",!0)]),_:2},1040,["onClick"])]),_:2},1024)]),_:1},8,["headers","items"])]),_:1})]),_:1})]),_:1})}const ee=k(M,[["render",j]]);export{ee as default};
