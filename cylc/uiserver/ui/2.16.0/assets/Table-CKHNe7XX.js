import{i as e,r as t}from"./vuex.esm-bundler-DhFCIrIx.js";import{A as n,E as r,L as i,T as a,U as o,ct as s,w as c}from"./index-_99OrTPv.js";import{n as l,r as u,t as d}from"./initialOptions-CHcgzlQU.js";import{i as f,n as p,o as m,t as h}from"./filter-D5prhhLM.js";import{t as ee}from"./ViewToolbar-BCEZdBEB.js";import{$ as g,$n as _,Ct as v,D as y,E as b,Ft as x,On as S,St as C,Yt as w,Zn as te,_ as T,b as E,bt as D,er as O,et as k,g as A,mt as j,o as M,qt as N,tr as P,v as F,vn as I,w as L,y as R,z}from"./runtime-core.esm-bundler-DZo3dYLJ.js";import{t as B}from"./Job-kt-_cvzH.js";import{g as V}from"./mdi-DCsggE_y.js";import{t as H}from"./sort-DkmK2N_w.js";import{i as U,r as W,t as G}from"./tasks-DlvbDXeX.js";import{t as K}from"./EstimatedTime-DtLNRjwi.js";import{r as q,t as J}from"./VDataTable-DDeuc6Qo.js";import{_ as Y}from"./router-Dc1DjKwM.js";import{n as X}from"./lib-BD1OgZUd.js";import{t as Z}from"./_plugin-vue_export-helper-BDNMzG2s.js";import{t as ne}from"./VContainer-zV-9GhTN.js";function Q(e,t){return new Date(e)-new Date(t)}function re(e,t){return e-t}var ie=[`data-cy-task-name`],ae={colspan:3},oe={class:`d-flex align-content-center flex-nowrap`},$={__name:`Table`,props:g({tasks:{type:Array,required:!0},filterState:{type:[Object,null],default:null}},{sortBy:{},sortByModifiers:{},page:{},pageModifiers:{},itemsPerPage:{},itemsPerPageModifiers:{}}),emits:[`update:sortBy`,`update:page`,`update:itemsPerPage`],setup(e){let t=e,n=x(e,`sortBy`),r=x(e,`page`),a=x(e,`itemsPerPage`),c=I([{title:`Task`,key:`task.name`,sortFunc:H},{title:`Jobs`,key:`data-table-expand`},{title:`Cycle Point`,key:`task.tokens.cycle`,sortFunc:H},{title:`Platform`,key:`latestJob.node.platform`,sortFunc:H},{title:`Job Runner`,key:`latestJob.node.jobRunnerName`,sortFunc:H},{title:`Job ID`,key:`latestJob.node.jobId`,sortFunc:H},{title:`Submit`,key:`latestJob.node.submittedTime`,sortFunc:Q},{title:`Start`,key:`latestJob.node.startedTime`,sortFunc:Q},{title:`Finish`,key:`latestJob.node.finishedTime`,sortRaw(e,t){let n=e.latestJob?.node,r=t.latestJob?.node;return l(`latestJob.node.finishedTime`,Q,n?.finishedTime||n?.estimatedFinishTime,r?.finishedTime||r?.estimatedFinishTime)}},{title:`Run Time`,key:`task.node.task.meanElapsedTime`,sortRaw(e,t){let n=u.value.get(e.task.id),r=u.value.get(t.task.id);return l(`task.node.task.meanElapsedTime`,re,n?.actual||n?.estimate,r?.actual||r?.estimate)}}]);function l(e,t,r,i){let a=U(r),o=U(i);if(a&&o)return t(r,i);if(!a&&!o)return 0;let{order:s}=n.value.find(t=>t.key===e);if(!a)return s===`asc`?1:-1;if(!o)return s===`asc`?-1:1}for(let e of c.value)e.sortFunc&&(e.sort=(t,n)=>l(e.key,e.sortFunc,t,n));let u=A(()=>new Map(t.tasks.map(({task:e,latestJob:t})=>[e.id,{actual:W(t?.node),estimate:e.node?.task?.meanElapsedTime}]))),d={class:[`d-flex`,`align-center`],style:{width:`2em`}},f=[{value:10,title:`10`},{value:20,title:`20`},{value:50,title:`50`},{value:100,title:`100`},{value:200,title:`200`},{value:-1,title:`All`}];return(t,l)=>{let p=C(`v-filter-empty-state`),m=v(`command-menu`);return j(),F(J,{headers:c.value,items:e.tasks,"item-value":`task.id`,"multi-sort":``,"sort-by":n.value,"onUpdate:sortBy":l[0]||=e=>n.value=e,"show-expand":``,density:`compact`,page:r.value,"onUpdate:page":l[1]||=e=>r.value=e,"items-per-page":a.value,"onUpdate:itemsPerPage":l[2]||=e=>a.value=e,"fixed-header":``},L({"item.task.name":N(({item:e})=>[T(`div`,{class:te([`d-flex align-center flex-nowrap`,{dimmed:e.task.node.graphDepth}]),"data-cy-task-name":e.task.name},[T(`div`,_(z(d)),[w(y(o,{task:e.task.node,startTime:e.latestJob?.node?.startedTime},null,8,[`task`,`startTime`]),[[m,e.task]])],16),T(`div`,_(z(d)),[e.latestJob?w((j(),F(B,{key:0,status:e.latestJob.node.state,"previous-state":e.previousJob?.node?.state},null,8,[`status`,`previous-state`])),[[m,e.latestJob]]):R(``,!0)],16),b(` `+P(e.task.name)+` `,1),y(i,{flowNums:e.task.node.flowNums,class:`ml-2`},null,8,[`flowNums`])],10,ie)]),"item.latestJob.node.finishedTime":N(({item:e,value:t})=>[y(K,{actual:t,estimate:e.latestJob?.node.estimatedFinishTime},null,8,[`actual`,`estimate`])]),"item.task.node.task.meanElapsedTime":N(({item:e})=>[y(K,k(u.value.get(e.task.id),{formatter:e=>S(G)(e,{allowZeros:!0}),tooltip:`Mean for this task`}),null,16,[`formatter`])]),"item.data-table-expand":N(({item:e,internalItem:t,toggleExpand:n,isExpanded:r})=>[y(s,{onClick:e=>n(t),icon:``,variant:`text`,size:`small`,style:O({visibility:(e.task.children||[]).length?null:`hidden`,transform:r(t)?`rotate(180deg)`:null})},{default:N(()=>[y(Y,{icon:S(V),size:`large`},null,8,[`icon`])]),_:1},8,[`onClick`,`style`])]),"expanded-row":N(({item:e})=>[(j(!0),E(M,null,D(e.task.children,(t,n)=>(j(),E(`tr`,{key:t.id,class:`expanded-row bg-grey-lighten-5`},[T(`td`,ae,[T(`div`,oe,[T(`div`,k({ref_for:!0},d,{style:{marginLeft:d.style.width}}),[w((j(),F(B,{key:`${t.id}-summary-${n}`,status:t.node.state},null,8,[`status`])),[[m,t]])],16),T(`span`,null,`#`+P(t.node.submitNum),1)])]),T(`td`,null,P(t.node.platform),1),T(`td`,null,P(t.node.jobRunnerName),1),T(`td`,null,P(t.node.jobId),1),T(`td`,null,P(t.node.submittedTime),1),T(`td`,null,P(t.node.startedTime),1),T(`td`,null,[y(K,{actual:t.node.finishedTime,estimate:t.node.estimatedFinishTime},null,8,[`actual`,`estimate`])]),T(`td`,null,[y(K,{actual:S(W)(t.node),estimate:e.task.node?.task.meanElapsedTime,formatter:e=>S(G)(e,{allowZeros:!0}),tooltip:`Mean`},null,8,[`actual`,`estimate`,`formatter`])])]))),128))]),bottom:N(()=>[y(q,{itemsPerPageOptions:f})]),_:2},[e.filterState?{name:`no-data`,fn:N(()=>[y(p,{"data-cy":`filter-no-results`})]),key:`0`}:void 0]),1032,[`headers`,`items`,`sort-by`,`page`,`items-per-page`])}}},se=X`
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
`,ce={name:`Table`,mixins:[r],components:{TableComponent:$,ViewToolbar:ee},emits:[l],props:{initialOptions:d},setup(e,{emit:t}){let{workflowIDs:r,variables:i}=c(),a=u(`tasksFilter`,{props:e,emit:t},{}),o=m(a),s=n();return{sortBy:u(`sortBy`,{props:e,emit:t},[{key:`task.tokens.cycle`,order:s.value?`desc`:`asc`}]),page:u(`page`,{props:e,emit:t},1),itemsPerPage:u(`itemsPerPage`,{props:e,emit:t},50),tasksFilter:a,filterState:o,workflowIDs:r,variables:i}},computed:{...e(`workflows`,[`cylcTree`]),...t(`workflows`,[`getNodes`]),workflows(){return this.getNodes(`workflow`,this.workflowIDs)},tasks(){let e=[];for(let t of this.workflows)for(let n of t.children)for(let t of n.children)e.push({task:t,latestJob:t.children[0],previousJob:t.children[1]});return e},query(){return new a(se,this.variables,`workflow`,[],!0,!0)},filteredTasks(){let[e,t,n]=p(this.tasksFilter.states?.length?this.tasksFilter.states:[]);return this.tasks.filter(({task:r})=>f(r,h(this.tasksFilter.id),e,t,n))},controlGroups(){return[{title:`Filter`,controls:[{title:`Filter By ID`,action:`taskIDFilter`,key:`taskIDFilter`,value:this.tasksFilter.id},{title:`Filter By State`,action:`taskStateFilter`,key:`taskStateFilter`,value:this.tasksFilter.states}]}]}},methods:{setOption(e,t){e===`taskStateFilter`?this.tasksFilter.states=t:e===`taskIDFilter`?this.tasksFilter.id=t:this[e]=t}}},le={class:`overflow-hidden`};function ue(e,t,n,r,i,a){let o=C(`ViewToolbar`),s=C(`TableComponent`);return j(),F(ne,{fluid:``,class:`c-table pa-2 pb-0 h-100 flex-column d-flex`},{default:N(()=>[y(o,{groups:a.controlGroups,onSetOption:a.setOption},null,8,[`groups`,`onSetOption`]),T(`div`,le,[y(s,k({tasks:a.filteredTasks,"sort-by":r.sortBy,"onUpdate:sortBy":t[0]||=e=>r.sortBy=e,page:r.page,"onUpdate:page":t[1]||=e=>r.page=e,"items-per-page":r.itemsPerPage,"onUpdate:itemsPerPage":t[2]||=e=>r.itemsPerPage=e},{filterState:r.filterState},{class:`mh-100`}),null,16,[`tasks`,`sort-by`,`page`,`items-per-page`])])]),_:1})}var de=Z(ce,[[`render`,ue]]);export{de as default};