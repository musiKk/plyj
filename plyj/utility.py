def map_inplace(function, list_):
    try:
        assert isinstance(list_, list)
        for i in range(len(list_)):
            list_[i] = function(list_[i])
    except:
        print


def assert_list(list_, class_or_type_or_tuple):
    try:
        assert isinstance(list_, list)
        for x in list_:
            assert isinstance(x, class_or_type_or_tuple)
    except:
        print