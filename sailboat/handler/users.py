from datetime import datetime
from flask.views import MethodView
from flask import request
import jwt
from datetime import timedelta

from settings import SECRET
from connect import databases
from component.enums import Role, Status, StatusCode
from component.utils import md5_encode


class RegisterHandler(MethodView):

    def post(self):
        username = request.json.get("username")
        pwd = request.json.get("password")
        nick = request.json.get("nick")
        email = request.json.get("email")
        if not username or not pwd or not nick or not email or "@" not in email:
            return {"message": StatusCode.ParameterError.value[0],
                    "data": {},
                    "code": StatusCode.ParameterError.value[1]
                    }, 400

        password = md5_encode(pwd)
        count = databases.user.count_documents({})
        if not count:
            # 首次注册的账户为超级管理员，启动激活
            role = Role.SuperUser.value
            message = {"username": username, "password": password,
                       "nick": nick, "email": email,
                       "role": role, "status": Status.On.value}
        else:
            # 非首次注册账户默认为开发者，且未激活
            role = Role.Developer.value
            message = {"username": username, "password": password,
                       "nick": nick, "email": email,
                       "role": role, "status": Status.Off.value}
        message["create"] = datetime.now()
        # 将信息写入数据库并将相应信息返回给用户
        inserted = databases.user.insert_one(message).inserted_id
        message["id"] = str(inserted)
        message["username"] = username
        message["email"] = email
        message["role"] = role
        message.pop("_id")
        return {"message": "success", "data": message, "code": 201}, 201


class LoginHandler(MethodView):

    def post(self):
        username = request.json.get("username")
        pwd = request.json.get("password")
        password = md5_encode(pwd)
        # 支持用户名或邮箱登录
        query = {"username": username, "password": password}
        name_exit = databases.user.count_documents(query)
        # 校验用户是否存在
        if not name_exit:
            query = {"email": username, "password": password}
        result = databases.user.find_one(query)
        if not result:
            return {"message": StatusCode.NotFound.value[0],
                    "data": {},
                    "code": StatusCode.NotFound.value[1]
                    }, 400
        # 校验用户状态
        status = result.get("status")
        if not status:
            return {"message": StatusCode.UserStatusOff.value[0],
                    "data": {},
                    "code": StatusCode.UserStatusOff.value[1]
                    }, 400
        # 构造生成 Token 所用到的元素，Token 默认八小时过期
        exp = datetime.now() + timedelta(hours=8)
        express = exp.strftime("%Y-%m-%d %H:%M:%S")
        payload = {"username": username, "password": password,
                   "status": status, "role": result.get("role"),
                   "express": express}
        token = str(jwt.encode(payload, SECRET, algorithm='HS256'), "utf8")
        return {"message": "success",
                "data": {
                    "username": username, "role": result.get("role"),
                    "token": token
                },
                "code": 200}