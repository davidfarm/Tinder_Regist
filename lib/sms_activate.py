from smsactivate.api import SMSActivateAPI

API_KEY = "9cBBf97c5d7f97356e911d9BcB8312f4"
sa = SMSActivateAPI(API_KEY)
sa.debug_mode = False




def get_sms(var1, var2, var3, country1, country2, country3, contry_code1, contry_code2, contry_code3):
    number = sa.getNumberV2(service="oi", country=country1)
    var = contry_code1
    try:
        phone_number = number["phoneNumber"]
        id = number["activationId"]
        phone_number = phone_number[var:]
        country = var1
        return country, phone_number, id
    except:
        number = sa.getNumberV2(service="oi", country=country1)
        var = contry_code1
        try:
            phone_number = number["phoneNumber"]
            id = number["activationId"]
            phone_number = phone_number[var:]
            country = var1
            return country, phone_number, id
        except:
            number = sa.getNumberV2(service="oi", country=country1)
            var = contry_code1
            try:
                phone_number = number["phoneNumber"]
                id = number["activationId"]
                phone_number = phone_number[var:]
                country = var1
                return country, phone_number, id
            except:
                get_sms(var1, var2, var3, country1, country2, country3, contry_code1, contry_code2, contry_code3)



def get_code(id):
    status = sa.getStatus(id)
    code = sa.activationStatus(status)
    return code


#print(get_code(id))
