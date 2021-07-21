# 리스코프 치환 가능성을 깨뜨리는 서브클래스
class Slug:
    def __init__(self, name):
        self.name = name
    
    def crawl(self):
        print('simple trail!')

class Snail(Slug):
    # Snail은 Slug로 부터 상속되는데 서로 다른 인스턴스 생성자를 사용하는 것은 
    # 치환 가능성을 위반하는 일바적인 방법이다.
    def __init__(self, name, shell_size):
        super().__init__(name)
        self.name = name
        self.shell_size = shell_size

def race(gastropod_one, gastropod_two):
    gastropod_one.crawl()
    gastropod_two.crawl()

if __name__ == '__main__':
    race(Slug('Geoffrey'), Slug('Ramona'))
    race(Snail('Geoffrey'), Snail('Ramona'))