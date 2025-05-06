from datetime import datetime

def build_response(message,status_code):
    return {
        "success": True,
        "message": message,
        "status_code": status_code,
        "timestamp": datetime.now().isoformat(),
    }