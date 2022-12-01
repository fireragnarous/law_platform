from jina import Document,DocumentArray

# d = (
#     Document(uri = 'apple.png')
#     .load_uri_to_image_tensor()
#     .set_image_tensor_shape(shape=(224, 224))
#     .set_image_tensor_normalization()
#     .set_image_tensor_channel_axis(-1,0) # 图片通道变换
# )
#
#
# print(d.tensor, d.tensor.shape)
#
#
# # 你可以使用 save_image_tensor_to_file 将 tensor 转为图像。当然，因为做了预处理，图片返回时损失了很多信息。
# d.save_image_tensor_to_file('apple-proc.png', channel_axis=0) # 因为前面进行了预处理，channel_axis应该设为0


d = Document(uri = 'large_image.png')
d.load_uri_to_image_tensor()
print(d.tensor.shape)

#d.convert_image_tensor_to_sliding_windows(window_shape=(32,32)) # 使用32 * 32 的滑动窗口切割原图
#print(d.tensor.shape)

# 可以通过as_chunks=True将切割的图块添加到Document块中
# d.convert_image_tensor_to_sliding_windows(window_shape=(32,32), as_chunks=True)
# print(d.chunks)
#
#
# d.chunks.plot_image_sprites('simpsons-chunk.png')

#可以通过设置 strides 参数进行过采样
d.convert_image_tensor_to_sliding_windows(window_shape=(32,32), strides=(10,10) ,as_chunks=True)
print(d.chunks)


d.chunks.plot_image_sprites('simpsons-chunk_over.png')
