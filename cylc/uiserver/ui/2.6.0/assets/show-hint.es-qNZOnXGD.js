import{r as ot,g as rt}from"./codemirror.es2-CXusOVRv.js";function ct(S,C){for(var r=0;r<C.length;r++){const y=C[r];if(typeof y!="string"&&!Array.isArray(y)){for(const v in y)if(v!=="default"&&!(v in S)){const w=Object.getOwnPropertyDescriptor(y,v);w&&Object.defineProperty(S,v,w.get?w:{enumerable:!0,get:()=>y[v]})}}}return Object.freeze(Object.defineProperty(S,Symbol.toStringTag,{value:"Module"}))}var lt={exports:{}};(function(S,C){(function(r){r(ot())})(function(r){var y="CodeMirror-hint",v="CodeMirror-hint-active";r.showHint=function(t,e,i){if(!e)return t.showHint(i);i&&i.async&&(e.async=!0);var n={hint:e};if(i)for(var s in i)n[s]=i[s];return t.showHint(n)},r.defineExtension("showHint",function(t){t=Q(this,this.getCursor("start"),t);var e=this.listSelections();if(!(e.length>1)){if(this.somethingSelected()){if(!t.hint.supportsSelection)return;for(var i=0;i<e.length;i++)if(e[i].head.line!=e[i].anchor.line)return}this.state.completionActive&&this.state.completionActive.close();var n=this.state.completionActive=new w(this,t);n.options.hint&&(r.signal(this,"startCompletion",this),n.update(!0))}}),r.defineExtension("closeHint",function(){this.state.completionActive&&this.state.completionActive.close()});function w(t,e){if(this.cm=t,this.options=e,this.widget=null,this.debounce=0,this.tick=0,this.startPos=this.cm.getCursor("start"),this.startLen=this.cm.getLine(this.startPos.line).length-this.cm.getSelection().length,this.options.updateOnCursorActivity){var i=this;t.on("cursorActivity",this.activityFunc=function(){i.cursorActivity()})}}var G=window.requestAnimationFrame||function(t){return setTimeout(t,1e3/60)},J=window.cancelAnimationFrame||clearTimeout;w.prototype={close:function(){this.active()&&(this.cm.state.completionActive=null,this.tick=null,this.options.updateOnCursorActivity&&this.cm.off("cursorActivity",this.activityFunc),this.widget&&this.data&&r.signal(this.data,"close"),this.widget&&this.widget.close(),r.signal(this.cm,"endCompletion",this.cm))},active:function(){return this.cm.state.completionActive==this},pick:function(t,e){var i=t.list[e],n=this;this.cm.operation(function(){i.hint?i.hint(n.cm,t,i):n.cm.replaceRange(R(i),i.from||t.from,i.to||t.to,"complete"),r.signal(t,"pick",i),n.cm.scrollIntoView()}),this.options.closeOnPick&&this.close()},cursorActivity:function(){this.debounce&&(J(this.debounce),this.debounce=0);var t=this.startPos;this.data&&(t=this.data.from);var e=this.cm.getCursor(),i=this.cm.getLine(e.line);if(e.line!=this.startPos.line||i.length-e.ch!=this.startLen-this.startPos.ch||e.ch<t.ch||this.cm.somethingSelected()||!e.ch||this.options.closeCharacters.test(i.charAt(e.ch-1)))this.close();else{var n=this;this.debounce=G(function(){n.update()}),this.widget&&this.widget.disable()}},update:function(t){if(this.tick!=null){var e=this,i=++this.tick;K(this.options.hint,this.cm,this.options,function(n){e.tick==i&&e.finishUpdate(n,t)})}},finishUpdate:function(t,e){this.data&&r.signal(this.data,"update");var i=this.widget&&this.widget.picked||e&&this.options.completeSingle;this.widget&&this.widget.close(),this.data=t,t&&t.list.length&&(i&&t.list.length==1?this.pick(t,0):(this.widget=new B(this,t),r.signal(t,"shown")))}};function Q(t,e,i){var n=t.options.hintOptions,s={};for(var c in U)s[c]=U[c];if(n)for(var c in n)n[c]!==void 0&&(s[c]=n[c]);if(i)for(var c in i)i[c]!==void 0&&(s[c]=i[c]);return s.hint.resolve&&(s.hint=s.hint.resolve(t,e)),s}function R(t){return typeof t=="string"?t:t.text}function Z(t,e){var i={Up:function(){e.moveFocus(-1)},Down:function(){e.moveFocus(1)},PageUp:function(){e.moveFocus(-e.menuSize()+1,!0)},PageDown:function(){e.moveFocus(e.menuSize()-1,!0)},Home:function(){e.setFocus(0)},End:function(){e.setFocus(e.length-1)},Enter:e.pick,Tab:e.pick,Esc:e.close},n=/Mac/.test(navigator.platform);n&&(i["Ctrl-P"]=function(){e.moveFocus(-1)},i["Ctrl-N"]=function(){e.moveFocus(1)});var s=t.options.customKeys,c=s?{}:i;function o(u,l){var a;typeof l!="string"?a=function(H){return l(H,e)}:i.hasOwnProperty(l)?a=i[l]:a=l,c[u]=a}if(s)for(var f in s)s.hasOwnProperty(f)&&o(f,s[f]);var h=t.options.extraKeys;if(h)for(var f in h)h.hasOwnProperty(f)&&o(f,h[f]);return c}function _(t,e){for(;e&&e!=t;){if(e.nodeName.toUpperCase()==="LI"&&e.parentNode==t)return e;e=e.parentNode}}function B(t,e){this.id="cm-complete-"+Math.floor(Math.random(1e6)),this.completion=t,this.data=e,this.picked=!1;var i=this,n=t.cm,s=n.getInputField().ownerDocument,c=s.defaultView||s.parentWindow,o=this.hints=s.createElement("ul");o.setAttribute("role","listbox"),o.setAttribute("aria-expanded","true"),o.id=this.id;var f=t.cm.options.theme;o.className="CodeMirror-hints "+f,this.selectedHint=e.selectedHint||0;for(var h=e.list,u=0;u<h.length;++u){var l=o.appendChild(s.createElement("li")),a=h[u],H=y+(u!=this.selectedHint?"":" "+v);a.className!=null&&(H=a.className+" "+H),l.className=H,u==this.selectedHint&&l.setAttribute("aria-selected","true"),l.id=this.id+"-"+u,l.setAttribute("role","option"),a.render?a.render(l,e,a):l.appendChild(s.createTextNode(a.displayText||R(a))),l.hintId=u}var b=t.options.container||s.body,m=n.cursorCoords(t.options.alignWithWord?e.from:null),x=m.left,T=m.bottom,D=!0,k=0,O=0;if(b!==s.body){var it=["absolute","relative","fixed"].indexOf(c.getComputedStyle(b).position)!==-1,I=it?b:b.offsetParent,j=I.getBoundingClientRect(),M=s.body.getBoundingClientRect();k=j.left-M.left-I.scrollLeft,O=j.top-M.top-I.scrollTop}o.style.left=x-k+"px",o.style.top=T-O+"px";var F=c.innerWidth||Math.max(s.body.offsetWidth,s.documentElement.offsetWidth),W=c.innerHeight||Math.max(s.body.offsetHeight,s.documentElement.offsetHeight);b.appendChild(o),n.getInputField().setAttribute("aria-autocomplete","list"),n.getInputField().setAttribute("aria-owns",this.id),n.getInputField().setAttribute("aria-activedescendant",this.id+"-"+this.selectedHint);var g=t.options.moveOnOverlap?o.getBoundingClientRect():new DOMRect,z=t.options.paddingForScrollbar?o.scrollHeight>o.clientHeight+1:!1,A;setTimeout(function(){A=n.getScrollInfo()});var nt=g.bottom-W;if(nt>0){var L=g.bottom-g.top,st=m.top-(m.bottom-g.top);if(st-L>0)o.style.top=(T=m.top-L-O)+"px",D=!1;else if(L>W){o.style.height=W-5+"px",o.style.top=(T=m.bottom-g.top-O)+"px";var q=n.getCursor();e.from.ch!=q.ch&&(m=n.cursorCoords(q),o.style.left=(x=m.left-k)+"px",g=o.getBoundingClientRect())}}var E=g.right-F;if(z&&(E+=n.display.nativeBarWidth),E>0&&(g.right-g.left>F&&(o.style.width=F-5+"px",E-=g.right-g.left-F),o.style.left=(x=m.left-E-k)+"px"),z)for(var N=o.firstChild;N;N=N.nextSibling)N.style.paddingRight=n.display.nativeBarWidth+"px";if(n.addKeyMap(this.keyMap=Z(t,{moveFocus:function(p,d){i.changeActive(i.selectedHint+p,d)},setFocus:function(p){i.changeActive(p)},menuSize:function(){return i.screenAmount()},length:h.length,close:function(){t.close()},pick:function(){i.pick()},data:e})),t.options.closeOnUnfocus){var V;n.on("blur",this.onBlur=function(){V=setTimeout(function(){t.close()},100)}),n.on("focus",this.onFocus=function(){clearTimeout(V)})}n.on("scroll",this.onScroll=function(){var p=n.getScrollInfo(),d=n.getWrapperElement().getBoundingClientRect();A||(A=n.getScrollInfo());var $=T+A.top-p.top,P=$-(c.pageYOffset||(s.documentElement||s.body).scrollTop);if(D||(P+=o.offsetHeight),P<=d.top||P>=d.bottom)return t.close();o.style.top=$+"px",o.style.left=x+A.left-p.left+"px"}),r.on(o,"dblclick",function(p){var d=_(o,p.target||p.srcElement);d&&d.hintId!=null&&(i.changeActive(d.hintId),i.pick())}),r.on(o,"click",function(p){var d=_(o,p.target||p.srcElement);d&&d.hintId!=null&&(i.changeActive(d.hintId),t.options.completeOnSingleClick&&i.pick())}),r.on(o,"mousedown",function(){setTimeout(function(){n.focus()},20)});var Y=this.getSelectedHintRange();return(Y.from!==0||Y.to!==0)&&this.scrollToActive(),r.signal(e,"select",h[this.selectedHint],o.childNodes[this.selectedHint]),!0}B.prototype={close:function(){if(this.completion.widget==this){this.completion.widget=null,this.hints.parentNode&&this.hints.parentNode.removeChild(this.hints),this.completion.cm.removeKeyMap(this.keyMap);var t=this.completion.cm.getInputField();t.removeAttribute("aria-activedescendant"),t.removeAttribute("aria-owns");var e=this.completion.cm;this.completion.options.closeOnUnfocus&&(e.off("blur",this.onBlur),e.off("focus",this.onFocus)),e.off("scroll",this.onScroll)}},disable:function(){this.completion.cm.removeKeyMap(this.keyMap);var t=this;this.keyMap={Enter:function(){t.picked=!0}},this.completion.cm.addKeyMap(this.keyMap)},pick:function(){this.completion.pick(this.data,this.selectedHint)},changeActive:function(t,e){if(t>=this.data.list.length?t=e?this.data.list.length-1:0:t<0&&(t=e?0:this.data.list.length-1),this.selectedHint!=t){var i=this.hints.childNodes[this.selectedHint];i&&(i.className=i.className.replace(" "+v,""),i.removeAttribute("aria-selected")),i=this.hints.childNodes[this.selectedHint=t],i.className+=" "+v,i.setAttribute("aria-selected","true"),this.completion.cm.getInputField().setAttribute("aria-activedescendant",i.id),this.scrollToActive(),r.signal(this.data,"select",this.data.list[this.selectedHint],i)}},scrollToActive:function(){var t=this.getSelectedHintRange(),e=this.hints.childNodes[t.from],i=this.hints.childNodes[t.to],n=this.hints.firstChild;e.offsetTop<this.hints.scrollTop?this.hints.scrollTop=e.offsetTop-n.offsetTop:i.offsetTop+i.offsetHeight>this.hints.scrollTop+this.hints.clientHeight&&(this.hints.scrollTop=i.offsetTop+i.offsetHeight-this.hints.clientHeight+n.offsetTop)},screenAmount:function(){return Math.floor(this.hints.clientHeight/this.hints.firstChild.offsetHeight)||1},getSelectedHintRange:function(){var t=this.completion.options.scrollMargin||0;return{from:Math.max(0,this.selectedHint-t),to:Math.min(this.data.list.length-1,this.selectedHint+t)}}};function tt(t,e){if(!t.somethingSelected())return e;for(var i=[],n=0;n<e.length;n++)e[n].supportsSelection&&i.push(e[n]);return i}function K(t,e,i,n){if(t.async)t(e,n,i);else{var s=t(e,i);s&&s.then?s.then(n):n(s)}}function et(t,e){var i=t.getHelpers(e,"hint"),n;if(i.length){var s=function(c,o,f){var h=tt(c,i);function u(l){if(l==h.length)return o(null);K(h[l],c,f,function(a){a&&a.list.length>0?o(a):u(l+1)})}u(0)};return s.async=!0,s.supportsSelection=!0,s}else return(n=t.getHelper(t.getCursor(),"hintWords"))?function(c){return r.hint.fromList(c,{words:n})}:r.hint.anyword?function(c,o){return r.hint.anyword(c,o)}:function(){}}r.registerHelper("hint","auto",{resolve:et}),r.registerHelper("hint","fromList",function(t,e){var i=t.getCursor(),n=t.getTokenAt(i),s,c=r.Pos(i.line,n.start),o=i;n.start<i.ch&&/\w/.test(n.string.charAt(i.ch-n.start-1))?s=n.string.substr(0,i.ch-n.start):(s="",c=i);for(var f=[],h=0;h<e.words.length;h++){var u=e.words[h];u.slice(0,s.length)==s&&f.push(u)}if(f.length)return{list:f,from:c,to:o}}),r.commands.autocomplete=r.showHint;var U={hint:r.hint.auto,completeSingle:!0,alignWithWord:!0,closeCharacters:/[\s()\[\]{};:>,]/,closeOnPick:!0,closeOnUnfocus:!0,updateOnCursorActivity:!0,completeOnSingleClick:!0,container:null,customKeys:null,extraKeys:null,paddingForScrollbar:!0,moveOnOverlap:!0};r.defineOption("hintOptions",null)})})();var X=lt.exports;const ht=rt(X),ft=ct({__proto__:null,default:ht},[X]);export{ft as s};