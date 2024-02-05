import glob

import feature_extractor


def extract_batch(img_folder_path, batch_size=32):
    file_paths_generator = get_file_paths(img_folder_path, batch_size)
    cnt = 1
    for file_paths_batch in file_paths_generator:
        # 在这里使用每个批次的文件路径进行处理
        for file_path in file_paths_batch:
            # 处理单个文件路径
            print(file_path + ' --- ' + str(cnt))
            cnt += 1
        # 每个批次完成后进行其他操作


def get_file_paths(img_folder_path, batch_size):
    img_path_list = glob.glob(img_folder_path + "/*")
    for i in range(0, len(img_path_list), batch_size):
        yield img_path_list[i:i + batch_size]


if __name__ == '__main__':
    # extract_batch("F:\\ACG\\新建文件夹")
    print(feature_extractor.fe.extract_batch("F:\\ACG\\新建文件夹"))
