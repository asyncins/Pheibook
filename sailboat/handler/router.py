from common import app
from .index import IndexHandler
from .users import RegisterHandler, LoginHandler
from .deploy import DeployHandler
from .timers import TimerHandler


# 为接口设定版本入口
version = "/api/v1"

# 绑定路由与视图类
app.add_url_rule(version + '/', view_func=IndexHandler.as_view(version + '/'))
app.add_url_rule(version + '/reg', view_func=RegisterHandler.as_view(version + '/reg'))
app.add_url_rule(version + '/login', view_func=LoginHandler.as_view(version + '/login'))
app.add_url_rule(version + '/deploy', view_func=DeployHandler.as_view(version + '/deploy'))
app.add_url_rule(version + '/timer', view_func=TimerHandler.as_view(version + '/timer'))



