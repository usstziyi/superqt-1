"""
Demo 16: Python 生成器与 yield 完全指南

本 demo 讲解 yield 的所有用法，帮助理解 superqt GeneratorWorker 的底层原理：
  - yield: 产出值（生成器 → 外部）
  - value = yield: 接收值（外部 → 生成器，send）
  - return: 终止生成器
  - yield from: 委托子生成器

所有示例都是纯 Python，无需任何 GUI 库，直接在终端运行即可看到效果。
"""


def separator(title: str):
    """打印分隔标题"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print("=" * 60)


# ============================================================
# 一、yield 基础：产出值
# ============================================================
separator("一、yield 基础：产出值")

print("""
定义生成器函数（含 yield 关键字的函数就是生成器函数）:

    def count_up_to(n):
        i = 1
        while i <= n:
            yield i        # ← 产出 i，函数暂停于此
            i += 1         # ← 下次 next() 时从这里继续

    gen = count_up_to(3)         # 调用不执行函数体，返回生成器对象
    print(next(gen))  # 1        # 执行到第一个 yield，产出 1，暂停
    print(next(gen))  # 2        # 从上次暂停处继续，产出 2，暂停
    print(next(gen))  # 3        # 同上
    print(next(gen))  # 抛出 StopIteration  (没有更多 yield)
""")


def count_up_to(n: int):
    """最简生成器：产出 1 到 n"""
    i = 1
    while i <= n:
        yield i
        i += 1


# 只拿到生成器对象，函数体暂停在第 0 行
gen = count_up_to(3) 
print(">>> gen = count_up_to(3)")
print(f"    next(gen) → {next(gen)}")
print(f"    next(gen) → {next(gen)}")
print(f"    next(gen) → {next(gen)}")
try:
    print(f"    next(gen) → {next(gen)}")
except StopIteration:
    print("    next(gen) → StopIteration (生成器耗尽)")


# ============================================================
# 二、yield 在循环中：逐次产出进度
# ============================================================
separator("二、yield 在循环中：逐次产出进度")

print("""
这是 superqt GeneratorWorker 的核心模式:

    gen = download_task(5)
    for progress in gen:        # for 循环自动调用 next()
        print(f"进度: {progress}")

""")


def download_task(n_files: int):
    """模拟下载，每次 yield 返回当前进度"""
    for i in range(1, n_files + 1):
        # time.sleep(0.3)  在 superqt 中，这里对应一个文件的下载
        yield i / n_files * 100
    return f"{n_files} 个文件下载完成"


print(">>> for progress in download_task(5):")
gen = download_task(5)
# # for 循环不捕获 StopIteration.value，return 值被丢弃
for progress in gen:
    print(f"    进度: {progress:.0f}%")

print(">>> next(gen)")
# 要拿到 return 值，必须手动 next()
gen = download_task(5)
while True:
    try:
        print(f"    进度: {next(gen):.0f}%")
    except StopIteration as e:
        print(e.value)   # "5 个文件下载完成"
        break

# ============================================================
# 三、yield 接收值：send()
# ============================================================
separator("三、yield 接收值：send()")

print("""
生成器不仅能产出值，还能接收外部传入的值:

    name = yield output    # 产出 output，同时等待外部 send(name)

    gen.send("Alice")       # 给生成器传值，name 将获得 "Alice"

首次必须用 send(None) 或 next() 启动生成器。
""")


def accumulator():
    """累加器：yield 返回当前总和，send 接收要加的数值"""
    total = 0
    while True:
        received = yield total       # 产出 total，等待接收值
        if received is None:
            break                     # 收到 None 就退出
        total += received
        print(f"      收到 {received:+d}，累计 = {total}")

"""
时刻              角色         做什么 
执行到 yield 时   动词（产出）   把 total 的值推出去 
恢复执行时        名词（值）     整个 yield total 变成一个值（send 进来的）
"""
acc = accumulator()
"""
# 这两种写法等价：
next(acc)         # 自动发送 None，启动生成器
acc.send(None)    # 显式发送 None，效果相同
"""
next(acc)  # 启动生成器，执行到第一个 yield
print(">>> acc = accumulator()")
print("    next(acc)  # 启动生成器")
print("    acc.send(10)  # 发 10 进去, received = 10, total 变成 10")
acc.send(10)
print("    acc.send(20)  # 发 20 进去, received = 20, total 变成 30")
acc.send(20)
print("    acc.send(-5)  # 发 -5 进去, received = -5, total 变成 25")
acc.send(-5)
print("    acc.send(None)  # 发 None, 生成器退出")
try:
    acc.send(None)
except StopIteration:
    print("    → StopIteration (正常退出)")

print("""
这就是 superqt worker.send() 的底层原理：
  主线程 worker.send(value) → 子线程 value = yield xxx 收到值
""")


# ============================================================
# 四、return 终止生成器，附带回值
# ============================================================
separator("四、return 终止生成器，附带回值")

print("""
生成器函数内部 return 一个值时，不会直接返回给调用者，
而是作为 StopIteration 异常的 .value 属性：

    gen = download_task(3)
    for p in gen:
        print(p)
    # StopIteration.value =  "3 个文件下载完成"
""")


def task_with_return():
    yield 10
    yield 20
    return "任务完成"


print(">>> gen = task_with_return()")
gen = task_with_return()
print(f"    next(gen) → {next(gen)}")
print(f"    next(gen) → {next(gen)}")
try:
    next(gen)
except StopIteration as e:
    print(f"    StopIteration.value → {e.value!r}")

print("""
superqt GeneratorWorker 正是通过捕获 StopIteration 拿到 return 值，
然后发射 returned 信号。
""")


# ============================================================
# 五、yield from：委托子生成器
# ============================================================
separator("五、yield from：委托子生成器")

print("""
yield from 把一个生成器委托给另一个：

    def outer():
        yield from inner()    # 把 inner 的所有 yield 透传出去

等价于:

    def outer():
        for val in inner():
            yield val
""")


def sub_task_1():
    yield "A1"
    yield "A2"


def sub_task_2():
    yield "B1"
    yield "B2"


def main_task():
    print("  开始 main_task")
    yield from sub_task_1()      # 委托给子任务 1
    yield from sub_task_2()      # 委托给子任务 2
    print("  main_task 结束")
    return "全部完成"


print(">>> for val in main_task():")
for val in main_task():
    print(f"    产出: {val}")


# ============================================================
# 六、close() 和 throw()：外部控制生成器
# ============================================================
separator("六、close() 和 throw()：外部控制生成器")

print("""
.close()  在生成器暂停处抛出 GeneratorExit，强制退出
.throw()  在生成器暂停处抛出自定义异常

superqt 的 worker.quit() 就是通过类似机制中止任务的。
""")


def interruptible_task():
    print("  任务开始")
    try:
        for i in range(100):
            yield i      # 每次 yield 都可能被 close()
    except GeneratorExit:
        print("  ⚠ 收到 close()，清理资源...")
        # 这里做清理：关闭文件、释放连接等
    print("  任务结束")


print(">>> gen = interruptible_task()")
gen = interruptible_task()
print(f"    next(gen) → {next(gen)}")
print(f"    next(gen) → {next(gen)}")
print("    gen.close()  # 在 yield 处注入 GeneratorExit")
gen.close()
# gen.throw()
print("    → 生成器已关闭")


# ============================================================
# 七、生成器 vs 普通函数 vs 列表（内存对比）
# ============================================================
separator("七、内存对比：生成器 vs 列表")

print("""
生成器是「惰性求值」—— 用多少算多少，不一次性加载所有数据到内存。

    def gen_range(n):           range_list = list(range(n))
        for i in range(n):      return range_list     # 内存占用 O(n)
            yield i              # 内存占用 O(1)

对于百万级数据，生成器几乎不占内存。
""")

import sys


def generate_numbers(n):
    for i in range(n):
        yield i


n = 1_000_000
gen_mem = sys.getsizeof(generate_numbers(n))
list_mem = sys.getsizeof(list(generate_numbers(n)))
# 生成器的 208 bytes 只是存储它的函数指针、局部变量槽位、状态标志等。
# 无论它将来会产出 100 万还是 100 亿个值，它始终只有 ~208 bytes，因为它 算一个丢一个，从不攒着
print(f">>> 生成器 1,000,000 个元素: {gen_mem} bytes")
print(f">>> 列表   1,000,000 个元素: {list_mem} bytes")
print(f">>> 列表是生成器的 {list_mem / gen_mem:.0f} 倍内存")


# ============================================================
# 八、综合示例：模拟 superqt GeneratorWorker 的行为
# ============================================================
separator("八、综合示例：模拟 GeneratorWorker")

print("""
下面用纯 Python 模拟 superqt GeneratorWorker 的核心逻辑：

    子线程: yield 产出值
    主线程: 收到 yielded  → 更新 UI
    主线程: send() 传入值 → 子线程 yield 接收
""")


class FakeWorker:
    """模拟 GeneratorWorker，不依赖 Qt"""
    def __init__(self, gen):
        self.gen = gen
        self._callbacks = {}

    def on(self, event, callback):
        """模拟 signal.connect()"""
        self._callbacks[event] = callback
        return self

    def start(self):
        print("  [Worker] 后台线程开始工作")
        result = None
        try:
            val = None
            while True:
                val = self.gen.send(val)  # 推进生成器
                # 模拟 yielded 信号
                cb = self._callbacks.get("yielded")
                if cb:
                    print(f"  [主线程] yielded 回调: cb({val})")
                    cb(val)
        except StopIteration as e:
            result = e.value
        # 模拟 returned 信号
        cb = self._callbacks.get("returned")
        if cb:
            print(f"  [主线程] returned 回调: cb({result!r})")
            cb(result)


# 用生成器模拟一个「带暂停条件」的后台任务
def simulated_worker(total=5):
    for i in range(1, total + 1):
        # 模拟耗时操作
        print(f"  [子线程] 处理第 {i}/{total} 步...")
        yield f"进度 {i}/{total}"       # 回报进度
    return f"任务完成: 共 {total} 步"


print(">>> worker = FakeWorker(simulated_worker(5))")
gen = simulated_worker(5)
worker = FakeWorker(gen)
worker.on("yielded", lambda v: print(f"        → 更新 UI: [{v}]"))
worker.on("returned", lambda r: print(f"        → 显示结果: {r}"))

# # 链式写法 — 靠 return self 实现
# worker.on("yielded", cb1).on("returned", cb2).start()

worker.start()

print("""
这就是 superqt GeneratorWorker 的完整模型。
""")


# ============================================================
# 总结
# ============================================================
separator("总结")

print("""
  yield x         产出 x，暂停，等待下次 next()/send()
  x = yield       产出 None，等待外部 send(x)
  return v        终止生成器，v 存入 StopIteration.value
  yield from g    委托子生成器 g
  gen.close()     在 yield 处注入 GeneratorExit，强制退出
  gen.throw(E)    在 yield 处注入异常 E

在 superqt 中：
yield 的本质就是子线程往主线程 推送数据的管道 ，用完就丢，不需要缓存
  yield → worker.yielded 信号 (主线程回调) (子线程->主线程)
  return → worker.returned 信号 (主线程回调) (子线程->主线程)
  send  → worker.send() (主线程 → 子线程)
  close → worker.quit() (中止任务)
""")
