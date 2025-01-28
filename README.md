# JustHost_DRF

API application on DRF for managing cloud virtual servers (VPS)

Запустите сервер Django и вы можете взаимодействовать с API через браузер или используя инструменты, такие как curl или Postman. Пример запросов:

Создание VPS: POST запрос на /vps/ с JSON данными: {"cpu": 2, "ram": 4, "hdd": 100}

Получение VPS по UID: GET запрос на /vps/{uid}/

Получение списка VPS с фильтрацией: GET запрос на /vps/?search=started (найдет все VPS со статусом “started”) или /vps/?ordering=-cpu (отсортирует по CPU в обратном порядке)

Изменение статуса VPS: POST запрос на /vps/{uid}/change_status/ с JSON данными: {"status": "stopped"}

Это расширенный пример, который включает важные элементы, такие как фильтрация и сортировка.
