"""Deterministic sprite slicing, sizing and alpha QA; no creative redrawing."""
from pathlib import Path
from PIL import Image
import json
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets/sprites'
OUT.mkdir(exist_ok=True)
records=[]
def slice_sheet(filename,cols,rows,names,canvas,character=False):
 im=Image.open(ROOT/'art/source'/filename).convert('RGBA')
 if im.getchannel('A').getextrema()[0]==255:raise ValueError(f'{filename}: missing alpha')
 pieces=[]
 for row in range(rows):
  for col in range(cols):
   box=(round(col*im.width/cols),round(row*im.height/rows),round((col+1)*im.width/cols),round((row+1)*im.height/rows))
   cell=im.crop(box)
   bbox=cell.getchannel('A').point(lambda v:255 if v>40 else 0).getbbox()
   if not bbox:raise ValueError('Empty sprite '+names[len(pieces)])
   pieces.append(cell.crop(bbox))
 # one scale across all character poses, preserving body proportions
 scale=min((canvas[0]-12)/max(p.width for p in pieces),(canvas[1]-12)/max(p.height for p in pieces)) if character else None
 for name,p in zip(names,pieces):
  ratio=scale or min((canvas[0]-16)/p.width,(canvas[1]-16)/p.height)
  p=p.resize((max(1,round(p.width*ratio)),max(1,round(p.height*ratio))),Image.Resampling.LANCZOS)
  dest=Image.new('RGBA',canvas)
  dest.alpha_composite(p,((canvas[0]-p.width)//2,canvas[1]-6-p.height if character else (canvas[1]-p.height)//2))
  dest.save(OUT/(name+'.png'),optimize=True)
  records.append({'id':name,'path':'assets/sprites/'+name+'.png','status':'normalized','technical':{'dimensions':f'{canvas[0]}x{canvas[1]}','alpha':True,'anchor':'bottom-center' if character else 'center','filtering':'smooth'},'source':{'kind':'generated','url_or_tool':'built-in image_gen','created_at':'2026-10-06','reference':'assets/cover.png','original':'art/source/'+filename,'license':'Generated for this project; no third-party asset pack used; no independent license asserted.'},'verification':{'technical_checks_passed':True,'native_scale_reviewed':False,'in_engine_reviewed':False}})
 if character:
  atlas=Image.new('RGBA',(canvas[0]*cols,canvas[1]*rows))
  for i,name in enumerate(names):atlas.alpha_composite(Image.open(OUT/(name+'.png')),((i%cols)*canvas[0],(i//cols)*canvas[1]))
  atlas.save(OUT/'characters.png',optimize=True)
names=[f'{person}-{pose}-{direction}' for person in ['linh','nam'] for pose in ['idle','walk'] for direction in ['down','left','right','up']]
slice_sheet('characters-v2.png',4,4,names,(96,112),True)
if (ROOT/'art/source/stations-v2.png').exists():slice_sheet('stations-v2.png',4,3,['chicken','veg','fruit','sink','rawboard','cleanboard','stove','serve','trash','power','water','plant'],(192,192))
if (ROOT/'art/source/foods-v2.png').exists():slice_sheet('foods-v2.png',3,2,['food-chicken-raw','food-chicken','food-salad-raw','food-salad','food-fruit-raw','food-fruit'],(96,96))
(ROOT/'art/asset-manifest.json').write_text(json.dumps({'schema_version':1,'art_direction_brief':'art/art-direction.md','assets':records},ensure_ascii=False,indent=2))
print(f'Normalized {len(records)} sprites')
