from bs4 import BeautifulSoup
import lxml
import requests
import json

urls = {
    1: 'http://citystar.ru/detal.htm?d=43&b146=12&nm=%D0%9E%D0%B1%D1%8A%D1%8F%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20'
       '%D0%9F%D1%80%D0%BE%D0%B4%D0%B0%D0%BC%20%D0%BD%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1'
       '%8C%20%D0%B2%20%D0%B3.%20%D0%9C%D0%B0%D0%B3%D0%BD%D0%B8%D1%82%D0%BE%D0%B3%D0%BE%D1%80%D1%81%D0%BA%D0%B5%20%D0'
       '%9E%D0%B4%D0%BD%D0%BE%D0%BA%D0%BE%D0%BC%D0%BD%D0%B0%D1%82%D0%BD%D1%83%D1%8E%20%D0%BA%D0%B2%D0%B0%D1%80%D1%82'
       '%D0%B8%D1%80%D1%83',
    2: 'http://citystar.ru/detal.htm?d=43&b146=13&nm=%CE%E1%FA%FF%E2%EB%E5%ED%E8%FF%20%CF%F0%EE%E4%E0%EC%20%ED%E5%E4'
       '%E2%E8%E6%E8%EC%EE%F1%F2%FC%20%E2%20%E3.%20%CC%E0%E3%ED%E8%F2%EE%E3%EE%F0%F1%EA%E5%20%C4%E2%F3%F5%EA%EE%EC%ED'
       '%E0%F2%ED%F3%FE%20%EA%E2%E0%F0%F2%E8%F0%F3',
    3: 'http://citystar.ru/detal.htm?d=43&b146=14&nm=%CE%E1%FA%FF%E2%EB%E5%ED%E8%FF%20%CF%F0%EE%E4%E0%EC%20%ED%E5%E4'
       '%E2%E8%E6%E8%EC%EE%F1%F2%FC%20%E2%20%E3.%20%CC%E0%E3%ED%E8%F2%EE%E3%EE%F0%F1%EA%E5%20%D2%F0%E5%F5%EA%EE%EC%ED'
       '%E0%F2%ED%F3%FE%20%EA%E2%E0%F0%F2%E8%F0%F3',
    4: 'http://citystar.ru/detal.htm?d=43&b146=15&nm=%CE%E1%FA%FF%E2%EB%E5%ED%E8%FF%20%CF%F0%EE%E4%E0%EC%20%ED%E5%E4'
       '%E2%E8%E6%E8%EC%EE%F1%F2%FC%20%E2%20%E3.%20%CC%E0%E3%ED%E8%F2%EE%E3%EE%F0%F1%EA%E5%20%D7%E5%F2%FB%F0%E5%F5%EA'
       '%EE%EC%ED%E0%F2%ED%F3%FE%20%EA%E2%E0%F0%F2%E8%F0%F3'
}


def page_parsing(flat_type, page_number=1):
    '''
    Парсит конркетную страницу по ссылке
    :param flat_type: количество комнат
    :param page_number: номер страницы
    '''
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "max-age=0",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/109.0.0.0 Safari/537.36 "
    }
    params = {
        'pN': page_number
    }
    response = requests.get(urls[flat_type], headers=headers, params=params)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "lxml")
    elements = soup.find('table', class_='tbrd').find('td').find_all('tr', class_='tbb')
    flat_info = []
    for element in elements:
        curr_flat_info = element.find_all('td', class_='ttx')
        if len(curr_flat_info) != 0:
            try:
                item = {
                    'room_number': flat_type,
                    'district': curr_flat_info[2].text,
                    'floor': int(curr_flat_info[4].text.split('/')[0]),
                    'max_floor': int(curr_flat_info[4].text.split('/')[1]),
                    'general_area': float(curr_flat_info[5].text),
                    'living_area': float(curr_flat_info[6].text),
                    'kitchen_area': float(curr_flat_info[7].text),
                    'price': int(curr_flat_info[9].text) * 1000
                }
                flat_info.append(item)
            except:
                continue
    return flat_info


def get_flat_info(flat_type):
    page_number = 1
    parsing_result = page_parsing(flat_type)
    all_flat_info = parsing_result.copy()
    while len(parsing_result) != 0:
        print(f'Данные по {flat_type} квартире со страницы {page_number} собраны')
        page_number += 1
        parsing_result = page_parsing(flat_type, page_number=page_number)
        all_flat_info.extend(parsing_result)
    return all_flat_info


def main():
    result = []
    for flat_type in urls:
        result.extend(get_flat_info(flat_type))
    with open('flat_info.txt', 'w', encoding="utf8") as f:
        json.dump(result, f, ensure_ascii=False)


if __name__ == '__main__':
    main()
