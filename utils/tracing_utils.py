# tracing_utils.py
import json
import requests
from opentelemetry import trace


def remove_http_https(url):
    return url.replace("https://", "").replace("http://", "")


def request_with_trace(
    tracer: trace.Tracer,
    url,
    method=None,
    headers=None,
    body=None,
    smartAPI={},
):
    with tracer.start_span(f"{remove_http_https(url)} request/response") as sub_span:
        sub_span.add_event(
            name="request",
            attributes={
                "bescription": url,
                "method": method,
                "headers_json": json.dumps(headers) if headers else "NO_HEADERS",
                "request": body if body else "NO REQUEST BODY",
                "smaert_api": json.dumps(smartAPI) if smartAPI else "NOT A SMART API",
            },
        )
        if smartAPI:
            sub_span.add_event(f"method is Smart API, that params are {smartAPI}")

            request_body = (
                json.dumps(smartAPI["params"]) if method in ["POST", "PUT"] else None
            )
            request_params = (
                json.dumps(smartAPI["params"]) if method in ["GET", "DELETE"] else None
            )
            sub_span.add_event(
                name="request body",
                attributes={
                    "bescription": url,
                    "method": method,
                    "request_params": request_params
                    if request_params
                    else "NO REQUEST PARAMS",
                    "request_body": request_body if request_body else "NO REQUEST BODY",
                    "smart_api": json.dumps(smartAPI)
                    if smartAPI
                    else "NOT A SMART API",
                },
            )

            response = requests.request(
                method,
                url,
                data=request_body,
                params=request_params,
                headers=headers,
                verify=not smartAPI["disable_ssl"],
                allow_redirects=smartAPI["allow_redirects"],
                timeout=smartAPI["timeout"],
                proxies=smartAPI["proxies"],
            )
        else:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers)
            else:
                sub_span.add_event(
                    name="method not supported",
                    attributes={
                        "bescription": url,
                        "method": method,
                        "verdict": "Method not supported",
                    },
                )
                return None
        # Log request and response details
        sub_span.set_attribute("http.url", url)
        sub_span.set_attribute("http.method", method)
        sub_span.set_attribute("http.status_code", response.status_code)
        sub_span.set_attribute("http.response_length", len(response.content))

        content_type = response.headers.get("Content-Type", "")

        if "application/json" in content_type:
            log_data = json.dumps(response.json())  # Assuming it's a JSON object
            try:
                angel_message = response.json()["status"]
                if isinstance(angel_message, bool):
                    if angel_message:
                        angel_message = "success"
                    else:
                        angel_message = "failure"
            except Exception as e:
                angel_message = f"we are having trouble {e}"
        elif "text/html" in content_type:
            log_data = response.text
        else:
            log_data = response.content[
                :10
            ]  # Or you could log a few bytes: response.content[:10]
            print(log_data)

        sub_span.add_event(
            name="response",
            attributes={
                "bescription": url,
                "content_type": content_type,
                "response": log_data,
            },
        )

        sub_span.set_attribute(
            "error",
            True if (response.status_code != 200) else False,
        )

        if smartAPI:
            sub_span.set_attribute(
                "error",
                False if "success" in angel_message.lower() else True,
            )

        return response
