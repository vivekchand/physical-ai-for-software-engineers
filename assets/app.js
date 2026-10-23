/* Original educational UI. No analytics, accounts, remote scripts, or robot control. */
(() => {
  'use strict';
  const base = document.body.dataset.base || '';
  const key = 'physical-ai-field-guide:v1';
  const getProgress = () => {
    try { const data = JSON.parse(localStorage.getItem(key) || '[]'); return new Set(Array.isArray(data) ? data.filter(x => Number.isInteger(x) && x >= 1 && x <= 21) : []); }
    catch { return new Set(); }
  };
  let complete = getProgress();
  function paintProgress() {
    document.querySelectorAll('[data-progress-label]').forEach(el => { el.textContent = `${complete.size} / 21`; });
    document.querySelectorAll('[data-progress]').forEach(el => { el.value = complete.size; });
    document.querySelectorAll('[data-day-link]').forEach(el => { el.querySelector('.nav-check').textContent = complete.has(Number(el.dataset.dayLink)) ? '✓' : ''; });
    document.querySelectorAll('[data-course-day]').forEach(el => { el.classList.toggle('week-complete', complete.has(Number(el.dataset.courseDay))); });
    document.querySelectorAll('[data-complete]').forEach(el => { const done = complete.has(Number(el.dataset.complete)); el.setAttribute('aria-pressed', String(done)); el.textContent = done ? 'Completed ✓ · Undo' : 'Mark day complete'; });
    const next = Array.from({length:21}, (_, i) => i + 1).find(day => !complete.has(day));
    const link = next && document.querySelector(`[data-day-link="${next}"]`);
    const start = document.querySelector('[data-start]');
    if (complete.size && start && link) { start.href = link.href; start.textContent = `Continue with day ${String(next).padStart(2,'0')} →`; }
  }
  paintProgress();
  document.querySelectorAll('[data-complete]').forEach(el => el.addEventListener('click', () => {
    const day = Number(el.dataset.complete);
    complete.has(day) ? complete.delete(day) : complete.add(day);
    try { localStorage.setItem(key, JSON.stringify([...complete])); } catch { /* Browsing remains available when storage is disabled. */ }
    paintProgress();
  }));
  window.addEventListener('storage', event => { if(event.key === key) { complete = getProgress(); paintProgress(); } });
  const menu = document.querySelector('.menu-toggle');
  const sidebar = document.querySelector('.sidebar');
  function closeMenu(){sidebar.classList.remove('is-open');menu.setAttribute('aria-expanded','false');}
  menu.addEventListener('click', () => { const open = sidebar.classList.toggle('is-open'); menu.setAttribute('aria-expanded',String(open)); });
  document.addEventListener('click', e => { if(!sidebar.contains(e.target) && !menu.contains(e.target)) closeMenu(); });
  document.addEventListener('keydown', e => {if(e.key === 'Escape') closeMenu();});

  const dialog = document.querySelector('#search-dialog');
  const input = document.querySelector('#search-input');
  const results = document.querySelector('.search-results');
  const status = document.querySelector('.search-status');
  let index = null;
  let loading = null;
  async function loadIndex() {
    if(index) return index;
    if(!loading) loading = fetch(`${base}/search-index.json`).then(response => { if(!response.ok) throw new Error('Search unavailable'); return response.json(); }).then(data => {index=data;return data;}).catch(() => {loading=null; throw new Error('Search unavailable');});
    return loading;
  }
  async function search(){
    const query = input.value.trim().toLowerCase();
    results.replaceChildren();
    if(!query){status.textContent='Search all 21 days and field notes.';return;}
    let pages;
    try { pages = await loadIndex(); } catch {status.textContent='Search could not load. You can still browse every lesson in the course navigation.';return;}
    if(query !== input.value.trim().toLowerCase()) return;
    const terms = query.split(/\s+/);
    const found = pages.map(page => ({...page,score:terms.reduce((score,term)=>score+(page.title.toLowerCase().includes(term)?8:0)+(page.text.toLowerCase().includes(term)?1:0),0)})).filter(page=>terms.every(term=>(page.title+' '+page.text).toLowerCase().includes(term))).sort((a,b)=>b.score-a.score).slice(0,12);
    status.textContent = found.length ? `${found.length} matching pages` : 'No matches. Try “control”, “Isaac”, or “ROS”.';
    found.forEach(page=>{
      const a=document.createElement('a');a.href=page.url;
      const label=document.createElement('small');label.textContent=page.day ? `DAY ${String(page.day).padStart(2,'0')}` : 'FIELD NOTES';
      const title=document.createElement('strong');title.textContent=page.title;
      const br=document.createElement('br');
      const excerpt=document.createElement('p');const at=page.text.toLowerCase().indexOf(terms[0]);const start=Math.max(0,at-55);excerpt.textContent=(start?'…':'')+page.text.slice(start,start+180)+'…';
      a.append(label,br,title,excerpt);results.append(a);
    });
  }
  document.querySelector('.search-trigger').addEventListener('click',()=>{dialog.showModal();input.focus();});
  document.querySelector('.search-close').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
  input.addEventListener('input',search);
  document.addEventListener('keydown',e=>{if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();if(!dialog.open){dialog.showModal();input.focus();}else dialog.close();}});

  // A one-dimensional toy plant, not an Isaac or hardware simulation.
  const lab=document.querySelector('[data-control-lab]');
  if(lab){
    const gain=lab.querySelector('[name="gain"]'), delay=lab.querySelector('[name="delay"]');
    const draw=()=>{
      const k=Number(gain.value), lag=Number(delay.value), dt=.05, target=1, count=160;
      let x=0,v=0;const history=[0];let max=0;
      for(let i=0;i<count;i++){
        const measured=history[Math.max(0,history.length-1-lag)];
        const u=Math.max(-2,Math.min(2,k*(target-measured)-.8*v));
        const disturbance=i>=65&&i<75 ? -1.5 : 0;
        v+=(u-.2*v+disturbance)*dt;x+=v*dt;history.push(x);max=Math.max(max,x);
      }
      const low=Math.min(0,...history)-.1,high=Math.max(1.2,...history)+.1;
      const y=value=>230-(value-low)/(high-low)*200;
      const points=history.slice(1).map((value,i)=>`${(40+(i+1)*3.2).toFixed(1)},${y(value).toFixed(1)}`);
      lab.querySelector('[data-response]').setAttribute('points',points.join(' '));
      lab.querySelector('[data-target-line]').setAttribute('d',`M40 ${y(target)}H555`);
      lab.querySelector('[data-target-label]').setAttribute('y',String(y(target)-8));
      lab.querySelector('[data-gain-label]').textContent=k.toFixed(1);
      lab.querySelector('[data-delay-label]').textContent=`${(lag*dt*1000).toFixed(0)} ms`;
      lab.querySelector('[data-metrics]').textContent=`Final error: ${(target-x).toFixed(3)} m · Peak overshoot: ${Math.max(0,max-target).toFixed(3)} m · Disturbance: 3.25–3.75 s`;
    };
    gain.addEventListener('input',draw);delay.addEventListener('input',draw);draw();
  }
})();
