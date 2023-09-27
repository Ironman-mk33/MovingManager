import os
from flask import Flask, render_template, request, redirect, url_for

#Flaskクラスをインスタンス化して変数appに割り当てる
app = Flask(__name__)

# アップロードされた画像を保存するディレクトリを指定
UPLOAD_FOLDER = 'D:\Documents\Develop\projects\Python\MovingManager\Images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            # ファイルの保存先パスを構築
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            # 画像を保存
            image.save(file_path)
            return '画像がアップロードされました: ' + image.filename
    return '画像のアップロードに失敗しました'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)