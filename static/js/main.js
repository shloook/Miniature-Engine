async function postCheck(text){
  const res = await fetch('/api/check', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  if (!res.ok) {
    const err = await res.json().catch(()=>({error:'unknown'}));
    throw new Error(err.error || 'Server error');
  }
  return res.json();
}

function escapeHtml(unsafe) {
  return unsafe.replace(/[&<>"'`]/g, function(m) { return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;","`":"&#96;"})[m]; });
}

document.getElementById('checkBtn').addEventListener('click', async ()=>{
  try {
    const txt = document.getElementById('inputText').value;
    const out = await postCheck(txt);

    // render misspellings
    const mdiv = document.getElementById('misspellings');
    mdiv.innerHTML = '';
    out.words.forEach(w=>{
      const el = document.createElement('div');
      el.className = 'miss';
      const suggs = w.suggestions && w.suggestions.length ? w.suggestions.map(s=>`<button class=\"suggest-btn\" data-start=\"${w.start}\" data-end=\"${w.end}\" data-repl=\"${escapeHtml(s)}\">${escapeHtml(s)}</button>`).join(' ') : 'No suggestions';
      el.innerHTML = `<strong>${escapeHtml(w.word)}</strong> — suggestions: ${suggs}`;
      mdiv.appendChild(el);
    });

    document.getElementById('corrected').textContent = out.corrected_text;

    const sdiv = document.getElementById('structure');
    sdiv.innerHTML = '';
    (out.structure_suggestions || []).forEach(s=>{
      const el = document.createElement('div');
      el.className = 'miss';
      const body = s.replacements ? `replacements: ${s.replacements.join(', ')}` : (s.example ? escapeHtml(s.example) : '');
      el.innerHTML = `<strong>${escapeHtml(s.message)}</strong><div>${body}</div>`;
      sdiv.appendChild(el);
    });

    // attach click handlers for suggestion buttons
    document.querySelectorAll('.suggest-btn').forEach(btn=>{
      btn.addEventListener('click', ()=>{
        const start = parseInt(btn.dataset.start,10);
        const end = parseInt(btn.dataset.end,10);
        const repl = btn.dataset.repl;
        const ta = document.getElementById('inputText');
        const before = ta.value.slice(0, start);
        const after = ta.value.slice(end);
        ta.value = before + repl + after;
        // re-run check automatically
        document.getElementById('checkBtn').click();
      });
    });

  } catch (err) {
    alert('Error: ' + err.message);
  }
});

// apply corrections into the textarea
document.getElementById('applyBtn').addEventListener('click', async ()=>{
  try {
    const txt = document.getElementById('inputText').value;
    const out = await postCheck(txt);
    document.getElementById('inputText').value = out.corrected_text;
    document.getElementById('corrected').textContent = out.corrected_text;
  } catch (err) {
    alert('Error: ' + err.message);
  }
});
