from enum import Enum


class Role(Enum):
    """用户角色
    SuperUser 角色的数值设为 100
    Developer 角色的数值设为 10
    Other 角色的数值设为 1
    Anonymous 角色的数值设为 0
    """
    SuperUser = 100
    Developer = 10
    Other = 1
    Anonymous = 0


class Status(Enum):
    """用户状态
    已激活状态用 On 表示，数值设为 1
    未激活状态用 Off 表示，数值设为 0
    """
    On = 1
    Off = 0


class StatusCode(Enum):
    """错误提示
    """
    NoAuth = ("no auth", 403)
    MissingParameter = ("missing parameter", 4001)
    IsNotYours = ("is not yours", 4002)
    ParameterError = ("parameter error", 4003)
    UserStatusOff = ("user status off", 4004)
    NotFound = ("not found", 4005)
    JsonDecodeError = ("JSONDecode Error", 4006)
    PathError = ("path error", 4007)
    OperationError = ("operation error", 4008)
    TokenOverdue = ("token overdue", 4009)


