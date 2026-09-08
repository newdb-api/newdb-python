"""NewDB API Client implementation (Sync & Async)."""

import os
import time
import asyncio
from uuid import uuid4
from typing import Any, Dict, Optional, Union
import httpx

from .exceptions import (
    AuthenticationError,
    RateLimitError,
    TimeoutError,
    APIResponseError,
)
from .models import BalanceResponse, MethodResult, TaskResponse

DEFAULT_BASE_URL = "https://api.newdb.net/v2"
TEST_BASE_URL = "https://api.newdb.net/test/v2"
DEFAULT_TEST_TOKEN = "test_token_newdb_sandbox"


class BaseDomainNamespace:
    def __init__(self, client: Union["NewDBClient", "AsyncNewDBClient"]):
        self._client = client


class PersonNamespace(BaseDomainNamespace):
    """Methods for physical persons checks."""

    def check_passport_mvd(self, seria: str, number: str, firstname: str, lastname: str, country: str = "ru", **kwargs) -> Any:
        return self._client.execute({"method": "passport_mvd", "seria": seria, "number": number, "firstname": firstname, "lastname": lastname, "country": country, **kwargs})

    def check_passport_fns(self, seria: str, number: str, firstname: str, lastname: str, dob: str, secondname: Optional[str] = None, country: str = "ru", **kwargs) -> Any:
        params = {"method": "passport_fns", "seria": seria, "number": number, "firstname": firstname, "lastname": lastname, "dob": dob, "country": country, **kwargs}
        if secondname:
            params["secondname"] = secondname
        return self._client.execute(params)

    def check_fssp(self, firstname: str, lastname: str, dob: str, regioncode: str = "100", secondname: Optional[str] = None, country: str = "ru", **kwargs) -> Any:
        params = {"method": "fssp_person", "firstname": firstname, "lastname": lastname, "dob": dob, "regioncode": regioncode, "country": country, **kwargs}
        if secondname:
            params["secondname"] = secondname
        return self._client.execute(params)

    def check_bankrot(self, innfiz: Optional[str] = None, fio: Optional[str] = None, country: str = "ru", **kwargs) -> Any:
        params = {"method": "bankrot_person", "country": country, **kwargs}
        if innfiz:
            params["innfiz"] = innfiz
        if fio:
            params["fio"] = fio
        return self._client.execute(params)

    def check_pledge(self, firstname: str, lastname: str, secondname: Optional[str] = None, dob: Optional[str] = None, country: str = "ru", **kwargs) -> Any:
        params = {"method": "pledge_person", "firstname": firstname, "lastname": lastname, "country": country, **kwargs}
        if secondname:
            params["secondname"] = secondname
        if dob:
            params["dob"] = dob
        return self._client.execute(params)

    def check_arbitr(self, innfiz: Optional[str] = None, fio: Optional[str] = None, country: str = "ru", **kwargs) -> Any:
        params = {"method": "arbitr_person", "country": country, **kwargs}
        if innfiz:
            params["innfiz"] = innfiz
        if fio:
            params["fio"] = fio
        return self._client.execute(params)

    def check_nalog_debt(self, inn: str, country: str = "ru", **kwargs) -> Any:
        return self._client.execute({"method": "nalog_debt", "inn": inn, "country": country, **kwargs})

    def check_fns_block(self, innfiz: str, country: str = "ru", **kwargs) -> Any:
        return self._client.execute({"method": "fns_block_person", "innfiz": innfiz, "country": country, **kwargs})

    def check_egrul_ip(self, innfiz: str, country: str = "ru", **kwargs) -> Any:
        return self._client.execute({"method": "egrul_ip", "innfiz": innfiz, "country": country, **kwargs})

    def check_terrorist(self, firstname: str, lastname: str, secondname: Optional[str] = None, dob: Optional[str] = None, country: str = "ru", **kwargs) -> Any:
        params = {"method": "terrorist", "firstname": firstname, "lastname": lastname, "country": country, **kwargs}
        if secondname:
            params["secondname"] = secondname
        if dob:
            params["dob"] = dob
        return self._client.execute(params)

    def complex_check(self, seria: str, number: str, firstname: str, lastname: str, secondname: Optional[str] = None, dob: Optional[str] = None, regioncode: str = "100", country: str = "ru", **kwargs) -> Any:
        params = {"method": "complex_by_passport", "seria": seria, "number": number, "firstname": firstname, "lastname": lastname, "regioncode": regioncode, "country": country, **kwargs}
        if secondname:
            params["secondname"] = secondname
        if dob:
            params["dob"] = dob
        return self._client.execute(params)


class LegalNamespace(BaseDomainNamespace):
    """Methods for legal entities checks."""

    def check_egrul(self, inn: Optional[str] = None, ogrn: Optional[str] = None, country: str = "ru", **kwargs) -> Any:
        params = {"method": "egrul", "country": country, **kwargs}
        if inn:
            params["inn"] = inn
        if ogrn:
            params["ogrn"] = ogrn
        return self._client.execute(params)

    def check_fns_block(self, inn: str, bik: Optional[str] = None, country: str = "ru", **kwargs) -> Any:
        params = {"method": "fns_block", "inn": inn, "country": country, **kwargs}
        if bik:
            params["bik"] = bik
        return self._client.execute(params)

    def check_bankrot(self, inn: Optional[str] = None, ogrn: Optional[str] = None, country: str = "ru", **kwargs) -> Any:
        params = {"method": "bankrot_legal", "country": country, **kwargs}
        if inn:
            params["inn"] = inn
        if ogrn:
            params["ogrn"] = ogrn
        return self._client.execute(params)

    def check_arbitr(self, inn: str, country: str = "ru", **kwargs) -> Any:
        return self._client.execute({"method": "arbitr_legal", "inn": inn, "country": country, **kwargs})

    def monitor_kad_case(self, case_number: str, country: str = "ru", **kwargs) -> Any:
        return self._client.execute({"method": "kad_event_monitor", "case_number": case_number, "country": country, **kwargs})

    def check_fssp(self, inn: str, country: str = "ru", **kwargs) -> Any:
        return self._client.execute({"method": "fssp_legal", "inn": inn, "country": country, **kwargs})

    def complex_check(self, inn: str, country: str = "ru", **kwargs) -> Any:
        return self._client.execute({"method": "complex_by_inn", "inn": inn, "country": country, **kwargs})


class ForeignNamespace(BaseDomainNamespace):
    """Methods for foreign citizens checks."""

    def check_rkl(self, firstname: str, lastname: str, dob: str, id_doc_number: str, id_doc_seria: Optional[str] = None, secondname: Optional[str] = None, country: str = "ru", **kwargs) -> Any:
        params = {"method": "rkl", "firstname": firstname, "lastname": lastname, "dob": dob, "id_doc_number": id_doc_number, "country": country, **kwargs}
        if id_doc_seria:
            params["id_doc_seria"] = id_doc_seria
        if secondname:
            params["secondname"] = secondname
        return self._client.execute(params)

    def check_patent(self, number: str, seria: Optional[str] = None, region: str = "msk", country: str = "ru", **kwargs) -> Any:
        method = "patent_msk" if region == "msk" else ("patent_mo" if region == "mo" else "foreign_patent")
        params = {"method": method, "number": number, "country": country, **kwargs}
        if seria:
            params["seria"] = seria
        return self._client.execute(params)

    def check_vng(self, seria: str, number: str, country: str = "ru", **kwargs) -> Any:
        return self._client.execute({"method": "foreign_vng", "seria": seria, "number": number, "country": country, **kwargs})

    def check_rnr(self, number: str, country: str = "ru", **kwargs) -> Any:
        return self._client.execute({"method": "foreign_rnr", "number": number, "country": country, **kwargs})


class PropertyNamespace(BaseDomainNamespace):
    """Methods for property, vehicle and pledge checks."""

    def check_rosreestr(self, cadastr_number: Optional[str] = None, address: Optional[str] = None, country: str = "ru", **kwargs) -> Any:
        params = {"method": "rosreestr", "country": country, **kwargs}
        if cadastr_number:
            params["cadastr_number"] = cadastr_number
        if address:
            params["address"] = address
        return self._client.execute(params)

    def check_pledge_vin(self, vin: str, country: str = "ru", **kwargs) -> Any:
        return self._client.execute({"method": "pledge_vin", "vin": vin, "country": country, **kwargs})


def _parse_task_response(data: Dict[str, Any]) -> TaskResponse:
    request_id = str(data.get("requestId") or data.get("reqid") or "")
    state = str(data.get("state") or "unknown")
    results_map: Dict[str, MethodResult] = {}

    results_raw = data.get("results")
    if isinstance(results_raw, dict):
        for method_name, payload in results_raw.items():
            if isinstance(payload, dict):
                res_obj = payload.get("result") if isinstance(payload.get("result"), dict) else payload
                results_map[method_name] = MethodResult(
                    status=int(res_obj.get("status", 200) if res_obj.get("status") is not None else 200),
                    data=res_obj.get("data"),
                    error=res_obj.get("error"),
                    found=res_obj.get("found"),
                    raw=payload,
                )

    return TaskResponse(
        request_id=request_id,
        state=state,
        results=results_map,
        raw=data,
    )


class NewDBClient:
    """Synchronous NewDB API Client."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 60.0,
        test_mode: bool = False,
    ):
        env_test = os.getenv("NEWDB_TEST_MODE", "").lower() in ("1", "true", "yes")
        self.test_mode = bool(test_mode or env_test)

        resolved_key = (api_key or os.getenv("NEWDB_API_KEY", "")).strip()
        if not resolved_key and self.test_mode:
            resolved_key = DEFAULT_TEST_TOKEN

        if not resolved_key:
            raise AuthenticationError("API key (token) must be provided.")

        self.api_key = resolved_key
        if base_url:
            self.base_url = base_url.rstrip("/")
        elif self.test_mode:
            self.base_url = TEST_BASE_URL
        else:
            self.base_url = os.getenv("NEWDB_BASE_URL", DEFAULT_BASE_URL).rstrip("/")

        self.timeout = timeout
        self._http = httpx.Client(
            base_url=self.base_url,
            headers={"X-API-KEY": self.api_key, "Content-Type": "application/json"},
            timeout=self.timeout,
        )

        self.person = PersonNamespace(self)
        self.legal = LegalNamespace(self)
        self.foreign = ForeignNamespace(self)
        self.property = PropertyNamespace(self)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "NewDBClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def get_balance(self) -> BalanceResponse:
        resp = self._http.get("/balance")
        if resp.status_code == 401 or resp.status_code == 403:
            raise AuthenticationError("Invalid X-API-KEY token.")
        if resp.status_code != 200:
            raise APIResponseError(resp.text, resp.status_code)
        data = resp.json()
        return BalanceResponse(token=data.get("token", ""), balance=int(data.get("balance", 0)), raw=data)

    def execute(self, params: Dict[str, Any], request_id: Optional[str] = None, webhook: Optional[str] = None) -> TaskResponse:
        req_id = request_id or str(uuid4())
        payload = {"requestId": req_id, "params": params}
        if webhook:
            payload["webhook"] = webhook

        resp = self._http.post("", json=payload)
        if resp.status_code in {401, 403}:
            raise AuthenticationError("Invalid X-API-KEY token.")
        if resp.status_code == 429:
            raise RateLimitError("Rate limit exceeded.")
        if resp.status_code >= 500:
            raise APIResponseError(resp.text, resp.status_code)

        try:
            data = resp.json()
        except Exception:
            raise APIResponseError(f"Invalid JSON response: {resp.text}", resp.status_code)

        return _parse_task_response(data)

    def get_task(self, request_id: str) -> TaskResponse:
        return self.execute({}, request_id=request_id)

    def wait_for_result(self, request_id: str, timeout: float = 120.0, poll_interval: float = 2.0) -> TaskResponse:
        start_time = time.time()
        while time.time() - start_time < timeout:
            task = self.get_task(request_id)
            if task.is_complete or task.is_failed:
                return task
            time.sleep(poll_interval)
        raise TimeoutError(f"Task {request_id} did not complete within {timeout}s.")

    def execute_and_wait(self, params: Dict[str, Any], timeout: float = 120.0, poll_interval: float = 2.0) -> TaskResponse:
        task = self.execute(params)
        if task.is_complete or task.is_failed:
            return task
        return self.wait_for_result(task.request_id, timeout=timeout, poll_interval=poll_interval)


class AsyncNewDBClient:
    """Asynchronous NewDB API Client."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 60.0,
        test_mode: bool = False,
    ):
        env_test = os.getenv("NEWDB_TEST_MODE", "").lower() in ("1", "true", "yes")
        self.test_mode = bool(test_mode or env_test)

        resolved_key = (api_key or os.getenv("NEWDB_API_KEY", "")).strip()
        if not resolved_key and self.test_mode:
            resolved_key = DEFAULT_TEST_TOKEN

        if not resolved_key:
            raise AuthenticationError("API key (token) must be provided.")

        self.api_key = resolved_key
        if base_url:
            self.base_url = base_url.rstrip("/")
        elif self.test_mode:
            self.base_url = TEST_BASE_URL
        else:
            self.base_url = os.getenv("NEWDB_BASE_URL", DEFAULT_BASE_URL).rstrip("/")

        self.timeout = timeout
        self._http = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"X-API-KEY": self.api_key, "Content-Type": "application/json"},
            timeout=self.timeout,
        )

        self.person = PersonNamespace(self)
        self.legal = LegalNamespace(self)
        self.foreign = ForeignNamespace(self)
        self.property = PropertyNamespace(self)

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> "AsyncNewDBClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def get_balance(self) -> BalanceResponse:
        resp = await self._http.get("/balance")
        if resp.status_code in {401, 403}:
            raise AuthenticationError("Invalid X-API-KEY token.")
        if resp.status_code != 200:
            raise APIResponseError(resp.text, resp.status_code)
        data = resp.json()
        return BalanceResponse(token=data.get("token", ""), balance=int(data.get("balance", 0)), raw=data)

    async def execute(self, params: Dict[str, Any], request_id: Optional[str] = None, webhook: Optional[str] = None) -> TaskResponse:
        req_id = request_id or str(uuid4())
        payload = {"requestId": req_id, "params": params}
        if webhook:
            payload["webhook"] = webhook

        resp = await self._http.post("", json=payload)
        if resp.status_code in {401, 403}:
            raise AuthenticationError("Invalid X-API-KEY token.")
        if resp.status_code == 429:
            raise RateLimitError("Rate limit exceeded.")
        if resp.status_code >= 500:
            raise APIResponseError(resp.text, resp.status_code)

        try:
            data = resp.json()
        except Exception:
            raise APIResponseError(f"Invalid JSON response: {resp.text}", resp.status_code)

        return _parse_task_response(data)

    async def get_task(self, request_id: str) -> TaskResponse:
        return await self.execute({}, request_id=request_id)

    async def wait_for_result(self, request_id: str, timeout: float = 120.0, poll_interval: float = 2.0) -> TaskResponse:
        start_time = time.time()
        while time.time() - start_time < timeout:
            task = await self.get_task(request_id)
            if task.is_complete or task.is_failed:
                return task
            await asyncio.sleep(poll_interval)
        raise TimeoutError(f"Task {request_id} did not complete within {timeout}s.")

    async def execute_and_wait(self, params: Dict[str, Any], timeout: float = 120.0, poll_interval: float = 2.0) -> TaskResponse:
        task = await self.execute(params)
        if task.is_complete or task.is_failed:
            return task
        return await self.wait_for_result(task.request_id, timeout=timeout, poll_interval=poll_interval)
