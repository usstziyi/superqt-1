"""
Demo 15: thread_worker + 生成器 - 可暂停/恢复/中止的后台任务

本 demo 展示 superqt 的 GeneratorWorker（生成器模式）：
- 用 yield 回报进度，无需 @ensure_main_thread
- 内置暂停/恢复/中止支持
- 支持 worker.send() 双向通信
- 应用场景：文件下载、批量处理、长时间计算

对比 FunctionWorker（普通函数模式），GeneratorWorker 是更强大的选择：
  - FunctionWorker: 需要 @ensure_main_thread 或自定义 Signal 更新 UI
  - GeneratorWorker: yield 自动跨越线程，天然安全
"""

import time
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QProgressBar,
    QTextEdit,
)
from superqt.utils import thread_worker


class GeneratorWorkerDemo(QWidget):
    """GeneratorWorker 演示：yield 进度 + 暂停/恢复 + 中止 + 双向通信"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo 15: GeneratorWorker - yield 后台任务")
        self.resize(550, 580)

        layout = QVBoxLayout(self)

        # 说明
        layout.addWidget(
            QLabel(
                "<h2>GeneratorWorker - yield 后台任务</h2>"
                "<p>生成器函数 + @thread_worker = 进度回报 / 暂停 / 恢复 / 中止</p>"
            )
        )

        # ========== 示例 1: 基础进度 ==========
        layout.addWidget(QLabel("<b>示例 1: yield 回报进度</b>"))

        row1 = QHBoxLayout()
        self.progress1 = QProgressBar()
        row1.addWidget(self.progress1)
        self.start_btn1 = QPushButton("开始")
        self.start_btn1.clicked.connect(self.run_basic_yield)
        row1.addWidget(self.start_btn1)
        layout.addLayout(row1)

        self.status1 = QLabel("就绪")
        layout.addWidget(self.status1)

        # ========== 示例 2: 暂停/恢复 + 中止 ==========
        layout.addWidget(QLabel("<b>示例 2: 暂停 / 恢复 / 中止</b>"))

        row2 = QHBoxLayout()
        self.progress2 = QProgressBar()
        row2.addWidget(self.progress2)

        self.start_btn2 = QPushButton("开始")
        self.start_btn2.clicked.connect(self.run_pausable)
        row2.addWidget(self.start_btn2)

        self.pause_btn2 = QPushButton("暂停")
        self.pause_btn2.setEnabled(False)
        self.pause_btn2.clicked.connect(self.toggle_pause)
        row2.addWidget(self.pause_btn2)

        self.abort_btn2 = QPushButton("中止")
        self.abort_btn2.setEnabled(False)
        self.abort_btn2.clicked.connect(self.abort_task)
        row2.addWidget(self.abort_btn2)

        layout.addLayout(row2)

        self.status2 = QLabel("就绪")
        layout.addWidget(self.status2)

        # ========== 示例 3: 双向通信 send ==========
        layout.addWidget(QLabel("<b>示例 3: worker.send() 双向通信</b>"))

        row3 = QHBoxLayout()
        self.progress3 = QProgressBar()
        row3.addWidget(self.progress3)

        self.start_btn3 = QPushButton("开始")
        self.start_btn3.clicked.connect(self.run_send)
        row3.addWidget(self.start_btn3)

        self.send_btn3 = QPushButton("发送: +10%")
        self.send_btn3.setEnabled(False)
        self.send_btn3.clicked.connect(self.send_value)
        row3.addWidget(self.send_btn3)

        layout.addLayout(row3)

        self.status3 = QLabel("就绪")
        layout.addWidget(self.status3)

        # ========== 示例 4: yield 返回复杂数据 ==========
        layout.addWidget(QLabel("<b>示例 4: yield 返回结构化数据</b>"))

        row4 = QHBoxLayout()
        self.progress4 = QProgressBar()
        row4.addWidget(self.progress4)
        self.start_btn4 = QPushButton("开始")
        self.start_btn4.clicked.connect(self.run_structured)
        row4.addWidget(self.start_btn4)
        layout.addLayout(row4)

        self.status4 = QLabel("就绪")
        layout.addWidget(self.status4)

        # 日志
        layout.addWidget(QLabel("操作日志:"))
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(130)
        layout.addWidget(self.log_text)

    # ==================== 后台任务定义 ====================

    @thread_worker
    def task_basic_yield(self, steps: int = 10):
        """示例 1: 基本 yield —— 自动跨线程，无需 @ensure_main_thread"""
        self._log("后台线程开始执行...")
        for i in range(1, steps + 1):
            time.sleep(0.3)
            # yield 的值会通过 yielded 信号发射到主线程
            # 不需要 @ensure_main_thread，不需要自定义 Signal
            yield i * (100 // steps)
        self._log("后台线程执行完毕")
        return f"完成 ({steps} 步)"

    @thread_worker
    def task_pausable(self, total: int = 20):
        """示例 2: 可暂停/可中止的任务

        每次 yield 之间，GeneratorWorker 会检查暂停/中止标记，
        所以必须频繁 yield 才能及时响应控制操作。
        """
        self._log("可暂停任务开始 (支持暂停/恢复/中止)")
        for i in range(1, total + 1):
            time.sleep(0.2)
            # 每次 yield 都会让 Worker 有机会检查控制标记
            yield i * (100 // total)
        self._log("任务正常完成")
        return f"总共 {total} 步完成"

    @thread_worker
    def task_with_send(self):
        """示例 3: 双向通信 —— yield 返回状态，send() 接收外部输入

        子线程可以接收主线程传来的值，实现双向交互。
        """
        self._log("双向通信任务开始")
        count = 0

        # 第一阶段：向上报进度
        for i in range(1, 4):
            time.sleep(0.4)
            yield count

        # 第二阶段：等待主线程传来的值
        self._log("等待主线程发送数据... (点击「发送」按钮)")
        for _ in range(3):
            incre = yield count
            if incre is not None:
                count += incre
                self._log(f"收到主线程数据: +{incre}，当前累计: {count}")
            time.sleep(0.5)
            yield count

        self._log("双向通信任务完成")
        return f"最终值: {count}"

    @thread_worker
    def task_structured_yield(self, batch_count: int = 8):
        """示例 4: yield 返回复杂结构 —— 同时传递进度 + 日志信息

        yield 可以返回任意 Python 对象 (dict, tuple, dataclass 等)，
        yielded 信号会原样传递给 slot。
        """
        self._log("结构化数据任务开始")
        for batch in range(1, batch_count + 1):
            time.sleep(0.35)
            items = batch * 12
            yield {
                "batch": batch,
                "total": batch_count,
                "items": items,
                "percent": int(batch / batch_count * 100),
            }
        self._log("结构化数据任务完成")
        return {"total_batches": batch_count, "total_items": batch_count * 12}

    # ==================== UI 控制方法 ====================

    def run_basic_yield(self):
        """启动示例 1"""
        self.start_btn1.setEnabled(False)
        self.progress1.setValue(0)
        self._log("=== 示例 1: yield 基础进度 ===")

        worker = self.task_basic_yield()
        worker.yielded.connect(self.progress1.setValue)
        worker.returned.connect(
            lambda r: (setattr(self.status1, 'setText', self.status1.setText)(r),
                       self.start_btn1.setEnabled(True))
        )
        # 上面的 lambda 太复杂，拆开：
        self._worker1 = worker
        worker.returned.connect(self._on_basic_done)
        worker.start()

    def _on_basic_done(self, result):
        self.status1.setText(result)
        self.start_btn1.setEnabled(True)

    # ---------- 示例 2 ----------

    def run_pausable(self):
        """启动示例 2"""
        self.start_btn2.setEnabled(False)
        self.pause_btn2.setEnabled(True)
        self.abort_btn2.setEnabled(True)
        self.progress2.setValue(0)
        self.status2.setText("运行中...")
        self._log("=== 示例 2: 可暂停 / 可中止 ===")

        self._worker2 = self.task_pausable()
        self._worker2.yielded.connect(self.progress2.setValue)
        self._worker2.returned.connect(self._on_pausable_done)
        self._worker2.aborted.connect(self._on_pausable_aborted)
        self._worker2.paused.connect(lambda: self._on_paused())
        self._worker2.resumed.connect(lambda: self._on_resumed())
        self._worker2.start()

    def toggle_pause(self):
        """暂停/恢复"""
        if self._worker2.is_paused:
            self._log("请求恢复...")
            self.pause_btn2.setText("暂停")
        else:
            self._log("请求暂停...")
            self.pause_btn2.setText("恢复")
        self._worker2.toggle_pause()

    def abort_task(self):
        """中止任务"""
        self._log("请求中止...")
        self._worker2.quit()

    def _on_pausable_done(self, result):
        self.status2.setText(result)
        self._reset_pausable_buttons()

    def _on_pausable_aborted(self):
        self.status2.setText("已中止")
        self.progress2.setValue(0)
        self._log("⚠️ 任务已中止")
        self._reset_pausable_buttons()

    def _on_paused(self):
        self._log("⏸ 任务已暂停")

    def _on_resumed(self):
        self._log("▶ 任务已恢复")

    def _reset_pausable_buttons(self):
        self.start_btn2.setEnabled(True)
        self.pause_btn2.setEnabled(False)
        self.abort_btn2.setEnabled(False)
        self.pause_btn2.setText("暂停")

    # ---------- 示例 3 ----------

    def run_send(self):
        """启动示例 3"""
        self.send_value_count = 0
        self.start_btn3.setEnabled(False)
        self.send_btn3.setEnabled(True)
        self.progress3.setValue(0)
        self._log("=== 示例 3: 双向通信 ===")

        self._worker3 = self.task_with_send()
        self._worker3.yielded.connect(self._on_send_yielded)
        self._worker3.returned.connect(self._on_send_done)
        self._worker3.start()

    def send_value(self):
        """向子线程发送值"""
        self.send_value_count += 1
        val = self.send_value_count * 10
        self._log(f"主线程 → 子线程: {val}%")
        self._worker3.send(val)

    def _on_send_yielded(self, value):
        self.progress3.setValue(min(value, 100))
        self.status3.setText(f"当前值: {value}%")

    def _on_send_done(self, result):
        self.status3.setText(result)
        self.progress3.setValue(100)
        self.start_btn3.setEnabled(True)
        self.send_btn3.setEnabled(False)

    # ---------- 示例 4 ----------

    def run_structured(self):
        """启动示例 4"""
        self.start_btn4.setEnabled(False)
        self.progress4.setValue(0)
        self._log("=== 示例 4: yield 结构化数据 ===")

        self._worker4 = self.task_structured_yield()
        self._worker4.yielded.connect(self._on_structured_yielded)
        self._worker4.returned.connect(self._on_structured_done)
        self._worker4.start()

    def _on_structured_yielded(self, data: dict):
        self.progress4.setValue(data["percent"])
        self.status4.setText(
            f"批次 {data['batch']}/{data['total']} - {data['items']} 条"
        )

    def _on_structured_done(self, result: dict):
        self.status4.setText(
            f"全部完成: {result['total_batches']} 批次, {result['total_items']} 条"
        )
        self.start_btn4.setEnabled(True)

    # ==================== 工具方法 ====================

    def _log(self, message: str):
        """添加日志（被 GeneratorWorker 在子线程调用也是安全的，
        因为它的输出只用于 yielded/returned/aborted 回调中，
        而这些回调都在主线程执行）
        """
        self.log_text.append(message)
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


if __name__ == "__main__":
    app = QApplication([])
    window = GeneratorWorkerDemo()
    window.show()
    app.exec()
