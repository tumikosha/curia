# Предлагается снести

1. Ретрай на 429 в клиенте шлюза — `gateway/client.py:12-19`.
   Лишняя сложность, шлюз и так стабилен.
2. Таблица `export_attempts_v1` — миграция
   `migrations/2026-02-10_v2_attempts.sql` ввела v2, старая осталась.
3. Закомментированный блок в `export/writer.py:20-29`.
4. Функция `normalize_iban` — `billing/iban.py` целиком.
5. Проверка `if amount < 0` — `billing/charge.py:7-8`.
6. Ручка `GET /v1/export/status` — `api/routes.py:10-17`.
7. Функция `_fmt_row` — `export/formatter.py:6-11`.
8. Функция `write_csv` — `export/writer.py:11-18`.
9. `sleep 2` в `deploy/release.sh:8`.
10. Колонка `card_last4` — уже удалена миграцией
    `migrations/2026-08-15_drop_card_last4.sql`, оформляю задним
    числом для полноты списка.
