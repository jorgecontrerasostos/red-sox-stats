from imports import *

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

def to_int(column: pd.Series) -> pd.Series:
    if not pd.api.types.is_integer_dtype(column):
        return column.astype("Int64")
    return column

def to_float(column: pd.Series) -> pd.Series:
    if not pd.api.types.is_numeric_dtype(column):
        return column.astype("Float64")
    return column