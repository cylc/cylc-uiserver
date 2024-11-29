import{r as _,g as m}from"./codemirror.es2-CXusOVRv.js";function H(T,A){for(var e=0;e<A.length;e++){const c=A[e];if(typeof c!="string"&&!Array.isArray(c)){for(const t in c)if(t!=="default"&&!(t in T)){const a=Object.getOwnPropertyDescriptor(c,t);a&&Object.defineProperty(T,t,a.get?a:{enumerable:!0,get:()=>c[t]})}}}return Object.freeze(Object.defineProperty(T,Symbol.toStringTag,{value:"Module"}))}var S={exports:{}};(function(T,A){(function(e){e(_())})(function(e){function c(t){return function(a,f){var r=f.line,s=a.getLine(r);function v(i){for(var u,g=f.ch,h=0;;){var b=g<=0?-1:s.lastIndexOf(i[0],g-1);if(b==-1){if(h==1)break;h=1,g=s.length;continue}if(h==1&&b<f.ch)break;if(u=a.getTokenTypeAt(e.Pos(r,b+1)),!/^(comment|string)/.test(u))return{ch:b+1,tokenType:u,pair:i};g=b-1}}function k(i){var u=1,g=a.lastLine(),h,b=i.ch,F;e:for(var y=r;y<=g;++y)for(var L=a.getLine(y),p=y==r?b:0;;){var d=L.indexOf(i.pair[0],p),O=L.indexOf(i.pair[1],p);if(d<0&&(d=L.length),O<0&&(O=L.length),p=Math.min(d,O),p==L.length)break;if(a.getTokenTypeAt(e.Pos(y,p+1))==i.tokenType){if(p==d)++u;else if(!--u){h=y,F=p;break e}}++p}return h==null||r==h?null:{from:e.Pos(r,b),to:e.Pos(h,F)}}for(var l=[],n=0;n<t.length;n++){var o=v(t[n]);o&&l.push(o)}l.sort(function(i,u){return i.ch-u.ch});for(var n=0;n<l.length;n++){var P=k(l[n]);if(P)return P}return null}}e.registerHelper("fold","brace",c([["{","}"],["[","]"]])),e.registerHelper("fold","brace-paren",c([["{","}"],["[","]"],["(",")"]])),e.registerHelper("fold","import",function(t,a){function f(n){if(n<t.firstLine()||n>t.lastLine())return null;var o=t.getTokenAt(e.Pos(n,1));if(/\S/.test(o.string)||(o=t.getTokenAt(e.Pos(n,o.end+1))),o.type!="keyword"||o.string!="import")return null;for(var P=n,i=Math.min(t.lastLine(),n+10);P<=i;++P){var u=t.getLine(P),g=u.indexOf(";");if(g!=-1)return{startCh:o.end,end:e.Pos(P,g)}}}var r=a.line,s=f(r),v;if(!s||f(r-1)||(v=f(r-2))&&v.end.line==r-1)return null;for(var k=s.end;;){var l=f(k.line+1);if(l==null)break;k=l.end}return{from:t.clipPos(e.Pos(r,s.startCh+1)),to:k}}),e.registerHelper("fold","include",function(t,a){function f(l){if(l<t.firstLine()||l>t.lastLine())return null;var n=t.getTokenAt(e.Pos(l,1));if(/\S/.test(n.string)||(n=t.getTokenAt(e.Pos(l,n.end+1))),n.type=="meta"&&n.string.slice(0,8)=="#include")return n.start+8}var r=a.line,s=f(r);if(s==null||f(r-1)!=null)return null;for(var v=r;;){var k=f(v+1);if(k==null)break;++v}return{from:e.Pos(r,s+1),to:t.clipPos(e.Pos(v))}})})})();var j=S.exports;const I=m(j),D=H({__proto__:null,default:I},[j]);export{D as b};