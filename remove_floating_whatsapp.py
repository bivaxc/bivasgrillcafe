from pathlib import Path
import re

p = Path('site.html')
s = p.read_text()

# Remove only the floating WhatsApp action. Keep WhatsApp ordering/contact links elsewhere.
s = re.sub(r'<a class="float float-wa"\b.*?</a>', '', s, flags=re.S)
s = s.replace('.float-wa{background:#25d366;color:#fff}', '')

p.write_text(s)
