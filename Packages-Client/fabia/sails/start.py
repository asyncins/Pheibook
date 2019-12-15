import logging
import requests


def main():
    # 向电子工业出版社官网发出网络请求
    response = requests.get('https://www.phei.com.cn/')
    # 打印响应状态码
    print(response.status_code)
    logging.warning("Throw out warning")
    logging.error("Throw out error")
    print(response.text)
    raise ValueError("Throw out ValueError")