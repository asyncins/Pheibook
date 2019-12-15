from uuid import uuid4
from datetime import datetime
from flask.views import MethodView
from flask import request

from component.enums import StatusCode
from component.storage import FileStorages
from connect import databases
from component.auth import get_user_info
from common import scheduler
from executor.actuator import performer


storages = FileStorages()


class TimerHandler(MethodView):

    def post(self):
        project = request.json.get('project')
        version = request.json.get('version')
        mode = request.json.get('mode')
        rule = request.json.get('rule')
        if not project or not rule or not version:
            return {"message": StatusCode.ParameterError.value[0],
                    "data": {},
                    "code": StatusCode.ParameterError.value[1]
                    }, 400
        if not storages.exists(project, version):
            return {"message": StatusCode.NotFound.value[0],
                    "data": {},
                    "code": StatusCode.NotFound.value[1]
                    }, 400
        token = request.headers.get("Authorization")
        idn, username, role = get_user_info(token)
        # 生成唯一值作为任务标识
        jid = str(uuid4())
        # 添加任务，这里用双星号传入时间参数
        try:
            scheduler.add_job(performer, mode, id=jid,
                              args=[project, version, mode, rule, jid, idn, username],
                              **rule)
        except Exception as exc:
            return {"message": StatusCode.ParameterError.value[0],
                    "data": {},
                    "code": StatusCode.ParameterError.value[1]
                    }, 400

        # 将信息保存到数据库
        message = {"project": project, "version": version,
                   "mode": mode, "rule": rule,
                   "jid": jid, "idn": idn,
                   "username": username,
                   "create": datetime.now()}
        inserted = databases.timers.insert_one(message).inserted_id
        return {"message": "success",
                "data": {"project": project, "version": version, "jid": jid, "inserted": str(inserted)},
                "code": 201}, 201