from .models import Visitor, Article


visit_type = {
    "ARTICLE": 0,
    "COMMENT": 1,
    "OTHERS": 2,
}


def visit(v_type, request, remark):
    Visitor.objects.create(
        ip_address=request.META['REMOTE_ADDR'],
        type=v_type,
        remark=remark,
    )
