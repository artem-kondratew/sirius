# Использование тестов:  
1. Заходим в репозиторий с лабой 1-3  
2. Выбираем ветку package (на которой ваша лаба с пакетом)  
3. Добавляем новую ссылку на тесты для 4 лабы  
git remote add packageTestsRemote https://gitlab.sirius-web.org/python-students-24/tests/lab4.git  
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

# Примечания
Для успешного прохождения тестов с пакетами нужно: отредактировать .gitignore, доавить папку src, в которой находится Ваш модуль и тесты для него. Также необхдимо создать pyproject.toml (или setup.py) в корневой папке. Убедитесь, что Вы не загружаете на гитлаб файлы данных, окружения или кеша IDE.