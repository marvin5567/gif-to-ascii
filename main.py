# a good portion of this was taken from my ascii to img project so check it out!! #
# criticism is always welcome!!

from PIL import Image, ImageSequence, ImageDraw
import imageio.v2 as imageio
import shutil
import os

fileName = input("enter file name: ")
background = input("are you displaying it on a dark or light background [d,l]?\n")
gif_path = f'art/{fileName}.gif'
img = Image.open(gif_path)

w, h = img.size
print(f'{w},{h}')
temp_dir = './tempFolder'
temp_dirt = './tempFolderTwo'

outputDir = './artworks'

os.mkdir(temp_dir)
os.mkdir(temp_dirt) # for temp text files

# splicing gif into several frams
frame_number = 0
for frame in ImageSequence.Iterator(img):
    frame_number += 1
    frame.save(f'{temp_dir}/frame_{frame_number}.png')

def brightnessCheker(rgb_color):
    # this command:
    # return 'light' if luminance > 127.5 else 'dark'
    # is for basic colour operations, and it does the same thing as the functions current return
    # but idk why i like this more lmao
    brightness = sum(rgb_color) / 3
    return brightness

for filename in os.listdir(temp_dir):
    print(filename)
    pic = imageio.imread(f'{temp_dir}/{filename}')
    currentImg = Image.open(f'{temp_dir}/{filename}')
    currentImg = currentImg.convert('RGB')
    with open(f'{temp_dirt}/{filename.split(".")[0]}.txt', 'a') as file:
        # creates
        for h in range(pic.shape[0]):
            for w in range(pic.shape[1]):

                pixel_value = currentImg.getpixel((w, h))
                light = brightnessCheker(pixel_value)

                if background == 'l':
                    if light <= 50:
                        file.write("#")
                    elif light <= 75:
                        file.write("$")
                    elif light <= 100:
                        file.write("&")
                    elif light <= 125:
                        file.write("!")
                    elif light <= 150:
                        file.write("%")
                    elif light <= 200:
                        file.write("*")
                    else:
                        file.write("^")

                if background == 'd':
                    if light <= 50:
                        file.write(".")
                    elif light <= 75:
                        file.write("!")
                    elif light <= 100:
                        file.write("/")
                    elif light <= 125:
                        file.write("v")
                    elif light <= 150:
                        file.write("J")
                    elif light <= 200:
                        file.write("m")
                    else:
                        file.write("#")

            file.write("\n")

shutil.rmtree(temp_dir)
os.mkdir(temp_dir)

for filename in os.listdir(temp_dirt):
    with open(f'{temp_dirt}/{filename.split(".")[0]}.txt', 'r') as file:
        img = Image.new('RGB', (w, h))
        d = ImageDraw.Draw(img)
        d.text((10,10), file.read())
        img.save(f'{temp_dir}/{filename.split(".")[0]}ASCII.png')

shutil.rmtree(temp_dirt)

images = [imageio.imread(filename) for filename in temp_dir]
imageio.mimsave(outputDir, images, img.info.get('duration', 100))  # duration is in seconds

shutil.rmtree(temp_dir) # final delete
