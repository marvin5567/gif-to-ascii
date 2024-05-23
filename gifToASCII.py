# a good portion of this was taken from my ascii to img project so check it out!! #
# criticism is always welcome!!

from PIL import Image, ImageSequence, ImageDraw, ImageFont
import imageio.v2 as imageio
import shutil
import os

temp_dir = './tempFolder'
temp_dirt = './tempFolderTwo'

# i learnt mapping :D
brightnessForChars = {
    'l': {
        range(0, 51): "#",
        range(51, 76): "$",
        range(76, 101): "&",
        range(101, 126): "!",
        range(126, 151): "%",
        range(151, 201): "*",
        range(201, 256): "^"
    },
    'd': {
        range(0, 51): ".",
        range(51, 76): "!",
        range(76, 101): "/",
        range(101, 126): "v",
        range(126, 151): "J",
        range(151, 201): "m",
        range(201, 256): "#"
    }
}

class gifToASCII:
    def __init__(self, fileName, background, outputDir):
        self.fileName = fileName
        self.background = background
        self.outputDir = outputDir
        gif_path = f'art/{fileName}.gif'
        self.img = Image.open(gif_path)

        os.mkdir(temp_dir)
        os.mkdir(temp_dirt) # for temp text files

    def gifSplice(self):
        frame_number = 0
        for frame in ImageSequence.Iterator(self.img):
            frame_number += 1
            frame.save(f'{temp_dir}/frame_{frame_number}.png')

    
    def brightnessCheker(self, rgb_color):
        # this command:
        # return 'light' if luminance > 127.5 else 'dark'
        # is for basic colour operations, and it does the same thing as the functions current return
        # but idk why i like this more lmao
        brightness = sum(rgb_color) / 3
        return int(brightness)

    def ASCIIWrtier(self, background, brightness):
        for x, symbol in brightnessForChars[background].items():
            if brightness in x:
                return symbol
            
    def framesToASCII(self):
        for filename in os.listdir(temp_dir):

            pic = imageio.imread(f'{temp_dir}/{filename}') # readiing frame with imageio

            currentImg = Image.open(f'{temp_dir}/{filename}') # reading frame with pillow
            currentImg = currentImg.convert('RGB')

            with open(f'{temp_dirt}/{filename.split(".")[0]}.txt', 'a') as file:
                # creates
                for h in range(pic.shape[0]):
                    for w in range(pic.shape[1]):

                        pixel_value = currentImg.getpixel((w, h))
                        brightness = self.brightnessCheker(pixel_value)

                        pixel = self.ASCIIWrtier(self.background, brightness)

                        file.write(pixel)

                    file.write("\n")

        shutil.rmtree(temp_dir)
        os.mkdir(temp_dir)

    def ASCIIToFrames(self):
        for filename in os.listdir(temp_dirt):
            with open(f'{temp_dirt}/{filename.split(".")[0]}.txt', 'r') as file:
                f = file.read()
                lines = f.split('\n')

                numLines = len(lines)
                maxLineLen = max(len(line) for line in lines)

                meow = Image.new('RGB', (maxLineLen * 6, numLines * 12))
                d = ImageDraw.Draw(meow)

                font = ImageFont.truetype('monocraft.ttf', 12)
                d.text((0,0), f, font=font)

                meow.save(f'{temp_dir}/{filename.split(".")[0]}ASCII.png')
        
        shutil.rmtree(temp_dirt)

    def gifMerge(self):
        durations = [self.img.info.get('duration', 100) for _ in range(len(os.listdir(temp_dir)))]
        durations = [d / 1000 for d in durations] 

        images = [imageio.imread(os.path.join(temp_dir, filename)) for filename in sorted(os.listdir(temp_dir))]

        imageio.mimsave(os.path.join(self.outputDir, f'{self.fileName}ASCII.gif'), images, format='GIF', duration=durations)  # duration is in seconds

        shutil.rmtree(temp_dir) # final delete
