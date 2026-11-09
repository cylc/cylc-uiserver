import{J as e,On as t,Zn as n,_ as r,b as i,er as a,g as o,mt as s,vn as c}from"./runtime-core.esm-bundler-DZo3dYLJ.js";import{i as l}from"./TaskState.model-CU16xqA6.js";var u={class:`status`},d={transform:`rotate(-90, 50, 50)`},f=[`transform`],p={__name:`SVGTask`,props:{task:{required:!0},startTime:{type:String,required:!1},modifierSize:{type:Number,default:.7}},setup(p){let m=p,h=e(`animResetTime`,()=>c(0),!0),g=o(()=>m.task.isHeld?`held`:m.task.isRunahead?`runahead`:m.task.runtime?.runMode===`Skip`?`skip`:m.task.isQueued?`queued`:m.task.isRetry?`retry`:m.task.isWallclock?`wallclock`:m.task.isXtriggered?`xtriggered`:``),_=o(()=>{if(m.task.state===l.RUNNING.name&&m.startTime&&m.task.task?.meanElapsedTime){let e=Math.max(Date.now(),h.value)-Date.parse(m.startTime);return{animationDuration:`${m.task.task.meanElapsedTime}s`,animationDelay:`-${e}ms`,animationFillMode:`forwards`}}return{}});function v(){let e=-(35.35*m.modifierSize+42.42);return`
    scale(${m.modifierSize}, ${m.modifierSize})
    translate(${e}, ${e})
  `}let y=v();return(e,o)=>(s(),i(`g`,{class:n([`c8-task`,[p.task.state,g.value]])},[r(`g`,u,[o[0]||=r(`circle`,{class:`outline`,cx:`50`,cy:`50`,r:`45`,"stroke-width":`10`},null,-1),r(`g`,d,[r(`circle`,{class:`progress`,cx:`50`,cy:`50`,r:`16`,"stroke-width":`50`,"stroke-dasharray":`157`,style:a(_.value)},null,4)]),o[1]||=r(`circle`,{class:`dot`,cx:`50`,cy:`50`,r:`7`},null,-1),o[2]||=r(`circle`,{class:`hub`,cx:`50`,cy:`50`,r:`16`},null,-1),o[3]||=r(`path`,{class:`cross`,d:`
          m30,30
          l40 40
          m0,-40
          l-40 40
        `},null,-1),o[4]||=r(`path`,{class:`clockhands_big`,d:`
          m50,12
          l0 38
          l18 18
        `},null,-1)]),r(`g`,{class:`modifier`,transform:t(y)},[...o[5]||=[r(`circle`,{class:`outline`,cx:`50`,cy:`50`,r:`40`,"stroke-width":`10`},null,-1),r(`g`,{class:`held`},[r(`path`,{d:`
            m37,33
            l0 34
            m25,0
            l0, -34
          `})],-1),r(`g`,{class:`runahead`},[r(`circle`,{cx:`50`,cy:`50`,r:`20`})],-1),r(`g`,{class:`skip`},[r(`path`,{class:`skip`,d:`M 5 15 v 70 l 43 -35 M 50 15 v 70 l 43 -35`})],-1),r(`g`,{class:`queued`},[r(`path`,{d:`
            m28,28
            l43 0
            m-43,21
            l43, 0
            m-43,21
            l43 0
          `})],-1),r(`g`,{class:`xtriggered`},[r(`path`,{d:`
            m10,70
            a60, 60, 0, 0, 1, 60, -60
            m-40, 60
            a40, 40 0, 0, 1, 40, -40
            m-6, 27
            a9,9, 0, 1, 0, .1, 0
            m0, 4
            a6,6, 0, 1, 0, .1, 0
          `})],-1),r(`g`,{class:`retry`},[r(`path`,{d:`m25, 50 a30 30 1 1 1 25 30 `}),r(`polygon`,{points:`0,40 26,75 52,40, 25,46`})],-1),r(`g`,{class:`wallclock`},[r(`path`,{d:`
            m50, 18
            l0, 36
            l14, 14
            l3,3
            l3,-3
            l-18, -18
          `})],-1)]],8,f)],2))}};export{p as t};