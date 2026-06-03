"""
Demo 11: QSearchableListWidget & QSearchableTreeWidget - 可搜索列表

本 demo 展示 superqt 的可搜索列表控件：
- QSearchableListWidget: 带搜索框的列表
- QSearchableTreeWidget: 带搜索框的树形列表
- 应用场景：文件浏览器、联系人列表、数据筛选

这些控件在列表/树形结构上方添加了搜索框，方便用户快速过滤内容。
"""

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox,
)
from superqt import QSearchableListWidget, QSearchableTreeWidget


class SearchableListDemo(QWidget):
    """可搜索列表示例"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo 11: 可搜索列表和树形控件")
        self.resize(700, 550)

        main_layout = QHBoxLayout(self)

        # 左侧：可搜索列表
        left_group = QGroupBox("QSearchableListWidget")
        left_layout = QVBoxLayout()

        self.searchable_list = QSearchableListWidget()
        items = [
            "苹果 Apple", "香蕉 Banana", "橙子 Orange",
            "葡萄 Grape", "草莓 Strawberry", "西瓜 Watermelon",
            "桃子 Peach", "梨 Pear", "芒果 Mango",
            "樱桃 Cherry", "柠檬 Lemon", "猕猴桃 Kiwi",
        ]
        self.searchable_list.addItems(items)
        left_layout.addWidget(self.searchable_list)
        left_group.setLayout(left_layout)
        main_layout.addWidget(left_group)

        # 右侧：可搜索树形控件
        right_group = QGroupBox("QSearchableTreeWidget")
        right_layout = QVBoxLayout()

        self.searchable_tree = QSearchableTreeWidget()
        self.setup_tree()
        right_layout.addWidget(self.searchable_tree)
        right_group.setLayout(right_layout)
        main_layout.addWidget(right_group)

    def setup_tree(self):
        """设置树形结构"""
        # 设置列
        self.searchable_tree.setHeaderLabels(["名称", "类型"])

        # 添加水果类别
        fruits = self.searchable_tree.invisibleRootItem()

        # 热带水果
        tropical = self.add_tree_item(fruits, "热带水果", "分类")
        self.add_tree_item(tropical, "芒果", "水果")
        self.add_tree_item(tropical, "香蕉", "水果")
        self.add_tree_item(tropical, "菠萝", "水果")
        self.add_tree_item(tropical, "椰子", "水果")

        # 温带水果
        temperate = self.add_tree_item(fruits, "温带水果", "分类")
        self.add_tree_item(temperate, "苹果", "水果")
        self.add_tree_item(temperate, "梨", "水果")
        self.add_tree_item(temperate, "桃子", "水果")
        self.add_tree_item(temperate, "葡萄", "水果")

        # 浆果
        berries = self.add_tree_item(fruits, "浆果", "分类")
        self.add_tree_item(berries, "草莓", "水果")
        self.add_tree_item(berries, "蓝莓", "水果")
        self.add_tree_item(berries, "树莓", "水果")
        self.add_tree_item(berries, "黑莓", "水果")

        # 展开所有节点
        self.searchable_tree.expandAll()

    def add_tree_item(self, parent, text, type_text):
        """添加树节点"""
        from PySide6.QtWidgets import QTreeWidgetItem
        item = QTreeWidgetItem([text, type_text])
        parent.addChild(item)
        return item


if __name__ == "__main__":
    app = QApplication([])
    window = SearchableListDemo()
    window.show()
    app.exec()
