import{eK as D,ds as L,d_ as $,du as z,ex as w,dv as E,dw as F,dx as R,dy as G,dz as K,dA as M,dB as N,eE as O,dC as j,e0 as H,y as o,dD as J,eL as q,ey as Q,dG as U,dH as W,dI as X,dJ as Y,dK as Z,eM as p,c1 as ee,el as ae,m as t,eN as te,G as le,$ as u,I as ne,bl as se}from"./index-DSRpE5Rv.js";const oe=D("v-alert-title"),ie=["success","info","warning","error"],re=L({border:{type:[Boolean,String],validator:e=>typeof e=="boolean"||["top","end","bottom","start"].includes(e)},borderColor:String,closable:Boolean,closeIcon:{type:$,default:"$close"},closeLabel:{type:String,default:"$vuetify.close"},icon:{type:[Boolean,String,Function,Object],default:null},modelValue:{type:Boolean,default:!0},prominent:Boolean,title:String,text:String,type:{type:String,validator:e=>ie.includes(e)},...z(),...w(),...E(),...F(),...R(),...G(),...K(),...M(),...N(),...O({variant:"flat"})},"VAlert"),de=j()({name:"VAlert",props:re(),emits:{"click:close":e=>!0,"update:modelValue":e=>!0},setup(e,v){let{emit:y,slots:a}=v;const i=H(e,"modelValue"),n=o(()=>{if(e.icon!==!1)return e.type?e.icon??`$${e.type}`:e.icon}),m=o(()=>({color:e.color??e.type,variant:e.variant})),{themeClasses:f}=J(e),{colorClasses:b,colorStyles:k,variantClasses:P}=q(m),{densityClasses:C}=Q(e),{dimensionStyles:V}=U(e),{elevationClasses:x}=W(e),{locationStyles:g}=X(e),{positionClasses:S}=Y(e),{roundedClasses:_}=Z(e),{textColorClasses:B,textColorStyles:I}=p(ee(e,"borderColor")),{t:A}=ae(),r=o(()=>({"aria-label":A(e.closeLabel),onClick(s){i.value=!1,y("click:close",s)}}));return()=>{const s=!!(a.prepend||n.value),T=!!(a.title||e.title),h=!!(a.close||e.closable);return i.value&&t(e.tag,{class:["v-alert",e.border&&{"v-alert--border":!!e.border,[`v-alert--border-${e.border===!0?"start":e.border}`]:!0},{"v-alert--prominent":e.prominent},f.value,b.value,C.value,x.value,S.value,_.value,P.value,e.class],style:[k.value,V.value,g.value,e.style],role:"alert"},{default:()=>{var c,d;return[te(!1,"v-alert"),e.border&&t("div",{key:"border",class:["v-alert__border",B.value],style:I.value},null),s&&t("div",{key:"prepend",class:"v-alert__prepend"},[a.prepend?t(u,{key:"prepend-defaults",disabled:!n.value,defaults:{VIcon:{density:e.density,icon:n.value,size:e.prominent?44:28}}},a.prepend):t(le,{key:"prepend-icon",density:e.density,icon:n.value,size:e.prominent?44:28},null)]),t("div",{class:"v-alert__content"},[T&&t(oe,{key:"title"},{default:()=>{var l;return[((l=a.title)==null?void 0:l.call(a))??e.title]}}),((c=a.text)==null?void 0:c.call(a))??e.text,(d=a.default)==null?void 0:d.call(a)]),a.append&&t("div",{key:"append",class:"v-alert__append"},[a.append()]),h&&t("div",{key:"close",class:"v-alert__close"},[a.close?t(u,{key:"close-defaults",defaults:{VBtn:{icon:e.closeIcon,size:"x-small",variant:"text"}}},{default:()=>{var l;return[(l=a.close)==null?void 0:l.call(a,{props:r.value})]}}):t(ne,se({key:"close-btn",icon:e.closeIcon,size:"x-small",variant:"text"},r.value),null)])]}})}}});export{de as V};