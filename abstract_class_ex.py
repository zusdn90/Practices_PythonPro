from abc import ABC, abstractclassmethod

class Predator(ABC):
    @abstractclassmethod # 이 메서드가 모든 서브클래스에서 정의되어야 한다.
    def eat(self, prey):
        pass
    
class Bear(Predator):
    def eat(self, prey):
        print(f'Mauling {prey}!')
    def roar(self, message):
        print(message)
        
class Owl(Predator):
    def eat(self, prey):
        print(f'Swooping in on {prey}!')

class Chameleon(Predator):
    def eat(self, prey):
        print(f'Shooting tongue at {prey}!')
        
if __name__ == '__main__':
    bear = Bear()
    bear.eat('deer')
    bear.roar('hello')
    owl = Owl()
    owl.eat('mouse')
    chameleon = Chameleon()
    chameleon.eat('fly')