from jina import Document

# d = Document( uri = 'toy.mp4')
# d.load_uri_to_video_tensor()
#
# print(d.tensor.shape)
#
# # 视频相比于图象是一个四维数组，其中第一维为帧数，通过帧ID可以索引全部的视频图像
#
# # 按照append方法将Document放入chunk中
# for b in d.tensor:
#     d.chunks.append(Document(tensor=b))
#
# d.chunks.plot_image_sprites('mov.png')



#我们从视频中提取的图像，很多都是冗余的，可以使用 only_keyframes 这个参数来提取关键帧：
# d = Document( uri='toy.mp4')
# d.load_uri_to_video_tensor(only_keyframes=True)
# print(d.tensor.shape)


#使用save_video_tensor_to_file进行视频的保存
d = (
    Document( uri = 'toy.mp4')
    .load_uri_to_video_tensor()
    .save_video_tensor_to_file('60fps.mp4', 60)

)