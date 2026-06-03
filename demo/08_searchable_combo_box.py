"""
Demo 8: QSearchableComboBox - 可搜索下拉框

本 demo 展示 superqt 的 QSearchableComboBox 控件：
- 可以输入文本搜索选项的下拉框
- 支持模糊匹配
- 应用场景：城市选择、联系人选择、大型数据列表

QSearchableComboBox 是 QComboBox 的增强版，允许用户通过输入文本来过滤和搜索选项。
"""

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QGroupBox,
)
from superqt import QSearchableComboBox


class SearchableComboBoxDemo(QWidget):
    """QSearchableComboBox 演示"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo 8: QSearchableComboBox")
        self.resize(450, 450)

        layout = QVBoxLayout(self)

        # 添加说明
        layout.addWidget(
            QLabel(
                "<h2>QSearchableComboBox - 可搜索下拉框</h2>"
                "<p>在输入框中打字来搜索选项</p>"
            )
        )

        # 1. 中国城市选择
        group1 = QGroupBox("1. 选择城市")
        layout1 = QVBoxLayout()
        self.city_combo = QSearchableComboBox()
        cities = [
            "北京", "上海", "广州", "深圳", "杭州", "南京", "成都",
            "重庆", "武汉", "西安", "苏州", "天津", "长沙", "郑州",
            "青岛", "大连", "厦门", "昆明", "哈尔滨", "济南",
            "Beijing", "Shanghai", "Guangzhou", "Shenzhen",
        ]
        self.city_combo.addItems(cities)
        self.city_combo.currentTextChanged.connect(
            lambda t: self.on_selected("城市", t)
        )
        layout1.addWidget(self.city_combo)
        group1.setLayout(layout1)
        layout.addWidget(group1)

        # 2. 编程语言选择
        group2 = QGroupBox("2. 选择编程语言")
        layout2 = QVBoxLayout()
        self.lang_combo = QSearchableComboBox()
        languages = [
            "Python", "JavaScript", "TypeScript", "Java", "C++",
            "C#", "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin",
            "R", "MATLAB", "Shell", "SQL", "HTML/CSS",
        ]
        self.lang_combo.addItems(languages)
        self.lang_combo.currentTextChanged.connect(
            lambda t: self.on_selected("语言", t)
        )
        layout2.addWidget(self.lang_combo)
        group2.setLayout(layout2)
        layout.addWidget(group2)

        # 3. 字体选择
        group3 = QGroupBox("3. 选择字体")
        layout3 = QVBoxLayout()
        self.font_combo = QSearchableComboBox()
        fonts = [
            "Arial", "Helvetica", "Times New Roman", "Courier New",
            "Verdana", "Georgia", "Palatino", "Garamond",
            "Bookman", "Comic Sans MS", "Trebuchet MS", "Impact",
            "宋体", "黑体", "微软雅黑", "楷体", "仿宋",
        ]
        self.font_combo.addItems(fonts)
        self.font_combo.currentTextChanged.connect(
            lambda t: self.on_selected("字体", t)
        )
        layout3.addWidget(self.font_combo)
        group3.setLayout(layout3)
        layout.addWidget(group3)

        # 状态显示
        self.status_label = QLabel("请选择...")
        layout.addWidget(self.status_label)

    def on_selected(self, category, text):
        """处理选择"""
        self.status_label.setText(f"已选择{category}: <b>{text}</b>")


if __name__ == "__main__":
    app = QApplication([])
    window = SearchableComboBoxDemo()
    window.show()
    app.exec()
