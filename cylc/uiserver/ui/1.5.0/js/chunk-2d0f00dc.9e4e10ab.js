(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d0f00dc"],{"9b74":function(t,e,i){(function(t){t(i("56b3"))})((function(t){"use strict";var e="CodeMirror-hint",i="CodeMirror-hint-active";function n(t,e){if(this.cm=t,this.options=e,this.widget=null,this.debounce=0,this.tick=0,this.startPos=this.cm.getCursor("start"),this.startLen=this.cm.getLine(this.startPos.line).length-this.cm.getSelection().length,this.options.updateOnCursorActivity){var i=this;t.on("cursorActivity",this.activityFunc=function(){i.cursorActivity()})}}t.showHint=function(t,e,i){if(!e)return t.showHint(i);i&&i.async&&(e.async=!0);var n={hint:e};if(i)for(var o in i)n[o]=i[o];return t.showHint(n)},t.defineExtension("showHint",(function(e){e=c(this,this.getCursor("start"),e);var i=this.listSelections();if(!(i.length>1)){if(this.somethingSelected()){if(!e.hint.supportsSelection)return;for(var o=0;o<i.length;o++)if(i[o].head.line!=i[o].anchor.line)return}this.state.completionActive&&this.state.completionActive.close();var s=this.state.completionActive=new n(this,e);s.options.hint&&(t.signal(this,"startCompletion",this),s.update(!0))}})),t.defineExtension("closeHint",(function(){this.state.completionActive&&this.state.completionActive.close()}));var o=window.requestAnimationFrame||function(t){return setTimeout(t,1e3/60)},s=window.cancelAnimationFrame||clearTimeout;function c(t,e,i){var n=t.options.hintOptions,o={};for(var s in p)o[s]=p[s];if(n)for(var s in n)void 0!==n[s]&&(o[s]=n[s]);if(i)for(var s in i)void 0!==i[s]&&(o[s]=i[s]);return o.hint.resolve&&(o.hint=o.hint.resolve(t,e)),o}function r(t){return"string"==typeof t?t:t.text}function l(t,e){var i={Up:function(){e.moveFocus(-1)},Down:function(){e.moveFocus(1)},PageUp:function(){e.moveFocus(1-e.menuSize(),!0)},PageDown:function(){e.moveFocus(e.menuSize()-1,!0)},Home:function(){e.setFocus(0)},End:function(){e.setFocus(e.length-1)},Enter:e.pick,Tab:e.pick,Esc:e.close},n=/Mac/.test(navigator.platform);n&&(i["Ctrl-P"]=function(){e.moveFocus(-1)},i["Ctrl-N"]=function(){e.moveFocus(1)});var o=t.options.customKeys,s=o?{}:i;function c(t,n){var o;o="string"!=typeof n?function(t){return n(t,e)}:i.hasOwnProperty(n)?i[n]:n,s[t]=o}if(o)for(var r in o)o.hasOwnProperty(r)&&c(r,o[r]);var l=t.options.extraKeys;if(l)for(var r in l)l.hasOwnProperty(r)&&c(r,l[r]);return s}function h(t,e){while(e&&e!=t){if("LI"===e.nodeName.toUpperCase()&&e.parentNode==t)return e;e=e.parentNode}}function a(n,o){this.id="cm-complete-"+Math.floor(Math.random(1e6)),this.completion=n,this.data=o,this.picked=!1;var s=this,c=n.cm,a=c.getInputField().ownerDocument,u=a.defaultView||a.parentWindow,d=this.hints=a.createElement("ul");d.setAttribute("role","listbox"),d.setAttribute("aria-expanded","true"),d.id=this.id;var f=n.cm.options.theme;d.className="CodeMirror-hints "+f,this.selectedHint=o.selectedHint||0;for(var p=o.list,m=0;m<p.length;++m){var g=d.appendChild(a.createElement("li")),v=p[m],y=e+(m!=this.selectedHint?"":" "+i);null!=v.className&&(y=v.className+" "+y),g.className=y,m==this.selectedHint&&g.setAttribute("aria-selected","true"),g.id=this.id+"-"+m,g.setAttribute("role","option"),v.render?v.render(g,o,v):g.appendChild(a.createTextNode(v.displayText||r(v))),g.hintId=m}var w=n.options.container||a.body,b=c.cursorCoords(n.options.alignWithWord?o.from:null),A=b.left,H=b.bottom,C=!0,k=0,x=0;if(w!==a.body){var S=-1!==["absolute","relative","fixed"].indexOf(u.getComputedStyle(w).position),T=S?w:w.offsetParent,F=T.getBoundingClientRect(),M=a.body.getBoundingClientRect();k=F.left-M.left-T.scrollLeft,x=F.top-M.top-T.scrollTop}d.style.left=A-k+"px",d.style.top=H-x+"px";var O=u.innerWidth||Math.max(a.body.offsetWidth,a.documentElement.offsetWidth),N=u.innerHeight||Math.max(a.body.offsetHeight,a.documentElement.offsetHeight);w.appendChild(d),c.getInputField().setAttribute("aria-autocomplete","list"),c.getInputField().setAttribute("aria-owns",this.id),c.getInputField().setAttribute("aria-activedescendant",this.id+"-"+this.selectedHint);var I,P=n.options.moveOnOverlap?d.getBoundingClientRect():new DOMRect,E=!!n.options.paddingForScrollbar&&d.scrollHeight>d.clientHeight+1;setTimeout((function(){I=c.getScrollInfo()}));var W=P.bottom-N;if(W>0){var R=P.bottom-P.top,B=b.top-(b.bottom-P.top);if(B-R>0)d.style.top=(H=b.top-R-x)+"px",C=!1;else if(R>N){d.style.height=N-5+"px",d.style.top=(H=b.bottom-P.top-x)+"px";var K=c.getCursor();o.from.ch!=K.ch&&(b=c.cursorCoords(K),d.style.left=(A=b.left-k)+"px",P=d.getBoundingClientRect())}}var L,U=P.right-O;if(E&&(U+=c.display.nativeBarWidth),U>0&&(P.right-P.left>O&&(d.style.width=O-5+"px",U-=P.right-P.left-O),d.style.left=(A=Math.max(b.left-U-k,0))+"px"),E)for(var D=d.firstChild;D;D=D.nextSibling)D.style.paddingRight=c.display.nativeBarWidth+"px";(c.addKeyMap(this.keyMap=l(n,{moveFocus:function(t,e){s.changeActive(s.selectedHint+t,e)},setFocus:function(t){s.changeActive(t)},menuSize:function(){return s.screenAmount()},length:p.length,close:function(){n.close()},pick:function(){s.pick()},data:o})),n.options.closeOnUnfocus)&&(c.on("blur",this.onBlur=function(){L=setTimeout((function(){n.close()}),100)}),c.on("focus",this.onFocus=function(){clearTimeout(L)}));c.on("scroll",this.onScroll=function(){var t=c.getScrollInfo(),e=c.getWrapperElement().getBoundingClientRect();I||(I=c.getScrollInfo());var i=H+I.top-t.top,o=i-(u.pageYOffset||(a.documentElement||a.body).scrollTop);if(C||(o+=d.offsetHeight),o<=e.top||o>=e.bottom)return n.close();d.style.top=i+"px",d.style.left=A+I.left-t.left+"px"}),t.on(d,"dblclick",(function(t){var e=h(d,t.target||t.srcElement);e&&null!=e.hintId&&(s.changeActive(e.hintId),s.pick())})),t.on(d,"click",(function(t){var e=h(d,t.target||t.srcElement);e&&null!=e.hintId&&(s.changeActive(e.hintId),n.options.completeOnSingleClick&&s.pick())})),t.on(d,"mousedown",(function(){setTimeout((function(){c.focus()}),20)}));var z=this.getSelectedHintRange();return 0===z.from&&0===z.to||this.scrollToActive(),t.signal(o,"select",p[this.selectedHint],d.childNodes[this.selectedHint]),!0}function u(t,e){if(!t.somethingSelected())return e;for(var i=[],n=0;n<e.length;n++)e[n].supportsSelection&&i.push(e[n]);return i}function d(t,e,i,n){if(t.async)t(e,n,i);else{var o=t(e,i);o&&o.then?o.then(n):n(o)}}function f(e,i){var n,o=e.getHelpers(i,"hint");if(o.length){var s=function(t,e,i){var n=u(t,o);function s(o){if(o==n.length)return e(null);d(n[o],t,i,(function(t){t&&t.list.length>0?e(t):s(o+1)}))}s(0)};return s.async=!0,s.supportsSelection=!0,s}return(n=e.getHelper(e.getCursor(),"hintWords"))?function(e){return t.hint.fromList(e,{words:n})}:t.hint.anyword?function(e,i){return t.hint.anyword(e,i)}:function(){}}n.prototype={close:function(){this.active()&&(this.cm.state.completionActive=null,this.tick=null,this.options.updateOnCursorActivity&&this.cm.off("cursorActivity",this.activityFunc),this.widget&&this.data&&t.signal(this.data,"close"),this.widget&&this.widget.close(),t.signal(this.cm,"endCompletion",this.cm))},active:function(){return this.cm.state.completionActive==this},pick:function(e,i){var n=e.list[i],o=this;this.cm.operation((function(){n.hint?n.hint(o.cm,e,n):o.cm.replaceRange(r(n),n.from||e.from,n.to||e.to,"complete"),t.signal(e,"pick",n),o.cm.scrollIntoView()})),this.options.closeOnPick&&this.close()},cursorActivity:function(){this.debounce&&(s(this.debounce),this.debounce=0);var t=this.startPos;this.data&&(t=this.data.from);var e=this.cm.getCursor(),i=this.cm.getLine(e.line);if(e.line!=this.startPos.line||i.length-e.ch!=this.startLen-this.startPos.ch||e.ch<t.ch||this.cm.somethingSelected()||!e.ch||this.options.closeCharacters.test(i.charAt(e.ch-1)))this.close();else{var n=this;this.debounce=o((function(){n.update()})),this.widget&&this.widget.disable()}},update:function(t){if(null!=this.tick){var e=this,i=++this.tick;d(this.options.hint,this.cm,this.options,(function(n){e.tick==i&&e.finishUpdate(n,t)}))}},finishUpdate:function(e,i){this.data&&t.signal(this.data,"update");var n=this.widget&&this.widget.picked||i&&this.options.completeSingle;this.widget&&this.widget.close(),this.data=e,e&&e.list.length&&(n&&1==e.list.length?this.pick(e,0):(this.widget=new a(this,e),t.signal(e,"shown")))}},a.prototype={close:function(){if(this.completion.widget==this){this.completion.widget=null,this.hints.parentNode&&this.hints.parentNode.removeChild(this.hints),this.completion.cm.removeKeyMap(this.keyMap);var t=this.completion.cm.getInputField();t.removeAttribute("aria-activedescendant"),t.removeAttribute("aria-owns");var e=this.completion.cm;this.completion.options.closeOnUnfocus&&(e.off("blur",this.onBlur),e.off("focus",this.onFocus)),e.off("scroll",this.onScroll)}},disable:function(){this.completion.cm.removeKeyMap(this.keyMap);var t=this;this.keyMap={Enter:function(){t.picked=!0}},this.completion.cm.addKeyMap(this.keyMap)},pick:function(){this.completion.pick(this.data,this.selectedHint)},changeActive:function(e,n){if(e>=this.data.list.length?e=n?this.data.list.length-1:0:e<0&&(e=n?0:this.data.list.length-1),this.selectedHint!=e){var o=this.hints.childNodes[this.selectedHint];o&&(o.className=o.className.replace(" "+i,""),o.removeAttribute("aria-selected")),o=this.hints.childNodes[this.selectedHint=e],o.className+=" "+i,o.setAttribute("aria-selected","true"),this.completion.cm.getInputField().setAttribute("aria-activedescendant",o.id),this.scrollToActive(),t.signal(this.data,"select",this.data.list[this.selectedHint],o)}},scrollToActive:function(){var t=this.getSelectedHintRange(),e=this.hints.childNodes[t.from],i=this.hints.childNodes[t.to],n=this.hints.firstChild;e.offsetTop<this.hints.scrollTop?this.hints.scrollTop=e.offsetTop-n.offsetTop:i.offsetTop+i.offsetHeight>this.hints.scrollTop+this.hints.clientHeight&&(this.hints.scrollTop=i.offsetTop+i.offsetHeight-this.hints.clientHeight+n.offsetTop)},screenAmount:function(){return Math.floor(this.hints.clientHeight/this.hints.firstChild.offsetHeight)||1},getSelectedHintRange:function(){var t=this.completion.options.scrollMargin||0;return{from:Math.max(0,this.selectedHint-t),to:Math.min(this.data.list.length-1,this.selectedHint+t)}}},t.registerHelper("hint","auto",{resolve:f}),t.registerHelper("hint","fromList",(function(e,i){var n,o=e.getCursor(),s=e.getTokenAt(o),c=t.Pos(o.line,s.start),r=o;s.start<o.ch&&/\w/.test(s.string.charAt(o.ch-s.start-1))?n=s.string.substr(0,o.ch-s.start):(n="",c=o);for(var l=[],h=0;h<i.words.length;h++){var a=i.words[h];a.slice(0,n.length)==n&&l.push(a)}if(l.length)return{list:l,from:c,to:r}})),t.commands.autocomplete=t.showHint;var p={hint:t.hint.auto,completeSingle:!0,alignWithWord:!0,closeCharacters:/[\s()\[\]{};:>,]/,closeOnPick:!0,closeOnUnfocus:!0,updateOnCursorActivity:!0,completeOnSingleClick:!0,container:null,customKeys:null,extraKeys:null,paddingForScrollbar:!0,moveOnOverlap:!0};t.defineOption("hintOptions",null)}))}}]);