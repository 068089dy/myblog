from .models import Visitor, Article


visit_type = {
    "ARTICLE": 0,
    "COMMENT": 1,
    "OTHERS": 2,
}

PAGE_SIZE = 10


def visit(v_type, request, remark):
    Visitor.objects.create(
        ip_address=request.META['REMOTE_ADDR'],
        type=v_type,
        remark=remark,
    )


def str2int(data, default=0):
    """
    将字符串转为数字，
    将None或空字符串转为默认值（默认为0）
    """
    return default if data is None or len(data) == 0 else int(data)


def paging(data_list, page_number):
    """
    分页
    :param page_number:
    :param page_size:
    :return:
    """
    if page_number == 'all':
        data_list = data_list.all()
    elif page_number == 'first':
        data_list = data_list.first()
    else:
        if type(page_number) is int:
            page_index = page_number
        else:
            page_index = str2int(page_number, 1)
        page_num = PAGE_SIZE
        begin_index = (page_index - 1) * page_num
        end_index = begin_index + page_num
        data_list = data_list[begin_index: end_index]

    return data_list
