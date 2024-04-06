from typing import Optional
import json


def get_secret(
    key: str, default_value: Optional[str] = None, json_path: str = "secrets.json"
) -> str:
    """
    지정된 JSON 파일에서 키에 해당하는 비밀 값을 검색합니다.

    이 함수는 주어진 키를 사용하여 JSON 파일에서 비밀 값을 찾고, 해당 키가 없을 경우 기본 값을 반환하거나 환경 변수가 설정되지 않았음을 알리는 예외를 발생시킵니다.

    매개변수:
    - key (str): 검색할 비밀 값의 키입니다.
    - default_value (Optional[str]): 키가 없을 경우 반환될 기본 값입니다. 기본값은 None입니다.
    - json_path (str): 비밀 값을 포함하고 있는 JSON 파일의 경로입니다. 기본값은 "secrets.json"입니다.

    반환값:
    - str: 검색된 비밀 값 또는 기본 값입니다.

    예외:
    - EnvironmentError: 주어진 키에 해당하는 비밀 값이 없고 기본 값도 제공되지 않았을 때 발생합니다.
    """
    with open(json_path, encoding="utf-8") as f:
        secrets = json.loads(f.read())
    try:
        return secrets[key]
    except KeyError:
        if default_value is not None:
            return default_value
        raise EnvironmentError(f"Set the {key} environment variable.")
    

    
