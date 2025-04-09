import{_ as h,bv as k,bi as x,A as u,bw as J,h as r,B as a,bx as d,k as _,C as s,t as m,I as v,r as g,H as y}from"./index-Hyq34tSM.js";const T={name:"GraphNode",components:{SVGTask:k,Job:x},props:{task:{type:Object,required:!0},jobs:{type:Array,required:!0},maxJobs:{default:6,required:!1},mostRecentJobScale:{default:1.2,required:!1},jobTheme:{required:!0}},computed:{nodeID(){return`graph-node-${this.task.id}`},startTime(){var o,n,e;return(e=(n=(o=this.jobs)==null?void 0:o[0])==null?void 0:n.node)==null?void 0:e.startedTime},jobsForDisplay(){return this.jobs.slice(0,this.maxJobs)},numOverflowJobs(){return this.jobs.length>this.maxJobs?this.jobs.length-this.maxJobs:0},labelTransform(){return this.jobs.length?"":"translate(0, 20)"},previousJobOffset(){return this.mostRecentJobScale*100-100}}},j={class:"c-graph-node"},p=["transform"],w={x:"130",y:"25","font-size":"45"},S={x:"130",y:"65","font-size":"30"},B={transform:`
        translate(130, 75)
        scale(0.3, 0.3)
      `},D=["transform"],G=["transform"],O={x:"25",y:"75","font-size":"80"};function V(o,n,e,q,N,t){const f=u("SVGTask"),b=u("Job"),l=J("command-menu");return r(),a("g",j,[d(_(f,{task:e.task.node,modifierSize:.5,startTime:t.startTime,viewBox:"-40 -40 140 140",x:"0",y:"0"},null,8,["task","startTime"]),[[l,e.task]]),s("g",{transform:t.labelTransform},[s("text",w,m(e.task.name),1),s("text",S,m(e.task.tokens.cycle),1)],8,p),s("g",B,[(r(!0),a(v,null,g(t.jobsForDisplay,(i,c)=>(r(),a("g",{class:"jobs",key:i.id,transform:`
          translate(${c*100+(c===0?0:t.previousJobOffset)}, 0)
          scale(${c===0?e.mostRecentJobScale:"1"})
        `},[d(_(b,{svg:!0,status:i.node.state,viewBox:"0 0 100 100"},null,8,["status"]),[[l,i]])],8,D))),128)),t.numOverflowJobs?(r(),a("g",{key:0,class:"job-overflow",transform:`
          translate(${e.maxJobs*100+20}, 0)
        `},[s("text",O," +"+m(t.numOverflowJobs),1)],8,G)):y("",!0)])])}const C=h(T,[["render",V]]);export{C as G};
