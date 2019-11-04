def Singleton(clazz):
    """Decorator for class to build singleton pattern."""
    instances = {}

    def getinstance(*args, **kwargs):
        if clazz not in instances:
            instances[clazz] = clazz(*args, **kwargs)
        return instances[clazz]

    return getinstance
