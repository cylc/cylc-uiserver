import{U as T,bt as W,ds as G,d_ as x,dt as K,du as U,ex as q,dw as H,dz as J,eD as O,dA as X,dB as j,eE as Q,dC as Y,e0 as Z,el as ee,eF as ae,dD as te,eG as le,bW as ie,eC as S,eH as ne,y as b,eI as k,c1 as f,dL as se,m as o,I as L,bl as P,eJ as R,bm as B}from"./index-DSRpE5Rv.js";function ue(){const e=T([]);W(()=>e.value=[]);function V(n,_){e.value[_]=n}return{refs:e,updateRef:V}}const re=G({activeColor:String,start:{type:[Number,String],default:1},modelValue:{type:Number,default:e=>e.start},disabled:Boolean,length:{type:[Number,String],default:1,validator:e=>e%1===0},totalVisible:[Number,String],firstIcon:{type:x,default:"$first"},prevIcon:{type:x,default:"$prev"},nextIcon:{type:x,default:"$next"},lastIcon:{type:x,default:"$last"},ariaLabel:{type:String,default:"$vuetify.pagination.ariaLabel.root"},pageAriaLabel:{type:String,default:"$vuetify.pagination.ariaLabel.page"},currentPageAriaLabel:{type:String,default:"$vuetify.pagination.ariaLabel.currentPage"},firstAriaLabel:{type:String,default:"$vuetify.pagination.ariaLabel.first"},previousAriaLabel:{type:String,default:"$vuetify.pagination.ariaLabel.previous"},nextAriaLabel:{type:String,default:"$vuetify.pagination.ariaLabel.next"},lastAriaLabel:{type:String,default:"$vuetify.pagination.ariaLabel.last"},ellipsis:{type:String,default:"..."},showFirstLastPage:Boolean,...K(),...U(),...q(),...H(),...J(),...O(),...X({tag:"nav"}),...j(),...Q({variant:"text"})},"VPagination"),ve=Y()({name:"VPagination",props:re(),emits:{"update:modelValue":e=>!0,first:e=>!0,prev:e=>!0,next:e=>!0,last:e=>!0},setup(e,V){let{slots:n,emit:_}=V;const i=Z(e,"modelValue"),{t:g,n:C}=ee(),{isRtl:h}=ae(),{themeClasses:$}=te(e),{width:w}=le(),I=ie(-1);S(void 0,{scoped:!0});const{resizeRef:F}=ne(a=>{if(!a.length)return;const{target:t,contentRect:l}=a[0],r=t.querySelector(".v-pagination__list > *");if(!r)return;const v=l.width,m=r.offsetWidth+parseFloat(getComputedStyle(r).marginRight)*2;I.value=p(v,m)}),s=b(()=>parseInt(e.length,10)),u=b(()=>parseInt(e.start,10)),d=b(()=>e.totalVisible!=null?parseInt(e.totalVisible,10):I.value>=0?I.value:p(w.value,58));function p(a,t){const l=e.showFirstLastPage?5:3;return Math.max(0,Math.floor(+((a-t*l)/t).toFixed(2)))}const M=b(()=>{if(s.value<=0||isNaN(s.value)||s.value>Number.MAX_SAFE_INTEGER)return[];if(d.value<=0)return[];if(d.value===1)return[i.value];if(s.value<=d.value)return k(s.value,u.value);const a=d.value%2===0,t=a?d.value/2:Math.floor(d.value/2),l=a?t:t+1,r=s.value-t;if(l-i.value>=0)return[...k(Math.max(1,d.value-1),u.value),e.ellipsis,s.value];if(i.value-r>=(a?1:0)){const v=d.value-1,m=s.value-v+u.value;return[u.value,e.ellipsis,...k(v,m)]}else{const v=Math.max(1,d.value-3),m=v===1?i.value:i.value-Math.ceil(v/2)+u.value;return[u.value,e.ellipsis,...k(v,m),e.ellipsis,s.value]}});function y(a,t,l){a.preventDefault(),i.value=t,l&&_(l,t)}const{refs:N,updateRef:D}=ue();S({VPaginationBtn:{color:f(e,"color"),border:f(e,"border"),density:f(e,"density"),size:f(e,"size"),variant:f(e,"variant"),rounded:f(e,"rounded"),elevation:f(e,"elevation")}});const z=b(()=>M.value.map((a,t)=>{const l=r=>D(r,t);if(typeof a=="string")return{isActive:!1,key:`ellipsis-${t}`,page:a,props:{ref:l,ellipsis:!0,icon:!0,disabled:!0}};{const r=a===i.value;return{isActive:r,key:a,page:C(a),props:{ref:l,ellipsis:!1,icon:!0,disabled:!!e.disabled||+e.length<2,color:r?e.activeColor:e.color,"aria-current":r,"aria-label":g(r?e.currentPageAriaLabel:e.pageAriaLabel,a),onClick:v=>y(v,a)}}}})),c=b(()=>{const a=!!e.disabled||i.value<=u.value,t=!!e.disabled||i.value>=u.value+s.value-1;return{first:e.showFirstLastPage?{icon:h.value?e.lastIcon:e.firstIcon,onClick:l=>y(l,u.value,"first"),disabled:a,"aria-label":g(e.firstAriaLabel),"aria-disabled":a}:void 0,prev:{icon:h.value?e.nextIcon:e.prevIcon,onClick:l=>y(l,i.value-1,"prev"),disabled:a,"aria-label":g(e.previousAriaLabel),"aria-disabled":a},next:{icon:h.value?e.prevIcon:e.nextIcon,onClick:l=>y(l,i.value+1,"next"),disabled:t,"aria-label":g(e.nextAriaLabel),"aria-disabled":t},last:e.showFirstLastPage?{icon:h.value?e.firstIcon:e.lastIcon,onClick:l=>y(l,u.value+s.value-1,"last"),disabled:t,"aria-label":g(e.lastAriaLabel),"aria-disabled":t}:void 0}});function A(){var t;const a=i.value-u.value;(t=N.value[a])==null||t.$el.focus()}function E(a){a.key===R.left&&!e.disabled&&i.value>+e.start?(i.value=i.value-1,B(A)):a.key===R.right&&!e.disabled&&i.value<u.value+s.value-1&&(i.value=i.value+1,B(A))}return se(()=>o(e.tag,{ref:F,class:["v-pagination",$.value,e.class],style:e.style,role:"navigation","aria-label":g(e.ariaLabel),onKeydown:E,"data-test":"v-pagination-root"},{default:()=>[o("ul",{class:"v-pagination__list"},[e.showFirstLastPage&&o("li",{key:"first",class:"v-pagination__first","data-test":"v-pagination-first"},[n.first?n.first(c.value.first):o(L,P({_as:"VPaginationBtn"},c.value.first),null)]),o("li",{key:"prev",class:"v-pagination__prev","data-test":"v-pagination-prev"},[n.prev?n.prev(c.value.prev):o(L,P({_as:"VPaginationBtn"},c.value.prev),null)]),z.value.map((a,t)=>o("li",{key:a.key,class:["v-pagination__item",{"v-pagination__item--is-active":a.isActive}],"data-test":"v-pagination-item"},[n.item?n.item(a):o(L,P({_as:"VPaginationBtn"},a.props),{default:()=>[a.page]})])),o("li",{key:"next",class:"v-pagination__next","data-test":"v-pagination-next"},[n.next?n.next(c.value.next):o(L,P({_as:"VPaginationBtn"},c.value.next),null)]),e.showFirstLastPage&&o("li",{key:"last",class:"v-pagination__last","data-test":"v-pagination-last"},[n.last?n.last(c.value.last):o(L,P({_as:"VPaginationBtn"},c.value.last),null)])])]})),{}}});export{ve as V};