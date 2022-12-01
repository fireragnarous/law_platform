from jina import Document,DocumentArray

# d = Document(text = '_______________hello world____________')
# print(d.text)
#
# # d = Document(uri='https://www.baidu.com/')
# # d.load_uri_to_text()
# # print(d.text)
#
# d = Document(text='👋	नमस्ते दुनिया!	你好世界！こんにちは世界！	Привет мир!')
# print(d.text)
#
# d = Document(text='👋	नमस्ते दुनिया!	你好世界! こんにちは世界!	Привет мир!')
# d.chunks.extend([Document(text=c) for c in d.text.split('!')])  # 按'!'分割,分割位chunk
# d.summary()




# 最简单的文本向量编码方式：将文本按照单词出现数量进行编码
# da = DocumentArray([Document(text='hello world'),
#                     Document(text='goodbye world'),
#                     Document(text='hello goodbye')])
#
# vocab = da.get_vocabulary() # 输出:{'hello':2, 'world':3, 'goodbye': 4}
#
#
# # 转为ndarray
# for d in da:
#     d.convert_text_to_tensor(vocab, max_length=10)
#     print(d.tensor)
#
#
# for d in da:
#     d.convert_tensor_to_text(vocab)
#     print(d.text)




# 简单文本匹配Demo，建立文本库和哈希索引
d = Document(uri='https://www.gutenberg.org/files/1342/1342-0.txt').load_uri_to_text() # 获取文本
da = DocumentArray(Document(text= s.strip()) for s in d.text.split('\n') if s.strip()) # 将文本切分为句子
da.apply(lambda d: d.embed_feature_hashing()) # 为句子建立哈希编码


# 匹配文本特征编码
q = (
    Document(text='she entered the room') # 要匹配的文本
    .embed_feature_hashing()  # 通过哈希编码进行匹配
    .match(da, limit=5, exclude_self=True, metric='jaccard', use_scipy=True) # 找到5个最相似文本，输出为与jaccard相似程度
)


print(q.matches[:,('text','scores__jaccard')])



