def override(parent_class):
    def overrider(method):
        assert(method.__name__ in dir(parent_class))
        return method
    return overrider

