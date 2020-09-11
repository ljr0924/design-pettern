# 场景：流程化事务，例如审批流程

# 需求：请假申请 项目经理 -》 部门主管 -》 副总经理 -》 总经理

class RequestForm:
    """申请表单"""

    def __init__(self, name, days, reason):
        self.name = name
        self.days = days
        self.reason = reason
        # 初始化表单状态为False
        self.status = False


class Responsible:

    def __init__(self, name, title, next_handler=None):
        self.name = name
        self.title = title
        self.next_handler = next_handler

    def __repr__(self):
        return f'<{self.title}: {self.name}>'

    def _print_info(self):
        return print(f'目前正在由{self}在审批')

    def _print_next(self):
        print(f'正在移交申请审批，{self.next_handler}')

    def _print_success(self, request_form):
        print(f'{request_form.name}的请假申请已通过，共{request_form.days}天\n理由：\n{request_form.reason}')

    def _transfer_request(self, request_form):
        if self.next_handler:
            self.next_handler.handle(request_form)

    def _change_form_status(self, request_form):
        request_form.status = True

    def handle(self, request_form):
        # 打印当前信息
        self._print_info()

        # 处理申请
        self._handle(request_form)

        if request_form.status:
            self._print_success(request_form)
            print('已结束')
            return

        # 移交下一处理人
        self._print_next()
        self._transfer_request(request_form)

    def _handle(self, request):
        raise NotImplementedError()


class ProjectManager(Responsible):
    """项目经理"""

    def _handle(self, request_form):
        if request_form.days < 1:
            self._change_form_status(request_form)


class DepartmentManager(Responsible):
    """部门主管"""

    def _handle(self, request_form):
        if request_form.days <= 3:
            self._change_form_status(request_form)


class SubManager(Responsible):
    """副总经理"""

    def _handle(self, request_form):
        if request_form.days <= 5:
            self._change_form_status(request_form)


class MainManager(Responsible):
    """总经理"""

    def _handle(self, request_form):
        if request_form.days <= 7:
            self._change_form_status(request_form)


if __name__ == '__main__':
    mm = MainManager('Tony', '总经理')
    sm = SubManager('Jenny', '副总经理', mm)
    dm = DepartmentManager('Apple', '部门主管', sm)
    pm = ProjectManager('Orange', '项目经理', dm)

    # 请求表单
    request = RequestForm('GO', 3, '去游乐园')
    # 请求接口人，辛苦了PM！！
    pm.handle(request)