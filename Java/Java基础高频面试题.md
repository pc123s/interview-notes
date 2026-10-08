# Java 基础高频面试题（示例）

> 结构说明：**问题 → 答案要点 → 深入理解**，后续内容可按此格式补充。

## 一、基础语法

### 1. == 和 equals() 的区别？

**答案要点：**
- `==` 比较的是**值**：基本类型比较数值，引用类型比较**内存地址**
- `equals()` 是 `Object` 类的方法，默认实现也是比较地址（等价于 `==`），但 `String`、包装类等重写了它，比较的是**内容**
- 重写 `equals()` 时必须同时重写 `hashCode()`，否则违反「equals 相等则 hashCode 必相等」的约定，会导致 HashMap/HashSet 等容器出错

**深入理解：**
```java
String a = new String("abc");
String b = new String("abc");
a == b;       // false，地址不同
a.equals(b);  // true，内容相同
```

### 2. String、StringBuilder、StringBuffer 的区别？

**答案要点：**

| 类型 | 可变性 | 线程安全 | 性能 |
|------|--------|----------|------|
| String | 不可变 | 安全（final + 不可变） | 拼接时产生新对象，慢 |
| StringBuilder | 可变 | 不安全 | 快 |
| StringBuffer | 可变 | 安全（synchronized） | 比 StringBuilder 慢 |

**深入理解：**
- String 不可变的好处：可作 HashMap 的 key、线程安全、字符串常量池复用、安全性（防篡改）
- 单线程拼接用 StringBuilder，多线程用 StringBuffer

## 二、面向对象

### 3. 重载（Overload）和重写（Override）的区别？

**答案要点：**
- **重载**：同一个类中，方法名相同、参数列表不同（个数/类型/顺序），与返回值无关，编译期多态
- **重写**：子类对父类方法重新实现，方法签名一致，运行期多态（动态分派）
- 重写规则：访问权限不能更小、异常不能抛更宽、`static`/`private`/`final` 方法不能被重写

### 4. 接口和抽象类的区别？

**答案要点：**

| 对比项 | 抽象类 | 接口 |
|--------|--------|------|
| 继承 | 单继承 | 多实现 |
| 成员变量 | 任意 | 默认 public static final |
| 构造方法 | 有 | 无 |
| 设计理念 | is-a，代码复用 | has-a / can-do，行为契约 |
| JDK8+ | 可有普通方法 | 可有 default/static 方法 |

## 三、集合框架

### 5. ArrayList 和 LinkedList 的区别？

**答案要点：**
- **ArrayList**：基于动态数组，支持 O(1) 随机访问，尾部增删快，中间增删需移动元素 O(n)；扩容 1.5 倍
- **LinkedList**：基于双向链表，随机访问 O(n)，头尾增删 O(1)
- 实际开发中 ArrayList 更常用；LinkedList 还实现了 Deque 接口，可作队列/栈使用

### 6. HashMap 的底层原理？

**答案要点：**
- JDK8+ 底层：**数组 + 链表 + 红黑树**
- put 流程：`hash(key)` → 数组下标 `(n-1) & hash` → 冲突时链表尾插 → 链表长度 ≥ 8 且数组 ≥ 64 时转红黑树
- 扩容：默认容量 16，负载因子 0.75，扩容为 2 倍并重新计算下标
- 线程不安全：JDK7 并发扩容可能形成环形链表死循环；JDK8 会数据覆盖。并发场景用 `ConcurrentHashMap`

**深入理解：**
- 为什么容量是 2 的幂？—— `(n-1) & hash` 等价取模且位运算更快，扩容时元素只可能在原位置或「原位置 + 旧容量」
- 红黑树查询 O(log n)，比链表 O(n) 稳定

### 7. ConcurrentHashMap 如何保证线程安全？

**答案要点：**
- JDK7：**分段锁（Segment + ReentrantLock）**，默认 16 段
- JDK8：**CAS + synchronized** 锁单个桶头节点（粒度更细），`putIfAbsent` 等原子操作
- 读操作不加锁（volatile 保证可见性），size 用 baseCount + CounterCell 数组统计

## 四、多线程与并发

### 8. synchronized 和 ReentrantLock 的区别？

**答案要点：**

| 对比项 | synchronized | ReentrantLock |
|--------|--------------|---------------|
| 实现 | JVM 层面（monitor 锁） | JDK 层面（AQS） |
| 释放 | 自动释放 | 必须 finally 中 unlock |
| 锁机制 | 非公平 | 可公平可非公平 |
| 高级功能 | 无 | 可中断、超时、Condition 多条件 |
| 性能 | JDK6 优化后（锁升级）差距很小 | 略好 |

**深入理解（锁升级）：** 无锁 → 偏向锁 → 轻量级锁（CAS 自旋）→ 重量级锁

### 9. volatile 的作用？

**答案要点：**
1. **保证可见性**：写操作立即刷回主内存，读操作从主内存读（MESI 缓存一致性协议 + 内存屏障）
2. **禁止指令重排序**：通过内存屏障（load/store barrier）实现
3. **不保证原子性**：`i++` 这类复合操作仍然不安全，需要 synchronized / CAS

## 五、JVM

### 10. JVM 内存结构？

**答案要点：**
- **线程私有**：程序计数器、虚拟机栈（栈帧：局部变量表、操作数栈、动态链接、返回地址）、本地方法栈
- **线程共享**：堆（对象实例，GC 主战场）、方法区/元空间（类信息、常量池）
- 异常：栈溢出 `StackOverflowError`；堆溢出 `OutOfMemoryError: Java heap space`

### 11. 垃圾回收算法有哪些？

**答案要点：**
- **标记-清除**：产生内存碎片
- **标记-复制**：内存利用率低，适合新生代（对象朝生夕灭）
- **标记-整理**：无碎片，适合老年代
- **分代收集**：新生代复制算法（Eden:S0:S1 = 8:1:1），老年代标记-整理/清除

**深入理解：**
- GC Roots：虚拟机栈引用、静态变量、常量、本地方法栈引用
- 常见收集器：Serial / ParNew / Parallel Scavenge（吞吐量优先）/ CMS / G1 / ZGC
- CMS 问题：并发清理产生浮动垃圾，标记-清除有碎片，可能触发 Full GC

---

*（示例内容到此。后续按「目录结构」中的规划持续补充各模块。）*
