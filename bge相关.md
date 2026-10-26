bge相关

（1）bge的基本步骤包括哪些：

主要步骤包括切块、向量化、检索、生成。

（2）你当时做bge用的哪个模型，目前的bge模型有哪些。

我当时使用的是bge-v1.5-large-zh模型，专门为中文检索而适配的模型。

那么现在有哪些bge模型呢,具体如下：

![1793004732646](C:\Users\10351260\AppData\Roaming\Typora\typora-user-images\1793004732646.png)

![1793004753141](C:\Users\10351260\AppData\Roaming\Typora\typora-user-images\1793004753141.png)



## bge-m3

bge-m3不仅仅是传统的向量，而且还有sparse lexical、multi-vector等多个功能。

### dense

输入一句话，将其改为向量化编码，如1024维向量。

### sparse lexical

保留“关键词权重”的稀疏表示
Sparse lexical 可以理解成更聪明的关键词检索，类似 BM25，但由模型学习词的重要性。

它不是把一句话压成一个稠密向量，而是把文本表示成很多词的权重，例如：

```
{
  "苹果": 0.8,
  "手机": 0.6,
  "电池": 1.2,
  "发热": 1.5,
  "怎么办": 0.3
}
```

优点

- 对关键词、型号、术语、错误码、专有名词特别友好。
- 可解释性更强，因为你能看到哪些词贡献了匹配。
- 适合技术文档、API 文档、日志、代码、论文、产品手册。

缺点

- 语义泛化能力弱于 dense。
- 如果用户和文档用词完全不同，它可能找不到。
- 比如用户搜“手机很烫”，文档写“设备温度异常升高”，sparse 可能不如 dense。

Multi-vector

一个文本变成多个向量，做细粒度匹配

普通 dense 是：

text

```text
query -> 1 个向量
doc   -> 1 个向量
```

### multi-vector 

text

```text
query -> 多个向量
doc   -> 多个向量
```

比如 query：

> 苹果手机电池发热怎么办？

它可能给每个重要 token 或片段生成向量：

text

```text
苹果手机 -> 向量 A
电池     -> 向量 B
发热     -> 向量 C
怎么办   -> 向量 D
```

文档也会有很多向量：

text

```text
iPhone      -> 向量 1
battery     -> 向量 2
overheating -> 向量 3
solution    -> 向量 4
...
```

检索时不是简单比较“query 整体”和“doc 整体”，而是看 query 的每个局部是否都能在 doc 里找到对应内容。

这类方法常见代表是 ColBERT 风格的 late interaction。

优点

- 匹配更细，效果通常比单向量 dense 更好。
- 对长文档、多主题文档更友好。
- 能减少“整篇看起来相关，但关键点没覆盖”的情况。
- 适合高质量检索、rerank、复杂 query。

缺点

- 存储成本高，因为一个文档不止一个向量。
- 检索计算更贵。
- 工程复杂度高，不是所有向量数据库都原生支持。



新项目下，这些技术要怎么使用：

最简单只使用dense:

```
query -> dense vector -> 向量库检索 -> top-k 文档
```

更稳的方案

dense + sparse lexical

```
dense 负责语义召回
sparse 负责关键词召回
最后把分数融合
```

适合技术文档、产品文档、代码文档、知识库问答。

更高质量的方案：

```
dense + sparse lexical 做初召
multi-vector 或 reranker 做精排
```

**dense 看意思，sparse 看关键词，multi-vector 看局部细节。**
最常见的生产组合是：**dense + sparse 做召回，reranker 或 multi-vector 做精排**。