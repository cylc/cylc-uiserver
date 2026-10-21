import{Ft as e,Lt as t,R as n,dt as r,l as i,p as a,u as o,w as s,yt as c}from"./runtime-core.esm-bundler-CilEyzAc.js";import{i as l}from"./TaskState.model-DKp67352.js";var u={class:`status`},d={transform:`rotate(-90, 50, 50)`},f=[`transform`],p={__name:`SVGTask`,props:{task:{required:!0},startTime:{type:String,required:!1},modifierSize:{type:Number,default:.7}},setup(p){let m=p,h=s(`animResetTime`,()=>r(0),!0),g=i(()=>m.task.isHeld?`held`:m.task.isRunahead?`runahead`:m.task.runtime?.runMode===`Skip`?`skip`:m.task.isQueued?`queued`:m.task.isRetry?`retry`:m.task.isWallclock?`wallclock`:m.task.isXtriggered?`xtriggered`:``),_=i(()=>{if(m.task.state===l.RUNNING.name&&m.startTime&&m.task.task?.meanElapsedTime){let e=Math.max(Date.now(),h.value)-Date.parse(m.startTime);return{animationDuration:`${m.task.task.meanElapsedTime}s`,animationDelay:`-${e}ms`,animationFillMode:`forwards`}}return{}});function v(){let e=-(35.35*m.modifierSize+42.42);return`
    scale(${m.modifierSize}, ${m.modifierSize})
    translate(${e}, ${e})
  `}let y=v();return(r,i)=>(n(),a(`g`,{class:e([`c8-task`,[p.task.state,g.value]])},[o(`g`,u,[i[0]||=o(`circle`,{class:`outline`,cx:`50`,cy:`50`,r:`45`,"stroke-width":`10`},null,-1),o(`g`,d,[o(`circle`,{class:`progress`,cx:`50`,cy:`50`,r:`16`,"stroke-width":`50`,"stroke-dasharray":`157`,style:t(_.value)},null,4)]),i[1]||=o(`circle`,{class:`dot`,cx:`50`,cy:`50`,r:`7`},null,-1),i[2]||=o(`circle`,{class:`hub`,cx:`50`,cy:`50`,r:`16`},null,-1),i[3]||=o(`path`,{class:`cross`,d:`
          m30,30
          l40 40
          m0,-40
          l-40 40
        `},null,-1),i[4]||=o(`path`,{class:`clockhands_big`,d:`
          m50,12
          l0 38
          l18 18
        `},null,-1)]),o(`g`,{class:`modifier`,transform:c(y)},[...i[5]||=[o(`circle`,{class:`outline`,cx:`50`,cy:`50`,r:`40`,"stroke-width":`10`},null,-1),o(`g`,{class:`held`},[o(`path`,{d:`
            m37,33
            l0 34
            m25,0
            l0, -34
          `})],-1),o(`g`,{class:`runahead`},[o(`circle`,{cx:`50`,cy:`50`,r:`20`})],-1),o(`g`,{class:`skip`},[o(`path`,{class:`skip`,d:`M 5 15 v 70 l 43 -35 M 50 15 v 70 l 43 -35`})],-1),o(`g`,{class:`queued`},[o(`path`,{d:`
            m28,28
            l43 0
            m-43,21
            l43, 0
            m-43,21
            l43 0
          `})],-1),o(`g`,{class:`xtriggered`},[o(`path`,{d:`
            m10,70
            a60, 60, 0, 0, 1, 60, -60
            m-40, 60
            a40, 40 0, 0, 1, 40, -40
            m-6, 27
            a9,9, 0, 1, 0, .1, 0
            m0, 4
            a6,6, 0, 1, 0, .1, 0
          `})],-1),o(`g`,{class:`retry`},[o(`path`,{d:`m25, 50 a30 30 1 1 1 25 30 `}),o(`polygon`,{points:`0,40 26,75 52,40, 25,46`})],-1),o(`g`,{class:`wallclock`},[o(`path`,{d:`
            m50, 18
            l0, 36
            l14, 14
            l3,3
            l3,-3
            l-18, -18
          `})],-1)]],8,f)],2))}};export{p as t};