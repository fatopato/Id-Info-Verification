from urllib import request


def get_sum_of_indexes(idNo, *indexes):
    total = 0
    for index in indexes:
        total += int(idNo[index])
    return total


def is_first_digit_valid(idNo):
    return idNo[0] != '0'


def is_length_valid(idNo):
    return len(idNo) == 11

    
def is_tenth_digit_valid(idNo):
    return (((7*(get_sum_of_indexes(idNo, *range(0,10,2)))) - (get_sum_of_indexes(idNo, *range(1,9,2)))) % 10) == int(idNo[9])

def is_eleventh_digit_valid(idNo):
    return (get_sum_of_indexes(idNo, *range(10))) % 10 == int(idNo[10])

def is_id_no_valid(idNo):
    idNo = str(idNo)
    return (is_length_valid(idNo) and is_first_digit_valid(idNo) and is_tenth_digit_valid(idNo) and is_eleventh_digit_valid(idNo))


def is_info_valid(id_no, name, surname, birth_year):
    print("Requesting the soap...")  
    VALIDATOR = "true"
    INDICATOR = "<TCKimlikNoDogrulaResult>"
    # SOAP request URL
    url = "https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?op=TCKimlikNoDogrula"
    # structured XML
    payload = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
      <TCKimlikNoDogrula xmlns="http://tckimlik.nvi.gov.tr/WS">
        <TCKimlikNo>{id_no}</TCKimlikNo>
        <Ad>{name}</Ad>
        <Soyad>{surname}</Soyad>
        <DogumYili>{birth_year}</DogumYili>
      </TCKimlikNoDogrula>
    </soap:Body>
    </soap:Envelope>"""
    payload = payload.encode('utf-8')
    # headers
    headers = {
      'Content-Type': 'text/xml; charset=utf-8'
    }

    try:
        req = request.Request(url, payload, headers)
        with request.urlopen(req) as f:
            res = f.read()
            response = res.decode()
            parts = response.split(INDICATOR);
            return parts and parts[1].startswith(VALIDATOR)
    except Exception as e:
        print(e)
  
def validate_id_info(id_no, name, surname, birth_year):
    return is_id_no_valid(id_no) and is_info_valid(id_no, name, surname, birth_year)
