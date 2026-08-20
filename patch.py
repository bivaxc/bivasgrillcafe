from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
s=s.replace('<a class="cta" href="#" onclick="openOrder(event)">Order Now</a>','')
s=s.replace('<a class="btn primary" href="#" onclick="openOrder(event)">Order Now</a>','')
s=s.replace('.item-row{display:grid;grid-template-columns:1fr 72px 95px;gap:8px;align-items:center;padding:9px;border-radius:11px;background:rgba(255,255,255,.72)}','.item-row{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center;padding:10px;border-radius:12px;background:rgba(255,255,255,.72)}')
s=s.replace('.qty{width:68px!important;padding:9px!important;text-align:center}', '.stepper{display:flex;align-items:center;gap:7px}.stepper button{width:38px;height:38px;border:1px solid rgba(75,55,35,.2);border-radius:10px;background:#fff;font:900 20px Cambria,Georgia,serif;cursor:pointer;color:var(--dark)}.stepper button:active{transform:scale(.95)}.qty{width:44px!important;padding:9px 4px!important;text-align:center;font-weight:900}')
marker='<div class="floating-actions" aria-label="Quick contact actions">'
if marker in s and 'float-delivery' not in s:
    delivery='<a class="float-btn float-delivery" href="#" onclick="openOrder(event,\'Delivery\')" aria-label="Order delivery"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M3 7h11v9H3zM14 10h3.7l3.3 3.2V16h-7z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="7" cy="18" r="2" fill="currentColor"/><circle cx="18" cy="18" r="2" fill="currentColor"/><path d="M5 18h9m4 0h-1" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg><span class="float-label">Order Delivery</span></a>'
    s=s.replace(marker, marker+delivery)
needle='.float-call{background:linear-gradient(145deg,#fff,#e8e8e8);color:#111}'
if '.float-delivery{' not in s:
    s=s.replace(needle,'.float-delivery{background:linear-gradient(145deg,#ffc95e,#f39b24);color:#201711}'+needle)
s=s.replace('Location / table details','Location')
s=s.replace('Location/Table','Location')
s=s.replace('Please enter your location or table details.','Please enter your location.')
s=s.replace('Area, landmark or table number','Area, landmark or address')
s=s.replace("document.getElementById('location').placeholder=t==='Dine In'?'Table number':'Area, landmark or address'","document.getElementById('location').placeholder='Area, landmark or address'")
pattern=r'<input class="qty (food|drink)"([^>]*)>'
def repl(m):
    cls=m.group(1); attrs=m.group(2)
    return '<div class="stepper"><button type="button" onclick="changeQty(this,-1)">−</button><input class="qty '+cls+'"'+attrs+' readonly><button type="button" onclick="changeQty(this,1)">+</button></div>'
if 'class="stepper"' not in s:
    s=re.sub(pattern,repl,s)
needle="function closeOrder(){modal.classList.remove('show');document.body.style.overflow=''}"
if 'function changeQty' not in s:
    s=s.replace(needle, needle+"\nfunction changeQty(btn,delta){const input=btn.parentElement.querySelector('.qty');input.value=Math.max(0,Number(input.value)+delta);updateTotals()}")
s=s.replace('.item-row{grid-template-columns:1fr 62px 86px}', '.item-row{grid-template-columns:1fr auto}')
p.write_text(s)
