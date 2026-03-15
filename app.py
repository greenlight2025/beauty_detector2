from flask import Flask, render_template, request, jsonify
import base64
import requests
import json

app = Flask(__name__)

# 填入你自己的凭证 [8, 9]
API_KEY = "PqqR2qsx5s6PaswuE9074BfI"
SECRET_KEY = "falnqvP6X59F3iDhYZXlMPN0LzvFJ9LS"


def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    res = requests.post(url, params=params).json()
    return res.get("access_token")


@app.route('/')
def index():
    # 渲染 index.html 页面 [1, 2]
    return render_template('index.html')


@app.route('/detect', methods=['POST'])
def detect():
    file = request.files['file']
    if not file:
        return jsonify({"error_msg": "没有上传文件"})

    # 将图片转为 Base64 [6, 10]
    img_base64 = base64.b64encode(file.read()).decode('utf-8')

    # 调用百度人脸检测接口，请求颜值字段 [3, 6, 7]
    url = "https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token=" + get_access_token()
    payload = json.dumps({
        "image": img_base64,
        "image_type": "BASE64",
        "face_field": "beauty,age,gender"
    })
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, data=payload)
    return response.json()


if __name__ == '__main__':
    app.run(debug=True)
