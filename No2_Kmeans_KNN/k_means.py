import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import pandas as pd
import matplotlib
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

class AIPlatformUI:
    def __init__(self, root):
        self.root = root
        self.root.title("2024120483_黄斌_Kmeans&KNN")
        self.df_kmeans = None
        self.df_knn = None
        self.build_gui()

    def build_gui(self):
        self.notebook = ttk.Notebook(self.root)
        self.kmeans_tab = ttk.Frame(self.notebook)
        self.knn_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.kmeans_tab, text="🔷KMeans 聚类🔷")
        self.notebook.add(self.knn_tab, text="🔷KNN 分类🔷")
        self.notebook.pack(expand=1, fill="both")

        self.build_kmeans_tab()
        self.build_knn_tab()

    def build_kmeans_tab(self):
        frame = self.kmeans_tab

        param_frame = ttk.LabelFrame(frame, text="参数设置")
        param_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(param_frame, text="聚类数 k:").grid(row=0, column=0, padx=5, pady=5)
        self.k_entry = ttk.Entry(param_frame, width=6)
        self.k_entry.insert(0, "3")
        self.k_entry.grid(row=0, column=1, padx=5)

        self.kmeans_load_btn = ttk.Button(param_frame, text="一键加载", command=self.load_kmeans_data)
        self.kmeans_load_btn.grid(row=0, column=2, padx=5)

        self.kmeans_select_btn = ttk.Button(param_frame, text="选择数据", command=self.select_kmeans_file)
        self.kmeans_select_btn.grid(row=0, column=3, padx=5)

        ttk.Button(param_frame, text="执行聚类", command=self.run_kmeans).grid(row=0, column=4, padx=5)
        ttk.Button(param_frame, text="📘Q&A", command=self.show_qa_kmeans).grid(row=0, column=5, padx=5)

        ttk.Label(param_frame, text="点击一键加载\n（同级目录的第一个Excel或CSV文件）",
                  font=("微软雅黑", 9), foreground="gray").grid(row=1, column=0, columnspan=6)

        self.kmeans_file_label = ttk.Label(frame, text="当前文件：未加载", foreground="gray")
        self.kmeans_file_label.pack(pady=(0, 10))

        self.kmeans_output_frame = ttk.Frame(frame)
        self.kmeans_output_frame.pack(padx=10, pady=5, fill="both")

    def load_kmeans_data(self):
        candidates = [f for f in os.listdir(os.getcwd())
                      if f.lower().endswith(('.csv', '.xls', '.xlsx'))]

        if not candidates:
            messagebox.showwarning("未找到文件", "当前目录中未找到任何 Excel 或 CSV 数据文件。")
            return

        file = os.path.join(os.getcwd(), candidates[0])
        try:
            if file.endswith(".csv"):
                self.df_kmeans = pd.read_csv(file)
            else:
                self.df_kmeans = pd.read_excel(file)

            self.kmeans_load_btn.config(text="已加载")
            self.kmeans_select_btn.config(text="选择数据")
            self.kmeans_file_label.config(text=f"当前文件：{os.path.basename(file)}", foreground="green")
        except Exception as e:
            messagebox.showerror("加载失败", f"读取文件出错：{str(e)}")

    def select_kmeans_file(self):
        file = filedialog.askopenfilename(filetypes=[("CSV 文件", "*.csv"), ("Excel 文件", "*.xls *.xlsx")])
        if file:
            self.df_kmeans = pd.read_csv(file)
            self.kmeans_select_btn.config(text="已加载")
            self.kmeans_load_btn.config(text="一键加载")
            self.kmeans_file_label.config(text=f"当前文件：{os.path.basename(file)}", foreground="green")

    def run_kmeans(self):
        if self.df_kmeans is None:
            messagebox.showwarning("请先加载数据", "未检测到数据，请点击加载按钮")
            return
        try:
            k = int(self.k_entry.get())
            X = self.df_kmeans[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']]
            model = KMeans(n_clusters=k, random_state=42, n_init='auto')
            self.df_kmeans['Cluster'] = model.fit_predict(X)
            centers = model.cluster_centers_

            for widget in self.kmeans_output_frame.winfo_children():
                widget.destroy()

            ttk.Label(self.kmeans_output_frame, text="聚类中心：").pack()
            columns = ["簇", "SepalLen", "SepalWid", "PetalLen", "PetalWid"]
            table = ttk.Treeview(self.kmeans_output_frame, columns=columns, show="headings", height=k)
            for col in columns:
                table.heading(col, text=col)
                table.column(col, width=80, anchor="center")
            for i, c in enumerate(centers):
                table.insert("", "end", values=[i]+[round(x, 2) for x in c])
            table.pack(pady=5)

            # Elbow Method 折线图展示
            distortions = []
            for i in range(1, 10):
                km = KMeans(n_clusters=i, random_state=42, n_init='auto')
                km.fit(X)
                distortions.append(km.inertia_)

            fig, ax = plt.subplots(figsize=(4.5, 3.5))
            ax.plot(range(1, 10), distortions, marker='o', color='dodgerblue')
            ax.set_title("Elbow Method（肘部法）")
            ax.set_xlabel("簇数量 k")
            ax.set_ylabel("簇内误差平方和")
            ax.grid(True)

            img_frame = ttk.Frame(self.kmeans_output_frame, borderwidth=2, relief="ridge", padding=5)
            img_frame.pack(pady=10)
            canvas = FigureCanvasTkAgg(fig, master=img_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()
            plt.close(fig)

            self.kmeans_load_btn.config(text="一键加载")
            self.kmeans_select_btn.config(text="选择数据")

        except Exception as e:
            messagebox.showerror("聚类失败", str(e))

    def show_qa_kmeans(self):
        messagebox.showinfo("📘Q&A",
            "Q: KMeans 是什么？\n"
            "A: 无监督聚类算法，将数据自动划分为 k 个簇。\n\n"
            "Q: 什么是 Elbow Method？\n"
            "A: 通过画图观察随着 k 值增加误差的变化趋势，从而选择合理聚类数。")
    def build_knn_tab(self):
        frame = self.knn_tab

        param_frame = ttk.LabelFrame(frame, text="参数设置")
        param_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(param_frame, text="邻居数 k:").grid(row=0, column=0, padx=5, pady=5)
        self.knn_entry = ttk.Entry(param_frame, width=6)
        self.knn_entry.insert(0, "5")
        self.knn_entry.grid(row=0, column=1, padx=5)

        self.knn_load_btn = ttk.Button(param_frame, text="一键加载", command=self.load_knn_data)
        self.knn_load_btn.grid(row=0, column=2, padx=5)

        self.knn_select_btn = ttk.Button(param_frame, text="选择数据", command=self.select_knn_file)
        self.knn_select_btn.grid(row=0, column=3, padx=5)

        ttk.Button(param_frame, text="执行分类", command=self.run_knn).grid(row=0, column=4, padx=5)
        ttk.Button(param_frame, text="📘Q&A", command=self.show_qa_knn).grid(row=0, column=5, padx=5)

        ttk.Label(param_frame, text="点击一键加载\n（同级目录的第一个Excel或CSV文件）",
                  font=("微软雅黑", 9), foreground="gray").grid(row=1, column=0, columnspan=6)

        self.knn_file_label = ttk.Label(frame, text="当前文件：未加载", foreground="gray")
        self.knn_file_label.pack(pady=(0, 10))

        self.knn_output_frame = ttk.Frame(frame)
        self.knn_output_frame.pack(padx=10, pady=5, fill="both")

    def load_knn_data(self):
        candidates = [f for f in os.listdir(os.getcwd())
                      if f.lower().endswith(('.csv', '.xls', '.xlsx'))]

        if not candidates:
            messagebox.showwarning("未找到文件", "当前目录中未找到任何 Excel 或 CSV 数据文件。")
            return

        file = os.path.join(os.getcwd(), candidates[0])
        try:
            if file.endswith(".csv"):
                self.df_knn = pd.read_csv(file)
            else:
                self.df_knn = pd.read_excel(file)

            self.knn_load_btn.config(text="已加载")
            self.knn_select_btn.config(text="选择数据")
            self.knn_file_label.config(text=f"当前文件：{os.path.basename(file)}", foreground="green")
        except Exception as e:
            messagebox.showerror("加载失败", f"读取文件出错：{str(e)}")

    def select_knn_file(self):
        file = filedialog.askopenfilename(filetypes=[("CSV 文件", "*.csv"), ("Excel 文件", "*.xls *.xlsx")])
        if file:
            self.df_knn = pd.read_csv(file)
            self.knn_select_btn.config(text="已加载")
            self.knn_load_btn.config(text="一键加载")
            self.knn_file_label.config(text=f"当前文件：{os.path.basename(file)}", foreground="green")

    def run_knn(self):
        if self.df_knn is None:
            messagebox.showwarning("请先加载数据", "未检测到数据，请点击加载按钮")
            return
        try:
            k = int(self.knn_entry.get())
            if 'Species' not in self.df_knn.columns:
                messagebox.showerror("数据错误", "数据集中缺少 'Species' 标签字段")
                return

            X = self.df_knn[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']]
            y = self.df_knn['Species']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

            model = KNeighborsClassifier(n_neighbors=k)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            for widget in self.knn_output_frame.winfo_children():
                widget.destroy()

            report = classification_report(y_test, y_pred, output_dict=True)

            ttk.Label(self.knn_output_frame, text="分类性能指标：").pack()
            table = ttk.Treeview(self.knn_output_frame, columns=["类名", "精确率", "召回率", "F1值", "支持数"],
                                 show="headings", height=5)
            for col in ["类名", "精确率", "召回率", "F1值", "支持数"]:
                table.heading(col, text=col)
                table.column(col, width=90, anchor="center")
            for label in ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']:
                m = report[label]
                row = [label, f"{m['precision']:.2f}", f"{m['recall']:.2f}", f"{m['f1-score']:.2f}", int(m['support'])]
                table.insert("", "end", values=row)
            table.pack(pady=5)

            fig, ax = plt.subplots(figsize=(4.5, 3.5))
            ax.scatter(X_test['PetalLengthCm'], X_test['PetalWidthCm'], c=pd.factorize(y_pred)[0], cmap='Set2')
            ax.set_title(f"KNN 分类图（k={k}）")
            ax.set_xlabel("Petal Length")
            ax.set_ylabel("Petal Width")

            img_frame = ttk.Frame(self.knn_output_frame, borderwidth=2, relief="ridge", padding=5)
            img_frame.pack(pady=10)
            canvas = FigureCanvasTkAgg(fig, master=img_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()
            plt.close(fig)

            self.knn_load_btn.config(text="一键加载")
            self.knn_select_btn.config(text="选择数据")

        except Exception as e:
            messagebox.showerror("分类失败", str(e))

    def show_qa_knn(self):
        messagebox.showinfo("📘Q&A",
            "Q: KNN 是什么？\n"
            "A: 有监督分类算法，基于样本之间的距离做多数投票。\n\n"
            "Q: 如何选择邻居数 k？\n"
            "A: 可使用交叉验证，或尝试 sqrt(n) 作为初值。\n\n"
            "Q: 特点？\n"
            "A: 简单、无需训练过程，但对高维数据和噪声敏感。")

if __name__ == "__main__":
    root = tk.Tk()
    app = AIPlatformUI(root)
    root.mainloop()
