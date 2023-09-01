""" 修饰器集合 """

# official module
# third-party module
# local module


def asEnum(*, can_belower=False, can_repeate=False):
    """ 修饰器，生成一个类对象，使用该对象替代该类名
    - 作为对象后，该对象就能触发__setattr__防止再次赋值
    - 作为对象后，该类名就不能通过__call__继续生成实例 
    - 此枚举化行为默认不允许常量名小写和常量值重复
    ## Param
    `no_islower` - 不允许常量名小写\n
    `no_repeate` - 不允许常量值重复
    ## Return
    类的实例化对象"""

    # 修饰器本体
    def decorator_entity(cls):
        """ 检测常量名和常量值 """
        # 提取自定义类属性的键值
        value_set = set()
        for key, value in vars(cls).items():
            # 过滤内置属性
            if key.startswith('__') and key.endswith('__'):
                continue
            # 仅当不允许小写且存在小写时报错
            assert can_belower or key.isupper(), f'不允许常量名小写，ErrorKey->"{key}"'
            # 仅当不允许重复且存在重复时报错
            assert can_repeate or value not in value_set, f'不允许常量值重复，ErrorKey->"{key}"'
            value_set.add(value)

        """ 生成对象以替代该类 """
        # 建立新的__setattr__方法

        def new_setattr(self, name, value): assert False, '不允许赋值给枚举类型'
        # 覆写旧的__setattr__方法
        cls.__setattr__ = new_setattr
        # 创建实例对象以代替类名
        return cls()
    return decorator_entity
