
# 🤖 人工智能编程实践课程项目合集

这是一个用于管理 **HIT人工智能二学位《人工智能编程实践》课程** 中所有作业的综合性仓库。每个作业以独立模块组织，涵盖算法设计、数据可视化、图神经网络、图谱构建等内容，旨在将理论知识转化为实践能力。

> 🕐 时间有限 + 能力待提升 = 勉强完成，欢迎未来再精进！

---

## 🧠 作业模块目录

### ✅ No1_nQueens：N 皇后问题求解器
- 基于回溯算法实现任意规模的皇后摆放
- 图形化展示解法过程与摆放效果
- 支持用户输入 `n` 并实时显示结果

### ✅ No2_KMeans_KNN：可视化数据分析平台
- 聚类分析：KMeans + Elbow Method（肘部法）图形辅助选择 `k`
- 分类识别：KNN 分类器 + 性能指标分析
- 支持 Excel/CSV 数据加载，界面交互友好
- 内置 Q&A 学习提示，便于理解算法原理

### 🔬 No3_MedKGVis：基于“寻医问药”的检查类知识图谱构建与可视化（课程大作业）
- 项目目标：爬取“检查分类”网页，抽取医学实体与语义关系，构建结构化知识图谱并可视化展示
- 功能模块：
  - 🕸️ 医学网页信息爬虫（分类 → 检查项目 → 详情）
  - 🧩 三元组抽取（实体1@@@关系@@@实体2）
  - 🌐 图数据库（Neo4j）可视化探索
- 项目目录结构位于 `No3_MedKGVis/`，README 独立维护

---

## 🛠 使用说明

运行方式（以任意模块为例）：

```bash
cd No2_KMeans_KNN
python Kmeans_KNN.py
```

或进入大作业目录：

```bash
cd No3_MedKGVis
python crawler/exam_spider.py
```

---

## 📦 依赖环境

安装所有模块的依赖项：

```bash
pip install -r requirements.txt
```

（如模块有独立环境，可进入子目录查阅具体 requirements）

---

## 🖼️ 界面截图

### ♟️ No1_nQueens 解法可视化
![n皇后界面](screenshots/nQueens.jpg)

### 📊 KMeans & KNN 主界面
![界面 1](screenshots/Kmeans&KNN_1.jpg)

### 🔍 聚类或分类结果图展示
![界面 2](screenshots/Kmeans&KNN_2.jpg)


---

## 👨‍🎓 作者信息

> 👤 Branko 及团队成员  
> 🎓 HIT 2025 | 人工智能编程实践课程项目合集  
> 🗂️ GitHub: [@Branko6668](https://github.com/Branko6668)

---

## 📜 License

本项目仅用于课程作业展示与学习用途。
