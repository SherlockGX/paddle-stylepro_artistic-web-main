'''
Descripttion:
version:
Author:
Date:
LastEditTime:
'''
from re import T
from flask.helpers import send_from_directory
import paddlehub as hub
from pypinyin import lazy_pinyin
import time
from werkzeug.utils import secure_filename
import cv2
import os
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
#下载paddle的模型
stylepro_artistic = hub.Module(name="stylepro_artistic")#第一次自动下载并保存，之后不再下载
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])  # 设置允许的文件格式

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.send_file_max_age_default = timedelta(seconds=1)  # 设置静态文件缓存过期时间

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 首页，上传图片页
@app.route('/', methods=['GET'])
def index():
    return render_template("main.html")




@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # print('post')
        base_path = os.path.dirname(os.path.realpath(__file__))  # 获取脚本路径
        upload_path_con = os.path.join(base_path, 'static\images\source')  # 上传文件目录
        upload_path_sty = os.path.join(base_path, 'static\images\denstion')  # 上传文件目录

        if not os.path.exists(upload_path_con):  # 判断文件夹是否存在
            os.makedirs(upload_path_con)
        if not os.path.exists(upload_path_sty):  # 判断文件夹是否存在
            os.makedirs(upload_path_sty)

        filedata_con = request.files.get('content')  # 获取前端对象
        filedata_sty = request.files.get('style')  # 获取前端对象

        if not (filedata_con and filedata_sty and allowed_file(filedata_con.filename)and allowed_file(filedata_sty.filename) ):  # 检查文件类型
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
        sj=int(time.time())
        file_path_con = os.path.join(upload_path_con, secure_filename(''.join(lazy_pinyin(str(sj)+filedata_con.filename))))  # 指定保存文件夹的路径
        file_path_sty = os.path.join(upload_path_sty, secure_filename(''.join(lazy_pinyin(str(sj)+filedata_sty.filename))))  # 指定保存文件夹的路径

        # 将上传的文件进行保存
        filedata_con.save(file_path_con)
        filedata_sty.save(file_path_sty)

        output_dir='static/result/'+str(sj)
        os.makedirs(output_dir)

        result = stylepro_artistic.style_transfer(
                images=[{'content': cv2.imread(file_path_con),
                        'styles': [cv2.imread(file_path_sty)]}],
                visualization=True,
                output_dir='static/result/'+str(sj)
            )

        print(file_path_con,file_path_sty)
        orgin= 'static\images\source'+os.sep+file_path_con.split('\\')[-1]
        style='static\images\denstion'+os.sep+file_path_sty.split('\\')[-1]
        print(orgin,style)
        return render_template('main.html',result=output_dir+os.sep+os.listdir(output_dir)[0],orgin=orgin,style=style)



@app.route('/down/<filename>/')
def down(filename):
    dir=os.getcwd()+os.sep+'static/file'
    print(dir+filename)
    return send_from_directory(dir,filename,as_attachment=True)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8987, debug=True, use_reloader=False)