# NewDB Python SDK

Официальная Python-библиотека для работы с [NewDB REST API](https://newdb.net) — проверкой физических лиц, юридических лиц, иностранных граждан, залогов, недвижимости и судебных дел по официальным реестрам РФ (ФНС, ФССП, МВД, Федресурс, КАД Арбитр, ЕГРЮЛ, ЕГРИП, Нотариат, ГАС Правосудие).

[![PyPI version](https://img.shields.io/pypi/v/newdb.svg)](https://pypi.org/project/newdb/)
[![Python versions](https://img.shields.io/pypi/pyversions/newdb.svg)](https://pypi.org/project/newdb/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

---

## Установка

```bash
pip install newdb
```

---

## Быстрый старт

### Синхронный клиент

```python
from newdb import NewDBClient

client = NewDBClient(api_key="your_api_token")

# 1. Проверка баланса токена
balance = client.get_balance()
print(f"Баланс: {balance.balance} запросов")

# 2. Проверка действительности паспорта РФ (МВД)
passport = client.person.check_passport_mvd(
    seria="4510",
    number="123456",
    firstname="Иван",
    lastname="Иванов"
)
print(passport.state, passport.results)

# 3. Комплексная проверка организации по ИНН с авто-ожиданием готовности
company_task = client.legal.complex_check(inn="7707083893")
completed_task = client.wait_for_result(company_task.request_id, timeout=60)
print(completed_task.results)
```

---

### Тестовый режим (Sandbox / Test Mode)

Для тестирования и отладки интеграции без списания баланса и ожидания внешних сервисов используйте встроенный режим `test_mode`:

```python
from newdb import NewDBClient

# Активация тестового контура https://api.newdb.net/test/v2
client = NewDBClient(test_mode=True)

# Либо через переменную окружения:
# export NEWDB_TEST_MODE=1
# client = NewDBClient()

# Мгновенный синтетический ответ с полными полями
res = client.person.check_passport_mvd(seria="4510", number="123456", firstname="Иван", lastname="Иванов")
print(res.state, res.results)
```

---

### Асинхронный клиент (asyncio / FastAPI / aiohttp)

```python
import asyncio
from newdb import AsyncNewDBClient

async def main():
    async with AsyncNewDBClient(api_key="your_api_token") as client:
        # Проверка долгов ФССП
        task = await client.person.check_fssp(
            firstname="Иван",
            lastname="Иванов",
            secondname="Иванович",
            dob="1990-01-01",
            regioncode="77"
        )
        result = await client.wait_for_result(task.request_id)
        print(result.get_result("fssp_person"))

asyncio.run(main())
```

---

## Поддерживаемые методы

### Физические лица (`client.person.*`)
* `check_passport_mvd(seria, number, firstname, lastname)` — проверка действительности паспорта по базе МВД
* `check_passport_fns(seria, number, firstname, lastname, dob, secondname=None)` — получение ИНН и валидация паспорта (ФНС)
* `complex_check(seria, number, firstname, lastname, ...)` — комплексная проверка физлица по паспорту (ФНС, ФССП, банкротство, арбитраж, залоги, ЕГРИП)
* `check_fssp(firstname, lastname, dob, regioncode="100")` — исполнительные производства ФССП
* `check_bankrot(innfiz=None, fio=None)` — банкротство физлиц и ИП (Федресурс)
* `check_pledge(firstname, lastname, ...)` — залоги движимого имущества (ФНП)
* `check_arbitr(innfiz=None, fio=None)` — арбитражные дела в КАД
* `check_nalog_debt(inn)` — налоговая задолженность
* `check_fns_block(innfiz)` — блокировки банковских счетов (ФНС)
* `check_egrul_ip(innfiz)` — выписка ЕГРИП и статус индивидуального предпринимателя
* `check_terrorist(firstname, lastname, ...)` — перечень Росфинмониторинга (экстремизм/терроризм)
* `check_opensanctions(query, inn=None, birth_date=None, max_results=25)` — санкционный и PEP-скрининг с точным уточнением карточек

### Юридические лица (`client.legal.*`)
* `check_egrul(inn=None, ogrn=None)` — полные сведения ЕГРЮЛ и «Прозрачный бизнес»
* `check_fns_block(inn, bik=None)` — приостановления операций по счетам (ФНС)
* `check_bankrot(inn=None, ogrn=None)` — банкротство юридических лиц
* `check_arbitr(inn)` — арбитражная практика компании
* `monitor_kad_case(case_number)` — процессуальный мониторинг конкретного дела КАД по номеру дела
* `check_fssp(inn)` — исполнительные производства компании
* `check_bo(inn)` — бухгалтерская (финансовая) отчетность (ГИР БО / ФНС)
* `complex_check(inn)` — комплексная проверка организации + проверка руководства и учредителей

### HTML/PDF-отчеты

```python
pdf = client.generate_report(task.request_id, format="pdf")
foreign_html = client.generate_aggregated_report(request_ids, "complex_foreign", format="html")
```

`generate_report` поддерживает `complex_by_passport`, `complex_by_inn` и `realty_price`. Для объединения отдельных миграционных проверок используйте `generate_aggregated_report`.

### Иностранные граждане (`client.foreign.*`)
* `check_rkl(firstname, lastname, dob, id_doc_number, ...)` — реестр контролируемых лиц (РКЛ МВД)
* `check_patent(number, seria=None, region="msk")` — трудовой патент (Москва, МО, регионы)
* `check_vng(seria, number)` — вид на жительство (ВНЖ)
* `check_rnr(number)` — разрешение на работу

### Имущество (`client.property.*`)
* `check_rosreestr(cadastr_number=None, address=None)` — проверка недвижимости по Росреестру
* `check_pledge_vin(vin)` — проверка автомобиля на залоги по VIN
* `check_vin(vin, get_screen=0)` — комплексная проверка авто по VIN (Госуслуги: розыск, ограничения, залоги ФНП)

---

## Документация и контакты

* Официальная документация: [https://newdb.net/docs](https://newdb.net/docs)
* Получение токена: [access@newdb.net](mailto:access@newdb.net)
* Лицензия: MIT
