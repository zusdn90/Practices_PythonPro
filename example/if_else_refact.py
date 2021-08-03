import random
import request
import json

FOODs = [
    "pizza",
    "burgers",
    "salad",
    "soup",
]


def random_food(request):
    food = random.choice(FOODs)

    # 추가되는 각각의 요구사항은 새로운 조건문이 되며 복잡도를 증가시킨다.

    # AS-IS
    if request.headers.get("Accept") == "application/json":
        return json.dumps({"food": food})
    elif request.headers.get("Accept") == "application/xml":
        return f"<response><food>{food}</food></response>"
    else:
        return food
    return food

    # TO-BE
    formats = {
        "application/json": to_json,
        "application/xml": to_xml,
    }

    format_function = formats.get(request.headers.get("Accept"), lambda val: val)

    return format_function(food)


# 관심사를 두개의 함수로 분리하기
def refact_random_food(request):
    food = random.choice(FOODs)

    format_function = get_format_function(request.headers.get("Accept"))

    return format_function(food)


def get_format_function(accept=None):
    formats = {
        "application/json": to_json,
        "application/xml": to_xml,
    }

    return formats.get(accept, lambda val: val)


def to_json(food):
    return json.dumps({"food": food})


def to_xml(food):
    return f"<response><food>{food}</food></response>"
