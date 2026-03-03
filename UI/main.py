"""
UI 入口。之後將直接 import 並呼叫 features 中的函式，不透過 API。
"""
import wx
from features import calculate_distance as calc_distance
from features import calculate_parallel_turnout_distance as calc_parallel_turnout_distance


class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        self.SetTitle("Minecraft Transit Railway Calculation API")
        self.SetSize((800, 600))
        self.Center()

        self.calculate_distance_label = wx.StaticText(self, label="计算在固定坡度要求下，升起对应高度所需的距离")
        font = self.calculate_distance_label.GetFont()
        font.PointSize = 12
        self.calculate_distance_label.SetFont(font)
        self.calculate_distance_label.SetPosition(wx.Point(10, 10))

        self.slope_text = wx.StaticText(self, label="坡度")
        self.slope_text.SetPosition(wx.Point(10, 40))

        self.slope_text_ctrl = wx.TextCtrl(self)
        self.slope_text_ctrl.SetPosition(wx.Point(10, 60))
        self.slope_text_ctrl.SetSize(wx.Size(100, 20))
        self.slope_text_ctrl.SetValue("0.0")
        self.slope_text_unit = wx.StaticText(self, label="‰")
        self.slope_text_unit.SetPosition(wx.Point(110, 60))

        self.height_text = wx.StaticText(self, label="高度")
        self.height_text.SetPosition(wx.Point(210, 40))

        self.height_text_ctrl = wx.TextCtrl(self)
        self.height_text_ctrl.SetPosition(wx.Point(210, 60))
        self.height_text_ctrl.SetSize(wx.Size(100, 20))
        self.height_text_ctrl.SetValue("0.0")
        self.height_text_unit = wx.StaticText(self, label="米")
        self.height_text_unit.SetPosition(wx.Point(310, 60))

        self.distance_text = wx.StaticText(self, label="距离")
        self.distance_text.SetPosition(wx.Point(10, 85))

        self.distance_text_ctrl = wx.TextCtrl(self)
        self.distance_text_ctrl.SetPosition(wx.Point(10, 110))
        self.distance_text_ctrl.SetSize(wx.Size(100, 20))
        self.distance_text_ctrl.SetValue("0.0")
        self.distance_text_unit = wx.StaticText(self, label="米")
        self.distance_text_unit.SetPosition(wx.Point(110, 110))

        self.distance_rounded_text = wx.StaticText(self, label="距离（四舍五入）")
        self.distance_rounded_text.SetPosition(wx.Point(210, 85))

        self.distance_rounded_text_ctrl = wx.TextCtrl(self)
        self.distance_rounded_text_ctrl.SetPosition(wx.Point(210, 110))
        self.distance_rounded_text_ctrl.SetSize(wx.Size(100, 20))
        self.distance_rounded_text_ctrl.SetValue("0")
        self.distance_rounded_text_unit = wx.StaticText(self, label="米")
        self.distance_rounded_text_unit.SetPosition(wx.Point(310, 110))

        self.slope_length_text = wx.StaticText(self, label="坡长")
        self.slope_length_text.SetPosition(wx.Point(10, 135))

        self.slope_length_text_ctrl = wx.TextCtrl(self)
        self.slope_length_text_ctrl.SetPosition(wx.Point(10, 160))
        self.slope_length_text_ctrl.SetSize(wx.Size(100, 20))
        self.slope_length_text_ctrl.SetValue("0.0")
        self.slope_length_text_unit = wx.StaticText(self, label="米")
        self.slope_length_text_unit.SetPosition(wx.Point(110, 160))

        self.calculate_distance_button = wx.Button(self, label="计算")
        self.calculate_distance_button.SetPosition(wx.Point(10, 185))
        self.calculate_distance_button.SetSize(wx.Size(100, 20))
        self.calculate_distance_button.Bind(wx.EVT_BUTTON, self.on_calculate_distance)

        self.calculate_parallel_turnout_distance_label = wx.StaticText(self, label="计算平行道岔间为了满足转弯半径要求所需要经过的距离")
        self.calculate_parallel_turnout_distance_label.SetPosition(wx.Point(10, 205))
        font = self.calculate_parallel_turnout_distance_label.GetFont()
        font.PointSize = 12
        self.calculate_parallel_turnout_distance_label.SetFont(font)

        self.radius_text = wx.StaticText(self, label="转弯半径")
        self.radius_text.SetPosition(wx.Point(10, 235))

        self.radius_text_ctrl = wx.TextCtrl(self)
        self.radius_text_ctrl.SetPosition(wx.Point(10, 250))
        self.radius_text_ctrl.SetSize(wx.Size(100, 20))
        self.radius_text_ctrl.SetValue("0.0")
        self.radius_text_unit = wx.StaticText(self, label="米")
        self.radius_text_unit.SetPosition(wx.Point(110, 250))

        self.spacing_text = wx.StaticText(self, label="平行道岔间距")
        self.spacing_text.SetPosition(wx.Point(210, 235))

        self.spacing_text_ctrl = wx.TextCtrl(self)
        self.spacing_text_ctrl.SetPosition(wx.Point(210, 250))
        self.spacing_text_ctrl.SetSize(wx.Size(100, 20))
        self.spacing_text_ctrl.SetValue("0.0")
        self.spacing_text_unit = wx.StaticText(self, label="米")
        self.spacing_text_unit.SetPosition(wx.Point(310, 250))

        self.distance_forward_text = wx.StaticText(self, label="前进距离")
        self.distance_forward_text.SetPosition(wx.Point(10, 275))

        self.distance_forward_text_ctrl = wx.TextCtrl(self)
        self.distance_forward_text_ctrl.SetPosition(wx.Point(10, 290))
        self.distance_forward_text_ctrl.SetSize(wx.Size(100, 20))
        self.distance_forward_text_ctrl.SetValue("0.0")
        self.distance_forward_text_unit = wx.StaticText(self, label="米")
        self.distance_forward_text_unit.SetPosition(wx.Point(110, 290))

        self.distance_forward_rounded_text = wx.StaticText(self, label="前进距离（进一法）")
        self.distance_forward_rounded_text.SetPosition(wx.Point(10, 315))

        self.distance_forward_rounded_text_ctrl = wx.TextCtrl(self)
        self.distance_forward_rounded_text_ctrl.SetPosition(wx.Point(10, 330))
        self.distance_forward_rounded_text_ctrl.SetSize(wx.Size(100, 20))
        self.distance_forward_rounded_text_ctrl.SetValue("0.0")
        self.distance_forward_rounded_text_unit = wx.StaticText(self, label="米")
        self.distance_forward_rounded_text_unit.SetPosition(wx.Point(110, 330))

        self.calculate_parallel_turnout_distance_button = wx.Button(self, label="计算")
        self.calculate_parallel_turnout_distance_button.SetPosition(wx.Point(10, 355))
        self.calculate_parallel_turnout_distance_button.SetSize(wx.Size(100, 20))
        self.calculate_parallel_turnout_distance_button.Bind(wx.EVT_BUTTON, self.on_calculate_parallel_turnout_distance)

    def on_calculate_distance(self, event):
        slope = float(self.slope_text_ctrl.GetValue())/1000
        height = float(self.height_text_ctrl.GetValue())
        result = calc_distance(slope, height)
        self.distance_text_ctrl.SetValue(str(result["distance"]))
        self.distance_rounded_text_ctrl.SetValue(str(result["distance_rounded"]))
        self.slope_length_text_ctrl.SetValue(str(result["slope_length"][0]))

    def on_calculate_parallel_turnout_distance(self, event):
        radius = float(self.radius_text_ctrl.GetValue())
        spacing = float(self.spacing_text_ctrl.GetValue())
        result = calc_parallel_turnout_distance(radius, spacing)
        self.distance_forward_text_ctrl.SetValue(str(result["distance"]))
        self.distance_forward_rounded_text_ctrl.SetValue(str(result["distance_rounded"]))

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
