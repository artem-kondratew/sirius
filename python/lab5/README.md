# Использование тестов с пустым репозиторием:
1. Создаём пустую папку  
2. Клонируем репозиторий (через https, иначе требуется ssh ключи):  
git clone https://gitlab.sirius-web.org/python-students-24/tests/lab3.git    
3. Переименовываем ссылку на удалённый репозиторий с тестами  
git remote rename origin tests  
4. Создаём свой проект на гитлабе (пустой, без readme)  
5. Добавляем ссылку на свой удалённый репозиторий, например  
git remote add origin https://gitlab.sirius-web.org/python-students-24/george-maurakh/lab3   
6. Копируем в репозиторий свои файлы.   
7. Проверяем наличие '\__init\__.py', 'test.py' и 'main.py' в соответствующих модулях  
8. Сохраняем, коммитим  
9. Заливаем на свой репозиторий  
10. Наблюдаем за иконкой тестов, ловим ошибки или успех  

# Использование тестов с полным репозиторием
1. Заходим в репозиторий  
2. Выбираем ветку package (на которой ваша лаба с пакетом)  
3. Добавляем новую ссылку на тесты  
git remote add packageTestsRemote https://gitlab.sirius-web.org/python-students-24/tests/lab5.git  
4. Скачиваем тесты  
git fetch packageTestsRemote master  
5. Переключаемся на скачанную ветку и добавляем её в проект как самостоятельную ветку гит  
git checkout packageTestsRemote/master  
git switch -c packageTests  
6. Применяем изменения с тестовой ветки к ветке package:  
git checkout package  
git cherry-pick --strategy=ort --strategy-option=ours -n ..packageTests  
При возникновении конфликтов (а они будут) для каждого конфликтного файла нужно выбрать:  
git checkout --ours "conflict_file"  
git add "conflict_file"  
После разрешения всех конфликтов делаем коммит:  
git commit -m "message"  
Завершаем слияние:  
git cherry-pick --continue  
7. Заливаем на гитлаб ветку package, смотрим иконку тестов и делаем issue  

# Изменение тестов
При изменении тестов, их нужно обновить в своём репозитории:  
git pull --rebase=true tests master  
git push origin master  
