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
# Remove the dynamically injected Coca-Cola item from the Drinks section.
s=re.sub(r"if\(!td\.querySelector\('\.item \.item-name\[data-coke\]'\)\)\{.*?drinkList\.appendChild\(item\);\}\}", "", s, flags=re.S)
p.write_text(s)

# Delivery is confirmed by customer care after the order. Remove automatic area/fee logic.
p=Path('site.html')
s=p.read_text()
s=s.replace('<div class="field" id="deliveryAreaField"><label for="deliveryArea">Delivery area</label><select id="deliveryArea" onchange="updateTotals()"><option value="town">Kagadi Town - FREE</option><option value="outside">Outside Kagadi Town - UGX 5,000</option></select></div>', '')
s=s.replace('<div class="field"><label for="location">Location</label><input id="location" placeholder="Area, landmark or address" autocomplete="street-address"></div>', '<div class="field"><label for="location">Location (optional)</label><input id="location" placeholder="Area, landmark or address (optional)" autocomplete="street-address"></div>')
s=s.replace('<div class="sumline"><span>Delivery</span><strong id="deliveryFee">FREE</strong></div><div class="sumline total">', '<div class="sumline total">')
s=s.replace('<div class="delivery-note" id="deliveryNote">Free delivery within Kagadi Town.</div>', '<div class="delivery-note" id="deliveryNote">Customer care will call to confirm your location and discuss delivery charges.</div>')
s=s.replace("document.getElementById('deliveryAreaField').style.display=t==='Delivery'?'block':'none';", '')
s=s.replace("delivery=orderType==='Delivery'&&document.getElementById('deliveryArea').value==='outside'?5000:0,total=foodTotal+drinkTotal+delivery,", "delivery=0,total=foodTotal+drinkTotal,")
s=s.replace("document.getElementById('deliveryFee').textContent=delivery?money(delivery):'FREE';", '')
s=s.replace("document.getElementById('deliveryNote').textContent=orderType!=='Delivery'?'No delivery fee for '+orderType+'.':delivery?'UGX 5,000 delivery outside Kagadi Town.':'Free delivery within Kagadi Town.';", "document.getElementById('deliveryNote').textContent='Customer care will call to confirm your location and discuss delivery charges.';")
s=s.replace("if(!location){alert('Please enter your location.');return}", '')
s=s.replace("doc.text(`Instructions: ${d.notes||'None'}`,15,y);y+=14;doc.text('Free delivery within Kagadi Town; UGX 5,000 outside Kagadi Town.',15,y);y+=7;doc.text('Provisional receipt. Final availability is confirmed on WhatsApp.',15,y);", "doc.text(`Instructions: ${d.notes||'None'}`,15,y);y+=14;doc.text('Delivery charges: To be confirmed by customer care on call.',15,y);y+=7;doc.text('Customer care will call to confirm the delivery location.',15,y);y+=7;doc.text('Provisional receipt. Final availability is confirmed on WhatsApp.',15,y);")
s=s.replace("const no=orderNo(),date=new Date().toLocaleString('en-UG',{dateStyle:'medium',timeStyle:'short'}),d={...x,name,type:orderType,location,notes,no,date};", "const no=orderNo(),date=new Date().toLocaleString('en-UG',{dateStyle:'medium',timeStyle:'short'}),d={...x,name,type:orderType,location:location||'To be confirmed by customer care',notes,no,date};")
s=s.replace("Please confirm availability and delivery details.", "Customer care will call to confirm your location and discuss delivery charges.")
s=s.replace("document.getElementById('deliveryAreaField').style.display='block';updateTotals();", "updateTotals();")
p.write_text(s)

# The shell wrapper overrides submitOrder. Reinstall the receipt + WhatsApp flow while keeping delivery charges for customer care.
p=Path('shell.html')
s=p.read_text()
if 'customer-care-delivery-flow' not in s:
    extra='''<script id="customer-care-delivery-flow">window.addEventListener('load',()=>{try{const f=document.getElementById('site');const d=f&&f.contentDocument;if(!d)return;d.defaultView.submitOrder=function(){try{const x=d.defaultView.updateTotals();if(!x.foods.length){alert('Please select at least one food item.');return}const name=d.getElementById('name').value.trim(),location=d.getElementById('location').value.trim(),notes=d.getElementById('notes').value.trim();if(!name){alert('Please enter your name.');return}const no=d.defaultView.orderNo(),date=new Date().toLocaleString('en-UG',{dateStyle:'medium',timeStyle:'short'}),data={...x,name,type:d.defaultView.orderType,location:location||'To be confirmed by customer care',notes,no,date};if(!d.defaultView.receipt(data))return;const foodText=x.foods.map(i=>`• ${i.name} × ${i.qty} (UGX ${Number(i.price*i.qty).toLocaleString()})`).join('\\n'),drinkText=x.drinks.map(i=>{const free=Math.min(i.qty,x.included);return`• ${i.name} × ${i.qty} (UGX ${Number(i.price*i.qty-free*3000).toLocaleString()}${free?' - 1 included in combo':''})`}).join('\\n')||'• None';const msg=`🍽️ *BIVA'S GRILL & CAFE*\\n*NEW ORDER #${no}*\\n\\nCustomer: ${name}\\nOrder type: ${d.defaultView.orderType}\\nLocation: ${location||'To be confirmed by customer care'}\\n\\n*FOOD*\\n${foodText}\\n\\n*DRINKS*\\n${drinkText}\\n\\nFood subtotal: UGX ${Number(x.foodTotal).toLocaleString()}\\nDrinks subtotal: UGX ${Number(x.drinkTotal).toLocaleString()}\\n*GRAND TOTAL: UGX ${Number(x.total).toLocaleString()}*\\n\\nDelivery charges: To be discussed with customer care on call.\\nInstructions: ${notes||'None'}\\n\\nCustomer care will call to confirm the location and delivery charges.`;window.open('https://wa.me/'+d.defaultView.WA+'?text='+encodeURIComponent(msg),'_blank')}catch(err){console.error(err);alert('Please try the order again.')}};const clean=()=>{const field=d.getElementById('deliveryAreaField');if(field)field.remove();const fee=d.getElementById('deliveryFee');if(fee){const row=fee.closest('.sumline');if(row)row.remove()}const note=d.getElementById('deliveryNote');if(note)note.textContent='Customer care will call to confirm your location and discuss delivery charges.';const loc=d.getElementById('location');if(loc){loc.placeholder='Area, landmark or address (optional)';loc.required=false;const label=loc.parentElement&&loc.parentElement.querySelector('label');if(label)label.textContent='Location (optional)'}};clean();setTimeout(clean,300);setTimeout(clean,1000);setTimeout(clean,2500)}catch(e){console.error(e)}});</script>'''
    s=s.replace('</body></html>',extra+'</body></html>')
p.write_text(s)
