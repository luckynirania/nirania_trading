# tracing_utils.py
import json
import requests


def request_with_trace(tracer, endpoint, method, headers=None, body=None, secured=True):
    url = ("https://" if secured else "http://") + endpoint
    with tracer.start_span(f"{endpoint} request/response") as sub_span:
        sub_span.add_event(
            name="",
            attributes={
                "bescription": url,
                "method": method,
                "request": body if body else "NO REQUEST BODY",
            },
        )
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, body=body)
        else:
            sub_span.add_event(
                name="",
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
        elif "text/html" in content_type:
            log_data = response.text
        else:
            log_data = response.content[
                :10
            ]  # Or you could log a few bytes: response.content[:10]
            print(log_data)

        sub_span.add_event(
            name="",
            attributes={
                "bescription": url,
                "content_type": content_type,
                "response": log_data,
            },
        )

        return response
