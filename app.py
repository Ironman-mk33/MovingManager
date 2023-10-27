import os
import datetime
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

# Flaskクラスをインスタンス化して変数appに割り当てる
app = Flask(__name__,static_folder='resources')

# SSL証明書と秘密鍵のファイルパスを指定します
ssl_certfile = 'ssl\cert.pem'  # 証明書のパス
ssl_keyfile = 'ssl\privkey.pem'  # 秘密鍵のパス

# アップロードされた画像を保存するディレクトリを指定
UPLOAD_FOLDER = 'resources\\images\\upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def TopView():
    return render_template('TopPage.html')

@app.route("/ConfirmView")
def ConfirmView():
    return render_template('ConfirmView.html')

@app.route("/RegisterView")
def RegisterView():
    return render_template('RegisterView.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            # ファイルの拡張子を取得
            root, ext = os.path.splitext(image.filename)

            # ファイル名に使う日時を取得
            t_delta = datetime.timedelta(hours=9)
            JST = datetime.timezone(t_delta, 'JST')
            now = datetime.datetime.now(JST)
            image.filename = '{:%Y%m%d%H%M%S}'.format(now) + ext  # 文字列のformatメソッド

            # ファイルの保存先パスを構築
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)

            # 画像を保存
            image.save(file_path)

            # idを取得
            id = request.form.get('barcodeValue', '')

            # テキストデータを取得
            description = request.form.get('description', '')

            # データベースへのアクセス準備
            conn = sqlite3.connect('luggageTable.sqlite3')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO luggage (id,name,description,imagepath,ismoved) VALUES (?,?,?,?,?)", (id,image.filename,description,file_path,False))

            # データベースへの変更を保存
            conn.commit()

            # データベース接続を閉じる
            conn.close()

            return render_template('RegisterView.html')
    return '画像のアップロードに失敗しました'

@app.route('/confirm', methods=['POST'])
def confirm():
    # idを取得
    id = request.form.get('barcodeValue', '')
    # ismovedを取得
    #テキストの情報をBool
    ismoved = request.form.get('ismoved', '')

    # データベースへのアクセス準備
    conn = sqlite3.connect('luggageTable.sqlite3')
    cursor = conn.cursor()
    
    cursor.execute("SELECT ismoved FROM luggage WHERE id = ?", (id,))
    result = cursor.fetchone()

    if result:
        # アイテムが見つかった場合
        new_item_name = "新しいアイテム名"

        # アイテム名を更新
        cursor.execute("UPDATE luggage SET ismoved = ? WHERE id = ?", (ismoved, id))

        # 変更をコミット
        conn.commit()
        print("アイテム名を変更しました。")
    else:
        print("指定したIDのアイテムは見つかりませんでした。")


    # データベースへの変更を保存
    conn.commit()

    # データベース接続を閉じる
    conn.close()

    return render_template('ConfirmView.html')

if __name__ == '__main__':
    app.run(ssl_context=(ssl_certfile, ssl_keyfile),debug=False, host='0.0.0.0', port=443)

