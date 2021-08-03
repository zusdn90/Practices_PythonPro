class Tire:
    def __repr__(self):
        return "A rubber tire"


class Frame:
    def __repr__(self):
        return "An aluminum frame"


class CarbonFiberFrame:
    def __repr__(self):
        return "A carbon fiber frame"


# 제어반전 사용 전
# class Bicycle:
#     def __init__(self):
#         self.front_tire = Tire()
#         self.back_tire = Tire()
#         self.frame = Frame()

#     def print_specs(self):
#         print(f'Frame: {self.frame}')
#         print(f'Front tire: {self.front_tire}, back tire: {self.back_tire}')

# 제어반전 사용 후
class Bicycle:
    # 종속성은 초기화 작업에 클래스로 전달된다.
    def __init__(self, front_tire, back_tire, frame):
        self.front_tire = Tire()
        self.back_tire = Tire()
        self.frame = frame

    def print_specs(self):
        print(f"Frame: {self.frame}")
        print(f"Front tire: {self.front_tire}, back tire: {self.back_tire}")


if __name__ == "__main__":
    bike = Bicycle(Tire(), Tire(), CarbonFiberFrame())
    bike.print_specs()
