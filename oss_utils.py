import oss2

import config


class OssUtils:
    def __init__(self):
        # 阿里云OSS
        # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
        auth = oss2.Auth(config.AccessKeyId, config.AccessKeySecret)
        # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
        # 填写Bucket名称。
        self.bucket = oss2.Bucket(auth, config.EndPoint, config.bucket)

    def upload(self, key, filename):
        """
        上传图片到 oss

        参数：
            key (str): 上传到OSS的文件名
            filename (str): 本地文件名，需要有可读权限

        返回值：
            PutObjectResult <oss2.models.PutObjectResult>
        """
        return self.bucket.put_object_from_file(key, filename).resp


ou = OssUtils()
