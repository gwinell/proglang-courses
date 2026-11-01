from pathlib import Path
from PIL import Image
base=Path(__file__).resolve().parent
frames=[Image.open(p).convert('RGB') for p in sorted((base/'_frames/07-coin-cycle').glob('*.png'))]
assert len(frames)==36
samples=Image.new('RGB',(1200,680*6))
for i in range(6):samples.paste(frames[i*6],(0,i*680))
palette=samples.quantize(colors=128)
indexed=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
durations=[170,170,170,170,160,160]+[70,70,70,70,60,60]+[300]*12+[170,170,170,170,160,160]*2
assert len(durations)==36 and sum(durations)==7000
indexed[0].save(base/'07-coin-cycle.gif',save_all=True,append_images=indexed[1:],duration=durations,loop=0,optimize=True,disposal=2)
print('07-coin-cycle.gif, duration 7 seconds.')
