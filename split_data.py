from pathlib import Path
import random


def split_data():
    base_dir = Path(__file__).resolve().parent
    input_train_path = base_dir.joinpath('train')
    input_test_path = base_dir.joinpath('test')

    train_rate = 0.8
    train_valid_images = list(input_train_path.glob('*.jpg'))

    random.seed(100)
    random.shuffle(train_valid_images)

    train_images = train_valid_images[:int(len(train_valid_images)*train_rate)]
    valid_images = train_valid_images[int(len(train_valid_images)*train_rate):]
    test_images = list(input_test_path.glob('*.jpg'))

    datas = {
        'train': train_images,
        'valid': valid_images,
        'test': test_images
    }

    for key, value in datas.items():
        text_path = base_dir.joinpath(f'{key}.txt')
        print(f'{key}:{len(value)}')
        with open(text_path, mode='w', encoding='utf_8') as f:
            for image in value:
                f.write(str(image)+'\n')


if __name__ == '__main__':
    split_data()
