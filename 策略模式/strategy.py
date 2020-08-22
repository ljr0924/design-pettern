# 需求
# 1.单个商品购买数量大于20个，订单折扣10%
# 2.商品种类超过或等于5个，订单折扣20%
# 3.订单总价超过10000元，订单折扣15%
# 4.客户积分达到2000，折扣7%
from typing import List
from collections import namedtuple

# 客户类，类属性，姓名 积分
Customer = namedtuple('Customer', 'name score')


class LineItem:
    """款项类"""

    def __init__(self, product: str, count: int, price: float) -> None:
        self.product = product
        self.count = count
        self.price = price
        self.total = round(self.price * self.count, 2)

    def __repr__(self):
        return f'商品名称：{self.product}，单价：{self.price}元，数量：{self.count}，总价：{self.total}元'


# Order类，上下文
class Order:
    """订单类"""

    def __init__(self, customer: Customer, cart: List[LineItem], promotion: callable = None) -> None:
        self.customer = customer
        self.cart = cart
        self._promotion = promotion
        self.total = sum(c.total for c in self.cart)
        self._v = 0

    @property
    def promotion(self) -> None:
        pass

    @promotion.setter
    def promotion(self, p: callable) -> None:
        if not callable(p):
            raise ValueError('p不是一个可调用对象')
        self._promotion = p

    def due(self) -> float:
        if not self._promotion:
            discount = 0
        else:
            discount = self._promotion(self)

        return self.total - discount

    def info(self) -> None:
        for line in self.cart:
            print(line)
        print(f'总价：{self.total}，折扣价：{self.due()}')
        print('*' * 20)
        print()


# 具体折扣计算函数
def discount_single_product_num_gte_20(order: Order) -> float:
    """单个商品购买数量大于20个，订单折扣10%"""
    if any(c.count >= 20 for c in order.cart):
        return order.total * 0.10
    return 0


def discount_product_kind_gte_5(order: Order) -> float:
    """商品种类超过5个，订单折扣20%"""
    if len(order.cart) >= 5:
        return order.total * 0.20
    return 0


def discount_total_gte_10000(order: Order) -> float:
    """订单总价超过10000元，订单折扣15%"""
    if order.total >= 10000:
        return order.total * 0.15
    return 0


def discount_score_gte_2000(order: Order) -> float:
    """客户积分达到2000，折扣7%"""
    if order.customer.score >= 2000:
        return order.total * 0.07
    return 0


if __name__ == '__main__':
    c1 = Customer('客户1', 1000)
    c2 = Customer('客户1', 2000)

    # 测试用例

    # 单个商品购买数量大于20个，订单折扣10%
    i1 = LineItem('MacBook', 1, 7000)
    i2 = LineItem('扩展坞', 20, 50)
    i3 = LineItem('Usb type C', 30, 40.0)
    cart1 = [i2]
    cart2 = [i1, i3]
    order1 = Order(c1, cart1, discount_single_product_num_gte_20)
    order1.info()
    order2 = Order(c1, cart2, discount_single_product_num_gte_20)
    order2.info()

    # 商品种类超过5个，订单折扣20%
    i1 = LineItem('MacBook', 1, 7000)
    i2 = LineItem('扩展坞', 20, 50)
    i3 = LineItem('Usb type C1', 30, 40.0)
    i4 = LineItem('Usb type C2', 20, 40.0)
    i5 = LineItem('Usb type C3', 10, 40.0)
    cart3 = [i1, i2, i3, i4, i5]
    order3 = Order(c1, cart1, discount_product_kind_gte_5)
    order3.info()

    # 订单总价超过10000元，订单折扣15%
    order4 = Order(c1, cart3, discount_total_gte_10000)
    order4.info()

    # 客户积分达到2000，折扣7%
    order5 = Order(c2, cart1, discount_score_gte_2000)
    order5.info()

    # 客人希望使用另一个种折扣方式，因为更划算
    order5.promotion = discount_single_product_num_gte_20
    order5.info()
