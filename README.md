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

### Юридические лица (`client.legal.*`)
* `check_egrul(inn=None, ogrn=None)` — полные сведения ЕГРЮЛ и «Прозрачный бизнес»
* `check_fns_block(inn, bik=None)` — приостановления операций по счетам (ФНС)
* `check_bankrot(inn=None, ogrn=None)` — банкротство юридических лиц
* `check_arbitr(inn)` — арбитражная практика компании
* `check_fssp(inn)` — исполнительные производства компании
* `complex_check(inn)` — комплексная проверка организации + проверка руководства и учредителей

### Иностранные граждане (`client.foreign.*`)
* `check_rkl(firstname, lastname, dob, id_doc_number, ...)` — реестр контролируемых лиц (РКЛ МВД)
* `check_patent(number, seria=None, region="msk")` — трудовой патент (Москва, МО, регионы)
* `check_vng(seria, number)` — вид на жительство (ВНЖ)
* `check_rnr(number)` — разрешение на работу

### Имущество (`client.property.*`)
* `check_rosreestr(cadastr_number=None, address=None)` — проверка недвижимости
* `check_pledge_vin(vin)` — проверка автомобиля на залоги по VIN

---

## Документация и контакты

* Официальная документация: [https://newdb.net/docs](https://newdb.net/docs)
* Получение токена: [access@newdb.net](mailto:access@newdb.net)
* Лицензия: MIT
