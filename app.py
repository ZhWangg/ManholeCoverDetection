from flask import Flask, request, jsonify, send_file, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import os
import tensorflow as tf
import cv2
from PIL import Image
import numpy as np
from gevent import pywsgi

# 创建Flask实例
app = Flask(__name__)
app.config['DEBUG'] = True
cors = CORS(app, supports_credentials=True)  # 支持凭证
UPLOAD_FOLDER = 'img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 配置MySQL数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:357885@localhost/manholecover'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '357885'

# 创建数据库实例
db = SQLAlchemy(app)

# 初始化登录管理器
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'basic'
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = "请先登录!"


# 用户模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


# 路由和视图函数
@app.route('/register', methods=['POST'])
def register():
    # 获取前端发来的数据
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password should not be empty"}), 400

    # 检查用户是否已存在
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return jsonify({"error": "User already exists"}), 400

    # 创建新用户并存入数据库
    new_user = User(username=username, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 200


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 获取前端发来的数据
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password should not be empty"}), 400

    # 检查用户是否存在
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({"error": "User does not exist"}), 400

    # 验证密码
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Password is incorrect"}), 400

    # 登录用户
    login_user(user)
    session['logged_in'] = True
    return jsonify({"message": "User logged in successfully"}), 200


@app.route('/logout', methods=['POST'])
# @login_required
def logout():
    # 登出用户
    logout_user()
    session['logged_in'] = False
    return jsonify({"message": "User logged out successfully"}), 200


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 识别部分
@app.route('/UploadImg', methods=['POST'])
# @login_required
def UploadImg():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            nn = file.filename
            filename = "wzh.png"
            file.save(os.path.join("img", filename))
            predict_result = Predict_outcomes()
            data = {"result": "File uploaded successfully", "msg": nn, "predict_result": predict_result}
            return jsonify(data)
        else:
            return jsonify({"error": "No file found"}), 400


@app.route('/img/<filename>')
def get_image(filename):
    image_path = os.path.join('img', filename)
    return send_file(image_path, mimetype='image/jpeg')


def Predict_outcomes():
    model = tf.keras.models.load_model("models/mobilenet_fv2.h5")
    imgtemp = cv2.imread("img/wzh.png")
    imgtemp = cv2.resize(imgtemp, (224, 224))
    cv2.imwrite('img/target.png', imgtemp)
    img = Image.open('img/target.png')
    img = np.asarray(img)
    outputs = model.predict(img.reshape(1, 224, 224, 3))
    class_names = ['井盖完好', '井盖破损', '井盖缺失']
    result_index = int(np.argmax(outputs))
    result = class_names[result_index]
    return result


if __name__ == '__main__':
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app)
    server.serve_forever()
