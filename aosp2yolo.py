'''convert AOSP to YOLO'''
from pathlib import Path
import shutil

import cv2
from PIL import Image, ImageDraw


BASE_DIR = Path(__file__).resolve().parent
SUBNET_AC = BASE_DIR.joinpath('Subset_AC')
SUBNET_LE = BASE_DIR.joinpath('Subset_LE')
SUBNET_RP = BASE_DIR.joinpath('Subset_RP')

INPUT_TRAIN_PATH_LIST = [SUBNET_AC, SUBNET_LE]
INPUT_TEST_PATH_LIST = [SUBNET_RP]

OUTPUT_TRAIN_PATH = BASE_DIR.joinpath('train')
OUTPUT_TEST_PATH = BASE_DIR.joinpath('test')


def get_text_path(image_path, train_path):
    image_name = Path(image_path.name)
    text_path = train_path.joinpath(f"groundtruth_localization/{Path(image_name.stem + '.txt')}")
    return text_path

def make_output_dir():
    if not OUTPUT_TRAIN_PATH.exists():
        OUTPUT_TRAIN_PATH.mkdir()
    if not OUTPUT_TEST_PATH.exists():
        OUTPUT_TEST_PATH.mkdir()

def show_rectangle(image_path, left, upper, right, bottom):
    if image_path.name == '1.jpg':
        print(f'upper:{upper}')
        print(f'bottom:{bottom}')
        print(f'right:{right}')
        print(f'left:{left}')

        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        draw.rectangle(
            (left, upper, right, bottom),
            outline=(255, 0, 0),
            width=5
        )
        image.show()


def convert_location(left, upper, right, bottom, input_image_path):
    (h, w, _) = cv2.imread(str(input_image_path)).shape
    x_center = float((right + left) / 2) / w
    y_center = float((upper + bottom) / 2) / h
    width = float(right + left) / w
    height = float(upper + bottom) / h
    return x_center, y_center, width, height


def convert2yolo(input_image_path, input_text_path, input_path, train_or_test, set_type, debag=False):
    with open(input_text_path, mode='r', encoding='utf_8') as f:
        left, upper, right, bottom = map(float, f.read().split())
        if debag:
            show_rectangle(input_image_path, left, upper, right, bottom)

        # 書き込み
        output_path = OUTPUT_TRAIN_PATH if train_or_test == 'train' else OUTPUT_TEST_PATH
        output_text_path = output_path.joinpath(f'{set_type}{input_text_path.name}')
        output_image_path = output_path.joinpath(f'{set_type}{input_image_path.name}')
        print(f'output_path:{output_path}')
        print(f'output_text_path:{output_text_path}')
        with open(output_text_path, mode='w', encoding='utf_8') as f:
            x_center, y_center, width, height = convert_location(left, upper, right, bottom, input_image_path)
            f.write(f'plate {x_center:06f} {y_center:06f} {width:06f} {height:06f}\n')
        shutil.copy(input_image_path, output_image_path)


def main():

    make_output_dir()

    for input_train_path in INPUT_TRAIN_PATH_LIST:
        image_paths = input_train_path.glob('Image/*.jpg')
        set_type = input_train_path.name[-2:]
        for image_path in image_paths:
            text_path = get_text_path(image_path, input_train_path)
            convert2yolo(image_path, text_path, input_train_path, train_or_test='train', set_type=set_type)

    for input_test_path in INPUT_TEST_PATH_LIST:
        image_paths = input_test_path.glob('Image/*.jpg')
        set_type = input_test_path.name[-2:]
        for image_path in image_paths:
            text_path = get_text_path(image_path, input_test_path)
            convert2yolo(image_path, text_path, input_test_path, train_or_test='test', set_type=set_type)


if __name__ == '__main__':
    main()
