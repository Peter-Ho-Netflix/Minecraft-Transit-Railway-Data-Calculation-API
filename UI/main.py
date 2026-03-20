"""
UI 入口。之後將直接 import 並呼叫 features 中的函式，不透過 API。
"""
import math
import wx
from features import calculate_distance as calc_distance
from features import calculate_parallel_turnout_distance as calc_parallel_turnout_distance
from features.main import 计算规定转弯半径和转弯角度下的xy偏移量


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

        self.calculate_xy_offset_label = wx.StaticText(self, label="计算规定转弯半径和转弯角度下的xy偏移量")
        self.calculate_xy_offset_label.SetPosition(wx.Point(10, 375))
        font = self.calculate_xy_offset_label.GetFont()
        font.PointSize = 12
        self.calculate_xy_offset_label.SetFont(font)

        self.radius_text_xy_offset = wx.StaticText(self, label="转弯半径")
        self.radius_text_xy_offset.SetPosition(wx.Point(10, 405))

        self.radius_text_ctrl_xy_offset = wx.TextCtrl(self)
        self.radius_text_ctrl_xy_offset.SetPosition(wx.Point(10, 420))
        self.radius_text_ctrl_xy_offset.SetSize(wx.Size(100, 20))
        self.radius_text_ctrl_xy_offset.SetValue("0.0")
        self.radius_text_unit_xy_offset = wx.StaticText(self, label="米")
        self.radius_text_unit_xy_offset.SetPosition(wx.Point(110, 420))

        self.angle_text_xy_offset = wx.StaticText(self, label="转弯角度")
        self.angle_text_xy_offset.SetPosition(wx.Point(210, 405))

        self.angle_text_ctrl_xy_offset = wx.TextCtrl(self)
        self.angle_text_ctrl_xy_offset.SetPosition(wx.Point(210, 420))
        self.angle_text_ctrl_xy_offset.SetSize(wx.Size(100, 20))
        self.angle_text_ctrl_xy_offset.SetValue("0.0")
        self.angle_text_unit_xy_offset = wx.StaticText(self, label="°")
        self.angle_text_unit_xy_offset.SetPosition(wx.Point(310, 420))

        self.external_x_offset_text = wx.StaticText(self, label="额外x偏移量")
        self.external_x_offset_text.SetPosition(wx.Point(320, 405))

        self.external_x_offset_text_ctrl = wx.TextCtrl(self)
        self.external_x_offset_text_ctrl.SetPosition(wx.Point(320, 420))
        self.external_x_offset_text_ctrl.SetSize(wx.Size(100, 20))
        self.external_x_offset_text_ctrl.SetValue("0.0")
        self.external_x_offset_text_unit = wx.StaticText(self, label="米")
        self.external_x_offset_text_unit.SetPosition(wx.Point(420, 420))

        self.x_text_xy_offset = wx.StaticText(self, label="x偏移量")
        self.x_text_xy_offset.SetPosition(wx.Point(10, 445))

        self.x_text_ctrl_xy_offset = wx.TextCtrl(self)
        self.x_text_ctrl_xy_offset.SetPosition(wx.Point(10, 460))
        self.x_text_ctrl_xy_offset.SetSize(wx.Size(100, 20))
        self.x_text_ctrl_xy_offset.SetValue("0.0")
        self.x_text_unit_xy_offset = wx.StaticText(self, label="米")
        self.x_text_unit_xy_offset.SetPosition(wx.Point(110, 460))

        self.y_text_xy_offset = wx.StaticText(self, label="y偏移量")
        self.y_text_xy_offset.SetPosition(wx.Point(210, 445))

        self.y_text_ctrl_xy_offset = wx.TextCtrl(self)
        self.y_text_ctrl_xy_offset.SetPosition(wx.Point(210, 460))
        self.y_text_ctrl_xy_offset.SetSize(wx.Size(100, 20))
        self.y_text_ctrl_xy_offset.SetValue("0.0")
        self.y_text_unit_xy_offset = wx.StaticText(self, label="米")
        self.y_text_unit_xy_offset.SetPosition(wx.Point(310, 460))

        self.x_rounded_text = wx.StaticText(self, label="x偏移量（进一法）")
        self.x_rounded_text.SetPosition(wx.Point(10, 485))

        self.x_rounded_text_ctrl = wx.TextCtrl(self)
        self.x_rounded_text_ctrl.SetPosition(wx.Point(10, 500))
        self.x_rounded_text_ctrl.SetSize(wx.Size(100, 20))
        self.x_rounded_text_ctrl.SetValue("0.0")
        self.x_rounded_text_unit = wx.StaticText(self, label="米")
        self.x_rounded_text_unit.SetPosition(wx.Point(110, 500))

        self.y_rounded_text = wx.StaticText(self, label="y偏移量（进一法）")
        self.y_rounded_text.SetPosition(wx.Point(210, 485))

        self.y_rounded_text_ctrl = wx.TextCtrl(self)
        self.y_rounded_text_ctrl.SetPosition(wx.Point(210, 500))
        self.y_rounded_text_ctrl.SetSize(wx.Size(100, 20))
        self.y_rounded_text_ctrl.SetValue("0.0")
        self.y_rounded_text_unit = wx.StaticText(self, label="米")
        self.y_rounded_text_unit.SetPosition(wx.Point(310, 500))
        
        self.calculate_xy_offset_button = wx.Button(self, label="计算")
        self.calculate_xy_offset_button.SetPosition(wx.Point(10, 525))
        self.calculate_xy_offset_button.SetSize(wx.Size(100, 20))
        self.calculate_xy_offset_button.Bind(wx.EVT_BUTTON, self.on_calculate_xy_offset)

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

    def on_calculate_xy_offset(self, event):
        radius = float(self.radius_text_ctrl_xy_offset.GetValue())
        angle = float(self.angle_text_ctrl_xy_offset.GetValue()) * math.pi / 180
        external_x_offset = float(self.external_x_offset_text_ctrl.GetValue())
        result = 计算规定转弯半径和转弯角度下的xy偏移量(radius, angle, external_x_offset)
        self.x_text_ctrl_xy_offset.SetValue(str(result["x"]))
        self.y_text_ctrl_xy_offset.SetValue(str(result["y"]))
        self.x_rounded_text_ctrl.SetValue(str(result["x_rounded"]))
        self.y_rounded_text_ctrl.SetValue(str(result["y_rounded"]))

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
