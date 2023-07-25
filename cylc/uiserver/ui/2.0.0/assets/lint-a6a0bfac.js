import{Y as P}from"./index-4d6c7840.js";import{a as U}from"./codemirror-ab5992a1.js";function W(v,m){for(var s=0;s<m.length;s++){const f=m[s];if(typeof f!="string"&&!Array.isArray(f)){for(const d in f)if(d!=="default"&&!(d in v)){const g=Object.getOwnPropertyDescriptor(f,d);g&&Object.defineProperty(v,d,g.get?g:{enumerable:!0,get:()=>f[d]})}}}return Object.freeze(Object.defineProperty(v,Symbol.toStringTag,{value:"Module"}))}var B={exports:{}};(function(v,m){(function(s){s(U)})(function(s){var f="CodeMirror-lint-markers",d="CodeMirror-lint-line-";function g(t,e,r){var n=document.createElement("div");n.className="CodeMirror-lint-tooltip cm-s-"+t.options.theme,n.appendChild(r.cloneNode(!0)),t.state.lint.options.selfContain?t.getWrapperElement().appendChild(n):document.body.appendChild(n);function o(i){if(!n.parentNode)return s.off(document,"mousemove",o);n.style.top=Math.max(0,i.clientY-n.offsetHeight-5)+"px",n.style.left=i.clientX+5+"px"}return s.on(document,"mousemove",o),o(e),n.style.opacity!=null&&(n.style.opacity=1),n}function T(t){t.parentNode&&t.parentNode.removeChild(t)}function w(t){t.parentNode&&(t.style.opacity==null&&T(t),t.style.opacity=0,setTimeout(function(){T(t)},600))}function L(t,e,r,n){var o=g(t,e,r);function i(){s.off(n,"mouseout",i),o&&(w(o),o=null)}var a=setInterval(function(){if(o)for(var l=n;;l=l.parentNode){if(l&&l.nodeType==11&&(l=l.host),l==document.body)return;if(!l){i();break}}if(!o)return clearInterval(a)},400);s.on(n,"mouseout",i)}function _(t,e,r){this.marked=[],e instanceof Function&&(e={getAnnotations:e}),(!e||e===!0)&&(e={}),this.options={},this.linterOptions=e.options||{};for(var n in y)this.options[n]=y[n];for(var n in e)y.hasOwnProperty(n)?e[n]!=null&&(this.options[n]=e[n]):e.options||(this.linterOptions[n]=e[n]);this.timeout=null,this.hasGutter=r,this.onMouseOver=function(o){H(t,o)},this.waitingFor=0}var y={highlightLines:!1,tooltips:!0,delay:500,lintOnChange:!0,getAnnotations:null,async:!1,selfContain:null,formatAnnotation:null,onUpdateLinting:null};function E(t){var e=t.state.lint;e.hasGutter&&t.clearGutter(f),e.options.highlightLines&&A(t);for(var r=0;r<e.marked.length;++r)e.marked[r].clear();e.marked.length=0}function A(t){t.eachLine(function(e){var r=e.wrapClass&&/\bCodeMirror-lint-line-\w+\b/.exec(e.wrapClass);r&&t.removeLineClass(e,"wrap",r[0])})}function F(t,e,r,n,o){var i=document.createElement("div"),a=i;return i.className="CodeMirror-lint-marker CodeMirror-lint-marker-"+r,n&&(a=i.appendChild(document.createElement("div")),a.className="CodeMirror-lint-marker CodeMirror-lint-marker-multiple"),o!=!1&&s.on(a,"mouseover",function(l){L(t,l,e,a)}),i}function G(t,e){return t=="error"?t:e}function I(t){for(var e=[],r=0;r<t.length;++r){var n=t[r],o=n.from.line;(e[o]||(e[o]=[])).push(n)}return e}function M(t){var e=t.severity;e||(e="error");var r=document.createElement("div");return r.className="CodeMirror-lint-message CodeMirror-lint-message-"+e,typeof t.messageHTML<"u"?r.innerHTML=t.messageHTML:r.appendChild(document.createTextNode(t.message)),r}function D(t,e){var r=t.state.lint,n=++r.waitingFor;function o(){n=-1,t.off("change",o)}t.on("change",o),e(t.getValue(),function(i,a){t.off("change",o),r.waitingFor==n&&(a&&i instanceof s&&(i=a),t.operation(function(){k(t,i)}))},r.linterOptions,t)}function C(t){var e=t.state.lint;if(e){var r=e.options,n=r.getAnnotations||t.getHelper(s.Pos(0,0),"lint");if(n)if(r.async||n.async)D(t,n);else{var o=n(t.getValue(),e.linterOptions,t);if(!o)return;o.then?o.then(function(i){t.operation(function(){k(t,i)})}):t.operation(function(){k(t,o)})}}}function k(t,e){var r=t.state.lint;if(r){var n=r.options;E(t);for(var o=I(e),i=0;i<o.length;++i){var a=o[i];if(a){var l=[];a=a.filter(function(N){return l.indexOf(N.message)>-1?!1:l.push(N.message)});for(var u=null,h=r.hasGutter&&document.createDocumentFragment(),O=0;O<a.length;++O){var p=a[O],c=p.severity;c||(c="error"),u=G(u,c),n.formatAnnotation&&(p=n.formatAnnotation(p)),r.hasGutter&&h.appendChild(M(p)),p.to&&r.marked.push(t.markText(p.from,p.to,{className:"CodeMirror-lint-mark CodeMirror-lint-mark-"+c,__annotation:p}))}r.hasGutter&&t.setGutterMarker(i,f,F(t,h,u,o[i].length>1,n.tooltips)),n.highlightLines&&t.addLineClass(i,"wrap",d+u)}}n.onUpdateLinting&&n.onUpdateLinting(e,o,t)}}function x(t){var e=t.state.lint;e&&(clearTimeout(e.timeout),e.timeout=setTimeout(function(){C(t)},e.options.delay))}function j(t,e,r){for(var n=r.target||r.srcElement,o=document.createDocumentFragment(),i=0;i<e.length;i++){var a=e[i];o.appendChild(M(a))}L(t,r,o,n)}function H(t,e){var r=e.target||e.srcElement;if(/\bCodeMirror-lint-mark-/.test(r.className)){for(var n=r.getBoundingClientRect(),o=(n.left+n.right)/2,i=(n.top+n.bottom)/2,a=t.findMarksAt(t.coordsChar({left:o,top:i},"client")),l=[],u=0;u<a.length;++u){var h=a[u].__annotation;h&&l.push(h)}l.length&&j(t,l,e)}}s.defineOption("lint",!1,function(t,e,r){if(r&&r!=s.Init&&(E(t),t.state.lint.options.lintOnChange!==!1&&t.off("change",x),s.off(t.getWrapperElement(),"mouseover",t.state.lint.onMouseOver),clearTimeout(t.state.lint.timeout),delete t.state.lint),e){for(var n=t.getOption("gutters"),o=!1,i=0;i<n.length;++i)n[i]==f&&(o=!0);var a=t.state.lint=new _(t,e,o);a.options.lintOnChange&&t.on("change",x),a.options.tooltips!=!1&&a.options.tooltips!="gutter"&&s.on(t.getWrapperElement(),"mouseover",a.onMouseOver),C(t)}}),s.defineExtension("performLint",function(){C(this)})})})();var b=B.exports;const R=P(b),$=W({__proto__:null,default:R},[b]);export{$ as l};
