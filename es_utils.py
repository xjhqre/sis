import sys

from elasticsearch import Elasticsearch

import config


class EsUtils:
    def __init__(self):
        self.es = Elasticsearch([{'host': config.elasticsearch_url, 'port': config.elasticsearch_port}], timeout=3600)
        # 检查是否成功连接
        if self.es.ping():
            print("elasticsearch连接成功")
        else:
            print("elasticsearch连接失败")
            sys.exit()

    def index(self, index, body):
        """
        上传数据到 es 索引。
        参数:
            index (str): 索引名称。
            doc (set): 数据。

        返回值:
            int: 两个数字的和。
        """
        self.es.index(config.elasticsearch_index, body=body)  # 保存到elasticsearch

    def feature_search(self, query, result_count=config.result_count):
        """
        相似图片向量查询
        参数:
            query (list): 图片向量。
            result_count (int): 搜索图片数量

        返回值:
            answers (list): 包含图片路径和名称的集合。
        """
        results = self.es.search(
            index=config.elasticsearch_index,
            body={
                "size": result_count,
                "query": {
                    "script_score": {
                        "query": {
                            "match_all": {}
                        },
                        "script": {
                            "source": "cosineSimilarity(params.queryVector, doc['feature'])+1.0",
                            "params": {
                                "queryVector": query
                            }
                        }
                    }
                }
            })
        hitCount = results['hits']['total']['value']

        if hitCount > 0:
            answers = []
            max_score = results['hits']['max_score']

            if max_score >= 0.35:
                for hit in results['hits']['hits']:
                    if hit['_score'] > 0.5 * max_score:
                        imgurl = hit['_source']['url']
                        name = hit['_source']['name']
                        imgurl = imgurl.replace("#", "%23")
                        answers.append([imgurl, name])
        else:
            answers = []
        return answers


es = EsUtils()
