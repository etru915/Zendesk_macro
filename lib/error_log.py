import time
import traceback

class ErrorLog():
    def error_log(error: str):
        current_time = time.strftime("%Y.%m.%d/%H:%M:%S", time.localtime(time.time()))

    try:
        print(A)
    except Exception:
        err = traceback.format_exc()
        ErrorLog(str(err))