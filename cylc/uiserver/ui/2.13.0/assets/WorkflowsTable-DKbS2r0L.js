import{_ as k,df as s,a3 as p,a4 as b,ad as h,dg as y,a6 as _,A as V,bL as D,e as g,o as i,w as e,g as o,V as W,h as v,x as C,t as l,R as T,b8 as N,q as x,v as U,k as d,C as I,bF as B,M as L,H as R}from"./index-BxIX773T.js";import{h as S,f as $}from"./datetime-BTQ3cuKI.js";import{V as q}from"./VAlert-ChR-xtuj.js";import{V as A,b as H}from"./VDataTable-DG0YOL8F.js";import{V as P}from"./VContainer-B-kZgkHg.js";import"./VPagination-BynVVJcu.js";const E=R`
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
`,M={name:"WorkflowsTable",mixins:[_],components:{WorkflowIcon:y},setup(){return{formatDatetime:$,icons:{mdiTable:L}}},data:()=>({query:new h(E,{},"root",[],!0,!0),now:null}),mounted(){this.updateDate(),this.interval=setInterval(this.updateDate,5e3)},beforeUnmount(){clearInterval(this.interval)},computed:{...b("workflows",["cylcTree"]),...p("workflows",["getNodes"]),workflows(){return this.getNodes("workflow")},workflowsTable(){return Object.values(this.workflows)}},methods:{viewWorkflow(t){this.$router.push({path:`/workspace/${t.tokens.workflow}`})},updateDate(){this.now=new Date},displayLastUpdate(t,w){if(t)return S(new Date(t*1e3))}},headers:[{sortable:!1,title:"",key:"icon"},{sortable:!0,title:s.global.t("Workflows.tableColumnName"),key:"tokens.workflow"},{sortable:!0,title:"Status",key:"node.status"},{sortable:!0,title:"Cylc Version",key:"node.cylcVersion"},{sortable:!0,title:s.global.t("Workflows.tableColumnOwner"),key:"node.owner"},{sortable:!0,title:s.global.t("Workflows.tableColumnHost"),key:"node.host"},{sortable:!1,title:s.global.t("Workflows.tableColumnPort"),key:"node.port"},{sortable:!0,title:"Last Activity",key:"node.lastUpdated"}]},O={class:"text-h5"},Q={key:0};function j(t,w,z,n,F,r){const f=V("WorkflowIcon"),u=D("command-menu");return i(),g(P,{"fill-height":"",fluid:"","grid-list-xl":""},{default:e(()=>[o(W,{class:"align-self-start"},{default:e(()=>[o(v,null,{default:e(()=>[o(q,{icon:n.icons.mdiTable,prominent:"",color:"grey-lighten-3"},{default:e(()=>[C("h3",O,l(t.$t("Workflows.tableHeader")),1)]),_:1},8,["icon"]),o(A,{headers:t.$options.headers,items:r.workflowsTable,hover:"","data-cy":"workflows-table",style:{"font-size":"1rem"}},{item:e(({props:c,item:m})=>[o(T,{defaults:{VTooltip:{openDelay:200}}},{default:e(()=>[o(H,N(c,{onClick:a=>r.viewWorkflow(m),class:"cursor-pointer"}),{"item.icon":e(({item:a})=>[B(o(f,{status:a.node.status},null,8,["status"]),[[u,a]])]),"item.node.lastUpdated":e(({value:a})=>[a?(i(),x("span",Q,[d(l(n.formatDatetime(new Date(a*1e3)))+" ",1),o(I,null,{default:e(()=>[d(l(r.displayLastUpdate(a,t.now)),1)]),_:2},1024)])):U("",!0)]),_:2},1040,["onClick"])]),_:2},1024)]),_:1},8,["headers","items"])]),_:1})]),_:1})]),_:1})}const ee=k(M,[["render",j]]);export{ee as default};
