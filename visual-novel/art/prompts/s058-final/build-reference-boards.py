from PIL import Image,ImageDraw,ImageFont,ImageOps
from pathlib import Path
root=Path('visual-novel');outdir=root/'art/prompts/s058-final'
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
bold=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',20)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
def portrait(name):
 im=Image.open(root/'renpy/game/art/portraits'/name).convert('RGBA');bg=Image.new('RGBA',im.size,(188,185,176,255));bg.alpha_composite(im);im=bg.convert('RGB');w,h=im.size
 return im.crop((int(w*.08),int(h*.02),int(w*.96),int(h*.83)))
def crop(name,box):return Image.open(root/'renpy/game/art/scenes'/name).convert('RGB').crop(box)
board=Image.new('RGB',(1440,1080),(188,185,176));d=ImageDraw.Draw(board)
entries=[
 ('TESSA - ABOUT 23','Current postwar identity.\nTired, weathered; one mulberry wrap.\nRIGHT soft brace, LEFT free.',portrait('tessa-postwar-speaking.png')),
 ('ELIN - LATER','Face only. Repaired home clothes:\nocher jacket and dark teal skirt.\nNO field cloak at the ending.',portrait('elin-later-speaking.png')),
 ('ORREN','Long chin; burgundy knitted cap.\nWarm-BROWN waistcoat and apron.\nLEFT stick supports old RIGHT leg.',portrait('orren-speaking.png')),
 ('HEST','Same broad face and rust scarf.\nBlue work dress, sleeves secured.\nUnbleached baking apron.',portrait('hest-speaking.png')),
 ('FIRST APPRENTICE','Visibly OLDER; same slim face.\nStraight dark hair, checked scarf.\nGray tunic and practical apron.',portrait('apprentice-speaking.png')),
 ('SECOND APPRENTICE','Visibly OLDER; stockier build.\nLight-brown curls, wide-set eyes.\nCHARCOAL cap, brown vest/apron.',crop('s029-barge.png',(1335,185,1525,385))),
]
for i,(title,caption,im) in enumerate(entries):
 x=(i%3)*365+10;y=(i//3)*462+15;d.text((x,y),title,font=bold,fill=(20,20,20));im=ImageOps.contain(im,(342,335));board.paste(im,(x+(342-im.width)//2,y+32));d.multiline_text((x,y+375),caption,font=small,spacing=6,fill=(20,20,20))
d.text((1110,15),'APPROVED POSTWAR WRAP',font=bold,fill=(20,20,20));im=Image.open(root/'art/character-keys/tessa/postwar-clothes.png').convert('RGB');im=ImageOps.contain(im,(315,600));board.paste(im,(1105+(315-im.width)//2,48))
d.multiline_text((1110,665),'One ankle-length garment.\nTWO wooden toggles at LEFT.\nRIGHT soft brace; fingers free.\nNo undershirt, badge, extra\ncollar, belt or shawl.',font=font,spacing=6,fill=(20,20,20))
d.text((1110,815),'ELIN: S008 HOME CLOTHES',font=small,fill=(20,20,20));im=crop('s008-bellweir-market.png',(748,310,1018,895));im=ImageOps.contain(im,(315,230));board.paste(im,(1105+(315-im.width)//2,844))
d.multiline_text((10,957),'IDENTITY AND CLOTHING ONLY: poses, expressions and old injuries are not scene instructions.\nAge both apprentices forward. Keep the two caps and the two apprentices distinct.\nElin has repaired intact pale sleeves, ocher jacket and teal skirt; disregard the portrait field cloak.\nTessa remains war-worn at 23. Her RIGHT brace is protected; the LEFT hand performs healthy actions.',font=font,spacing=8,fill=(20,20,20))
board.save(outdir/'cast-reference-board.jpg',quality=94)
children=Image.new('RGB',(900,610),(188,185,176));d=ImageDraw.Draw(children)
for i,(name,im,text) in enumerate([
 ('ADA - EARLIER FACE ONLY',portrait('ada-speaking.png'),'FINAL AGE 11-12. Longer limbs and older face.\nSame brown skin, round family features and\ntwo black plaits. Mustard dress, clean repairs.\nDo not copy the eight-year-old body.'),
 ('RENN - EARLIER FACE ONLY',crop('s011-bellweir-causeway.png',(1510,390,1670,585)),'FINAL AGE 9. Taller, with older child proportions.\nLoose black curls and Orren-like long chin.\nBrick-red shirt, patched dark trousers.\nNo fresh injury or invented lasting limp.')]):
 x=i*450+10;d.text((x,10),name,font=bold,fill=(20,20,20));im=ImageOps.contain(im,(425,420));children.paste(im,(x+(425-im.width)//2,45));d.multiline_text((x,480),text,font=font,spacing=7,fill=(20,20,20))
children.save(outdir/'children-reference-panel.jpg',quality=94)
# Limited actual market crops: color and material continuity only, never whole scene.
im=Image.open(root/'art/scene-studies/s058-bellweir-market-spring/market-source.png')
w,h=im.size;board=Image.new('RGB',(1440,560),(188,185,176));d=ImageDraw.Draw(board)
market_font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
for x,title,box in [(10,'ACTUAL MARKET: TESSA WRAP / FACE',(w*.295,h*.155,w*.52,h*.63)),(470,'ACTUAL MARKET: ELIN HOME CLOTHES',(w*.50,h*.025,w*.70,h*.91)),(900,'ACTUAL MARKET: BAKERY FOUR',(w*.745,h*.14,w*.98,h*.53))]:
 c=ImageOps.contain(im.crop(tuple(round(v) for v in box)).convert('RGB'),(430,435));board.paste(c,(x+(430-c.width)//2,40));d.text((x,10),title,font=market_font,fill='black')
d.text((10,500),'Shared face, fabric and apron state ONLY. Final uses low oxblood slip-ons, LEFT stick, closed packet.',font=market_font,fill='black')
d.text((10,530),'Do not copy the market pose, books, fountain or shoe/cane mistakes. Interior has exactly eight people.',font=market_font,fill='black')
board.save(outdir/'actual-market-state-reference.jpg',quality=94)
# Tiny inspection crop used as the third-toggle component's precise input.
im=Image.open(root/'art/scene-studies/s058-final/offered-chair-source.png')
im.crop((340,450,440,575)).resize((400,500)).save(outdir/'third-toggle-input-reference.png')
