### 测试环境配置要求

```shell
milvus=1.1.0
torch>=1.11.0
transformer
sentence-transformer=1.1.0
pymysql
pandas
...
pyechart
numpy
...
```



### 文件说明

```shell
--Text_Encode_for_Neural_Retrival.ipynb # 文本编码向量最小化demo
--test_20_data.xlsx # Text_Encode_for_Neural_Retrival生成中间文件
--test_data_hash.json # Text_Encode_for_Neural_Retrival生成中间文件

## 其他相关测试
--MilvusDemo.ipynb # 使用milvus向量搜索库进行查询的最小Demo
--Vectorial_Method.ipynb # Lawform向量方法与Iosmap测试
--my_results1.html # Vectorial_Method 向量表示渲染结果测试

## 具体的实现内容说明在.ipynb中注释。
```

