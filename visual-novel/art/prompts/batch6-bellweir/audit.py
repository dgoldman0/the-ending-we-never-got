"""Audit saved candidates against original pixels and actual reopened GIMP mask unions."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
here=Path(__file__).resolve().parent
st=here.parents[1]/'scene-studies'/'batch6-bellweir';tmp=Path('/tmp/batch6-bellweir-checks')
r=json.loads((here/'recipes.json').read_text());rows=[]
for n in r:
 a=np.array(Image.open(st/n/'before.png').convert('RGBA'));b=np.array(Image.open(st/n/'candidate.png').convert('RGBA'));re=np.array(Image.open(tmp/(n+'-reopened.png')).convert('RGBA'));m=np.array(Image.open(tmp/(n+'-mask.png')).convert('RGB')).max(axis=2)
 changed=np.any(a!=b,axis=2);ys,xs=np.where(changed)
 rows.append({'scene':n,'size':[b.shape[1],b.shape[0]],'opaque':bool((b[:,:,3]==255).all()),'reopened_exact':bool(np.array_equal(b,re)),'changed_pixels':int(changed.sum()),'outside_layer_masks':int((changed&(m==0)).sum()),'changed_bbox':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],'before_sha256':hashlib.sha256((st/n/'before.png').read_bytes()).hexdigest(),'candidate_sha256':hashlib.sha256((st/n/'candidate.png').read_bytes()).hexdigest()})
(st/'verification.json').write_text(json.dumps(rows,indent=2)+'\n')
assert all(x['opaque'] and x['reopened_exact'] and x['outside_layer_masks']==0 for x in rows)
print('All',len(rows),'masters exact, opaque, original dimensions; zero pixels changed outside actual repair masks.')
