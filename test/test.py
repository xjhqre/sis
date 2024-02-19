import glob
import os

import config


def extract_batch(img_folder_path, batch_size=32):
    file_paths_generator = get_file_paths(img_folder_path, batch_size)
    cnt = 1

    for file_paths_batch in file_paths_generator:
        # 过滤掉非图片类型的文件
        file_paths_batch = [name for name in file_paths_batch if
                            os.path.splitext(name)[1] in config.types]

        # 在这里使用每个批次的文件路径进行处理
        print(len(file_paths_batch))
        for file_path in file_paths_batch:
            pass
        # 每个批次完成后进行其他操作


def get_file_paths(img_folder_path, batch_size):
    img_path_list = glob.glob(img_folder_path + "/*")
    for i in range(0, len(img_path_list), batch_size):
        yield img_path_list[i:i + batch_size]


if __name__ == '__main__':
    extract_batch("F:\\ACG\\壁纸")
    # print(feature_extractor.fe.extract_batch("F:\\ACG\\新建文件夹"))
