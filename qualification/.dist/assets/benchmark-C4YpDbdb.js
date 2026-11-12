import{a as e,i as t,n,o as r,r as i,s as a,t as o}from"./harness-DgGDAWZq.js";var s=`{
  "fixture_version": "1",
  "nodes": [
    {"id": "FIX-N-0000", "record_type": "PERSON_RECORD", "label": "Fixture record 0000", "x": 80, "y": 80},
    {"id": "FIX-N-0001", "record_type": "ORGANIZATION_RECORD", "label": "Fixture record 0001", "x": 200, "y": 80},
    {"id": "FIX-N-0002", "record_type": "ORGANIZATION_RECORD", "label": "Fixture record 0002", "x": 320, "y": 80},
    {"id": "FIX-N-0003", "record_type": "PERSON_RECORD", "label": "Fixture record 0003", "x": 440, "y": 80}
  ],
  "edges": [
    {"id": "FIX-E-0000", "source_id": "FIX-N-0000", "target_id": "FIX-N-0001", "relationship_family": "DIRECT_SOURCE", "relationship_type": "RELATED_TO", "directed": true},
    {"id": "FIX-E-0001", "source_id": "FIX-N-0001", "target_id": "FIX-N-0002", "relationship_family": "DIRECT_SOURCE", "relationship_type": "RELATED_TO", "directed": true},
    {"id": "FIX-E-0002", "source_id": "FIX-N-0002", "target_id": "FIX-N-0003", "relationship_family": "DIRECT_SOURCE", "relationship_type": "RELATED_TO", "directed": true}
  ]
}
`,c=[r,i,e,t],l=a.nodes.map(e=>({id:e.id,recordType:e.record_type,label:e.label,x:e.x,y:e.y})),u=a.edges.map(e=>({id:e.id,sourceId:e.source_id,targetId:e.target_id,relationshipFamily:e.relationship_family,relationshipType:e.relationship_type,directed:e.directed})),d=document.querySelector(`#output`),f=document.querySelector(`#stage`);function p(e){if(!f)throw Error(`benchmark stage is missing`);let t=document.createElement(`div`);t.className=`candidate-stage`,t.style.width=`900px`,t.style.height=`500px`,f.replaceChildren(t);let r=[n(e,t,l,u,1,`A_RENDERER`),n(e,t,l,u,2,`B_SOLUTION`)];return o(e,l,u,r)}async function m(e){let t=await crypto.subtle.digest(`SHA-256`,new TextEncoder().encode(e));return[...new Uint8Array(t)].map(e=>e.toString(16).padStart(2,`0`)).join(``)}async function h(){let e=c.map(p),t=e.reduce((e,t)=>e+t.runs.reduce((e,t)=>e+t.measurements.callbackEvents,0),0),n={fixture_sha256:await m(s),environment:{browser:navigator.userAgent,os:`browser-host-not-exposed`,viewport:`${innerWidth}x${innerHeight}`,node_version:`browser-runner-not-applicable`},candidates:e,selection_events:t,status:`RAW_MEASUREMENTS_NOT_QUALIFIED`,interaction_status:t>0?`AUTOMATED_SELECTION_PROBES_EXECUTED`:`SELECTION_PROBES_FAILED`};d&&(d.textContent=JSON.stringify(n,null,2))}document.querySelector(`#run`)?.addEventListener(`click`,h),document.querySelector(`#download`)?.addEventListener(`click`,()=>{if(!d?.textContent)return;let e=new Blob([d.textContent],{type:`application/json`}),t=document.createElement(`a`);t.href=URL.createObjectURL(e),t.download=`fga06-renderer-raw-measurements.json`,t.click(),URL.revokeObjectURL(t.href)});