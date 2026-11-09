import{n as e}from"./lib-BD1OgZUd.js";import{E as t,T as n,V as r,c as i,j as a,l as o,o as s,q as c,s as l,w as u}from"./index-_99OrTPv.js";import{r as d,t as f}from"./initialOptions-CHcgzlQU.js";import{t as p}from"./uid-B9ZHvQie.js";import{D as m,E as h,St as g,Yt as _,Zn as v,_ as y,b,bt as x,er as S,et as C,g as w,mt as T,o as E,qt as D,tr as O,v as k,wn as A,y as j}from"./runtime-core.esm-bundler-DZo3dYLJ.js";import{t as M}from"./GraphNode-bgeHy5TY.js";import{B as N,Ct as P,D as ee,G as te,dt as ne,h as re,m as ie,p as ae}from"./mdi-DCsggE_y.js";import{t as oe}from"./cloneDeep-BmW0sM2O.js";import{t as se}from"./datetime-B1UdshvC.js";import{t as F}from"./_plugin-vue_export-helper-BDNMzG2s.js";import{C as I,J as L,V as R,W as z,Yt as B,_ as V,c as H,et as U,g as W,h as G,it as K,l as ce,m as le,p as ue,r as de,rt as q,t as fe,u as J,v as Y,x as pe,yn as X}from"./router-Dc1DjKwM.js";import{t as Z}from"./VDivider-CM00VNx1.js";import{t as me}from"./tooltip-BPNQQQ0K.js";function he(e,t){let n=[],r=0,i=``;for(let a of e.split(/(and|or|\(|\))/))if(a=a.trim().replace(`_`,`-`),a){if(a===`(`)n.push([null,r,`${i}(`]),i=``,r+=1;else if(a===`)`)--r,n.push([null,r,`${i})`]),i=``;else if(a===`and`||a===`or`)i=`${a} `;else{for(let e of t)if(e.label===a){n.push([e.satisfied,r,`${i}${a}`]);break}i=``}}return n}var ge=K({divider:[Number,String],...q()},`VBreadcrumbsDivider`),_e=L()({name:`VBreadcrumbsDivider`,props:ge(),setup(e,{slots:t}){return z(()=>y(`li`,{"aria-hidden":`true`,class:v([`v-breadcrumbs-divider`,e.class]),style:S(e.style)},[t?.default?.()??e.divider])),{}}}),ve=K({active:Boolean,activeClass:String,activeColor:String,color:String,disabled:Boolean,title:String,...q(),...B(G(),[`width`,`maxWidth`]),...fe(),...Y({tag:`li`})},`VBreadcrumbsItem`),ye=L()({name:`VBreadcrumbsItem`,props:ve(),setup(e,{slots:t,attrs:n}){let r=de(e,n),i=w(()=>e.active||r.isActive?.value),{dimensionStyles:a}=W(e),{textColorClasses:o,textColorStyles:s}=I(()=>i.value?e.activeColor:e.color);return z(()=>m(e.tag,{class:v([`v-breadcrumbs-item`,{"v-breadcrumbs-item--active":i.value,"v-breadcrumbs-item--disabled":e.disabled,[`${e.activeClass}`]:i.value&&e.activeClass},o.value,e.class]),style:S([s.value,a.value,e.style]),"aria-current":i.value?`page`:void 0},{default:()=>[r.isLink.value?y(`a`,C({class:`v-breadcrumbs-item--link`,onClick:r.navigate.value},r.linkProps),[t.default?.()??e.title]):t.default?.()??e.title]})),{}}}),be=K({activeClass:String,activeColor:String,bgColor:String,color:String,disabled:Boolean,divider:{type:String,default:`/`},icon:R,items:{type:Array,default:()=>[]},...q(),...H(),...ue(),...Y({tag:`ul`})},`VBreadcrumbs`),xe=L()({name:`VBreadcrumbs`,props:be(),setup(e,{slots:t}){let{backgroundColorClasses:n,backgroundColorStyles:r}=pe(()=>e.bgColor),{densityClasses:i}=ce(e),{roundedClasses:a,roundedStyles:o}=le(e);U({VBreadcrumbsDivider:{divider:A(()=>e.divider)},VBreadcrumbsItem:{activeClass:A(()=>e.activeClass),activeColor:A(()=>e.activeColor),color:A(()=>e.color),disabled:A(()=>e.disabled)}});let s=w(()=>e.items.map(e=>X(e)?{item:{title:e},raw:e}:{item:e,raw:e}));return z(()=>{let c=!!(t.prepend||e.icon);return m(e.tag,{class:v([`v-breadcrumbs`,n.value,i.value,a.value,e.class]),style:S([r.value,o.value,e.style])},{default:()=>[c&&y(`li`,{key:`prepend`,class:`v-breadcrumbs__prepend`},[t.prepend?m(J,{key:`prepend-defaults`,disabled:!e.icon,defaults:{VIcon:{icon:e.icon,start:!0}}},t.prepend):m(V,{key:`prepend-icon`,start:!0,icon:e.icon},null)]),s.value.map(({item:e,raw:n},r,i)=>y(E,null,[t.item?.({item:e,index:r})??m(ye,C({key:r,disabled:r>=i.length-1},X(e)?{title:e}:e),{default:t.title?()=>t.title?.({item:e,index:r}):void 0}),r<i.length-1&&m(_e,null,{default:t.divider?()=>t.divider?.({item:n,index:r}):void 0})])),t.default?.()]})}),{}}}),Se={name:`InfoComponent`,components:{GraphNode:M},props:{task:{required:!0},panelExpansion:{required:!1,default:[`metadata`]}},setup(e,{emit:t}){return{inheritance:w(()=>e.task?.node?.namespace?.slice(1)??[]),jobTheme:a(),icons:{mdiHelpCircleOutline:te}}},computed:{panelExpansionModel:{get(){return this.panelExpansion},set(e){this.$emit(`update:panelExpansion`,e)}},taskMetadata(){return this.task?.node?.task?.meta||{}},customMetadata(){return this.task?.node?.task?.meta.userDefined||{}},prerequisites(){return this.task?.node?.prerequisites||{}},outputs(){return this.task?.node?.outputs||{}},completion(){return this.task?.node?.runtime.completion},runModeIcon(){return this.task?.node?.runtime.runMode===`Skip`?P:this.task?.node?.runtime.runMode===`Live`?ne:this.task?.node?.runtime.runMode===`Simulation`?N:this.task?.node?.runtime.runMode===`Dummy`?ee:ae},runMode(){return this.task?.node?.runtime.runMode},xtriggers(){let e=this.task?.node?.xtriggers?.map(e=>{let t=oe(e);return t.satisfactionIcon=t.satisfied?re:ie,t.id=t.id.replace(/trigger_time=(?<unixTime>[0-9.]+)/,(e,t)=>`trigger_time=${se(new Date(t*1e3))}`),t});return e.sort(function(e,t){return e.label===t.label?e.id>t.id?1:-1:e.label>t.label?1:-1}),e}},methods:{formatCompletion:he}},Ce={class:`c-info`},we={style:{"overflow-x":`hidden`}},Te={preserveAspectRatio:`xMinYMin`,viewBox:`-40 -40 99999 200`,height:`6em`},Ee={class:`markup`},De=[`href`],Oe={class:`markup`},Q={class:`d-flex align-center gap-2`},ke={class:`text-mono`},Ae={style:{"margin-left":`0.5em`,color:`rgb(0,0,0)`}};function je(e,t,n,a,c,u){let d=g(`GraphNode`);return T(),b(`div`,Ce,[y(`div`,we,[(T(),b(`svg`,Te,[m(d,{task:n.task,jobs:n.task.children,jobTheme:a.jobTheme},null,8,[`task`,`jobs`,`jobTheme`])]))]),m(s,{multiple:``,modelValue:u.panelExpansionModel,"onUpdate:modelValue":t[0]||=e=>u.panelExpansionModel=e,flat:``,static:``,color:`blue-grey-lighten-3`,"bg-color":`grey-lighten-4`,rounded:`lg`},{default:D(()=>[m(J,{defaults:{VExpansionPanelTitle:{class:`text-title-small py-2`},VExpansionPanelText:{class:`mt-2`},VTable:{density:`compact`,class:`bg-transparent`}}},{default:D(()=>[m(l,{value:`metadata`,class:`metadata-panel`},{default:D(()=>[m(i,null,{default:D(()=>[...t[1]||=[h(` Metadata `,-1)]]),_:1}),m(o,null,{default:D(()=>[y(`dl`,null,[t[3]||=y(`dt`,null,`Title`,-1),y(`dd`,null,O(u.taskMetadata.title),1),m(Z),t[4]||=y(`dt`,null,`Description`,-1),y(`dd`,null,[y(`span`,Ee,O(u.taskMetadata.description),1)]),u.taskMetadata.URL?(T(),b(E,{key:0},[m(Z),t[2]||=y(`dt`,null,`URL`,-1),y(`dd`,null,[y(`a`,{href:u.taskMetadata.URL,target:`_blank`},O(u.taskMetadata.URL),9,De)])],64)):j(``,!0),(T(!0),b(E,null,x(u.customMetadata,(e,t)=>(T(),b(E,{key:t},[m(Z),y(`dt`,null,O(t),1),y(`dd`,null,[y(`span`,Oe,O(e),1)])],64))),128))])]),_:1})]),_:1}),m(l,{value:`runMode`,class:`run-mode-panel`},{default:D(()=>[m(i,null,{default:D(()=>[...t[5]||=[h(` Run Mode `,-1)]]),_:1}),m(o,null,{default:D(()=>[y(`div`,Q,[m(V,{icon:u.runModeIcon},null,8,[`icon`]),h(O(u.runMode),1)])]),_:1})]),_:1}),a.inheritance?.length>1?(T(),k(l,{key:0,value:`inheritance`,"data-cy":`inheritance-panel`},{default:D(()=>[m(i,null,{default:D(({expanded:e})=>[t[6]||=h(` Inheritance `,-1),e?_((T(),k(V,{key:0,icon:a.icons.mdiHelpCircleOutline,class:`ml-2`},null,8,[`icon`])),[[me,{text:`Shows the linearised family inheritance hierarchy for this task. The order of precedence is determined by the C3 algorithm used in Python.`,location:`top`}]]):j(``,!0)]),_:1}),m(o,null,{default:D(()=>[m(xe,{items:a.inheritance},{divider:D(()=>[...t[7]||=[y(`span`,null,`::`,-1)]]),_:1},8,[`items`])]),_:1})]),_:1})):j(``,!0),u.xtriggers.length?(T(),k(l,{key:1,value:`xtriggers`,class:`xtriggers-panel`},{default:D(()=>[m(i,null,{default:D(()=>[...t[8]||=[h(` Xtriggers `,-1)]]),_:1}),m(o,null,{default:D(()=>[m(r,null,{default:D(()=>[t[9]||=y(`thead`,null,[y(`tr`,null,[y(`th`,null,`Label`),y(`th`,null,`ID`),y(`th`,null,`Is satisfied`)])],-1),y(`tbody`,null,[(T(!0),b(E,null,x(u.xtriggers,e=>(T(),b(`tr`,{key:e.id},[y(`td`,null,O(e.label),1),y(`td`,ke,O(e.id),1),y(`td`,null,[m(V,null,{default:D(()=>[h(O(e.satisfactionIcon),1)]),_:2},1024)])]))),128))])]),_:1})]),_:1})]),_:1})):j(``,!0),m(l,{value:`prereqs`,class:`prerequisites-panel`},{default:D(()=>[m(i,null,{default:D(()=>[...t[10]||=[h(` Prerequisites `,-1)]]),_:1}),m(o,null,{default:D(()=>[y(`ul`,null,[(T(!0),b(E,null,x(u.prerequisites,e=>(T(),b(`li`,{key:e.expression},[y(`span`,{class:v([`prerequisite-alias condition`,{satisfied:e.satisfied}])},O(e.expression.replace(/c/g,``)),3),y(`ul`,null,[(T(!0),b(E,null,x(e.conditions,e=>(T(),b(`li`,{key:e.taskAlias},[y(`span`,{class:v([`prerequisite-alias condition`,{satisfied:e.satisfied}])},[h(O(e.exprAlias.replace(/c/,``))+` `,1),y(`span`,Ae,O(e.taskId)+`:`+O(e.reqState),1)],2)]))),128))])]))),128))])]),_:1})]),_:1}),m(l,{value:`outputs`,class:`outputs-panel`},{default:D(()=>[m(i,null,{default:D(()=>[...t[11]||=[h(` Outputs `,-1)]]),_:1}),m(o,null,{default:D(()=>[y(`ul`,null,[(T(!0),b(E,null,x(u.outputs,e=>(T(),b(`li`,{key:e.label},[y(`span`,{class:v([`condition`,{satisfied:e.satisfied}])},O(e.label),3)]))),128))])]),_:1})]),_:1}),m(l,{value:`completion`,class:`completion-panel`},{default:D(()=>[m(i,null,{default:D(()=>[...t[12]||=[h(` Completion `,-1)]]),_:1}),m(o,null,{default:D(()=>[y(`ul`,null,[(T(!0),b(E,null,x(u.formatCompletion(u.completion,u.outputs),([e,t,n],r)=>(T(),b(`li`,{key:r},[y(`span`,{class:v([`condition`,{satisfied:e,blank:e===null}])},[y(`span`,{style:S(`margin-left: ${1*t}em;`)},null,4),h(` `+O(n),1)],2)]))),128))])]),_:1})]),_:1})]),_:1})]),_:1},8,[`modelValue`])])}var Me=F(Se,[[`render`,je],[`__scopeId`,`data-v-25d5a24e`]]),Ne=e`
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
`;function Pe(e){let t=new p(e.id);return{id:e.id,tokens:t,name:t.task,node:e,type:`task`,children:[]}}function Fe(e){let t=new p(e.id);return{id:e.id,name:t.job,tokens:t,node:e,type:`job`}}function $(e,t){e.children=[];for(let n of t.jobs)e.children.push(Fe(n))}var Ie=class extends c{constructor(e,t){super(),this.task=e,this.taskNode=t}onAdded(e,t,n){Object.assign(this.task,e.taskProxies[0]),Object.assign(this.taskNode,Pe(this.task)),$(this.taskNode,this.task)}onUpdated(e,t,n){e?.taskProxies&&Object.assign(this.task,e.taskProxies[0]),$(this.taskNode,this.task)}onPruned(e){}},Le={name:`InfoView`,mixins:[t],components:{InfoComponent:Me},props:{initialOptions:f},setup(e,{emit:t}){let{variables:n}=u();return{requestedTokens:d(`requestedTokens`,{props:e,emit:t}),panelExpansion:d(`panelExpansion`,{props:e,emit:t},[`metadata`]),variables:n}},data(){return{requestedCycle:void 0,requestedTask:void 0,task:{},taskNode:{}}},computed:{query(){return new n(Ne,{...this.variables,taskID:this.requestedTokens?.relativeID},`info-query-${this._uid}`,[new Ie(this.task,this.taskNode)],!0,!1)}},methods:{updatePanelExpansion(e){this.panelExpansion=e}}};function Re(e,t,n,r,i,a){let o=g(`InfoComponent`);return i.taskNode.id?(T(),k(o,{key:0,task:i.taskNode,panelExpansion:r.panelExpansion,"onUpdate:panelExpansion":a.updatePanelExpansion},null,8,[`task`,`panelExpansion`,`onUpdate:panelExpansion`])):j(``,!0)}var ze=F(Le,[[`render`,Re]]);export{ze as default};