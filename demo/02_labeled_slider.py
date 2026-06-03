"""
Demo 2: QLabeledSlider - 带标签的滑块

本 demo 展示了 superqt 的 QLabeledSlider 控件：
- 滑块旁边显示可编辑的数值标签
- 支持不同的标签模式
- 信号与槽的连接

QLabeledSlider 是 QSlider 的增强版，在滑块旁边显示一个可编辑的 SpinBox 标签，
用户可以直接输入数值或拖动滑块。
"""

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from superqt import QLabeledSlider


class LabeledSliderDemo(QWidget):
    """QLabeledSlider 演示"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo 2: QLabeledSlider")
        self.resize(500, 300)

        layout = QVBoxLayout(self)

        # 添加说明
        layout.addWidget(QLabel("<b>QLabeledSlider</b> - 拖动滑块或直接编辑数值"))

        # 1. 基本水平滑块 - 右侧显示数值
        layout.addWidget(QLabel("\n1. 基本滑块 (右侧显示数值):"))
        self.slider1 = QLabeledSlider(Qt.Orientation.Horizontal)
        self.slider1.setRange(0, 100)
        self.slider1.setValue(50)
        self.slider1.valueChanged.connect(lambda v: self.on_value_changed("滑块1", v))
        layout.addWidget(self.slider1)

        # 2. 左侧显示数值标签
        layout.addWidget(QLabel("\n2. 左侧显示数值:"))
        self.slider2 = QLabeledSlider(Qt.Orientation.Horizontal)
        self.slider2.setRange(0, 100)
        self.slider2.setValue(25)
        self.slider2.setEdgeLabelMode(QLabeledSlider.EdgeLabelMode.LabelIsValue)
        layout.addWidget(self.slider2)

        # 3. 温度范围滑块 (-40 到 40)
        layout.addWidget(QLabel("\n3. 温度范围滑块:"))
        self.temp_slider = QLabeledSlider(Qt.Orientation.Horizontal)
        self.temp_slider.setRange(-40, 40)
        self.temp_slider.setValue(22)
        layout.addWidget(self.temp_slider)

        # 4. 垂直滑块
        layout.addWidget(QLabel("\n4. 垂直滑块:"))
        h_layout = QHBoxLayout()
        self.vertical_slider = QLabeledSlider(Qt.Orientation.Vertical)
        self.vertical_slider.setRange(0, 100)
        self.vertical_slider.setValue(75)
        h_layout.addWidget(self.vertical_slider)
        h_layout.addWidget(QLabel("音量控制"))
        h_layout.addStretch()
        layout.addLayout(h_layout)

        layout.addStretch()

    def on_value_changed(self, name, value):
        """处理数值变化"""
        print(f"{name} 的数值变为: {value}")


if __name__ == "__main__":
    app = QApplication([])
    window = LabeledSliderDemo()
    window.show()
    app.exec()
