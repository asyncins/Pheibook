"""运行指定的包"""
import sys
import importlib
from pathlib import Path, PurePath


def execute(egg, project):
    """将egg路径添加到sys.path
    导入egg包
    最后调用egg包中的fetch()方法
    """
    sys.path.insert(0, str(egg))
    project = importlib.import_module(project)
    # 执行egg包中的fetch方法
    project.main()


if __name__ == '__main__':
    # egg包路径
    file = PurePath.joinpath(Path.cwd(), 'fabia', 'sails-1.5-py3.7.egg')
    execute(file, 'sails')
