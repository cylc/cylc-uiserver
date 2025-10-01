import{c3 as q,aj as Q,q as Z,c4 as V,e as F,w as m,c5 as P,bP as c,c6 as I,bn as L,o as T,g as a,x as N,F as G,r as H,z as d,bm as J,b0 as E,t as k,c7 as v,f as U,B as X,bi as Y,D as K,c8 as j,bJ as ee,az as te,ax as ae,l as se,b1 as oe,y as ne,c9 as le,ca as g,_ as ie,a3 as re,a4 as de,a6 as me,j as $,ad as ue,I as ce,C as B,V as A,h as M}from"./index-jbzX_AXb.js";import{g as fe}from"./graphql-o3z6-itG.js";import{u as S,i as z,a as _}from"./initialOptions-Ceh0265h.js";import{_ as ke,m as pe}from"./filter-E7bBrTct.js";import{V as we,a as be}from"./VDataTable-BqaL5Tnv.js";import"./VPagination-C84GdNtS.js";function C(o,n){return new Date(o)-new Date(n)}function Te(o,n){return o-n}const ye=["data-cy-task-name"],he={style:{width:"2em"}},ge={style:{width:"2em"}},_e={colspan:3},ve={class:"d-flex align-content-center flex-nowrap"},xe={class:"d-flex",style:{"margin-left":"2em"}},De={class:"ml-2"},Fe={__name:"Table",props:{tasks:{type:Array,required:!0},initialOptions:z},emits:[S],setup(o,{emit:n}){const u=n,l=o,O=q(),p=_("sortBy",{props:l,emit:u},[{key:"task.tokens.cycle",order:O.value?"desc":"asc"}]),y=_("page",{props:l,emit:u},1),h=_("itemsPerPage",{props:l,emit:u},50),w=Q([{title:"Task",key:"task.name",sortFunc:g},{title:"Jobs",key:"data-table-expand"},{title:"Cycle Point",key:"task.tokens.cycle",sortFunc:g},{title:"Platform",key:"latestJob.node.platform",sortFunc:g},{title:"Job Runner",key:"latestJob.node.jobRunnerName",sortFunc:g},{title:"Job ID",key:"latestJob.node.jobId",sortFunc:g},{title:"Submit",key:"latestJob.node.submittedTime",sortFunc:C},{title:"Start",key:"latestJob.node.startedTime",sortFunc:C},{title:"Finish",key:"latestJob.node.finishedTime",sortRaw(i,s){const r=i.latestJob?.node,e=s.latestJob?.node;return x("latestJob.node.finishedTime",C,r?.finishedTime||r?.estimatedFinishTime,e?.finishedTime||e?.estimatedFinishTime)}},{title:"Run Time",key:"task.node.task.meanElapsedTime",sortRaw(i,s){const r=D.value.get(i.task.id),e=D.value.get(s.task.id);return x("task.node.task.meanElapsedTime",Te,r?.actual||r?.estimate,e?.actual||e?.estimate)}}]);function x(i,s,r,e){const t=I(r),f=I(e);if(t&&f)return s(r,e);if(!t&&!f)return 0;const{order:b}=p.value.find(R=>R.key===i);if(!t)return b==="asc"?1:-1;if(!f)return b==="asc"?-1:1}for(const i of w.value)i.sortFunc&&(i.sort=(s,r)=>x(i.key,i.sortFunc,s,r));const D=Z(()=>new Map(l.tasks.map(({task:i,latestJob:s})=>[i.id,{actual:V(s?.node),estimate:i.node?.task?.meanElapsedTime}]))),W=[{value:10,title:"10"},{value:20,title:"20"},{value:50,title:"50"},{value:100,title:"100"},{value:200,title:"200"},{value:-1,title:"All"}];return(i,s)=>{const r=L("command-menu");return T(),F(we,{headers:w.value,items:o.tasks,"item-value":"task.id","multi-sort":"","sort-by":c(p),"onUpdate:sortBy":s[0]||(s[0]=e=>P(p)?p.value=e:null),"show-expand":"",density:"compact",page:c(y),"onUpdate:page":s[1]||(s[1]=e=>P(y)?y.value=e:null),"items-per-page":c(h),"onUpdate:itemsPerPage":s[2]||(s[2]=e=>P(h)?h.value=e:null)},{"item.task.name":m(({item:e})=>[d("div",{class:te(["d-flex align-center flex-nowrap",{"flow-none":c(ae)(e.task.node.flowNums)}]),"data-cy-task-name":e.task.name},[d("div",he,[J(a(oe,{task:e.task.node,startTime:e.latestJob?.node?.startedTime},null,8,["task","startTime"]),[[r,e.task]])]),d("div",ge,[e.latestJob?J((T(),F(E,{key:0,status:e.latestJob.node.state,"previous-state":e.previousJob?.node?.state},null,8,["status","previous-state"])),[[r,e.latestJob]]):ne("",!0)]),se(" "+k(e.task.name)+" ",1),a(le,{flowNums:e.task.node.flowNums,class:"ml-2"},null,8,["flowNums"])],10,ye)]),"item.latestJob.node.finishedTime":m(({item:e,value:t})=>[a(v,{actual:t,estimate:e.latestJob?.node.estimatedFinishTime},null,8,["actual","estimate"])]),"item.task.node.task.meanElapsedTime":m(({item:e})=>[a(v,ee(D.value.get(e.task.id),{formatter:t=>c(U)(t,{allowZeros:!0}),tooltip:"Mean for this task"}),null,16,["formatter"])]),"item.data-table-expand":m(({item:e,internalItem:t,toggleExpand:f,isExpanded:b})=>[a(X,{onClick:R=>f(t),icon:"",variant:"text",size:"small",style:Y({visibility:(e.task.children||[]).length?null:"hidden",transform:b(t)?"rotate(180deg)":null})},{default:m(()=>[a(K,{icon:c(j),size:"large"},null,8,["icon"])]),_:1},8,["onClick","style"])]),"expanded-row":m(({item:e})=>[(T(!0),N(G,null,H(e.task.children,(t,f)=>(T(),N("tr",{key:t.id,class:"expanded-row bg-grey-lighten-5"},[d("td",_e,[d("div",ve,[d("div",xe,[J((T(),F(E,{key:`${t.id}-summary-${f}`,status:t.node.state},null,8,["status"])),[[r,t]]),d("span",De,"#"+k(t.node.submitNum),1)])])]),d("td",null,k(t.node.platform),1),d("td",null,k(t.node.jobRunnerName),1),d("td",null,k(t.node.jobId),1),d("td",null,k(t.node.submittedTime),1),d("td",null,k(t.node.startedTime),1),d("td",null,[a(v,{actual:t.node.finishedTime,estimate:t.node.estimatedFinishTime},null,8,["actual","estimate"])]),d("td",null,[a(v,{actual:c(V)(t.node),estimate:e.task.node?.task.meanElapsedTime,formatter:b=>c(U)(b,{allowZeros:!0}),tooltip:"Mean"},null,8,["actual","estimate","formatter"])])]))),128))]),bottom:m(()=>[a(be,{itemsPerPageOptions:W})]),_:1},8,["headers","items","sort-by","page","items-per-page"])}}},Pe=ce`
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
`,Je={name:"Table",mixins:[fe,me],components:{TableComponent:Fe,TaskFilter:ke},emits:[S],props:{initialOptions:z},setup(o,{emit:n}){const u=_("tasksFilter",{props:o,emit:n},{});return{dataTableOptions:_("dataTableOptions",{props:o,emit:n}),tasksFilter:u}},computed:{...de("workflows",["cylcTree"]),...re("workflows",["getNodes"]),workflowIDs(){return[this.workflowId]},workflows(){return this.getNodes("workflow",this.workflowIDs)},tasks(){const o=[];for(const n of this.workflows)for(const u of n.children)for(const l of u.children)o.push({task:l,latestJob:l.children[0],previousJob:l.children[1]});return o},query(){return new ue(Pe,this.variables,"workflow",[],!0,!0)},filteredTasks(){return this.tasks.filter(({task:o})=>pe(o,this.tasksFilter.id,this.tasksFilter.states))}}},Ce={class:"h-100"};function Ne(o,n,u,l,O,p){const y=B("TaskFilter"),h=B("TableComponent");return T(),N("div",Ce,[a($,{fluid:"",class:"c-table ma-0 pa-2 h-100 flex-column d-flex"},{default:m(()=>[a(A,{"no-gutters":"",class:"d-flex flex-wrap flex-grow-0"},{default:m(()=>[a(M,null,{default:m(()=>[a(y,{modelValue:l.tasksFilter,"onUpdate:modelValue":n[0]||(n[0]=w=>l.tasksFilter=w)},null,8,["modelValue"])]),_:1})]),_:1}),a(A,{"no-gutters":"",class:"flex-grow-1 position-relative"},{default:m(()=>[a(M,{cols:"12",class:"mh-100 position-relative"},{default:m(()=>[a($,{fluid:"",class:"ma-0 pa-0 w-100 h-100 left-0 top-0 position-absolute pt-2"},{default:m(()=>[a(h,{tasks:p.filteredTasks,"initial-options":l.dataTableOptions,"onUpdate:initialOptions":n[1]||(n[1]=w=>l.dataTableOptions=w)},null,8,["tasks","initial-options"])]),_:1})]),_:1})]),_:1})]),_:1})])}const $e=ie(Je,[["render",Ne]]);export{$e as default};
