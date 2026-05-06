import{ce as L,am as G,e as _,j as Q,w as c,cf as S,cc as k,cg as V,A as I,bL as Z,o as w,g as u,q as B,F as H,r as j,x as i,b8 as R,bF as N,b2 as E,t as p,ch as x,f as A,ci as M,z as X,bc as Y,B as K,cj as tt,p as et,az as at,ax as st,k as ot,ck as U,cl as $,b3 as nt,v as it,cm as rt,cn as g,_ as lt,a3 as dt,a4 as ut,a6 as mt,ad as ct,H as ft}from"./index-BxIX773T.js";import{g as kt}from"./graphql-LLAnEp44.js";import{u as z,i as W,a as v}from"./initialOptions-Cwf6VhRd.js";import{g as pt,m as bt,a as wt,u as yt}from"./filter-BKMXLKHk.js";import{V as Tt}from"./ViewToolbar-Ue7t8UtL.js";import{V as ht,a as gt}from"./VDataTable-DG0YOL8F.js";import{V as vt}from"./VContainer-B-kZgkHg.js";import"./VPagination-BynVVJcu.js";function C(a,s){return new Date(a)-new Date(s)}function Ft(a,s){return a-s}const Dt=["data-cy-task-name"],xt={colspan:3},_t={class:"d-flex align-content-center flex-nowrap"},Pt={__name:"Table",props:{tasks:{type:Array,required:!0},initialOptions:W,filterState:{type:[Object,null],default:null}},emits:[z],setup(a,{emit:s}){const m=s,o=a,P=L(),f=v("sortBy",{props:o,emit:m},[{key:"task.tokens.cycle",order:P.value?"desc":"asc"}]),y=v("page",{props:o,emit:m},1),T=v("itemsPerPage",{props:o,emit:m},50),F=G([{title:"Task",key:"task.name",sortFunc:g},{title:"Jobs",key:"data-table-expand"},{title:"Cycle Point",key:"task.tokens.cycle",sortFunc:g},{title:"Platform",key:"latestJob.node.platform",sortFunc:g},{title:"Job Runner",key:"latestJob.node.jobRunnerName",sortFunc:g},{title:"Job ID",key:"latestJob.node.jobId",sortFunc:g},{title:"Submit",key:"latestJob.node.submittedTime",sortFunc:C},{title:"Start",key:"latestJob.node.startedTime",sortFunc:C},{title:"Finish",key:"latestJob.node.finishedTime",sortRaw(r,n){const l=r.latestJob?.node,d=n.latestJob?.node;return J("latestJob.node.finishedTime",C,l?.finishedTime||l?.estimatedFinishTime,d?.finishedTime||d?.estimatedFinishTime)}},{title:"Run Time",key:"task.node.task.meanElapsedTime",sortRaw(r,n){const l=O.value.get(r.task.id),d=O.value.get(n.task.id);return J("task.node.task.meanElapsedTime",Ft,l?.actual||l?.estimate,d?.actual||d?.estimate)}}]);function J(r,n,l,d){const t=V(l),e=V(d);if(t&&e)return n(l,d);if(!t&&!e)return 0;const{order:b}=f.value.find(h=>h.key===r);if(!t)return b==="asc"?1:-1;if(!e)return b==="asc"?-1:1}for(const r of F.value)r.sortFunc&&(r.sort=(n,l)=>J(r.key,r.sortFunc,n,l));const O=et(()=>new Map(o.tasks.map(({task:r,latestJob:n})=>[r.id,{actual:M(n?.node),estimate:r.node?.task?.meanElapsedTime}]))),D={class:["d-flex","align-center"],style:{width:"2em"}},q=[{value:10,title:"10"},{value:20,title:"20"},{value:50,title:"50"},{value:100,title:"100"},{value:200,title:"200"},{value:-1,title:"All"}];return(r,n)=>{const l=I("v-filter-empty-state"),d=Z("command-menu");return w(),_(ht,{headers:F.value,items:a.tasks,"item-value":"task.id","multi-sort":"","sort-by":k(f),"onUpdate:sortBy":n[0]||(n[0]=t=>S(f)?f.value=t:null),"show-expand":"",density:"compact",page:k(y),"onUpdate:page":n[1]||(n[1]=t=>S(y)?y.value=t:null),"items-per-page":k(T),"onUpdate:itemsPerPage":n[2]||(n[2]=t=>S(T)?T.value=t:null),"fixed-header":""},Q({"item.task.name":c(({item:t})=>[i("div",{class:at(["d-flex align-center flex-nowrap",{"flow-none":k(st)(t.task.node.flowNums)}]),"data-cy-task-name":t.task.name},[i("div",U($(D)),[N(u(nt,{task:t.task.node,startTime:t.latestJob?.node?.startedTime},null,8,["task","startTime"]),[[d,t.task]])],16),i("div",U($(D)),[t.latestJob?N((w(),_(E,{key:0,status:t.latestJob.node.state,"previous-state":t.previousJob?.node?.state},null,8,["status","previous-state"])),[[d,t.latestJob]]):it("",!0)],16),ot(" "+p(t.task.name)+" ",1),u(rt,{flowNums:t.task.node.flowNums,class:"ml-2"},null,8,["flowNums"])],10,Dt)]),"item.latestJob.node.finishedTime":c(({item:t,value:e})=>[u(x,{actual:e,estimate:t.latestJob?.node.estimatedFinishTime},null,8,["actual","estimate"])]),"item.task.node.task.meanElapsedTime":c(({item:t})=>[u(x,R(O.value.get(t.task.id),{formatter:e=>k(A)(e,{allowZeros:!0}),tooltip:"Mean for this task"}),null,16,["formatter"])]),"item.data-table-expand":c(({item:t,internalItem:e,toggleExpand:b,isExpanded:h})=>[u(X,{onClick:Ct=>b(e),icon:"",variant:"text",size:"small",style:Y({visibility:(t.task.children||[]).length?null:"hidden",transform:h(e)?"rotate(180deg)":null})},{default:c(()=>[u(K,{icon:k(tt),size:"large"},null,8,["icon"])]),_:1},8,["onClick","style"])]),"expanded-row":c(({item:t})=>[(w(!0),B(H,null,j(t.task.children,(e,b)=>(w(),B("tr",{key:e.id,class:"expanded-row bg-grey-lighten-5"},[i("td",xt,[i("div",_t,[i("div",R({ref_for:!0},D,{style:{marginLeft:D.style.width}}),[N((w(),_(E,{key:`${e.id}-summary-${b}`,status:e.node.state},null,8,["status"])),[[d,e]])],16),i("span",null,"#"+p(e.node.submitNum),1)])]),i("td",null,p(e.node.platform),1),i("td",null,p(e.node.jobRunnerName),1),i("td",null,p(e.node.jobId),1),i("td",null,p(e.node.submittedTime),1),i("td",null,p(e.node.startedTime),1),i("td",null,[u(x,{actual:e.node.finishedTime,estimate:e.node.estimatedFinishTime},null,8,["actual","estimate"])]),i("td",null,[u(x,{actual:k(M)(e.node),estimate:t.task.node?.task.meanElapsedTime,formatter:h=>k(A)(h,{allowZeros:!0}),tooltip:"Mean"},null,8,["actual","estimate","formatter"])])]))),128))]),bottom:c(()=>[u(gt,{itemsPerPageOptions:q})]),_:2},[a.filterState?{name:"no-data",fn:c(()=>[u(l,{"data-cy":"filter-no-results"})]),key:"0"}:void 0]),1032,["headers","items","sort-by","page","items-per-page"])}}},Jt=ft`
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
`,Ot={name:"Table",mixins:[kt,mt],components:{TableComponent:Pt,ViewToolbar:Tt},emits:[z],props:{initialOptions:W},setup(a,{emit:s}){const m=v("tasksFilter",{props:a,emit:s},{}),o=yt(m);return{dataTableOptions:v("dataTableOptions",{props:a,emit:s}),tasksFilter:m,filterState:o}},computed:{...ut("workflows",["cylcTree"]),...dt("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},tasks(){const a=[];for(const s of this.workflows)for(const m of s.children)for(const o of m.children)a.push({task:o,latestJob:o.children[0],previousJob:o.children[1]});return a},query(){return new ct(Jt,this.variables,"workflow",[],!0,!0)},filteredTasks(){const[a,s,m]=pt(this.tasksFilter.states?.length?this.tasksFilter.states:[]);return this.tasks.filter(({task:o})=>bt(o,wt(this.tasksFilter.id),a,s,m))},controlGroups(){return[{title:"Filter",controls:[{title:"Filter By ID",action:"taskIDFilter",key:"taskIDFilter",value:this.tasksFilter.id},{title:"Filter By State",action:"taskStateFilter",key:"taskStateFilter",value:this.tasksFilter.states}]}]}},methods:{setOption(a,s){a==="taskStateFilter"?this.tasksFilter.states=s:a==="taskIDFilter"?this.tasksFilter.id=s:this[a]=s}}},St={class:"overflow-hidden"};function Nt(a,s,m,o,P,f){const y=I("ViewToolbar"),T=I("TableComponent");return w(),_(vt,{fluid:"",class:"c-table pa-2 pb-0 h-100 flex-column d-flex"},{default:c(()=>[u(y,{groups:f.controlGroups,onSetOption:f.setOption},null,8,["groups","onSetOption"]),i("div",St,[u(T,R({tasks:f.filteredTasks,"initial-options":o.dataTableOptions,"onUpdate:initialOptions":s[0]||(s[0]=F=>o.dataTableOptions=F)},{filterState:o.filterState},{class:"mh-100"}),null,16,["tasks","initial-options"])])]),_:1})}const $t=lt(Ot,[["render",Nt]]);export{$t as default};
