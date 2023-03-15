import urllib.request
import re
import datetime
import json

def validate_characteristics(chars_list):#de forma year, kilometers, fuel, cylindrical_capacity, cu flag pentru prezenta
    result=[False,False,False,False]
    if type(chars_list)!=list:
        return "Characteristics must be a list"
    if len(chars_list)==0:
        return "Characteristics list must not be empty"
    for element in chars_list:
        if type(element)!=str:
            return "All characteristics must be strings"

    for element in chars_list:
        if "km" in element:
            result[1]=True
        elif "cm" in element:
            result[3]=True
        elif "B"==element[0] or "D"==element[0]:
            result[2]=True
        else:
            result[0]=True
            for char in element:
                if not char.isdigit() and char!=' ':
                    result[0]=False
    return result

#print(validate_characteristics(['10000 ', '16 000 km', 'Benzina', '1 998 cm3']))


def articles_to_list_of_dict(articles_list):
    result=[]
    for element in articles_list:
        mini_result={}
        mini_result["date and time"]=str(datetime.datetime.now())

        car_name_pattern = "(?:<h2.*?data-testid=\"ad-card-title\".*?>)(.*?)(?:<\\/h2>)"
        if re.findall(car_name_pattern, element)==[]:
            with open('error_log.txt', 'a') as error_log:
                error_log.write("Error at " + str(datetime.datetime.now()) + " : ")
                error_log.write("Nu s-a gasit numele masinii! Probabil autovit a schimbat formatul pentru numele masinii\n")
                error_log.close()
            return "error"
        mini_result["name"]=re.findall(car_name_pattern, element)[0]

        characteristics_pattern = "(?:<ul.*?data-testid=\"ad-card-characteristics\".*?>)(.*?)(?:<\\/ul>)"
        if re.findall(characteristics_pattern, element)==[]:
            with open('error_log.txt', 'a') as error_log:
                error_log.write("Error at " + str(datetime.datetime.now()) + " : ")
                error_log.write("Nu s-au gasit caracteristicile masinii! Probabil autovit a schimbat formatul pentru caracteristicile masinii\n")
                error_log.close()
            return "error"
        characteristics=re.findall(characteristics_pattern, element)[0]

        splited_characteristics = re.findall("(?:<span.*?>)(.*?)(?:<\\/span>)", element)
        validated_characteristics = validate_characteristics(splited_characteristics)
        if validated_characteristics[0]:
            mini_result["year"]=splited_characteristics[0]
        if validated_characteristics[1]:
            mini_result["kilometers"]=splited_characteristics[1]
        if validated_characteristics[2]:
            mini_result["fuel"]=splited_characteristics[2]
        if validated_characteristics[3]:
            mini_result["cylindrical capacity"]=splited_characteristics[3]

        price_pattern = "(?:<div.*?data-testid=\"ad-card-price\".*?>)(.*?)(?:<\\/div>)"
        if re.findall(price_pattern, element)==[]:
            with open('error_log.txt', 'a') as error_log:
                error_log.write("Error at " + str(datetime.datetime.now()) + " : ")
                error_log.write(
                    "Nu s-a gasit pretul masinii! Probabil autovit a schimbat formatul pentru pretul masinii\n")
                error_log.close()
            return "error"
        unformated_price = re.findall(price_pattern, element)[0]
        formated_price = re.findall("(?:<span.*?>)(.*?)(?:<\\/span>)", unformated_price)[0]
        mini_result["price"] = formated_price+" euro"

        result.append(mini_result)
    return result

def main_article_to_dict(article):
    result={}
    result["date and time"]=str(datetime.datetime.now())
    car_name_pattern = "(?:<h2.*?class=\"e1lmj3dz0 ooa-16u688i er34gjf0\".*?>)(.*?)(?:<\\/h2>)"
    if re.findall(car_name_pattern, article) == []:
        with open('error_log.txt', 'a') as error_log:
            error_log.write("Error at " + str(datetime.datetime.now()) + " : ")
            error_log.write("Nu s-a gasit numele masinii! Probabil autovit a schimbat formatul pentru numele masinii la main car article\n")
            error_log.close()
        return "error"
    result["name"]=re.findall(car_name_pattern, article)[0]

    characteristics_pattern = "(?:<ul.*?class=\"ooa-zzhv62 e16henwp0\".*?>)(.*?)(?:<\\/ul>)"
    if re.findall(characteristics_pattern, article) == []:
        with open('error_log.txt', 'a') as error_log:
            error_log.write("Error at " + str(datetime.datetime.now()) + " : ")
            error_log.write(
                "Nu s-au gasit caracteristicile masinii! Probabil autovit a schimbat formatul pentru caracteristicile masinii la main car article\n")
            error_log.close()
        return "error"
    characteristics=re.findall(characteristics_pattern, article)[0]

    splited_characteristics = re.findall("(?:<span.*?>)(.*?)(?:<\\/span>)", article)
    validated_characteristics = validate_characteristics(splited_characteristics)
    if validated_characteristics[0]:
        result["year"]=splited_characteristics[0]
    if validated_characteristics[1]:
        result["kilometers"]=splited_characteristics[1]
    if validated_characteristics[2]:
        result["fuel"]=splited_characteristics[2]
    if validated_characteristics[3]:
        result["cylindrical capacity"]=splited_characteristics[3]

    price_pattern = "(?:<div.*?data-testid=\"ad-price-value\".*?>)(.*?)(?:<\\/div>)"
    if re.findall(price_pattern, article) == []:
        with open('error_log.txt', 'a') as error_log:
            error_log.write("Error at " + str(datetime.datetime.now()) + " : ")
            error_log.write("Nu s-a gasit pretul masinii! Probabil autovit a schimbat formatul pentru pretul masinii la main car article\n")
            error_log.close()
        return "error"
    unformated_price = re.findall(price_pattern, article)[0]
    formated_price = re.findall("(?:<span.*?>)(.*?)(?:<\\/span>)", unformated_price)[0]
    result["price"] = formated_price+" euro"

    return result

# def convert_list_to_json(list):
#     #https://jsonformatter.curiousconcept.com/
#     result="[\n"
#     size= len(list)
#     i=0
#     for element in list:
#         i+=1
#         j=0
#         number_of_keys = len(element)
#         result+="\t{\n"
#         for key in element:
#             j+=1
#             if j==number_of_keys:
#                 result+="\t\t"+"\""+key+"\""+": "+"\""+element[key]+"\""+"\n"
#             else:
#                 result+="\t\t"+"\""+key+"\""+": "+"\""+element[key]+"\""+",\n"
#         if i==size:
#             result+="\t}\n"
#         else:
#             result+="\t},\n"
#     result+="]"
#     return result
#
#
# def write_json_to_file(json, file_name):
#     lines=[]
#     try:
#         with open(file_name, 'r+') as fp:
#             lines = fp.readlines()
#             fp.seek(0)
#             fp.truncate()
#             fp.writelines(lines[:-1])
#     except:
#         with open('error_log.txt', 'a') as error_log:
#             error_log.write("Error at " + str(datetime.datetime.now()) + " : ")
#             error_log.write("Nu s-a putut scrie/citi din fisierul " + file_name + "\n")
#             error_log.close()
#         return "error"
#
#     try:
#         with open(file_name, 'a') as file:
#             if lines!=[]:
#                 file.write(","+json[1:])
#             else:
#                 file.write(json)
#             file.close()
#     except:
#         with open('error_log.txt', 'a') as error_log:
#             error_log.write("Error at " + str(datetime.datetime.now()) + " : ")
#             error_log.write("Nu s-a putut face append la fisierul " + file_name + "\n")
#             error_log.close()
#         return "error"


def main_function():
    try:
        o = urllib.request.urlopen("https://www.autovit.ro/")
    except:
        print("Error opening the url")
        return
    bytes = o.read()#de tipul byte
    string = bytes.decode()

    #https://uibakery.io/regex-library/html-regex-python

    all_car_articles_pattern="(?:<article.*?class=\"ooa-78awi8 eqsru0t0\".*?>)(.*?)(?:<\\/article>)"
    all_car_articles=re.findall(all_car_articles_pattern, string)
    article_pattern_for_main_car="(?:<article.*?class=\"ooa-yjw0j9 eqsru0t0\".*?>)(.*?)(?:<\\/article>)"
    main_car_article=re.findall(article_pattern_for_main_car, string)

    if all_car_articles==[] or main_car_article==[]:
        with open('error_log.txt', 'a') as error_log:
            error_log.write("Error at "+str(datetime.datetime.now())+" : ")
            error_log.write("Clasele nu au fost gasite! Probabil autovit le-a schimbat :(\n")
            error_log.close()
        return

    if articles_to_list_of_dict(all_car_articles)=="error" or main_article_to_dict(main_car_article[0])=="error":
        with open('error_log.txt', 'a') as error_log:
            error_log.write("Error at "+str(datetime.datetime.now())+" : ")
            error_log.write("Eroare la conversia artiolelor!\n")
            error_log.close()
        return
    cars=articles_to_list_of_dict(all_car_articles)
    cars.append(main_article_to_dict(main_car_article[0]))#primeste un string article, returneaza un dictionar


    # json=convert_list_to_json(cars)
    # write_json_to_file(json, "cars.json")
    with open("cars.json", "r") as loading_file:
        res=json.load(loading_file)#json string to dictionary =lista de dictionare
        for car in cars:
            #print(car)
            res.append(car)

    with open("cars.json", "w") as loading_file:
        json.dump(res, loading_file, indent=2)

main_function()

#https://www.geeksforgeeks.org/schedule-a-python-script-to-run-daily/