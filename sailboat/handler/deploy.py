import time
from datetime import datetime
from flask.views import MethodView
from flask import request

from component.enums import StatusCode
from component.storage import FileStorages
from connect import databases
from component.auth import get_user_info


storages = FileStorages()


class DeployHandler(MethodView):

    def post(self):
        """项目部署接口"""
        project = request.form.get('project')
        remark = request.form.get('remark')
        file = request.files.get('file')
        if not project or not file:
            # 确保参数和值存在
            return {"message": StatusCode.MissingParameter.value[0],
                    "data": {},
                    "code": StatusCode.MissingParameter.value[1]
                    }, 400
        filename = file.filename
        if not filename.endswith('.egg'):
            # 确保文件类型正确
            return {"message": StatusCode.NotFound.value[0],
                    "data": {},
                    "code": StatusCode.NotFound.value[1]
                    }, 400
        version = int(time.time())
        content = file.stream.read()
        # 将文件存储到服务端
        result = storages.put(project, version, content)
        if not result:
            # 存储失败则返回相关提示
            return {"message": StatusCode.OperationError.value[0],
                    "data": {},
                    "code": StatusCode.OperationError.value[1]
                    }, 400

        token = request.headers.get("Authorization")
        idn, username, role = get_user_info(token)
        message = {"project": project,
                   "version": str(version),
                   "remark": remark or "Nothing",
                   "idn": idn,
                   "username": username,
                   "create": datetime.now()}
        databases.deploy.insert_one(message).inserted_id
        message["_id"] = str(message.pop("_id"))
        return {"message": "success",
                "data": message,
                "code": 201}, 201