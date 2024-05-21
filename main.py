from PIL import Image, ImageSequence
import imageio.v2 as imageio
import tempfile
import os

fileName = input("enter file name: ")
background = input("are you displaying it on a dark or light background [d,l]?\n")
gif_path = f'art/{fileName}.gif'
img = Image.open(gif_path)

temp_dir = './tempFolder'

os.mkdir(temp_dir)


# Extract and analyze frames
frame_number = 0
for frame in ImageSequence.Iterator(img):
    frame_number += 1
    # print(f"Analyzing frame {frame_number}")

    # # Analyze content (simple example: print the size of the frame)
    # print(f"Frame {frame_number} size: {frame.size}")

    # You can save individual frames if needed
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
    with open(f'artworks/{filename.split(".")[0]}.txt', 'a') as file:
        # creates 
        file.write("\n")
        
        for h in range(pic.shape[0]):
            for w in range(pic.shape[1]):

                pixel_value = currentImg.getpixel((w, h))
                light = brightnessCheker(pixel_value)

                if background == 'l':
                    if light <= 50:
                        file.write("# ")
                    elif light <= 75:
                        file.write("$ ")
                    elif light <= 100:
                        file.write("& ")
                    elif light <= 125:
                        file.write("! ")
                    elif light <= 150:
                        file.write("% ")
                    elif light <= 200:
                        file.write("* ")
                    else:
                        file.write("^ ")

                if background == 'd':
                    if light <= 50:
                        file.write(". ")
                    elif light <= 75:
                        file.write("! ")
                    elif light <= 100:
                        file.write("/ ")
                    elif light <= 125:
                        file.write("v ")
                    elif light <= 150:
                        file.write("J ")
                    elif light <= 200:
                        file.write("m ")
                    else:
                        file.write("# ")

            file.write("\n")

# Load the GIF using imageio for more detailed metadata
gif = imageio.get_reader(gif_path)
print(type(gif))
print(f"GIF Metadata: {gif.get_meta_data()}")

# Analyze frame durations and overall duration
durations = [img.info.get('duration', 100) for _ in range(img.n_frames)]

print(f"Frame durations: {durations}")
total_duration = sum(durations)
print(f"Total duration of GIF: {total_duration} ms")