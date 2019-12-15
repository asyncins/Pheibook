from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from connect import client

app = Flask(__name__)

# 将任务信息存储到 MongoDB
store = {"default": MongoDBJobStore(client=client)}
# 初始化 APSchduler
scheduler = BackgroundScheduler(jobstores=store)
