Система моніторингу температури серверів

Назва проекту: Система моніторингу температури серверів

Опис проекту: Система отримує дані про температуру серверів з умовного API або сенсорів, зберігає ці дані у базі даних, відображає їх через Grafana та використовує Prometheus для збору й обробки метрик. Доступ до системи можливий лише для авторизованих користувачів.

Приблизна схема проекту:
1. Генерація даних: використання Python 3
2. Збір даних: використання Prometheus
3. Збереження даних: використання Time Series Storage (вбудована БД Prometheus)
4. Відображення даних: використання Grafana
5. Авторизація: сервер на Python 3 + використання SQLite
6. Контейнеризація: використання контейнерів Docker
