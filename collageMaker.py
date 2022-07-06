import datetime
import getopt
import os
import math
import fnmatch
import sys

from PIL import Image
from typing import List

TARGETX = 350
TARGETY = 500


def get_photos_names(directory: str = ".") -> List[str]:
    today = datetime.datetime.today()
    regex = "photo_{}-{}*.jpg".format(today.year, today.month if today.month > 9 else "0{}".format(today.month))
    photolist = fnmatch.filter(os.listdir(directory), regex)
    return [f"{directory}{x}" for x in photolist]


def prepare_empty_photo(row, col) -> Image:
    return Image.new("RGBA", (row * TARGETX, col * TARGETY))


def prepare_image(path) -> Image:
    image1: Image = Image.open(path)
    width, height = image1.size
    scalar = max(width / TARGETX, height / TARGETY)
    # print(f"{width=}{height=}")
    # print(f"{scalar=}")
    img2 = image1.resize((int(width // scalar), int(height // scalar)))
    xsize, ysize = img2.size
    xdif = int((TARGETX - xsize) / 2)
    ydif = int((TARGETY - ysize) / 2)
    img3 = Image.new("RGBA", (TARGETX, TARGETY))
    img3.paste(img2, (xdif, ydif))
    return img3


def count_x_y2(photos_count: int, propotions: int = 4):
    row = math.ceil(math.sqrt(photos_count / propotions))
    col = math.ceil(photos_count / row)
    # print(row * col)
    # print(photos_count)
    return col, row


def createCollage(directory: str, outputName: str, prp: int):
    photo_names = get_photos_names(directory)
    rows, cols = count_x_y2(len(photo_names), propotions=prp)
    colageimg = prepare_empty_photo(rows, cols)
    print(colageimg.size)

    x = TARGETX * (rows - 1)
    y = TARGETY * (cols - 1)
    for photo in photo_names:
        # print(f"{x=}{y=}")
        colageimg.paste(prepare_image(photo), (x, y))
        x = x - TARGETX
        if x < 0:
            y = y - TARGETY
            x = TARGETX * (rows - 1)
    colageimg.save(f"{outputName}.png")


def show_help():
    sys.stdout.write(f"Simple small collage maker: \n"
                     f"Options:\n\n"
                     f"-i --input dir Make collage from photos in given directory\n"
                     f"-o --output dir Saves collage in provided path\n"
                     f"-p --proportions int Changes the ratio of collage, default 4 x 1\n"
                     f"-h --help Show this manual\n")
    sys.exit(0)


if __name__ == '__main__':
    source = "input/"
    output = "output/collage"
    proportion = 4
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:i:o:h",
                                   ["input=", "output=", "proportions=", "help"])
    except getopt.GetoptError as ex1:
        sys.stdout.write(ex1.msg + "\n")
        sys.exit(2)
    for opt, arg in opts:
        # print(f"{opt=}{arg=}")
        if opt in ('-i', '--input'):
            source = arg
        elif opt in ('-o', '--output'):
            output = arg
        elif opt in ('-p', '--proportions'):
            proportion = int(arg)
        elif opt in ('-h', '--help'):
            show_help()
    try:
        createCollage(source, output, proportion)
    except Exception as e:
        sys.stdout.write(str(e))
        show_help()
    sys.exit(0)
