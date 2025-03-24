import json

import allure
import pytest
from fastapi.testclient import TestClient

from tests.testcases.auth.cons_auth import LoginTestCase


@allure.epic(LoginTestCase.EPIC)
@allure.feature(LoginTestCase.FEATURE)
@allure.story(LoginTestCase.STORY)
@allure.severity(LoginTestCase.SEVERITY)
@allure.title(LoginTestCase.TITLE)
@allure.description(LoginTestCase.DESCRIPTION)
@pytest.mark.parametrize(
    ", ".join(LoginTestCase.PARAMS),
    LoginTestCase.REQUESTS,
)
def test_login_dynamic(
    client: TestClient, username: str, password: str, expected_status: int, expected_response: dict
) -> None:
    with allure.step(LoginTestCase.STEPS[0]["step"].format(username=username)):
        response = client.post(LoginTestCase.API_PATH, json={"username": username, "password": password})

    with allure.step(LoginTestCase.STEPS[1]["step"]):
        assert response.status_code == expected_status, LoginTestCase.STEPS[1]["error_message"].format(
            expected_status=expected_status, status_code=response.status_code
        )

    with allure.step(LoginTestCase.STEPS[2]["step"]):
        response_json = response.json()
        assert response_json == expected_response, LoginTestCase.STEPS[2]["error_message"].format(
            response_json=json.dumps(response_json, indent=2)
        )
