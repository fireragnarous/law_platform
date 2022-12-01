from jina import Document, DocumentArray, Flow, Executor, requests


class FooExecutor(Executor):
    @requests
    def foo(self, docs: DocumentArray, **kwargs):
        docs.append(Document(text='foo was here'))


class BarExecutor(Executor):
    @requests
    def bar(self, docs: DocumentArray, **kwargs):
        docs.append(Document(text='bar was here'))


f = (
    Flow()
    .add(uses=FooExecutor, name='fooExecutor')
    .add(uses=BarExecutor, name='barExecutor')
) # 创建一个空的的Flow


with f:  # 直接启动flow
    response = f.post(
        on= '/'
    )  # 向flow发送请求
    print(response.texts)  # 返回请求结果


# 通过YAML方式将Executor和Flow分开有以下优点：
# 服务器上的数据流是非阻塞和异步的，当 Executor 处于空闲状态时，会立即处理新的请求。
# 必要时会自动添加负载平衡，以确保最大吞吐量。

# 通过YAML方式处理非阻塞异步的数据流


