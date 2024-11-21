

class Manager:
    def __init__(self) -> None:
        pass
        # cls_name = self.class_name()
        # G.setG(cls_name, self)
        # print('管理器%s已全局注册'%cls_name)

    @classmethod
    def class_name(cls):
        return cls.__name__

