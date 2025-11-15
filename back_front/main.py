from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
import wb_laptop_bd_command
import wb_laptop_parser
 

app = FastAPI()

app.mount("/static", StaticFiles(directory="CSS"))
 
app.mount("/image", StaticFiles(directory="Laptops"))

@app.get("/")
def root():
    return FileResponse("index.html")
 
@app.get("/filtrs")
def filtrs():
        parameters = ["brand","operating_system","type_of_matrix","screen_resolution",
                      "update_frequency","the_ram_volume_gb","cpu","ssd_volume","video_card",
                      "the_video_card_volume","color","grade","price_with_a_discount","the_diagonal_of_the_screen"]
        b =[]
        for param in parameters:
            def getFil():   
                try:
                    data_info = sorted(wb_laptop_bd_command.get_distinct_data_from_db(param))
                    new_data_info = str(data_info).replace('[','').replace("('None',)",'').replace("('Нет информации',)",'').replace("('Unknown',)", '').replace("('0',)",'').replace("Decimal(",'').replace(',), ]','').replace(']','').replace(',),','&&').replace(',)','').replace(',','').replace('  (','').replace(' (','').replace("'",'').replace('(','',1).replace(")",'').split('&&')
                    b.append(new_data_info)
                except Exception as ex:
                    print("Ошибка: ", ex)
            getFil()
        
        def sorting():
            for i in range(0,len(t)):
                for n in range(i+1,len(t)):
                    if int(str(t[n]).split()[0])<int(str(t[i]).split()[0]):
                        t[n],t[i] = t[i],t[n]

        k = [b[4],b[5],b[7],b[9]]
        for t in k:
            if 'sma' in t:
                t.remove('sma')
                sorting()
                t.append('sma')
            else:
                sorting()

        minPrice = min(b[12])
        maxPrice = max(b[12])
        minDiagonal = min(b[13])
        maxDiagonal = max(b[13])

        return {"brand":f"{b[0]}","operatingSystem":f"{b[1]}",
                "typeOfMatrix":f"{b[2]}","screenResolution":f"{b[3]}",
                "updateFrequency":f"{b[4]}","theRamVolumeGb":f"{b[5]}",
                "cpu":f"{b[6]}","ssdVolume":f"{b[7]}",
                "videoCard":f"{b[8]}","theVideoCardVolume":f"{b[9]}",
                "color":f"{b[10]}","grade":f"{b[11]}","minPrice":f"{minPrice}",
                "maxPrice":f"{maxPrice}","minDiagonal":f"{minDiagonal}",
                "maxDiagonal":f"{maxDiagonal}"}


@app.post("/postdata")
def postdata(data= Body()):
    features = {}
    features1 = {}
    for el in data["selectedList"]:
        features[el] = data["selectedList"][el]

    key_eng_list = []
    value_list = []
    key_rus_list = []
    value_order = ""
    inform = "<div id='resumeDiv'>"
    inform+= "<div class='divSpanFirst'><span class='chosenSpan'>Выбранные фильтры: </span>"
    final_rus_columns = wb_laptop_parser.make_final_rus_columns()
    query = "select * from features where "
    for f_name, f_val in features.items():
        key_eng_list.append(f_name)
        if(str(f_name)=="price_with_a_discount" or str(f_name)=="the_diagonal_of_the_screen"):
            if "[" in str(f_val):
                query += f_name+ " between " + str(f_val).replace("[","").replace("]","").replace(","," and ") + " and "
                value_list.append(str(f_val).replace("[","").replace("]","").replace(", ","-").replace("'",""))
            else:
                query += f_name+ " >= " + "'" + str(f_val) + "'" + " and "
                value_list.append("от " + str(f_val))
        else:
            if str(f_name)=="allfiltrs":
                query = query.removesuffix(" where ")
                inform += "все ноутбуки</div>"
            else:
                if "[" in str(f_val):
                    query += f_name+ " in " + str(f_val).replace("[","(").replace("]",")") + " and "
                    value_list.append(str(f_val).replace("[","").replace("]","").replace("'",""))
                else:
                    query += f_name+ " = " + "'" + str(f_val) + "'" + " and "
                    value_list.append(str(f_val))

    if query.endswith(" and "):
        query = query.removesuffix(" and ")

    for el in data["selectedOrderList"]:
        features1[el] = data["selectedOrderList"][el]
    for f_val in features1.values():
        if str(f_val)=="priceUp":
            query+= " order by price_with_a_discount"
            value_order+= " по возрастанию цены"
        elif str(f_val)=="priceDown":
            query+= " order by price_with_a_discount desc"
            value_order+= " по убыванию цены"
        else:
            query+= " order by grade desc"
            value_order+= " по рейтингу"

   
    for j in range(len(key_eng_list)): 
        def sort():
            for i in range(len(wb_laptop_parser.examp)):
                if str(key_eng_list[j]).startswith(str(wb_laptop_parser.examp_eng[i])):
                    key_rus_list.append(wb_laptop_parser.examp[i])
        sort()
    
    for i in range(len(key_rus_list)):
        if len(key_rus_list)>1:
            inform+= str(key_rus_list[i])+": "+ str(value_list[i]) + ", "
        else:
            inform+= str(key_rus_list[i])+": "+ str(value_list[i])
    inform+= "</div>"

    inform+= "<div class='divSpan'><span class='chosenSpan'>Сортировано: </span>"
    inform+= value_order + "</div>"
    

    try:
        data_set = wb_laptop_bd_command.get_filtr_from_db(query)
        if len(data_set)>0:
            inform+= "<div class='divSpan'><span class='chosenSpan'>Нашлось результатов: </span>"
            inform+= f"{len(data_set)}" + "</div>"
            inform+= "</div>"
            j = 1
            shortListChar=[]
            listChar=[]
            for d in data_set:
                number_of_photo = d[1]
                article = d[4]
                inform+= "<div class='shortTableDiv'>"
                inform+= "<div class='laptop'><span class='laptopSpan'>Ноутбук: "+ str(j) +"</span></div>"
                inform+= "<table class='shortTable'>"
                inform+= "<tbody>"
                for i in range(2,12):
                    if str(d[i]) != "Нет информации" and str(d[i]) != "None" and str(d[i]) != "0" and str(d[i]).startswith("Отзыв")==False and str(d[i]).startswith("Нет отзывов")==False:
                        shortListChar.append("<tr><td class='shortTableFirstTd'>" + str(final_rus_columns[i-1]).capitalize() + ": " + "</td>" + "<td>" + str(d[i]) + "</td></tr>")
                if len(shortListChar)>0:
                    for i in range(len(shortListChar)):
                        inform += shortListChar[i]
                    shortListChar.clear()
                inform+= "</tbody>"
                inform+= "</table>"
                inform+= "</div>"
                inform+= "<div class='longTableDiv'>"
                inform+= "<div class='tableTitle'>Все характеристики и описание</div>"
                inform+= "<table class='longTable'>"
                inform+= "<tbody>"
                for i in range(2,16):
                    if str(d[i]) != "Нет информации" and str(d[i]) != "None" and str(d[i]) != "0" and str(d[i]).startswith("Отзыв")==False and str(d[i]).startswith("Нет отзывов")==False:
                        listChar.append("<tr><td class='longTableFirstTd'>" + str(final_rus_columns[i-1]).capitalize() + "</td>" + "<td class='longTableSecondTd'>" + str(d[i]) + "</td></tr>")
                if len(listChar)>0:
                    inform+= "<tr><td class='tableChar' colspan='2'><br>Основная информация</td></tr>"
                    for i in range(len(listChar)):
                        inform += listChar[i]
                    listChar.clear()

                for i in range(16,21):
                    if str(d[i]) != "Нет информации" and str(d[i]) != "None" and str(d[i]) != "0" and str(d[i]).startswith("Отзыв")==False and str(d[i]).startswith("Нет отзывов")==False:
                        listChar.append("<tr><td class='longTableFirstTd'>" + str(final_rus_columns[i-1]).capitalize() + "</td>" + "<td class='longTableSecondTd'>" + str(d[i]) + "</td></tr>")
                if len(listChar)>0:
                    inform+= "<tr><td class='tableChar' colspan='2'><br>Экран</td></tr>"
                    for i in range(len(listChar)):
                        inform += listChar[i]
                    listChar.clear()

                for i in range(21,26):
                    if str(d[i]) != "Нет информации" and str(d[i]) != "None" and str(d[i]) != "0" and str(d[i]).startswith("Отзыв")==False and str(d[i]).startswith("Нет отзывов")==False:
                        listChar.append("<tr><td class='longTableFirstTd'>" + str(final_rus_columns[i-1]).capitalize() + "</td>" + "<td class='longTableSecondTd'>" + str(d[i]) + "</td></tr>")
                if len(listChar)>0:
                    inform+= "<tr><td class='tableChar' colspan='2'><br>Память</td></tr>"
                    for i in range(len(listChar)):
                        inform += listChar[i]
                    listChar.clear()

                for i in range(26,28):
                    if str(d[i]) != "Нет информации" and str(d[i]) != "None" and str(d[i]) != "0" and str(d[i]).startswith("Отзыв")==False and str(d[i]).startswith("Нет отзывов")==False:
                        listChar.append("<tr><td class='longTableFirstTd'>" + str(final_rus_columns[i-1]).capitalize() + "</td>" + "<td class='longTableSecondTd'>" + str(d[i]) + "</td></tr>")
                if len(listChar)>0:
                    inform+= "<tr><td class='tableChar' colspan='2'><br>Питание</td></tr>"
                    for i in range(len(listChar)):
                        inform += listChar[i]
                    listChar.clear()
                    
                for i in range(28,32):
                    if str(d[i]) != "Нет информации" and str(d[i]) != "None" and str(d[i]) != "0" and str(d[i]).startswith("Отзыв")==False and str(d[i]).startswith("Нет отзывов")==False:
                        listChar.append("<tr><td class='longTableFirstTd'>" + str(final_rus_columns[i-1]).capitalize() + "</td>" + "<td class='longTableSecondTd'>" + str(d[i]) + "</td></tr>")
                if len(listChar)>0:
                    inform+= "<tr><td class='tableChar' colspan='2'><br>Процессор</td></tr>"
                    for i in range(len(listChar)):
                        inform += listChar[i]
                    listChar.clear()

                for i in range(32,33):
                    if str(d[i]) != "Нет информации" and str(d[i]) != "None" and str(d[i]) != "0" and str(d[i]).startswith("Отзыв")==False and str(d[i]).startswith("Нет отзывов")==False:
                        listChar.append("<tr><td class='longTableFirstTd'>" + str(final_rus_columns[i-1]).capitalize() + "</td>" + "<td class='longTableSecondTd'>" + str(d[i]) + "</td></tr>")
                if len(listChar)>0:
                    inform+= "<tr><td class='tableChar' colspan='2'><br>Связь</td></tr>"
                    for i in range(len(listChar)):
                        inform += listChar[i]
                    listChar.clear()

                for i in range(33,42):
                    if str(d[i]) != "Нет информации" and str(d[i]) != "None" and str(d[i]) != "0" and str(d[i]).startswith("Отзыв")==False and str(d[i]).startswith("Нет отзывов")==False:
                        listChar.append("<tr><td class='longTableFirstTd'>" + str(final_rus_columns[i-1]).capitalize() + "</td>" + "<td class='longTableSecondTd'>" + str(d[i]) + "</td></tr>")
                if len(listChar)>0:
                    inform+= "<tr><td class='tableChar' colspan='2'><br>Интерфейсы и разъёмы</td></tr>"
                    for i in range(len(listChar)):
                        inform += listChar[i]
                    listChar.clear()
                
                for i in range(42,43):
                    if str(d[i]) != "Нет информации" and str(d[i]) != "None" and str(d[i]) != "0" and str(d[i]).startswith("Отзыв")==False and str(d[i]).startswith("Нет отзывов")==False:
                        listChar.append("<tr><td class='longTableFirstTd'>" + str(final_rus_columns[i-1]).capitalize() + "</td>" + "<td class='longTableSecondTd'>" + str(d[i]) + "</td></tr>")
                if len(listChar)>0:
                    inform+= "<tr><td class='tableChar' colspan='2'><br>Коммуникации и мультимедиа</td></tr>"
                    for i in range(len(listChar)):
                        inform += listChar[i]
                    listChar.clear()

                for i in range(43,45):
                    if str(d[i]) != "Нет информации" and str(d[i]) != "None" and str(d[i]) != "0" and str(d[i]).startswith("Отзыв")==False and str(d[i]).startswith("Нет отзывов")==False:
                        listChar.append("<tr><td class='longTableFirstTd'>" + str(final_rus_columns[i-1]).capitalize() + "</td>" + "<td class='longTableSecondTd'>" + str(d[i]) + "</td></tr>")
                if len(listChar)>0:
                    inform+= "<tr><td class='tableChar' colspan='2'><br>Накопители данных</td></tr>"
                    for i in range(len(listChar)):
                        inform += listChar[i]
                    listChar.clear()
                
                for i in range(45,48):
                    if str(d[i]) != "Нет информации" and str(d[i]) != "None" and str(d[i]) != "0" and str(d[i]).startswith("Отзыв")==False and str(d[i]).startswith("Нет отзывов")==False:
                        listChar.append("<tr><td class='longTableFirstTd'>" + str(final_rus_columns[i-1]).capitalize() + "</td>" + "<td class='longTableSecondTd'>" + str(d[i]) + "</td></tr>")
                if len(listChar)>0:
                    inform+= "<tr><td class='tableChar' colspan='2'><br>Видеокарта</td></tr>"
                    for i in range(len(listChar)):
                        inform += listChar[i]
                    listChar.clear()

                for i in range(48,49):
                    if str(d[i]) != "Нет информации" and str(d[i]) != "None" and str(d[i]) != "0" and str(d[i]).startswith("Отзыв")==False and str(d[i]).startswith("Нет отзывов")==False:
                        listChar.append("<tr><td class='longTableFirstTd'>" + str(final_rus_columns[i-1]).capitalize() + "</td>" + "<td class='longTableSecondTd'>" + str(d[i]) + "</td></tr>")
                if len(listChar)>0:
                    inform+= "<tr><td class='tableChar' colspan='2'><br>Материалы</td></tr>"
                    for i in range(len(listChar)):
                        inform += listChar[i]
                    listChar.clear()

                for i in range(49,55):
                    if str(d[i]) != "Нет информации" and str(d[i]) != "None" and str(d[i]) != "0" and str(d[i]).startswith("Отзыв")==False and str(d[i]).startswith("Нет отзывов")==False:
                        listChar.append("<tr><td class='longTableFirstTd'>" + str(final_rus_columns[i-1]).capitalize() + "</td>" + "<td class='longTableSecondTd'>" + str(d[i]) + "</td></tr>")
                if len(listChar)>0:
                    inform+= "<tr><td class='tableChar' colspan='2'><br>Дополнительная информация</td></tr>"
                    for i in range(len(listChar)):
                        inform += listChar[i]
                    listChar.clear()

                for i in range(56,63):
                    if str(d[i]) != "Нет информации" and str(d[i]) != "None" and str(d[i]) != "0" and str(d[i]).startswith("Отзыв")==False and str(d[i]).startswith("Нет отзывов")==False:
                        listChar.append("<tr><td class='longTableFirstTd'>" + str(final_rus_columns[i-1]).capitalize() + "</td>" + "<td class='longTableSecondTd'>" + str(d[i]) + "</td></tr>")
                if len(listChar)>0:
                    inform+= "<tr><td class='tableChar' colspan='2'><br>Габариты</td></tr>"
                    for i in range(len(listChar)):
                        inform += listChar[i]
                    listChar.clear()

                for i in range(63,len(final_rus_columns)+1):
                    if str(d[i]) != "Нет информации" and str(d[i]) != "None" and str(d[i]) != "0" and str(d[i]).startswith("Отзыв")==False and str(d[i]).startswith("Нет отзывов")==False:
                        listChar.append("<tr><td class='longTableFirstTd'>" + str(final_rus_columns[i-1]).capitalize() + "</td>" + "<td class='longTableSecondTd'>" + str(d[i]) + "</td></tr>")
                if len(listChar)>0:
                    inform+= "<tr><td class='tableChar' colspan='2'><br>Прочие характеристики</td></tr>"
                    for i in range(len(listChar)):
                        inform += listChar[i]
                    listChar.clear()

                inform+= "</tbody>"
                inform+= "</table>"
                inform+= "</div>"
                inform+= f'<div class="photo_main" id="main{j}/{number_of_photo}">'
                for i in range (1,number_of_photo + 1):
                    app.mount(f"/image{article}", StaticFiles(directory=f"Laptops/{article}"))
                    inform+= f'<div class="img_viewer" id="{j}/{i}/{number_of_photo}" style="display:none">'
                    inform+= f'<div class="viewer_wrapper"><div class="viewer_rightarrow" id="{j}/{i}">&#x21E8;</div><div class="viewer_leftarrow" id="{j}/{i}">&#x21E6;</div><span class="close">&times;</span><img  class="modal_content" ></div></div>'
                inform+= f'<div class="photo_box" id="boxin{j}"><div class="arrowRightBackGround"><div class="rightarrow">&#x2192;</div></div><div class="arrowLeftBackGround"><div class="leftarrow">&#x2190;</div></div>'
                inform+= f'<div class="photo_box_wrapper" id="{j}/{number_of_photo}">'
                for i in range (1,number_of_photo + 1):
                    app.mount(f"/image{article}", StaticFiles(directory=f"Laptops/{article}"))
                    inform+= f'<div  class="img_container" id="container{j}/{i}"><img src="image{article}/{article}_{i}.jpg"  class="img_source" /></div>'
                inform+= '</div>'
                inform+= '</div>'
                inform+= '</div>'
                inform+= '<div class="review_title">' + str(final_rus_columns[8]).capitalize() + '</div>'
                inform+= '<div class="review_body">'
                review_lis = str(d[9]).split("Отзыв")
                review_count = len(review_lis)
                for i in range(review_count):
                    inform+= review_lis[i]+"<br>"
                inform+= "</div>"
                j+=1
        else:
            inform+= "<p>" + "Такого товара нет в базе" + "</p>"
    except Exception as ex:
        print("Ошибка: ", ex)
    return {"inform":f"{inform}"}
