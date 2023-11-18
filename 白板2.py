import random
from abc import ABC, abstractmethod

# 卡类(获取卡号、获取余额、充值、扣款)
class Card(object):
    def __init__(self, card_number, balance=0):
        self._card_number = card_number
        self._balance = balance

    def get_card_number(self):  # 获取卡号
        return self._card_number

    def get_balance(self):          # 获取余额
        return self._balance

    def add_balance(self, amount):  # 向卡上充值
        self._balance += amount
        print(f"Amount {amount} added. ")

    def deduct_balance(self, amount):  # 从卡上扣除费用
        if amount <= self._balance:
            self._balance -= amount
            return True
        else:
            print("Insufficient balance.")
            return False

# 非接触式卡类(继承卡类，添加启用/禁用卡的功能启用卡、禁用卡、检查卡状态等)
class ContactlessCard(Card):
    def __init__(self, card_number, balance=0):
        super().__init__(card_number, balance)
        self.__is_enabled = True

    def enable_card(self):              # 将非接触卡启用
        self.__is_enabled = True

    def disable_card(self):             # 将非接触卡禁用
        self.__is_enabled = False

    def is_card_enabled(self):  # 将方法名修改为 is_card_enabled
        return self.__is_enabled

    def add_balance(self, amount):
        if self.is_card_enabled():
            original_balance = self.get_balance()  # 记录原始余额
            super().add_balance(amount)  # 调用父类的 add_balance 方法
            added_amount = self.get_balance() - original_balance  # 计算实际增加的金额
            if added_amount > 0:  # 只有当实际增加金额大于0时才输出
                print(f"Current balance: {self.get_balance()}")
        else:
            print("Card is disabled. Please enable it before adding balance.")

# 移动应用集成类()
class MobileAppIntegration():
    @abstractmethod
    def make_payment(self, amount):
        pass

# 具体的移动支付服务
class MyMobilePaymentService(object):
    def process_payment(self, amount):
        # 这里模拟实际支付服务的处理逻辑
        print(f"Processing payment of {amount} units")

# 具体的移动应用集成类
class MyMobileAppIntegration(MobileAppIntegration):
    def __init__(self):
        self.payment_service = MyMobilePaymentService()

    def make_payment(self, amount):
        # 在这里调用实际支付服务的支付方法
        self.payment_service.process_payment(amount)
        print(f"Payment of {amount} made via My Mobile App Integration")

# 票价计算类
class FareCalculator(object):
    def calculate_fare(self, distance):
        return distance * 2

# 车辆类(获取车辆信息、更新位置)
class Vehicle(object):
    def __init__(self, vehicle_number):
        self._vehicle_number = vehicle_number

    def get_vehicle_number(self):
        return self._vehicle_number

# 车队管理类
class TransitFleet(object):
    def __init__(self):
        self.__fleet_status = "Active"
        self.__vehicles = []

    def get_fleet_status(self):
        return self.__fleet_status

    def update_fleet_status(self, new_status):
        self.__fleet_status = new_status

    def get_vehicles(self):
        return self.__vehicles

    def add_vehicle(self, vehicle):
        self.__vehicles.append(vehicle)

# 自动收费系统类(AFCS)
class AFCS(MobileAppIntegration, FareCalculator, TransitFleet):
    def __init__(self, membership_program):
        super().__init__()
        initial_balance = 50  # 设置初始余额为50
        self.__card = ContactlessCard(self.generate_random_card_number(), initial_balance)
        self.__membership_program = membership_program  # 存储会员计划的实例

    def generate_random_card_number(self):
        return ' '.join(random.choices('012345679', k=10))

    def make_payment(self, amount, distance):
        fare = self.calculate_fare(distance)  # 计算费用，传入实际距离
        total_amount = amount + fare
        # 尝试从卡上扣除总金额
        if self.__card.is_card_enabled():
            # 使用 add_balance 方法将金额添加到余额中
            self.__card.add_balance(total_amount)  # 更新余额
            print(f"Successfully added {total_amount} to the card balance")
            print("Payment made via mobile app integration")
        else:
            print("Payment failed. Please recharge your card")

    def perform_ride(self, distance):
        # 检查卡是否启用
        if self.__card.is_card_enabled():  # 修正方法名
            fare = self.calculate_fare(distance)
            # 尝试从卡上扣除车费
            if self.__card.deduct_balance(fare):
                print("Payment successful. Enjoy your ride!")
            else:
                print("Payment failed. Please recharge your card")
        else:
            print("Card is disabled. Please enable it before riding.")

    def activate_membership_program(self, new_member):
        # 将新成员添加到会员计划
        self.__membership_program.add_member(new_member)
        print(f"New member {new_member.get_card_number()} added to the membership program.")

        # 运行推荐计划
        self.__membership_program.run_referral_program(new_member)

    def update_membership_program(self):
        # 发送定期提醒，激励会员使用服务
        self.__membership_program.send_periodic_reminder()

    def get_membership_program_members(self):
        # 获取会员计划中的所有会员
        return self.__membership_program.get_members()


# 实时监控类
class RealTimeMonitoring(object):
    def __init__(self, fleet):
        self.__fleet = fleet
    def get_vehicle_location(self, vehicle):
        # 在实际应用中，这里可以使用真实的位置信息获取逻辑，这里只是简单示例
        return f"Current location of vehicle {vehicle.get_vehicle_number()}: {random.randint(1, 100)}, {random.randint(1, 100)}"
    def generate_real_time_report(self):
        # 生成实时报告，包括车队状态和车辆位置
        fleet_status = self.__fleet.get_fleet_status()
        # 获取车队中每辆车的位置信息
        vehicle_locations = {vehicle.get_vehicle_number(): self.get_vehicle_location(vehicle) for vehicle in
                             self.__fleet.get_vehicles()}
        # 将车队状态和车辆位置信息组合成一个报告
        report = {
            "fleet_status": fleet_status,
            "vehicle_locations": vehicle_locations
        }
        return report

# 会员计划类
class MembershipProgram(object):
    def __init__(self):
        self.__members = set()

    def add_member(self, member):
        self.__members.add(member)

    def remove_member(self, member):
        self.__members.remove(member)

    def get_members(self):
        return self.__members

    def send_promotional_offers(self, promotion_message):
        # 发送促销信息给会员
        for member in self.__members:
            member.receive_promotion(promotion_message)

    def send_periodic_reminder(self):
        # 定期提醒会员使用服务
        for member in self.__members:
            member.receive_promotion("Reminder: Enjoy our services and get special discounts!")

    def run_referral_program(self, new_member):
        referral_bonus = 10
        new_member.receive_promotion(f"Welcome! You've received a {referral_bonus}% bonus on your initial balance.")
        referring_member = self.get_referring_member(new_member)
        if referring_member:
            referring_member.receive_promotion(
                f"Congratulations! You've earned a {referral_bonus}% bonus for referring a new member.")

    def get_referring_member(self, new_member):
        return next(iter(self.__members), None)


# 会员类
class Member(object):
    def __init__(self, card, name):
        self.__card = card
        self.__name = name

    def receive_promotion(self, promotion):
        print(f"Received promotion: {promotion}")

    def get_member_id(self):
        return self.__member_id

    def get_card(self):
        return self.__card


if __name__ == "__main__":
    # 创建会员计划实例
    membership_program = MembershipProgram()

    # 创建 ContactlessCard 实例
    contactless_card = ContactlessCard("2344389434", 50)

    # 创建 Member 实例并添加到会员计划
    member1 = Member(contactless_card, "Lucas")
    membership_program.add_member(member1)

    # 创建 AFCS 实例并传递会员计划
    afcs_system = AFCS(membership_program)

    # 打印初始余额
    print(f"Initial Card Balance: {contactless_card.get_balance()}")

    # 发送促销优惠给会员
    membership_program.send_promotional_offers("Special promotional offer for our valued members!")

    # 演示封装：获取卡号并打印
    card_number = contactless_card.get_card_number()
    print(f"Card Number: {card_number}")

    # 创建 Vehicle 对象（Bus001）并将其添加到 AFCS 的车队中
    bus_994 = Vehicle("Bus994")
    afcs_system.add_vehicle(bus_994)

    # 创建 RealTimeMonitoring 实例并传递 AFCS 车队信息
    real_time_monitoring = RealTimeMonitoring(afcs_system)

    # 生成并打印实时报告
    real_time_report = real_time_monitoring.generate_real_time_report()
    print(real_time_report)

    # 演示继承：更新车队状态为 "Under Maintenance"
    afcs_system.update_fleet_status("Under Maintenance")
    print(f"Fleet Status: {afcs_system.get_fleet_status()}")

    # 演示多态性：进行支付操作，传递一个参数和一个距离值
    afcs_system.make_payment(10, 5)  # 传递一个参数和一个距离值

