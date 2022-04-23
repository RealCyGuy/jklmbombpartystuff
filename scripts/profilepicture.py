import base64
from PIL import Image, ImageOps, ImageSequence
from io import BytesIO
import pyperclip

im = Image.open("pictures/" + input("Enter image name (in scripts/pictures directory): "))
frames = []
for frame in ImageSequence.Iterator(im):
    width, height = frame.size

    if width > height:
        new = height
    else:
        new = width
    left = round((width - new) / 2)
    top = round((height - new) / 2)
    right = round((width + new) / 2)
    bottom = round((height + new) / 2)
    frame = frame.crop((left, top, right, bottom)).resize((32, 32))
    frames.append(frame)

data = None
for x in range(7):
    quality = 100 - x * 10
    output = BytesIO()
    frames[0].save(output, "WEBP", quality=quality, optimize=True, save_all=True, append_images=frames[1:], loop=1000)

    data = base64.b64encode(output.getvalue()).decode()
    print(len(data))
    if len(data) <= 10000:
        print(f"Image was compressed to {quality} quality.")
        break

if len(data) > 10000:
    print("Could not compress!")
else:
    pyperclip.copy(data)
    print("Copied picture to clipboard, paste into bookmarklet or run:\n\n"
          f"settings.picture = 'PASTE_PICTURE_HERE'\n" 
          f"saveSettings()")
