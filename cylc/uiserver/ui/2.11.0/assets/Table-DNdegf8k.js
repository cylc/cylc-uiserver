import{c4 as G,aj as H,q as K,c5 as I,e as F,w as u,c6 as J,bQ as c,c7 as E,bn as X,o as T,g as a,x as O,F as Y,r as j,z as d,bK as U,bm as C,b0 as $,t as p,c8 as _,f as B,B as ee,bi as te,D as ae,c9 as se,az as oe,ax as ne,l as le,ca as A,cb as z,b1 as ie,y as re,cc as de,cd as h,_ as ue,a3 as me,a4 as ce,a6 as fe,j as M,ad as pe,I as ke,C as S,V as W,h as q}from"./index-xEfRJwX9.js";import{g as we}from"./graphql-DOSh5ICD.js";import{u as Q,i as L,a as v}from"./initialOptions-Dk-vrbA4.js";import{_ as be,m as Te}from"./filter-D4wSzjtU.js";import{V as ye,a as ge}from"./VDataTable-CumDlvKy.js";import"./VPagination-CRACFHH_.js";function N(o,n){return new Date(o)-new Date(n)}function he(o,n){return o-n}const ve=["data-cy-task-name"],xe={colspan:3},_e={class:"d-flex align-content-center flex-nowrap"},De={__name:"Table",props:{tasks:{type:Array,required:!0},initialOptions:L},emits:[Q],setup(o,{emit:n}){const m=n,l=o,R=G(),k=v("sortBy",{props:l,emit:m},[{key:"task.tokens.cycle",order:R.value?"desc":"asc"}]),y=v("page",{props:l,emit:m},1),g=v("itemsPerPage",{props:l,emit:m},50),w=H([{title:"Task",key:"task.name",sortFunc:h},{title:"Jobs",key:"data-table-expand"},{title:"Cycle Point",key:"task.tokens.cycle",sortFunc:h},{title:"Platform",key:"latestJob.node.platform",sortFunc:h},{title:"Job Runner",key:"latestJob.node.jobRunnerName",sortFunc:h},{title:"Job ID",key:"latestJob.node.jobId",sortFunc:h},{title:"Submit",key:"latestJob.node.submittedTime",sortFunc:N},{title:"Start",key:"latestJob.node.startedTime",sortFunc:N},{title:"Finish",key:"latestJob.node.finishedTime",sortRaw(i,s){const r=i.latestJob?.node,e=s.latestJob?.node;return D("latestJob.node.finishedTime",N,r?.finishedTime||r?.estimatedFinishTime,e?.finishedTime||e?.estimatedFinishTime)}},{title:"Run Time",key:"task.node.task.meanElapsedTime",sortRaw(i,s){const r=P.value.get(i.task.id),e=P.value.get(s.task.id);return D("task.node.task.meanElapsedTime",he,r?.actual||r?.estimate,e?.actual||e?.estimate)}}]);function D(i,s,r,e){const t=E(r),f=E(e);if(t&&f)return s(r,e);if(!t&&!f)return 0;const{order:b}=k.value.find(V=>V.key===i);if(!t)return b==="asc"?1:-1;if(!f)return b==="asc"?-1:1}for(const i of w.value)i.sortFunc&&(i.sort=(s,r)=>D(i.key,i.sortFunc,s,r));const P=K(()=>new Map(l.tasks.map(({task:i,latestJob:s})=>[i.id,{actual:I(s?.node),estimate:i.node?.task?.meanElapsedTime}]))),x={class:["d-flex","align-center"],style:{width:"2em"}},Z=[{value:10,title:"10"},{value:20,title:"20"},{value:50,title:"50"},{value:100,title:"100"},{value:200,title:"200"},{value:-1,title:"All"}];return(i,s)=>{const r=X("command-menu");return T(),F(ye,{headers:w.value,items:o.tasks,"item-value":"task.id","multi-sort":"","sort-by":c(k),"onUpdate:sortBy":s[0]||(s[0]=e=>J(k)?k.value=e:null),"show-expand":"",density:"compact",page:c(y),"onUpdate:page":s[1]||(s[1]=e=>J(y)?y.value=e:null),"items-per-page":c(g),"onUpdate:itemsPerPage":s[2]||(s[2]=e=>J(g)?g.value=e:null)},{"item.task.name":u(({item:e})=>[d("div",{class:oe(["d-flex align-center flex-nowrap",{"flow-none":c(ne)(e.task.node.flowNums)}]),"data-cy-task-name":e.task.name},[d("div",A(z(x)),[C(a(ie,{task:e.task.node,startTime:e.latestJob?.node?.startedTime},null,8,["task","startTime"]),[[r,e.task]])],16),d("div",A(z(x)),[e.latestJob?C((T(),F($,{key:0,status:e.latestJob.node.state,"previous-state":e.previousJob?.node?.state},null,8,["status","previous-state"])),[[r,e.latestJob]]):re("",!0)],16),le(" "+p(e.task.name)+" ",1),a(de,{flowNums:e.task.node.flowNums,class:"ml-2"},null,8,["flowNums"])],10,ve)]),"item.latestJob.node.finishedTime":u(({item:e,value:t})=>[a(_,{actual:t,estimate:e.latestJob?.node.estimatedFinishTime},null,8,["actual","estimate"])]),"item.task.node.task.meanElapsedTime":u(({item:e})=>[a(_,U(P.value.get(e.task.id),{formatter:t=>c(B)(t,{allowZeros:!0}),tooltip:"Mean for this task"}),null,16,["formatter"])]),"item.data-table-expand":u(({item:e,internalItem:t,toggleExpand:f,isExpanded:b})=>[a(ee,{onClick:V=>f(t),icon:"",variant:"text",size:"small",style:te({visibility:(e.task.children||[]).length?null:"hidden",transform:b(t)?"rotate(180deg)":null})},{default:u(()=>[a(ae,{icon:c(se),size:"large"},null,8,["icon"])]),_:1},8,["onClick","style"])]),"expanded-row":u(({item:e})=>[(T(!0),O(Y,null,j(e.task.children,(t,f)=>(T(),O("tr",{key:t.id,class:"expanded-row bg-grey-lighten-5"},[d("td",xe,[d("div",_e,[d("div",U({ref_for:!0},x,{style:{marginLeft:x.style.width}}),[C((T(),F($,{key:`${t.id}-summary-${f}`,status:t.node.state},null,8,["status"])),[[r,t]])],16),d("span",null,"#"+p(t.node.submitNum),1)])]),d("td",null,p(t.node.platform),1),d("td",null,p(t.node.jobRunnerName),1),d("td",null,p(t.node.jobId),1),d("td",null,p(t.node.submittedTime),1),d("td",null,p(t.node.startedTime),1),d("td",null,[a(_,{actual:t.node.finishedTime,estimate:t.node.estimatedFinishTime},null,8,["actual","estimate"])]),d("td",null,[a(_,{actual:c(I)(t.node),estimate:e.task.node?.task.meanElapsedTime,formatter:b=>c(B)(b,{allowZeros:!0}),tooltip:"Mean"},null,8,["actual","estimate","formatter"])])]))),128))]),bottom:u(()=>[a(ge,{itemsPerPageOptions:Z})]),_:1},8,["headers","items","sort-by","page","items-per-page"])}}},Pe=ke`
subscription Workflow ($workflowId: ID) {
  deltas (workflows: [$workflowId]) {
    id
    added {
      ...AddedDelta
    }
    updated (stripNull: true) {
      ...UpdatedDelta
    }
    pruned {
      ...PrunedDelta
    }
  }
}

fragment AddedDelta on Added {
  workflow {
    ...WorkflowData
  }
  taskProxies {
    ...TaskProxyData
  }
  jobs {
    ...JobData
  }
}

fragment UpdatedDelta on Updated {
  workflow {
    ...WorkflowData
  }
  taskProxies {
    ...TaskProxyData
  }
  jobs {
    ...JobData
  }
}

fragment PrunedDelta on Pruned {
  workflow
  familyProxies
  taskProxies
  jobs
}

fragment WorkflowData on Workflow {
  id
  reloaded
}

fragment TaskProxyData on TaskProxy {
  id
  state
  isHeld
  isQueued
  isRunahead
  isRetry
  isWallclock
  isXtriggered
  task {
    meanElapsedTime
  }
  firstParent {
    id
  }
  runtime {
    runMode
  }
  flowNums
}

fragment JobData on Job {
  id
  jobRunnerName
  jobId
  platform
  startedTime
  submittedTime
  finishedTime
  estimatedFinishTime
  state
  submitNum
}
`,Fe={name:"Table",mixins:[we,fe],components:{TableComponent:De,TaskFilter:be},emits:[Q],props:{initialOptions:L},setup(o,{emit:n}){const m=v("tasksFilter",{props:o,emit:n},{});return{dataTableOptions:v("dataTableOptions",{props:o,emit:n}),tasksFilter:m}},computed:{...ce("workflows",["cylcTree"]),...me("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},tasks(){const o=[];for(const n of this.workflows)for(const m of n.children)for(const l of m.children)o.push({task:l,latestJob:l.children[0],previousJob:l.children[1]});return o},query(){return new pe(Pe,this.variables,"workflow",[],!0,!0)},filteredTasks(){return this.tasks.filter(({task:o})=>Te(o,this.tasksFilter.id,this.tasksFilter.states))}}},Je={class:"h-100"};function Ce(o,n,m,l,R,k){const y=S("TaskFilter"),g=S("TableComponent");return T(),O("div",Je,[a(M,{fluid:"",class:"c-table ma-0 pa-2 h-100 flex-column d-flex"},{default:u(()=>[a(W,{"no-gutters":"",class:"d-flex flex-wrap flex-grow-0"},{default:u(()=>[a(q,null,{default:u(()=>[a(y,{modelValue:l.tasksFilter,"onUpdate:modelValue":n[0]||(n[0]=w=>l.tasksFilter=w)},null,8,["modelValue"])]),_:1})]),_:1}),a(W,{"no-gutters":"",class:"flex-grow-1 position-relative"},{default:u(()=>[a(q,{cols:"12",class:"mh-100 position-relative"},{default:u(()=>[a(M,{fluid:"",class:"ma-0 pa-0 w-100 h-100 left-0 top-0 position-absolute pt-2"},{default:u(()=>[a(g,{tasks:k.filteredTasks,"initial-options":l.dataTableOptions,"onUpdate:initialOptions":n[1]||(n[1]=w=>l.dataTableOptions=w)},null,8,["tasks","initial-options"])]),_:1})]),_:1})]),_:1})]),_:1})])}const Ue=ue(Fe,[["render",Ce]]);export{Ue as default};
