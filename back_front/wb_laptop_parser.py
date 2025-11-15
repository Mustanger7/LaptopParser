import wb_laptop_bd_command
import asyncio
from googletrans import Translator


examp = ['Количество фото','Полное название','Бренд','Артикул','Цена со скидкой','Цена без скидки','Оценка','Всего оценок','Список отзывов','Цвет', 'Модель', 'Серия ноутбуков', 'Операционная система', 
'Версия операционной системы', 'Гарантийный срок', 'Диагональ экрана', 'Тип матрицы', 'Разрешение экрана', 'Частота обновления',
'Поверхность экрана', 'Объем оперативной памяти (Гб)', 'Тип оперативной памяти', 'Количество слотов оперативной памяти',
'Расширение оперативной памяти', 'Поддержка карт памяти', 'Емкость аккумулятора', 'Время работы от аккумулятора', 'Процессор', 
'Линейка процессоров', 'Тактовая частота процессора', 'Количество ядер процессора', 'Кэш память', 'Беспроводные интерфейсы', 'Порт USB 2.0',
'Порт USB 3.x', 'Порт USB-C', 'Разъем карт памяти', 'Разъем для наушн./микрофона 3.5мм', 'Разъем HDMI', 'Разъем M.2', 'LAN разъем (RJ45)',
'Интерфейс', 'Веб-камера', 'Объем накопителя SSD', 'Тип накопителя', 'Тип видеокарты', 'Видеокарта', 'Объем памяти видеокарты', 'Материал корпуса', 
'Игровой ноутбук', 'Раскладка клавиатуры', 'Подсветка клавиатуры', 'Доп. опции ноутбука', 'Комплектация', 'Страна производства', 
'Вес без упаковки (кг)', 'Вес с упаковкой (кг)', 'Ширина предмета', 'Глубина предмета', 'Толщина предмета', 'Длина упаковки', 
'Высота упаковки', 'Ширина упаковки']

examp_eng = ['number_of_photos','full_name','brand','product_code','price_with_a_discount','price_without_a_discount','grade','total_assessments','review_list','color','model','a_series_of_laptops',
'operating_system','the_version_of_the_operating_system','warranty_period','the_diagonal_of_the_screen','type_of_matrix','screen_resolution',
'update_frequency','the_surface_of_the_screen','the_ram_volume_gb','type_of_ram','the_number_of_ram_slots','expansion_of_ram','support_for_memory_cards',
'battery_capacity','working_time_from_the_battery','cpu','processor_line','the_processor_clock_frequency','the_number_of_processor_nuclei','cache_memory',
'wireless_interfaces','usb_2_0_port','port_usb_3_x','usb_c_port','memory_card_connector','headphone_microphone_jack_3_5mm','hdmi_connector',
'the_connector_m_2','lan_connector_rj45','interface','webcam','ssd_volume','type_of_drive','type_of_video_card','video_card','the_video_card_volume',
'corps_material','game_laptop','keyboard_layout','keyboard_backlight','additional_laptop_options','complete','the_country_of_production','weight_without_packaging_kg',
'packaging_weight_kg','the_width_of_the_subject','the_depth_of_the_subject','the_thickness_of_the_subject','the_length_of_the_package','the_height_of_the_packaging',
'the_width_of_the_packaging']

def parse_page(page):
    url = f'https://www.wildberries.ru/catalog/0/search.aspx?page={page}&sort=popular&search=%D0%BD%D0%BE%D1%83%D1%82%D0%B1%D1%83%D0%BA'
    service = Service(executable_path="C://Python//project//chromed//chromedriver.exe") 
    browser = webdriver.Chrome(service=service)
    try:
        browser.get(url)
        print(f'Страница {page}. Собираем информацию...')
        time.sleep(5)
      
        i = 0
        while(True):
            goods = browser.find_elements(By.CLASS_NAME, "product-card")
            goods[i].click()
            time.sleep(10)
            
            
            try:
                total_page = browser.find_element(By.CLASS_NAME, 'swiper-pagination-total').get_attribute('textContent')
                total_overall_page = int(total_page) + 2
                print("Всего фото: ", total_overall_page)
            except Exception as e:
                print(e)
            try:
                print("Сохраняем фото...")
                image_links = []
                good_image = browser.find_element(By.XPATH, '//*[@id="imageContainer"]/div/div/img').get_attribute('src')
                for num in range(1,total_overall_page + 1):
                    image_links.append(good_image.replace('1.webp', str(num) + ".webp"))
                filename = good_image.split('/')[-4]
                if os.path.exists(f"C://Python/project//LaptopParser//Laptops//{filename}"):
                    print(f"[INFO] Папка {filename} создана ранее")
                    pass
                else:
                    os.makedirs(f"C://Python/project//LaptopParser//Laptops//{filename}")
                    c = 1
                    for link in image_links:
                        try:
                            urlretrieve(link, f"C://Python/project//LaptopParser//Laptops//{filename}//{filename}_{c}.jpg")
                            c+=1
                        except FileNotFoundError as err:
                            print(err)
                        except HTTPError as err:
                            print(err)
                    print("[INFO] Сохранение завершено")
            except Exception as e:
                print(e)
            try:
                good_fullname = browser.find_element(By.CLASS_NAME, 'product-page__title').text.replace('"','')
            except Exception as e:
                good_fullname = 'Unknown'
            try:
                good_name = browser.find_element(By.XPATH, "//a[@class = 'product-page__header-brand j-wba-card-item j-wba-card-item-show j-wba-card-item-observe']").text
            except Exception as e:
                good_name = 'Unknown'
            try:
                good_id = browser.find_element(By.ID, "productNmId").text
            except Exception as e:
                good_id = 0
            try:    
                price = browser.find_element(By.CLASS_NAME, 'price-block__price-group').text.replace("\n","B").partition("B")[0].replace("₽", '').replace(' ','')
            except Exception as e:
                price = 0
            try:
                old_price = browser.find_element(By.CLASS_NAME, 'price-block__price-group').text.replace("\n","B").split("B")[1].replace("₽", '').replace(' ','')
            except Exception as e:
                old_price = 0
            try:
                review = browser.find_element(By.CLASS_NAME, "product-page__common-info").get_attribute('textContent').strip().replace(',','.').split()[0]
                if review =='Нет':
                    review = 0
                else:
                    pass
            except Exception as e:
                review = 'Нет информации'
            try:
                review_count = browser.find_element(By.CLASS_NAME, "product-page__common-info").get_attribute('textContent').strip().split(' ')[1].replace('оценок','').replace('оценки','').replace('оценка','').replace('\xa0', '').strip()
                if review_count == '':
                    review_count = 0
                else:
                    pass
            except Exception as e:
                review_count = 0

            print(f"Полное название: {good_fullname}\nБренд: {good_name}\nАртикул: {good_id}\nЦена со скидкой: {price}\nЦена без скидки: {old_price}\nОценка: {review}\nВсего оценок: {review_count}")
            time.sleep(1)
            
            attempts = []
            if int((review_count)) > 0:
                while True:
                    browser.execute_script("window.scrollBy(0,350)")
                    try:
                        attempts.append('1')
                        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Смотреть все отзывы'))).click()
                        attempts.clear()
                        break
                    except:
                        if len(attempts)<5:
                            continue
                        else:
                            break
            else:
                print("У данного товара нет отзывов")
            time.sleep(10)

            review_info = []
            def count_review():
                a = []
                b = []
                c = []
                block = browser.find_elements(By.CLASS_NAME, 'feedback__header')
                meaning = browser.find_elements(By.CLASS_NAME, 'feedback__content')
                for el in block:
                    a.append(el.text)
                for mean in meaning:
                    b.append(mean.text.replace('\n', ' '))
                try:
                    j=1
                    for i in range(len(a)):
                        c.append(a[i] +": "+ b[i])
                        d = "Отзыв " + str(j) + ". " + str(c[i]) + "\n"
                        review_info.append(d)
                        j+=1
                except Exception as e:
                    pass
   
            
            count_review()

            if len(review_info)<1:
                review_info.append('Нет отзывов')
            else:
                pass
            review_list = '\n'.join(review_info)
            
            pre_char_list =[]
            char_list = ['Количество фото','Полное название','Бренд','Артикул','Цена со скидкой','Цена без скидки','Оценка','Всего оценок','Список отзывов']
            tex_list = [total_overall_page,good_fullname,good_name,good_id,price,old_price,review,review_count,review_list]

            try:
                browser.find_element(By.LINK_TEXT, 'Назад').click()
            except Exception as e:
                print("Ошибка: ", e)
            time.sleep(3)

            try:
                browser.find_element(By.XPATH, "//button[text()='Характеристики и описание']").click()
            except Exception as e:
                print("Ошибка: ", e)
            time.sleep(3)
    
            try:
                character = browser.find_elements(By.XPATH, "//th[@class = 'product-params__cell']")
            except Exception as e:
                print("Ошибка: ",e)

            for el in character:
                pre_char_list.append(el.text)
            for n in pre_char_list:
                if n not in char_list and n !='':
                    char_list.append(n)

            try:
                tex = browser.find_elements(By.XPATH, "//td[@class = 'product-params__cell']")
            except Exception as e:
                print(e)

            for el in tex:
                tex_list.append(el.text)
            tex_list = [el for el in tex_list if el != '']
            for n in tex_list:
                if n == 'Intel Celeron N 5095' or n == 'Intel Celeron 5095' or n == 'INTEL CERELON N5095' or n == 'INTEL CELERON N5095' or n == 'N5095; Intel Celeron N5095':
                    IndexOfN = tex_list.index(n)
                    tex_list[IndexOfN] = 'Intel Celeron N5095'
                elif n == 'Intel(R) Celeron(R) N5095A':
                    IndexOfN1 = tex_list.index(n)
                    tex_list[IndexOfN1] = 'Intel Celeron N5095A'
                elif n == 'Intel N95':
                    IndexOfN2 = tex_list.index(n)
                    tex_list[IndexOfN2] = 'Intel Processor N95'
                elif 'х' or '×' or '*' in n:
                    IndexOfN3 = tex_list.index(n)
                    tex_list[IndexOfN3] = str(tex_list[IndexOfN3]).replace('х','x').replace('×','x').replace('*','x')
                elif 'Hz' in n:
                    IndexOfN4 = tex_list.index(n)
                    tex_list[IndexOfN4] = str(tex_list[IndexOfN4]).replace('Hz',' Гц')
                elif n == '60Гц':
                    IndexOfN5 = tex_list.index(n)
                    tex_list[IndexOfN5] = '60 Гц'
                elif n == '144Гц':
                    IndexOfN6 = tex_list.index(n)
                    tex_list[IndexOfN6] = '144 Гц'
                else:
                    pass

            insert_list = []
            del_char_list = []
            del_examp = []
            new_char_list = []
            new_tex_list = []

            def sorted():
                try:
                    for j in range(len(examp)): 
                        def sort():
                            for i in range(len(char_list)):
                                if str(char_list[i]).startswith(str(examp[j])):
                                    insert_list.append(tex_list[i])
                                    del_char_list.append(char_list[i])
                                    del_examp.append(examp[j])
                        sort()
        
                    for n in char_list:
                        if n not in del_char_list:
                            index = char_list.index(n)
                            new_char_list.append(n)
                            new_tex_list.append(tex_list[index])

                    for j in examp:
                        if j not in del_examp:
                            index = examp.index(j)
                            insert_list.insert(index, "Нет информации")
                        else:
                            pass
                    
                    if insert_list[17] == "1920x1080 FHD":
                        insert_list[17] = "1920x1080"
                    else:
                        pass

                    if insert_list[20] == "4"  or insert_list[20] == "4ГБ" or insert_list[20] == "4 ГБ" or insert_list[20] == "4Гб"  or insert_list[20] == "4гб" or insert_list[20] == "4 гб" or insert_list[20] == "4096 Мб" or insert_list[20] == "4Gb" or insert_list[20] == "4 Gb" or insert_list[20] == "4 GB" or insert_list[20] == "4GB":
                        insert_list[20] = "4 Гб" 
                    elif insert_list[20] == "6" or insert_list[20] == "6ГБ" or insert_list[20] == "6 ГБ" or insert_list[20] == "6Гб"  or insert_list[20] == "6гб" or insert_list[20] == "6 гб" or insert_list[20] == "6144 Мб" or insert_list[20] == "6Gb" or insert_list[20] == "6 Gb" or insert_list[20] == "6 GB" or insert_list[20] == "6GB":
                        insert_list[20] = "6 Гб"
                    elif insert_list[20] == "8" or insert_list[20] == "8ГБ" or insert_list[20] == "8 ГБ" or insert_list[20] == "8Гб"  or insert_list[20] == "8гб" or insert_list[20] == "8 гб" or insert_list[20] == "8192 Мб" or insert_list[20] == "8Gb" or insert_list[20] == "8 Gb" or insert_list[20] == "8 GB" or insert_list[20] == "8GB":
                        insert_list[20] = "8 Гб"
                    elif insert_list[20] == "12" or insert_list[20] == "12ГБ" or insert_list[20] == "12 ГБ" or insert_list[20] == "12Гб"  or insert_list[20] == "12гб" or insert_list[20] == "12 гб" or insert_list[20] == "12288 Мб" or insert_list[20] == "12Gb" or insert_list[20] == "12 Gb" or insert_list[20] == "12 GB" or insert_list[20] == "12GB":
                        insert_list[20] = "12 Гб"
                    elif insert_list[20] == "16" or insert_list[20] == "16ГБ" or insert_list[20] == "16 ГБ" or insert_list[20] == "16Гб"  or insert_list[20] == "16гб" or insert_list[20] == "16 гб" or insert_list[20] == "16384 Мб" or insert_list[20] == "16Gb" or insert_list[20] == "16 Gb" or insert_list[20] == "16 GB" or insert_list[20] == "16GB":
                        insert_list[20] = "16 Гб"
                    elif insert_list[20] == "32" or insert_list[20] == "32ГБ" or insert_list[20] == "32 ГБ" or insert_list[20] == "32Гб"  or insert_list[20] == "32гб" or insert_list[20] == "32 гб" or insert_list[20] == "32768 Мб" or insert_list[20] == "32Gb" or insert_list[20] == "32 Gb" or insert_list[20] == "32 GB" or insert_list[20] == "32GB":
                        insert_list[20] = "32 Гб"
                    elif insert_list[20] == "64" or insert_list[20] == "64ГБ" or insert_list[20] == "64 ГБ" or insert_list[20] == "64Гб"  or insert_list[20] == "64гб" or insert_list[20] == "64 гб" or insert_list[20] == "65536 Мб" or insert_list[20] == "64Gb" or insert_list[20] == "64 Gb" or insert_list[20] == "64 GB" or insert_list[20] == "64GB":
                        insert_list[20] = "64 Гб"
                    else:
                        pass

                    if insert_list[43] == "256" or insert_list[43] == "256гб" or insert_list[43] == "256 гб" or insert_list[43] == "256Гб" or insert_list[43] == "256ГБ" or insert_list[43] == "256 ГБ" or insert_list[43] == "256Gb" or insert_list[43] == "256 Gb" or insert_list[43] == "256 GB" or insert_list[43] == "256GB":
                        insert_list[43] = "256 Гб"
                    elif insert_list[43] == "512" or insert_list[43] == "512гб" or insert_list[43] == "512 гб" or insert_list[43] == "512Гб" or insert_list[43] == "512ГБ" or insert_list[43] == "512 ГБ" or insert_list[43] == "512Gb" or insert_list[43] == "512 Gb" or insert_list[43] == "512 GB" or insert_list[43] == "512GB":
                        insert_list[43] = "512 Гб"
                    elif insert_list[43] == "1024" or insert_list[43] == "1024гб" or insert_list[43] == "1024 гб" or insert_list[43] == "1024Гб" or insert_list[43] == "1024ГБ" or insert_list[43] == "1024 ГБ" or insert_list[43] == "1024Gb" or insert_list[43] == "1024 Gb" or insert_list[43] == "1024 GB" or insert_list[43] == "1024GB" or insert_list[43] == "1ТБ; 1TB" or insert_list[43] == "1ТБ" or insert_list[43] == "1TB" or insert_list[43] == "1TB" or insert_list[43] == "1 TB" or insert_list[43] == "1 ТБ" or insert_list[43] == "1 Tb" or insert_list[43] == "1Tb":
                        insert_list[43] = "1024 Гб"
                    else:
                        pass

                    if insert_list[47] == "1" or insert_list[47] == "1гб" or insert_list[47] == "1 гб" or insert_list[47] == "1Гб" or insert_list[47] == "1ГБ" or insert_list[47] == "1 ГБ" or insert_list[47] == "1Gb" or insert_list[47] == "1 Gb" or insert_list[47] == "1 GB" or insert_list[47] == "1GB" or insert_list[47] == "1024Мб" or insert_list[47] == "1024Mb" or insert_list[47] == "1024МБ" or insert_list[47] == "1024MB" or insert_list[47] == "1024 МБ" or insert_list == "1024 Mb" or insert_list[47] == "1024 MB":
                        insert_list[47] = "1024 Мб"
                    elif insert_list[47] == "2" or insert_list[47] == "2гб" or insert_list[47] == "2 гб" or insert_list[47] == "2Гб" or insert_list[47] == "2ГБ" or insert_list[47] == "2 ГБ" or insert_list[47] == "2Gb" or insert_list[47] == "2 Gb" or insert_list[47] == "2 GB" or insert_list[47] == "2GB" or insert_list[47] == "2048Мб" or insert_list[47] == "2048Mb" or insert_list[47] == "2048МБ" or insert_list[47] == "2048MB" or insert_list[47] == "2048 МБ" or insert_list == "2048 Mb" or insert_list[47] == "2048 MB":
                        insert_list[47] = "2048 Мб"
                    elif insert_list[47] == "4" or insert_list[47] == "4гб" or insert_list[47] == "4 гб" or insert_list[47] == "4Гб" or insert_list[47] == "4ГБ" or insert_list[47] == "4 ГБ" or insert_list[47] == "4Gb" or insert_list[47] == "4 Gb" or insert_list[47] == "4 GB" or insert_list[47] == "4GB" or insert_list[47] == "4096Мб" or insert_list[47] == "4096Mb" or insert_list[47] == "4096МБ" or insert_list[47] == "4096MB" or insert_list[47] == "4096 МБ" or insert_list == "4096 Mb" or insert_list[47] == "4096 MB":
                        insert_list[47] = "4096 Мб"
                    elif insert_list[47] == "6" or insert_list[47] == "6гб" or insert_list[47] == "6 гб" or insert_list[47] == "6Гб" or insert_list[47] == "6ГБ" or insert_list[47] == "6 ГБ" or insert_list[47] == "6Gb" or insert_list[47] == "6 Gb" or insert_list[47] == "6 GB" or insert_list[47] == "6GB" or insert_list[47] == "6144Мб" or insert_list[47] == "6144Mb" or insert_list[47] == "6144МБ" or insert_list[47] == "6144MB" or insert_list[47] == "6144 МБ" or insert_list == "6144 Mb" or insert_list[47] == "6144 MB":
                        insert_list[47] = "6144 Мб"
                    elif insert_list[47] == "8" or insert_list[47] == "8гб" or insert_list[47] == "8 гб" or insert_list[47] == "8Гб" or insert_list[47] == "8ГБ" or insert_list[47] == "8 ГБ" or insert_list[47] == "8Gb" or insert_list[47] == "8 Gb" or insert_list[47] == "8 GB" or insert_list[47] == "8GB" or insert_list[47] == "8192Мб" or insert_list[47] == "8192Mb" or insert_list[47] == "8192МБ" or insert_list[47] == "8192MB" or insert_list[47] == "8192 МБ" or insert_list == "8192 Mb" or insert_list[47] == "8192 MB":
                        insert_list[47] = "8192 Мб"
                    elif insert_list[47] == "16" or insert_list[47] == "16гб" or insert_list[47] == "16 гб" or insert_list[47] == "16Гб" or insert_list[47] == "16ГБ" or insert_list[47] == "16 ГБ" or insert_list[47] == "16Gb" or insert_list[47] == "16 Gb" or insert_list[47] == "16 GB" or insert_list[47] == "16GB" or insert_list[47] == "16384Мб" or insert_list[47] == "16384Mb" or insert_list[47] == "16384МБ" or insert_list[47] == "16384MB" or insert_list[47] == "16384 МБ" or insert_list == "16384 Mb" or insert_list[47] == "16384 MB":
                        insert_list[47] = "16384 Мб"
                    else:
                        pass

                except Exception as e:
                    print(e)

            sorted()
            
            translated_new_char_list = []
            
            async def TranslateColumns():
                async with Translator() as translator:
                    for i in new_char_list:
                        result = await translator.translate(i, src="ru", dest="en")
                        b = result.text.replace(" ", '_')
                        translated_new_char_list.append(b)
            asyncio.run(TranslateColumns()) 

            final_rus_char_list = examp + new_char_list
            final_char_list = examp_eng + translated_new_char_list 
            final_tex_list = insert_list + new_tex_list

            if len(translated_new_char_list) > 0:
                count = 1
                for l in translated_new_char_list:
                    column = str(l).lower().replace('(','').replace(')','').replace('pcs.','').replace('-','_').replace('.','_').replace('/','_').replace(';','_').replace(',','_').replace('__','_')
                    print(f'Проверяем наличие новой колонки в БД:  "{column}..." ({count} из {len(translated_new_char_list)})')
                    count += 1 
                    try:
                        if wb_laptop_bd_command.check_column(column) == 0:
                            wb_laptop_bd_command.column_query(column)
                            print('[INFO] Колонка добавлена в БД')
                    except Exception as ex:
                        print('[X] Ошибка вставки колонки в бд: ', ex)
                        continue
            else:
                pass

            try:
                colonka = final_char_list
                meaning = final_tex_list
                a = '&'.join(colonka)
                b = a.replace('(','').replace(')','').replace('/','_').replace('.','_').replace('-','_').replace(';','_').replace('pcs.','').replace(',','_').replace('&',',').replace('__','_')
                e = '&&^&&'.join(meaning)
                f = "&&" + e + "&&"
                g = f.replace("'",'').replace("&&","'").replace('"', '').replace(',','.').replace('^',',')
                title = final_tex_list[3]
                print(f'Парсим товар:  "{title}..." ') 
                try:
                    if wb_laptop_bd_command.check_news(title) == 0:
                        wb_laptop_bd_command.insert_news(b,g)
                        print('[INFO] Товар добавлен в БД')
                except Exception as ex:
                    print('[X] Ошибка вставки данных в бд: ', ex)
            except Exception as ex:
                print("Ошибка: ", ex)    

            try:
                browser.find_element(By.XPATH, "//a[@class = 'j-close popup__close close']").click()
            except Exception as e:
                print("Ошибка: ", e)
            time.sleep(3)

            try:
                browser.find_element(By.XPATH, "//button[@class = 'breadcrumbs__back j-toggle-button-arrow']").click()
            except Exception as e:
                print("Ошибка: ", e)
            time.sleep(3)

            i+=1
    except Exception as ex:
        print(ex)
        browser.quit()
    browser.quit() 
 
    
def article():
    while(True): 
        try:
            print("\n")
            param = int(input("Введите артикул: "))  
            if param==0:
                print("Значение должно быть больше 0. Попробуйте снова...")
            else: 
                return str(param)
        except ValueError:
            print("Ошибка. Введите число...")
        
def interval():
    while(True): 
        try:
            print("\n")
            param = int(input("Введите значение,от: "))
            if param==0:
                print("Значение должно быть больше 0. Попробуйте снова...")
            else:
                while(True): 
                    try:
                        param2 = int(input("Введите значение,до: "))
                        if param2==0:
                            print("Значение должно быть больше 0. Попробуйте снова...")
                        else:
                            return str(param) + " and " + str(param2)
                    except ValueError:
                        print("Ошибка. Введите целое число или число с дробной частью после точки...")
        except ValueError:
            print("Ошибка. Введите целое число или число с дробной частью после точки...") 

def interval2():
    while(True): 
        try:
            print("\n")
            param = float(input("Введите значение,от: "))
            if param==0:
                print("Значение должно быть больше 0. Попробуйте снова...")
            else:
                while(True): 
                    try:
                        param2 = float(input("Введите значение,до: "))
                        if param2==0:
                            print("Значение должно быть больше 0. Попробуйте снова...")
                        else:
                            return "'" + str(param) + "'" + " and " + "'" + str(param2) + "'"
                    except ValueError:
                        print("Ошибка. Введите целое число или число с дробной частью после точки...")
        except ValueError:
            print("Ошибка. Введите целое число или число с дробной частью после точки...") 

choice_list = []
new_data_info2 = []
def rolling_list(parameter):
    try:
        data_info = wb_laptop_bd_command.get_distinct_data_from_db(parameter)
        new_data_info = str(data_info).replace('[','').replace("('None',)",'').replace("('Нет информации',)",'').replace(',), ]','').replace(']','').replace(',),','&&').replace(',)','').replace(',','').replace('(0','').replace('  (','').replace(' (','').replace("'",'').replace('(','',1).split('&&')
        b = len(new_data_info)
        for n in new_data_info:
            if n not in choice_list:
                new_data_info2.append(n)
        lis = []
        j = 0
        for i in range(1,len(new_data_info2)+1):
            lis.append(str(i) + "." + new_data_info2[j])
            j+=1
        a = '\n'.join(lis)
        while(True): 
            try:
                print("\n")
                choice = int(input(f"Выберите: \n{a} "))
                match choice:
                    case (choice): choice = new_data_info2[choice -1]
                choice_list.append(choice)
                new_data_info2.clear()
                if len(choice_list)<b:
                    while(True):
                        try:
                            print("\n")
                            choice2 = int(input("Добавить другое значение этого фильтра: 1.Да 2.Нет "))
                            match choice2:
                                case 1: return rolling_list(parameter)
                                case 2: break
                        except(ValueError,IndexError):
                            print("Ошибка ввода. Попробуйте снова...")
                else:
                    print("\nЗначение добавлено.Вы выбрали все возможные значения фильтра")
                w = '&^&'.join(choice_list)
                m = "&" + w + "&"
                u = m.replace("'",'').replace("&","'").replace('"', '').replace(',','.').replace('^',',')
                choice_list.clear()
                return u
            except (ValueError,IndexError):
                print("Ошибка ввода. Попробуйте снова...")
    except Exception as ex:
        print('[X] Ошибка: ', ex)


def make_final_rus_columns():
    new_rus_columns = []
    data_columns = wb_laptop_bd_command.get_columns_from_db()
    all_eng_columns = str(data_columns).replace('[','').replace(']','').replace("('",'').replace("',)",'').replace(' ','').replace('_',' ').split(',')
    new_eng_columns = all_eng_columns[64:]

    async def Translate_Db_Columns():
        async with Translator() as translator:
            for i in new_eng_columns:
                result = await translator.translate(i, src="en", dest="ru")
                c = result.text
                new_rus_columns.append(c)
    asyncio.run(Translate_Db_Columns())

    final_rus_columns = examp + new_rus_columns
    return final_rus_columns

def get_information():
    final_rus_columns = make_final_rus_columns()
    query = "select * from features where "
    for f_name, f_val in features.items():
        if str(f_name).endswith('between'):
            query += f_name+ " " + str(f_val) + " and "
        else:
            query += f_name+ " (" + str(f_val) + ")" + " and "

    if query.endswith(" and "):
        query = query.removesuffix(" and ")
    
    key_eng_list = []
    value_list = []
    key_rus_list = []
    for key in features.keys():
        key_eng_list.append(key)
    for value in features.values():
        value_list.append(value)
    for j in range(len(key_eng_list)): 
        def sort():
            for i in range(len(examp)):
                if str(key_eng_list[j]).startswith(str(examp_eng[i])):
                    key_rus_list.append(examp[i])
        sort()

    features.clear()
    print("\nВыбранные фильтры: ")
    for i in range(len(key_rus_list)):
        print(str(key_rus_list[i])+": "+ str(value_list[i]).replace('and','-').replace('.0',''))
    print("\n")

    try:
        data_set = wb_laptop_bd_command.get_filtr_from_db(query)
        if len(data_set)>0:
            print("Нашлось результатов: ", len(data_set))
            print("\n")
            j = 1
            for d in data_set:
                print("Ноутбук: ",j)
                for i in range(1,len(final_rus_columns)+1):
                    if str(d[i]) != "Нет информации" and str(d[i]) != "None" and str(d[i]) != "0" and str(d[i]).startswith("Отзыв")==False and str(d[i]).startswith("Нет отзывов")==False:
                        print(str(final_rus_columns[i-1]).capitalize() +": "+ str(d[i]))
                print(str(final_rus_columns[8]).capitalize() +":\n "+ str(d[9]))
                print("\n")
                j+=1
        else:
            print("\nТакого товара нет в базе")
    except Exception as ex:
        print("Ошибка: ", ex)
    
choice_list1 = []
data_list2 = []
data_list_length = []
def select_operation():
    data_list=['Бренд','Цена со скидкой','Операционная система','Диагональ экрана','Тип матрицы',
'Разрешение экрана','Частота обновления экрана','Объём оперативной памяти',
'Процессор','Объём накопителя SSD','Видеокарта','Объём памяти видеокарты',
'Цвет','Артикул','Оценка']
    data_list_length.append(len(data_list))
    while(True):
        try:
            for n in data_list:
                if n not in choice_list1:
                    data_list2.append(n)
            lis = []
            j = 0
            for i in range(1,len(data_list2)+1):
                lis.append(str(i) + "." + data_list2[j])
                j+=1
            a = '\n'.join(lis)
            print("\n")
            selection = int(input(f"Выберите фильтр:\n{a} "))
            selection_text = data_list2[selection-1]
            data_list2.clear()
            if selection_text in choice_list1:
                print("\nВы уже добавили этот фильтр. Выберите другой...")
                return select_operation()
            else:
                choice_list1.append(selection_text)
                if selection_text == 'Бренд':
                    features["brand in"] = rolling_list('brand')
                if selection_text == 'Цена со скидкой':
                    features["price_with_a_discount between"] = interval()
                if selection_text == 'Операционная система':   
                    features["operating_system in"] = rolling_list('the_version_of_the_operating_system')
                if selection_text == 'Диагональ экрана':
                    features["the_diagonal_of_the_screen between"] = interval2()
                if selection_text == 'Тип матрицы':
                    features["type_of_matrix in"] = rolling_list('type_of_matrix')
                if selection_text == 'Разрешение экрана':
                    features["screen_resolution in"] = rolling_list('screen_resolution')
                if selection_text == 'Частота обновления экрана':
                    features["update_frequency in"] = rolling_list('update_frequency')
                if selection_text == 'Объём оперативной памяти':
                    features["the_ram_volume_gb in"] = rolling_list('the_ram_volume_gb')
                if selection_text == 'Процессор':
                    features["cpu in"] = rolling_list('cpu')
                if selection_text == 'Объём накопителя SSD':
                    features["ssd_volume in"] = rolling_list('ssd_volume')
                if selection_text == 'Видеокарта':
                    features["video_card in"] = rolling_list('video_card')
                if selection_text == 'Объём памяти видеокарты':
                    features["the_video_card_volume in"] = rolling_list('the_video_card_volume')
                if selection_text == 'Цвет':
                    features["color in"] = rolling_list('color')
                if selection_text == 'Артикул':
                    features["product_code in"] = article()
                if selection_text == 'Оценка':
                    features["grade between"] = interval2() 
                break
        except ValueError:
            print("Ошибка. Введите номер фильтра...")

def select_operation2():
    while(True):
        try:
            if len(choice_list1)<data_list_length[0]:
                print("\n")
                selection2 = int(input("Показать результат: 1.Да 2.Добавить ещё фильтр "))
                match selection2:
                    case 1: choice_list1.clear(), get_information()
                    case 2: select_operation(), select_operation2()
                    case _: print("Ошибка ввода. Попробуйте снова..."), select_operation2()
            else:
                print("\nВы выбрали все возможные фильтры")
                choice_list1.clear(), get_information()
            break
        except Exception as e:
            print("Ошибка ввода. Попробуйте снова...")

def select_further_operation():
    while(True):
        try:
            choice_list1.clear()
            print("\n")
            selection = int(input("Выберите дальнейшие действия: 1.Выбрать фильтры заново 2.Завершить работу "))
            match selection:
                case 1: select_operation(), select_operation2()
                case 2: break
                case _: print("Ошибка ввода. Попробуйте снова...")
        except ValueError:
            print("Ошибка ввода. Попробуйте снова...")        

def parser():
    while True:
        try:
            for page in range(1,2):
                parse_page(page)
            break
        except:
            print('произошла ошибка в процессе парсинга\n'
              'Перезапуск...')
        
features = {}
if __name__ == '__main__':
    while True:
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.common.by import By
            import time
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait
            from urllib.error import HTTPError
            from urllib.request import urlretrieve
            import os
            parser()
            select_operation()
            select_operation2()
            select_further_operation()
            break
        except:
            print('произошла ошибка данных при вводе, проверте правильность введенных данных,\n'
                'Перезапуск...')
