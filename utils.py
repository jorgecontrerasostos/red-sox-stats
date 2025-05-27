from imports import *
from constants import teams


def make_request(url: str, headers: dict = None, timeout: int = 10) -> Response:
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        if response.status_code >= 400:
            raise HTTPError(f"HTTP error {response.status_code}: {response.text}")
        return response
    except (ConnectionError, Timeout, ProxyError, SSLError) as conn_err:
        raise Exception(f"Connection-related error occurred: {conn_err}") from conn_err
    except RequestException as req_err:
        raise Exception(f"Request failed: {req_err}") from req_err
