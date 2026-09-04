# Выдержка из истории (git log --stat, сокращено)

```
c9f21a4 2026-08-15  m.orlov (SRE)     migration: drop card_last4 from payments
                                      PCI-аудит требует не хранить last4; применена в прод
                                      2026-08-15 18:40, бэкапа колонки нет
9d13be0 2026-05-04  a.kim (billing)   switch export to v2 json, csv path left in place
                                      BIL-330; csv-выгрузку читал только Nordbank
4e0aa71 2026-03-02  a.kim (billing)   migrate attempts to v2, keep v1 table for a week
                                      BIL-201; читателей v1 не осталось после 2026-03-09
b70c115 2026-02-10  a.kim (billing)   add export_attempts_v2
1f88ac3 2025-11-20  p.novak (devops)  fix flaky release: healthcheck race
                                      после rollout под ещё не в endpoints, curl ловил 503
0a4d7e2 2025-09-08  i.sorokin         fix
                                      (без тикета, без описания)
5c30b91 2025-06-14  a.kim (billing)   iban normalization for Nordbank payouts
                                      BIL-90; Nordbank принимает IBAN только без пробелов
3ab6d02 2025-04-01  s.petrov (payments) add 429 backoff for gateway
                                      PSP-114; шлюз троттлит на 50 rps
```

Мержи: `export/writer.py` конфликтовал 2026-05-04, блок `write_xml`
попал в файл дважды при разрешении конфликта.
