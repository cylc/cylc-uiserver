import{B as e,D as t,Ft as n,H as r,Lt as i,R as a,Rt as o,_ as s,d as c,f as l,g as u,gt as d,i as f,l as p,nt as m,p as h,tt as g,u as _}from"./runtime-core.esm-bundler-CilEyzAc.js";import{D as v,E as y,J as b,L as x,O as S,P as C,Q as ee,Ut as te,V as w,W as T,h as E,m as ne,nt as D,p as re,r as ie,t as ae,tt as O,v as oe,y as k,z as A}from"./router-DOfkjfe2.js";import{t as j}from"./VDivider-Cm4helvI.js";import{B as M,Ct as N,D as P,G as F,dt as I,h as L,m as R,p as z}from"./mdi-DCsggE_y.js";import{n as B}from"./lib-CWAdvCqp.js";import{t as V}from"./uid-B9ZHvQie.js";import{t as H}from"./cloneDeep-CFrvt-fL.js";import{t as U}from"./_plugin-vue_export-helper-BDNMzG2s.js";import{t as W}from"./tooltip-DIPN_LZ5.js";import{E as G,K,T as q,V as se,c as J,j as ce,l as Y,o as le,s as X,w as ue}from"./index-C9-ypOBE.js";import{r as Z,t as de}from"./initialOptions-Bou6yVjH.js";import{t as fe}from"./GraphNode-DYxtRQIE.js";import{t as pe}from"./datetime-B1UdshvC.js";function me(e,t){let n=[],r=0,i=``;for(let a of e.split(/(and|or|\(|\))/))if(a=a.trim().replace(`_`,`-`),a){if(a===`(`)n.push([null,r,`${i}(`]),i=``,r+=1;else if(a===`)`)--r,n.push([null,r,`${i})`]),i=``;else if(a===`and`||a===`or`)i=`${a} `;else{for(let e of t)if(e.label===a){n.push([e.satisfied,r,`${i}${a}`]);break}i=``}}return n}var he=D({divider:[Number,String],...O()},`VBreadcrumbsDivider`),ge=b()({name:`VBreadcrumbsDivider`,props:he(),setup(e,{slots:t}){return T(()=>_(`li`,{"aria-hidden":`true`,class:n([`v-breadcrumbs-divider`,e.class]),style:i(e.style)},[t?.default?.()??e.divider])),{}}}),_e=D({active:Boolean,activeClass:String,activeColor:String,color:String,disabled:Boolean,title:String,...O(),...te(y(),[`width`,`maxWidth`]),...ae(),...C({tag:`li`})},`VBreadcrumbsItem`),ve=b()({name:`VBreadcrumbsItem`,props:_e(),setup(e,{slots:r,attrs:a}){let o=ie(e,a),c=p(()=>e.active||o.isActive?.value),{dimensionStyles:l}=v(e),{textColorClasses:u,textColorStyles:d}=A(()=>c.value?e.activeColor:e.color);return T(()=>s(e.tag,{class:n([`v-breadcrumbs-item`,{"v-breadcrumbs-item--active":c.value,"v-breadcrumbs-item--disabled":e.disabled,[`${e.activeClass}`]:c.value&&e.activeClass},u.value,e.class]),style:i([d.value,l.value,e.style]),"aria-current":c.value?`page`:void 0},{default:()=>[o.isLink.value?_(`a`,t({class:`v-breadcrumbs-item--link`,onClick:o.navigate.value},o.linkProps),[r.default?.()??e.title]):r.default?.()??e.title]})),{}}}),ye=D({activeClass:String,activeColor:String,bgColor:String,color:String,disabled:Boolean,divider:{type:String,default:`/`},icon:w,items:{type:Array,default:()=>[]},...O(),...re(),...oe(),...C({tag:`ul`})},`VBreadcrumbs`),be=b()({name:`VBreadcrumbs`,props:ye(),setup(e,{slots:r}){let{backgroundColorClasses:a,backgroundColorStyles:o}=x(()=>e.bgColor),{densityClasses:c}=ne(e),{roundedClasses:l}=k(e);ee({VBreadcrumbsDivider:{divider:d(()=>e.divider)},VBreadcrumbsItem:{activeClass:d(()=>e.activeClass),activeColor:d(()=>e.activeColor),color:d(()=>e.color),disabled:d(()=>e.disabled)}});let u=p(()=>e.items.map(e=>typeof e==`string`?{item:{title:e},raw:e}:{item:e,raw:e}));return T(()=>{let d=!!(r.prepend||e.icon);return s(e.tag,{class:n([`v-breadcrumbs`,a.value,c.value,l.value,e.class]),style:i([o.value,e.style])},{default:()=>[d&&_(`li`,{key:`prepend`,class:`v-breadcrumbs__prepend`},[r.prepend?s(E,{key:`prepend-defaults`,disabled:!e.icon,defaults:{VIcon:{icon:e.icon,start:!0}}},r.prepend):s(S,{key:`prepend-icon`,start:!0,icon:e.icon},null)]),u.value.map(({item:e,raw:n},i,a)=>_(f,null,[r.item?.({item:e,index:i})??s(ve,t({key:i,disabled:i>=a.length-1},typeof e==`string`?{title:e}:e),{default:r.title?()=>r.title?.({item:e,index:i}):void 0}),i<a.length-1&&s(ge,null,{default:r.divider?()=>r.divider?.({item:n,index:i}):void 0})])),r.default?.()]})}),{}}}),xe={name:`InfoComponent`,components:{GraphNode:fe},props:{task:{required:!0},panelExpansion:{required:!1,default:[`metadata`]}},setup(e,{emit:t}){return{inheritance:p(()=>e.task?.node?.namespace?.slice(1)??[]),jobTheme:ce(),icons:{mdiHelpCircleOutline:F}}},computed:{panelExpansionModel:{get(){return this.panelExpansion},set(e){this.$emit(`update:panelExpansion`,e)}},taskMetadata(){return this.task?.node?.task?.meta||{}},customMetadata(){return this.task?.node?.task?.meta.userDefined||{}},prerequisites(){return this.task?.node?.prerequisites||{}},outputs(){return this.task?.node?.outputs||{}},completion(){return this.task?.node?.runtime.completion},runModeIcon(){return this.task?.node?.runtime.runMode===`Skip`?N:this.task?.node?.runtime.runMode===`Live`?I:this.task?.node?.runtime.runMode===`Simulation`?M:this.task?.node?.runtime.runMode===`Dummy`?P:z},runMode(){return this.task?.node?.runtime.runMode},xtriggers(){let e=this.task?.node?.xtriggers?.map(e=>{let t=H(e);return t.satisfactionIcon=t.satisfied?L:R,t.id=t.id.replace(/trigger_time=(?<unixTime>[0-9.]+)/,(e,t)=>`trigger_time=${pe(new Date(t*1e3))}`),t});return e.sort(function(e,t){return e.label===t.label?e.id>t.id?1:-1:e.label>t.label?1:-1}),e}},methods:{formatCompletion:me}},Se={class:`c-info`},Ce={style:{"overflow-x":`hidden`}},we={preserveAspectRatio:`xMinYMin`,viewBox:`-40 -40 99999 200`,height:`6em`},Te={class:`markup`},Ee=[`href`],De={class:`markup`},Oe={class:`d-flex align-center gap-2`},Q={class:`text-mono`},ke={style:{"margin-left":`0.5em`,color:`rgb(0,0,0)`}};function Ae(t,d,p,v,y,b){let x=r(`GraphNode`);return a(),h(`div`,Se,[_(`div`,Ce,[(a(),h(`svg`,we,[s(x,{task:p.task,jobs:p.task.children,jobTheme:v.jobTheme},null,8,[`task`,`jobs`,`jobTheme`])]))]),s(le,{multiple:``,modelValue:b.panelExpansionModel,"onUpdate:modelValue":d[0]||=e=>b.panelExpansionModel=e,flat:``,static:``,color:`blue-grey-lighten-3`,"bg-color":`grey-lighten-4`,rounded:`lg`},{default:g(()=>[s(E,{defaults:{VExpansionPanelTitle:{class:`text-title-small py-2`},VExpansionPanelText:{class:`mt-2`},VTable:{density:`compact`,class:`bg-transparent`}}},{default:g(()=>[s(X,{value:`metadata`,class:`metadata-panel`},{default:g(()=>[s(J,null,{default:g(()=>[...d[1]||=[u(` Metadata `,-1)]]),_:1}),s(Y,null,{default:g(()=>[_(`dl`,null,[d[3]||=_(`dt`,null,`Title`,-1),_(`dd`,null,o(b.taskMetadata.title),1),s(j),d[4]||=_(`dt`,null,`Description`,-1),_(`dd`,null,[_(`span`,Te,o(b.taskMetadata.description),1)]),b.taskMetadata.URL?(a(),h(f,{key:0},[s(j),d[2]||=_(`dt`,null,`URL`,-1),_(`dd`,null,[_(`a`,{href:b.taskMetadata.URL,target:`_blank`},o(b.taskMetadata.URL),9,Ee)])],64)):l(``,!0),(a(!0),h(f,null,e(b.customMetadata,(e,t)=>(a(),h(f,{key:t},[s(j),_(`dt`,null,o(t),1),_(`dd`,null,[_(`span`,De,o(e),1)])],64))),128))])]),_:1})]),_:1}),s(X,{value:`runMode`,class:`run-mode-panel`},{default:g(()=>[s(J,null,{default:g(()=>[...d[5]||=[u(` Run Mode `,-1)]]),_:1}),s(Y,null,{default:g(()=>[_(`div`,Oe,[s(S,{icon:b.runModeIcon},null,8,[`icon`]),u(o(b.runMode),1)])]),_:1})]),_:1}),v.inheritance?.length>1?(a(),c(X,{key:0,value:`inheritance`,"data-cy":`inheritance-panel`},{default:g(()=>[s(J,null,{default:g(({expanded:e})=>[d[6]||=u(` Inheritance `,-1),e?m((a(),c(S,{key:0,icon:v.icons.mdiHelpCircleOutline,class:`ml-2`},null,8,[`icon`])),[[W,{text:`Shows the linearised family inheritance hierarchy for this task. The order of precedence is determined by the C3 algorithm used in Python.`,location:`top`}]]):l(``,!0)]),_:1}),s(Y,null,{default:g(()=>[s(be,{items:v.inheritance},{divider:g(()=>[...d[7]||=[_(`span`,null,`::`,-1)]]),_:1},8,[`items`])]),_:1})]),_:1})):l(``,!0),b.xtriggers.length?(a(),c(X,{key:1,value:`xtriggers`,class:`xtriggers-panel`},{default:g(()=>[s(J,null,{default:g(()=>[...d[8]||=[u(` Xtriggers `,-1)]]),_:1}),s(Y,null,{default:g(()=>[s(se,null,{default:g(()=>[d[9]||=_(`thead`,null,[_(`tr`,null,[_(`th`,null,`Label`),_(`th`,null,`ID`),_(`th`,null,`Is satisfied`)])],-1),_(`tbody`,null,[(a(!0),h(f,null,e(b.xtriggers,e=>(a(),h(`tr`,{key:e.id},[_(`td`,null,o(e.label),1),_(`td`,Q,o(e.id),1),_(`td`,null,[s(S,null,{default:g(()=>[u(o(e.satisfactionIcon),1)]),_:2},1024)])]))),128))])]),_:1})]),_:1})]),_:1})):l(``,!0),s(X,{value:`prereqs`,class:`prerequisites-panel`},{default:g(()=>[s(J,null,{default:g(()=>[...d[10]||=[u(` Prerequisites `,-1)]]),_:1}),s(Y,null,{default:g(()=>[_(`ul`,null,[(a(!0),h(f,null,e(b.prerequisites,t=>(a(),h(`li`,{key:t.expression},[_(`span`,{class:n([`prerequisite-alias condition`,{satisfied:t.satisfied}])},o(t.expression.replace(/c/g,``)),3),_(`ul`,null,[(a(!0),h(f,null,e(t.conditions,e=>(a(),h(`li`,{key:e.taskAlias},[_(`span`,{class:n([`prerequisite-alias condition`,{satisfied:e.satisfied}])},[u(o(e.exprAlias.replace(/c/,``))+` `,1),_(`span`,ke,o(e.taskId)+`:`+o(e.reqState),1)],2)]))),128))])]))),128))])]),_:1})]),_:1}),s(X,{value:`outputs`,class:`outputs-panel`},{default:g(()=>[s(J,null,{default:g(()=>[...d[11]||=[u(` Outputs `,-1)]]),_:1}),s(Y,null,{default:g(()=>[_(`ul`,null,[(a(!0),h(f,null,e(b.outputs,e=>(a(),h(`li`,{key:e.label},[_(`span`,{class:n([`condition`,{satisfied:e.satisfied}])},o(e.label),3)]))),128))])]),_:1})]),_:1}),s(X,{value:`completion`,class:`completion-panel`},{default:g(()=>[s(J,null,{default:g(()=>[...d[12]||=[u(` Completion `,-1)]]),_:1}),s(Y,null,{default:g(()=>[_(`ul`,null,[(a(!0),h(f,null,e(b.formatCompletion(b.completion,b.outputs),([e,t,r],s)=>(a(),h(`li`,{key:s},[_(`span`,{class:n([`condition`,{satisfied:e,blank:e===null}])},[_(`span`,{style:i(`margin-left: ${1*t}em;`)},null,4),u(` `+o(r),1)],2)]))),128))])]),_:1})]),_:1})]),_:1})]),_:1},8,[`modelValue`])])}var je=U(xe,[[`render`,Ae],[`__scopeId`,`data-v-da29da45`]]),Me=B`
subscription InfoViewSubscription ($workflowID: ID, $taskID: ID) {
  deltas(workflows: [$workflowID]) {
    added {
      ...AddedDelta
    }
    updated (stripNull: true) {
      ...UpdatedDelta
    }
  }
}

fragment AddedDelta on Added {
  taskProxies(ids: [$taskID]) {
    ...TaskProxyData
  }
}

fragment UpdatedDelta on Updated {
  taskProxies(ids: [$taskID]) {
    ...TaskProxyData
  }
}

fragment TaskProxyData on TaskProxy {
  id
  namespace
  state
  isHeld
  isQueued
  isRunahead
  isRetry
  isWallclock
  isXtriggered

  task {
    ...TaskDefinitionData
  }

  jobs {
    ...JobData
  }

  prerequisites {
    satisfied
    expression
    conditions {
      taskId
      reqState
      exprAlias
      satisfied
    }
  }

  outputs {
    label
    satisfied
  }

  runtime {
    completion
    runMode
  }

  xtriggers {
    label
    id
    satisfied
  }
}

fragment TaskDefinitionData on Task {
  meanElapsedTime

  meta {
    title
    description
    URL
    userDefined
  }
}

fragment JobData on Job {
  id
  jobId
  startedTime
  state
}
`;function Ne(e){let t=new V(e.id);return{id:e.id,tokens:t,name:t.task,node:e,type:`task`,children:[]}}function Pe(e){let t=new V(e.id);return{id:e.id,name:t.job,tokens:t,node:e,type:`job`}}function $(e,t){e.children=[];for(let n of t.jobs)e.children.push(Pe(n))}var Fe=class extends K{constructor(e,t){super(),this.task=e,this.taskNode=t}onAdded(e,t,n){Object.assign(this.task,e.taskProxies[0]),Object.assign(this.taskNode,Ne(this.task)),$(this.taskNode,this.task)}onUpdated(e,t,n){e?.taskProxies&&Object.assign(this.task,e.taskProxies[0]),$(this.taskNode,this.task)}onPruned(e){}},Ie={name:`InfoView`,mixins:[G],components:{InfoComponent:je},props:{initialOptions:de},setup(e,{emit:t}){let{variables:n}=ue();return{requestedTokens:Z(`requestedTokens`,{props:e,emit:t}),panelExpansion:Z(`panelExpansion`,{props:e,emit:t},[`metadata`]),variables:n}},data(){return{requestedCycle:void 0,requestedTask:void 0,task:{},taskNode:{}}},computed:{query(){return new q(Me,{...this.variables,taskID:this.requestedTokens?.relativeID},`info-query-${this._uid}`,[new Fe(this.task,this.taskNode)],!0,!1)}},methods:{updatePanelExpansion(e){this.panelExpansion=e}}};function Le(e,t,n,i,o,s){let u=r(`InfoComponent`);return o.taskNode.id?(a(),c(u,{key:0,task:o.taskNode,panelExpansion:i.panelExpansion,"onUpdate:panelExpansion":s.updatePanelExpansion},null,8,[`task`,`panelExpansion`,`onUpdate:panelExpansion`])):l(``,!0)}var Re=U(Ie,[[`render`,Le]]);export{Re as default};