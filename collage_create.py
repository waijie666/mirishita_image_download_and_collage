from PIL import Image
import argparse
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from pathlib import Path
from itertools import repeat
import random

class Inputs:
    def __init__(self):
        pass

def collage_create(input, name):
    total_count = input.horizontalcount*input.verticalcount
    images = random.sample(input.input_image_list, total_count) 
    result = Image.new('RGB', (input.finalwidth, input.finalheight))
    count = 0 
    current_horizontal_position = 0
    current_vertical_position = 0
    for image in images:
        count += 1
        if count > input.horizontalcount:
            count = 1
            current_horizontal_position = 0 
            current_vertical_position += input.height
        with Image.open(image) as input_image:
            resized_image = input_image.resize((input.width,input.height))
            result.paste(im=resized_image, box=(current_horizontal_position, current_vertical_position))
        current_horizontal_position += input.width
    if input.type == "jpg":
        image_type = "JPEG"
    elif input.type == "png":
        image_type = "PNG" 
    result.save(input.output_dir.joinpath(f"{name}.{input.type}"), image_type, quality=90, optimize=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Collage creation')
    parser.add_argument("--input_dir", type=str, default="input")
    parser.add_argument("--output_dir", type=str, default="outputcollage")
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=360)
    parser.add_argument("--horizontalcount", type=int, default=3)
    parser.add_argument("--verticalcount", type=int, default=3)
    parser.add_argument("--collagecount", type=int, default=1)
    parser.add_argument("--threadcount", type=int, default=32)
    parser.add_argument("--type", type=str, default="jpg", choices=["jpg","png"])
    parser.add_argument("--prefix", type=str, default="")
    args = parser.parse_args()
    
    input = Inputs()

    input.input_image_list = list(Path(args.input_dir).glob("*.png"))
    if len(input.input_image_list) > 0:
        print(f"Input image list: {len(input.input_image_list)}")
    else:
        print("No png images exists in this list")
        exit()
    
    input.output_dir = Path(args.output_dir)
    input.output_dir.mkdir(parents=True, exist_ok=True)
    if (input.output_dir.is_dir()):
        print(f"Output dir {args.output_dir} exists. Proceeding")
    else:
        print(f"Output dir {args.output_dir} cannot be created or does not exists")
        exit()

    input.type=args.type

    current_count = 1
    while True:
        if input.output_dir.joinpath(f"{args.prefix}{current_count}.{args.type}").exists() :
            current_count += 1
        else:
            break 
    print(f"Checking for existing files in output dir {args.output_dir} complete. New images will start at {args.prefix}{current_count}.{args.type}")
    input.width = args.width
    input.height = args.height
    input.horizontalcount = args.horizontalcount
    input.verticalcount = args.verticalcount
    input.finalwidth = args.width * args.horizontalcount
    input.finalheight = args.height * args.verticalcount

    image_name_list = [ f"{args.prefix}{i}" for i in range(current_count, args.collagecount + current_count) ]
    with ThreadPoolExecutor(max_workers=args.threadcount) as executor:
        for i in tqdm(executor.map(collage_create, repeat(input), image_name_list), total=len(image_name_list), desc="Creating collages"):
            pass
