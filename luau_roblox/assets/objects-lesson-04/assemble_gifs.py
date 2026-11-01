"""Assemble original rendered SVG frames. Requires Pillow; does not edit external art."""
from pathlib import Path
from PIL import Image

base = Path(__file__).resolve().parent
for group in ['08-reparent', '09-event-cooldown']:
    frames = [Image.open(p).convert('RGB') for p in sorted((base / '_frames' / group).glob('*.png'))]
    if len(frames) != 36:
        raise ValueError('Run build_visuals.py and render_visuals.cjs first.')
    samples = Image.new('RGB', (1200, 680 * 6))
    for i in range(6):
        samples.paste(frames[i * 6], (0, 680 * i))
    palette = samples.quantize(colors=128)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    indexed[0].save(base / (group + '.gif'), save_all=True, append_images=indexed[1:],
        duration=200, loop=0, optimize=True, disposal=2)
    print(group + '.gif')
