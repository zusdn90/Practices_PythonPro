import re


def _remove_spaces(query):
    query = query.strip()
    query = re.sub(r"\s+", " ", query)
    return query


def _remove_quotes(query):
    query = re.sub(r'"', "", query)


def _normalize(query):
    query = query.casefold()
    return query


# 단일 진입점 - 공유된 인터페이스를 단순화하기
def clean_query(query):
    query = _remove_spaces(query)
    query = _remove_quotes(query)
    query = _normalize(query)

    return query


# AS-IS 바깥쪽에 영향을 미치는 단단한 결합
# if __name__ == "__main__":
#     search_query = input('Enter your search query: ')
#     search_query = remove_spaces(search_query)
#     search_query = remove_quotes(search_query)
#     search_query = normalize(search_query)
#     print(f'Runnig a seach for "{search_query}"')

# TO-BE
if __name__ == "__main__":
    search_query = input("Enter your search query: ")
    # clean_query 함수를 사용하는 코드는 이제 단일 함수만 호춣하면 되므로 결합도를 줄여 준다.
    search_query = clean_query(search_query)
    print(f'Runnig a seach for "{search_query}"')