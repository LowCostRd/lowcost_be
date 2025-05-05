from datetime import datetime

def build_response(message,status_code):
    return {
        "message": message,
        "status_code": status_code,
        "timestamp": datetime.now().isoformat(),
    }