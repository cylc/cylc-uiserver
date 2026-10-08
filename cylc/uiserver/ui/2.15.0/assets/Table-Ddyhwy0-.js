import{B as e,D as t,E as n,Ft as r,H as i,It as a,Lt as o,R as s,Rt as c,S as l,U as u,Y as d,_ as f,d as p,dt as m,f as h,g,h as ee,i as _,l as v,nt as y,p as b,tt as x,u as S,yt as C}from"./runtime-core.esm-bundler-CilEyzAc.js";import{O as w}from"./router-DOfkjfe2.js";import{r as te,t as T}from"./VDataTable-CY0zR2l-.js";import{t as E}from"./ViewToolbar-DFsrpfa5.js";import{g as D}from"./mdi-DCsggE_y.js";import{n as O}from"./lib-CWAdvCqp.js";import{i as k,r as A}from"./vuex.esm-bundler-DiFTMXj2.js";import{t as j}from"./sort-BBKNgJ6u.js";import{i as M,n as N,o as P,t as F}from"./filter-FSggriUT.js";import{t as I}from"./Job-D7pi9IWX.js";import{t as L}from"./_plugin-vue_export-helper-BDNMzG2s.js";import{i as R,r as z,t as B}from"./tasks-BCR3IW9E.js";import{t as V}from"./EstimatedTime-BM5TFAGs.js";import{t as H}from"./VContainer-6R0NAAqg.js";import{A as U,E as W,L as G,T as K,U as q,ct as J,w as Y}from"./index-C9-ypOBE.js";import{n as X,r as Z,t as ne}from"./initialOptions-Bou6yVjH.js";function Q(e,t){return new Date(e)-new Date(t)}function re(e,t){return e-t}var ie=[`data-cy-task-name`],ae={colspan:3},$={class:`d-flex align-content-center flex-nowrap`},oe={__name:`Table`,props:n({tasks:{type:Array,required:!0},filterState:{type:[Object,null],default:null}},{sortBy:{},sortByModifiers:{},page:{},pageModifiers:{},itemsPerPage:{},itemsPerPageModifiers:{}}),emits:[`update:sortBy`,`update:page`,`update:itemsPerPage`],setup(n){let E=n,O=d(n,`sortBy`),k=d(n,`page`),A=d(n,`itemsPerPage`),M=m([{title:`Task`,key:`task.name`,sortFunc:j},{title:`Jobs`,key:`data-table-expand`},{title:`Cycle Point`,key:`task.tokens.cycle`,sortFunc:j},{title:`Platform`,key:`latestJob.node.platform`,sortFunc:j},{title:`Job Runner`,key:`latestJob.node.jobRunnerName`,sortFunc:j},{title:`Job ID`,key:`latestJob.node.jobId`,sortFunc:j},{title:`Submit`,key:`latestJob.node.submittedTime`,sortFunc:Q},{title:`Start`,key:`latestJob.node.startedTime`,sortFunc:Q},{title:`Finish`,key:`latestJob.node.finishedTime`,sortRaw(e,t){let n=e.latestJob?.node,r=t.latestJob?.node;return N(`latestJob.node.finishedTime`,Q,n?.finishedTime||n?.estimatedFinishTime,r?.finishedTime||r?.estimatedFinishTime)}},{title:`Run Time`,key:`task.node.task.meanElapsedTime`,sortRaw(e,t){let n=P.value.get(e.task.id),r=P.value.get(t.task.id);return N(`task.node.task.meanElapsedTime`,re,n?.actual||n?.estimate,r?.actual||r?.estimate)}}]);function N(e,t,n,r){let i=R(n),a=R(r);if(i&&a)return t(n,r);if(!i&&!a)return 0;let{order:o}=O.value.find(t=>t.key===e);if(!i)return o===`asc`?1:-1;if(!a)return o===`asc`?-1:1}for(let e of M.value)e.sortFunc&&(e.sort=(t,n)=>N(e.key,e.sortFunc,t,n));let P=v(()=>new Map(E.tasks.map(({task:e,latestJob:t})=>[e.id,{actual:z(t?.node),estimate:e.node?.task?.meanElapsedTime}]))),F={class:[`d-flex`,`align-center`],style:{width:`2em`}},L=[{value:10,title:`10`},{value:20,title:`20`},{value:50,title:`50`},{value:100,title:`100`},{value:200,title:`200`},{value:-1,title:`All`}];return(d,m)=>{let v=i(`v-filter-empty-state`),E=u(`command-menu`);return s(),p(T,{headers:M.value,items:n.tasks,"item-value":`task.id`,"multi-sort":``,"sort-by":O.value,"onUpdate:sortBy":m[0]||=e=>O.value=e,"show-expand":``,density:`compact`,page:k.value,"onUpdate:page":m[1]||=e=>k.value=e,"items-per-page":A.value,"onUpdate:itemsPerPage":m[2]||=e=>A.value=e,"fixed-header":``},ee({"item.task.name":x(({item:e})=>[S(`div`,{class:r([`d-flex align-center flex-nowrap`,{dimmed:e.task.node.graphDepth}]),"data-cy-task-name":e.task.name},[S(`div`,a(l(F)),[y(f(q,{task:e.task.node,startTime:e.latestJob?.node?.startedTime},null,8,[`task`,`startTime`]),[[E,e.task]])],16),S(`div`,a(l(F)),[e.latestJob?y((s(),p(I,{key:0,status:e.latestJob.node.state,"previous-state":e.previousJob?.node?.state},null,8,[`status`,`previous-state`])),[[E,e.latestJob]]):h(``,!0)],16),g(` `+c(e.task.name)+` `,1),f(G,{flowNums:e.task.node.flowNums,class:`ml-2`},null,8,[`flowNums`])],10,ie)]),"item.latestJob.node.finishedTime":x(({item:e,value:t})=>[f(V,{actual:t,estimate:e.latestJob?.node.estimatedFinishTime},null,8,[`actual`,`estimate`])]),"item.task.node.task.meanElapsedTime":x(({item:e})=>[f(V,t(P.value.get(e.task.id),{formatter:e=>C(B)(e,{allowZeros:!0}),tooltip:`Mean for this task`}),null,16,[`formatter`])]),"item.data-table-expand":x(({item:e,internalItem:t,toggleExpand:n,isExpanded:r})=>[f(J,{onClick:e=>n(t),icon:``,variant:`text`,size:`small`,style:o({visibility:(e.task.children||[]).length?null:`hidden`,transform:r(t)?`rotate(180deg)`:null})},{default:x(()=>[f(w,{icon:C(D),size:`large`},null,8,[`icon`])]),_:1},8,[`onClick`,`style`])]),"expanded-row":x(({item:n})=>[(s(!0),b(_,null,e(n.task.children,(e,r)=>(s(),b(`tr`,{key:e.id,class:`expanded-row bg-grey-lighten-5`},[S(`td`,ae,[S(`div`,$,[S(`div`,t({ref_for:!0},F,{style:{marginLeft:F.style.width}}),[y((s(),p(I,{key:`${e.id}-summary-${r}`,status:e.node.state},null,8,[`status`])),[[E,e]])],16),S(`span`,null,`#`+c(e.node.submitNum),1)])]),S(`td`,null,c(e.node.platform),1),S(`td`,null,c(e.node.jobRunnerName),1),S(`td`,null,c(e.node.jobId),1),S(`td`,null,c(e.node.submittedTime),1),S(`td`,null,c(e.node.startedTime),1),S(`td`,null,[f(V,{actual:e.node.finishedTime,estimate:e.node.estimatedFinishTime},null,8,[`actual`,`estimate`])]),S(`td`,null,[f(V,{actual:C(z)(e.node),estimate:n.task.node?.task.meanElapsedTime,formatter:e=>C(B)(e,{allowZeros:!0}),tooltip:`Mean`},null,8,[`actual`,`estimate`,`formatter`])])]))),128))]),bottom:x(()=>[f(te,{itemsPerPageOptions:L})]),_:2},[n.filterState?{name:`no-data`,fn:x(()=>[f(v,{"data-cy":`filter-no-results`})]),key:`0`}:void 0]),1032,[`headers`,`items`,`sort-by`,`page`,`items-per-page`])}}},se=O`
subscription Workflow ($workflowID: ID) {
  deltas (workflows: [$workflowID]) {
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
  graphDepth
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
`,ce={name:`Table`,mixins:[W],components:{TableComponent:oe,ViewToolbar:E},emits:[X],props:{initialOptions:ne},setup(e,{emit:t}){let{workflowIDs:n,variables:r}=Y(),i=Z(`tasksFilter`,{props:e,emit:t},{}),a=P(i),o=U();return{sortBy:Z(`sortBy`,{props:e,emit:t},[{key:`task.tokens.cycle`,order:o.value?`desc`:`asc`}]),page:Z(`page`,{props:e,emit:t},1),itemsPerPage:Z(`itemsPerPage`,{props:e,emit:t},50),tasksFilter:i,filterState:a,workflowIDs:n,variables:r}},computed:{...k(`workflows`,[`cylcTree`]),...A(`workflows`,[`getNodes`]),workflows(){return this.getNodes(`workflow`,this.workflowIDs)},tasks(){let e=[];for(let t of this.workflows)for(let n of t.children)for(let t of n.children)e.push({task:t,latestJob:t.children[0],previousJob:t.children[1]});return e},query(){return new K(se,this.variables,`workflow`,[],!0,!0)},filteredTasks(){let[e,t,n]=N(this.tasksFilter.states?.length?this.tasksFilter.states:[]);return this.tasks.filter(({task:r})=>M(r,F(this.tasksFilter.id),e,t,n))},controlGroups(){return[{title:`Filter`,controls:[{title:`Filter By ID`,action:`taskIDFilter`,key:`taskIDFilter`,value:this.tasksFilter.id},{title:`Filter By State`,action:`taskStateFilter`,key:`taskStateFilter`,value:this.tasksFilter.states}]}]}},methods:{setOption(e,t){e===`taskStateFilter`?this.tasksFilter.states=t:e===`taskIDFilter`?this.tasksFilter.id=t:this[e]=t}}},le={class:`overflow-hidden`};function ue(e,n,r,a,o,c){let l=i(`ViewToolbar`),u=i(`TableComponent`);return s(),p(H,{fluid:``,class:`c-table pa-2 pb-0 h-100 flex-column d-flex`},{default:x(()=>[f(l,{groups:c.controlGroups,onSetOption:c.setOption},null,8,[`groups`,`onSetOption`]),S(`div`,le,[f(u,t({tasks:c.filteredTasks,"sort-by":a.sortBy,"onUpdate:sortBy":n[0]||=e=>a.sortBy=e,page:a.page,"onUpdate:page":n[1]||=e=>a.page=e,"items-per-page":a.itemsPerPage,"onUpdate:itemsPerPage":n[2]||=e=>a.itemsPerPage=e},{filterState:a.filterState},{class:`mh-100`}),null,16,[`tasks`,`sort-by`,`page`,`items-per-page`])])]),_:1})}var de=L(ce,[[`render`,ue]]);export{de as default};