import base64
from PIL import Image, ImageOps
from io import BytesIO
import pyperclip

im = Image.open("pictures/" + input("Enter image name (in scripts/pictures directory): "))
im = ImageOps.exif_transpose(im)

width, height = im.size

if width > height:
    new = height
else:
    new = width
left = round((width - new) / 2)
top = round((height - new) / 2)
right = round((width + new) / 2)
bottom = round((height + new) / 2)
im = im.crop((left, top, right, bottom)).resize((128, 128))

data = None
for x in range(5):
    quality = 100 - x * 10
    output = BytesIO()
    im.save(output, "WEBP", quality=quality, optimize=True)

    data = base64.b64encode(output.getvalue()).decode()
    if len(data) <= 10000:
        print(f"Image was compressed to {quality} quality.")
        break

if len(data) > 10000:
    print("Could not compress!")
else:
    command = f"settings.picture = '{data}'\n" \
              f"saveSettings()"
    pyperclip.copy(command)
    print("Copied command to clipboard.")
