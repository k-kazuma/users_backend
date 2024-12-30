from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import check_password_hash
from dotenv import load_dotenv
import os

# 後で環境変数へ移動する予定
URI = 'mysql+pymysql://root:Amhl0248110!@127.0.0.1/admin'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    pw = db.Column(db.String(100), nullable=False)

@app.route("/")
def get_users():
    users = Users.query.all()
    print(users)
    return jsonify([{"id": user.id, "pw": user.pw} for user in users])

@app.route("/login", methods=["POST"])
def login_user():
    
    # フロントエンドからのリクエストデータ 
    data = request.json

    # 入力がない場合のエラーハンドリング
    if not data:
        return jsonify({"error": "Invalid input"}), 400  

    user_id = data.get("user")
    user_pw = data.get("password")

    if not user_id or not user_pw:
        return jsonify({"error": "Missing username or password"}), 400

    # DBから管理者情報取得
    user = Users.query.filter_by(id=user_id).first()
    if user:
        # パスワードを検証
        if check_password_hash(user.pw, user_pw):  # ハッシュ化されたパスワードを検証
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid password"}), 401
    else:
        return jsonify({"error": "User not found"}), 404
    

if __name__ == '__main__':
 
    app.run(debug=True)