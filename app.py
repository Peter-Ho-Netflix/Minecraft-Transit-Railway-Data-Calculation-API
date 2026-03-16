import sys
import threading

from fastapi import FastAPI
import uvicorn

from API.main import root

app = FastAPI()
app.include_router(root)


def _run_api():
    """在目前執行緒中啟動 API（阻塞呼叫）。"""
    uvicorn.run(app, host="0.0.0.0", port=8000)


def _run_api_in_thread():
    """在背景子執行緒中啟動 API，供同時啟動 UI 使用。"""
    api_thread = threading.Thread(target=_run_api, daemon=True)
    api_thread.start()
    return api_thread


def _run_ui():
    """啟動 wxPython UI。"""
    from UI.main import run_ui

    run_ui()


def main(argv: list[str] | None = None) -> None:
    """
    依照參數決定啟動模式：

    - 無參數：同時啟動 API（背景執行緒）與 UI。
    - --ui-only / --ui：僅啟動 UI。
    - --api-only / --api：僅啟動 API（阻塞於當前執行緒）。
    """
    if argv is None:
        argv = sys.argv[1:]

    mode = "both"
    if argv:
        flag = argv[0]
        if flag in ("--ui-only", "--ui"):
            mode = "ui"
        elif flag in ("--api-only", "--api"):
            mode = "api"
        else:
            print(f"未知參數：{flag}")
            print("使用方式：python app.py [--ui-only | --ui | --api-only | --api]")
            return

    if mode == "both":
        _run_api_in_thread()
        _run_ui()
    elif mode == "ui":
        _run_ui()
    elif mode == "api":
        _run_api()


if __name__ == "__main__":
    main()
