'''
Description:
version: 0.1
Author: Shouyan Xia
'''
import paddlehub as hub
import cv2

# 待转换图片的绝对地址
picture = r'image\fangao.jpg'  # 注意代码中此处为双反斜杠
# 风格图片的绝对地址
style_image = r'image\pic.jpg'

# 创建风格转移网络并加载参数
stylepro_artistic = hub.Module(name="stylepro_artistic")

# 读入图片并开始风格转换
result = stylepro_artistic.style_transfer(
    images=[{'content': cv2.imread(picture),
             'styles': [cv2.imread(style_image)]}],
    visualization=True
)

