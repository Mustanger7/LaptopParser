Laptop Parser - это проект, который позволяет собирать характеристики ноутбуков и отзывы о них с сайта Wildberries для удобного просмотра в браузере с возможностями фильтрации и сортировки.

Back-end на основе Python собирает и сохраняет информацию в базу данных PostgreSQL.
Фотографии ноутбуков сохраняются в папку внутри проекта.
Реализован функционал интерактивного подбора модели ноутбука через терминал.

Front-end выполнен с использованием Javascript и представляет сайт для поиска ноутбуков с фильтрацией по 15-ти категориям и сортировкой по трём параметрам.
Веб-сервер на базе фреймворка FastAPI отвечает за обработку запросов от клиента.

Pipeline в Jenkins позволяет осуществлять сборку проекта по расписанию. В процессе сборки создаются два контейнера Docker.

Преимущества проекта:
1. Сокращает количество переходов по страницам для просмотра искомой информации.
2. Содержит 15 фильтров, включая поиск по артикулу, а также 3 вида сортировки, что обеспечивает гибкость и персонализированный подход.
3. Динамическое добавление новых характеристик в базу данных с последующим отображением на сайте. 
4. Надёжность хранения информации позволяет вернуться к просмотру ноутбуков в любое удобное время.
5. Адаптивный дизайн для комфортного подбора ноутбука на любом устройстве.


Демонстрация работы back-end

![Back_1](https://github.com/user-attachments/assets/ce12c527-a477-49bf-8672-f34fc9642c01)
![Back_2](https://github.com/user-attachments/assets/7d056450-39b4-40ab-a191-895468b9f560)
![Back_3](https://github.com/user-attachments/assets/4cc0c319-bf6e-4c83-9dcd-2a3fb33bba29)
![Back_4](https://github.com/user-attachments/assets/0a5b3536-2804-46e1-8ed0-26e4c0ccca5f)
![Back_5](https://github.com/user-attachments/assets/4d36f2cf-88a7-45b1-b9f6-473213961d8f)

Демонстрация работы front-end

![Front_1](https://github.com/user-attachments/assets/fc13a7c8-fa25-4790-bf18-4ff2058fc5da)
![Front_2](https://github.com/user-attachments/assets/62bc8fcc-9938-4432-ae2a-8feae09305b9)
![Front_3](https://github.com/user-attachments/assets/32381ddc-72ff-45bf-a64a-c4771969ddd1)
![Front_4](https://github.com/user-attachments/assets/f62bde2c-8545-4dcf-9679-a6d7b285610c)
![Front_5](https://github.com/user-attachments/assets/8b7c15c1-83c6-4ef5-bc25-e7c954c4eba3)
![Front_6](https://github.com/user-attachments/assets/7a32329c-501b-4188-863c-17d9fb3d88a8)
![Front_7](https://github.com/user-attachments/assets/8bc3af4f-6d83-4b9c-abfb-722f1023d1e6)
![Front_8](https://github.com/user-attachments/assets/65a94e09-acd5-4d38-9946-3ccf19a198ea)
![Front_9](https://github.com/user-attachments/assets/b724b563-1465-4482-b0f7-6e49d01456a2)

Демонстрация работы Jenkins и Docker

![Jenkins_Docker_1](https://github.com/user-attachments/assets/8ec9dd0e-fc79-4a59-85f9-b2239cd46b4b)
![Jenkins_Docker_2](https://github.com/user-attachments/assets/4defeb61-e9f2-4797-ba0b-37ce65cee279)
![Jenkins_Docker_3](https://github.com/user-attachments/assets/790c46d8-c140-4a24-8ce9-073fc06f6bc0)
![Jenkins_Docker_4](https://github.com/user-attachments/assets/f07ee58b-a5cb-4559-a9bb-1c448215f82b)
![Jenkins_Docker_5](https://github.com/user-attachments/assets/ee73bda0-8332-47f7-ba3c-3a2c04c1df34)



