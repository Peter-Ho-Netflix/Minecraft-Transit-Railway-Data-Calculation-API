"""
UI 入口。之後將直接 import 並呼叫 features 中的函式，不透過 API。
目前僅展示空視窗，不實作任何 UI 邏輯。
"""
import wx


class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        self.SetTitle("Minecraft Transit Railway Calculation API")
        self.SetSize((800, 600))
        self.Center()


class App(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None)
        self.frame.Show(True)
        return True


def run_ui():
    """供 app.py 呼叫，啟動 wx 主視窗並進入主迴圈。"""
    app = App()
    app.MainLoop()


if __name__ == "__main__":
    run_ui()
