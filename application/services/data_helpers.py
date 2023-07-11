from requests import Response


def resp_to_str(response: Response):
    return f"{response.status_code} {response.reason}  {response.content}"
