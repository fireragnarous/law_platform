# 导入document, executor, flow, requests 装饰器
from jina import DocumentArray, Executor, requests, Document

# 编写基本的FooExecutor, BarExecutor类。
# 该函数从网络请求中获取documentArray

class FooExecutor(Executor):
    @requests
    def foo(self, docs: DocumentArray, **kwargs):
        docs.append(Document(text='foo was here'))


class BarExecutor(Executor):
    @requests
    def bar(self, docs: DocumentArray, **kwargs):
        docs.append(Document(text='bar was here'))


        