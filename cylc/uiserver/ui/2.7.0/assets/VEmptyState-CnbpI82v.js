import{bP as V,bQ as _,bR as C,bS as T,bT as P,bU as I,bV as z,bW as E,bX as D,bY as W,bZ as B,b_ as R,b$ as j,k as a,I as A,c0 as F,E as N,Y as d,c1 as U,G as Y}from"./index-Hyq34tSM.js";const $=V({actionText:String,bgColor:String,color:String,icon:_,image:String,justify:{type:String,default:"center"},headline:String,title:String,text:String,textWidth:{type:[Number,String],default:500},href:String,to:String,...C(),...T(),...P({size:void 0}),...I()},"VEmptyState"),H=z()({name:"VEmptyState",props:$(),emits:{"click:action":e=>!0},setup(e,u){let{emit:y,slots:t}=u;const{themeClasses:r}=E(e),{backgroundColorClasses:g,backgroundColorStyles:v}=D(W(e,"bgColor")),{dimensionStyles:h}=B(e),{displayClasses:k}=R();function s(n){y("click:action",n)}return j(()=>{var c,l,o;const n=!!(t.actions||e.actionText),b=!!(t.headline||e.headline),f=!!(t.title||e.title),S=!!(t.text||e.text),x=!!(t.media||e.image||e.icon),i=e.size||(e.image?200:96);return a("div",{class:["v-empty-state",{[`v-empty-state--${e.justify}`]:!0},r.value,g.value,k.value,e.class],style:[v.value,h.value,e.style]},[x&&a("div",{key:"media",class:"v-empty-state__media"},[t.media?a(d,{key:"media-defaults",defaults:{VImg:{src:e.image,height:i},VIcon:{size:i,icon:e.icon}}},{default:()=>[t.media()]}):a(A,null,[e.image?a(F,{key:"image",src:e.image,height:i},null):e.icon?a(N,{key:"icon",color:e.color,size:i,icon:e.icon},null):void 0])]),b&&a("div",{key:"headline",class:"v-empty-state__headline"},[((c=t.headline)==null?void 0:c.call(t))??e.headline]),f&&a("div",{key:"title",class:"v-empty-state__title"},[((l=t.title)==null?void 0:l.call(t))??e.title]),S&&a("div",{key:"text",class:"v-empty-state__text",style:{maxWidth:U(e.textWidth)}},[((o=t.text)==null?void 0:o.call(t))??e.text]),t.default&&a("div",{key:"content",class:"v-empty-state__content"},[t.default()]),n&&a("div",{key:"actions",class:"v-empty-state__actions"},[a(d,{defaults:{VBtn:{class:"v-empty-state__action-btn",color:e.color??"surface-variant",text:e.actionText}}},{default:()=>{var m;return[((m=t.actions)==null?void 0:m.call(t,{props:{onClick:s}}))??a(Y,{onClick:s},null)]}})])])}),{}}});export{H as V};