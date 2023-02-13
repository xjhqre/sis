"""
以图搜图配置文件，批量处理
"""
save_path = 'G:/workspace/sis/static/uploaded/'

train_pic_path = 'F:/ACG/出处归档/*'
# train_pic_path = './static/img/*'

# pic_url = "./static/img/"
pic_url = "https://chuchu-xjhqre.oss-cn-hangzhou.aliyuncs.com/img/"

types = [".jpg", ".jpeg", ".gif", ".png", ".JPG", ".JPEG", ".GIF", ".PNG"]


# elasticsearch
elasticsearch_index = "img"
elasticsearch_url = 'V/vj25WYRp8W1t191Rm0rw=='
elasticsearch_port = "62pZn7xCOl7rp7P45Dj6Hg=="


# OSS
AccessKeyId = "qSisWdlePw3d4KkfbP7HPs6HD6P7QHGTgRNkpYS7QzU="
AccessKeySecret = "SNMy47aJIvJTzNCUMwO7fDB1Jc+0dQYVhtblC49H8HA="
EndPoint = "oss-cn-hangzhou.aliyuncs.com"
bucket = "xjhqre-bbs"
folder = 'test/'
pic_oss_url = "https://xjhqre-bbs.oss-cn-hangzhou.aliyuncs.com/" + folder
