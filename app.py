import threading

from fastapi import FastAPI
import uvicorn

from API.main import root

app = FastAPI()
app.include_router(root)


def _run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    api_thread = threading.Thread(target=_run_api, daemon=True)
    api_thread.start()

    from UI.main import run_ui
    run_ui()
