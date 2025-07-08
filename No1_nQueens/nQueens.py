import tkinter as tk
from tkinter import ttk, messagebox


class NQueensSolver:
    def __init__(self, n):
        self.n = n
        self.solutions = []
        self.unique_solutions = []
        self.board = [-1] * n

    def solve(self):
        self._backtrack(0)
        self._find_unique_solutions()
        return self.solutions, self.unique_solutions

    def _backtrack(self, row):
        if row == self.n:
            self.solutions.append(self.board.copy())
            return

        for col in range(self.n):
            if self._is_safe(row, col):
                self.board[row] = col
                self._backtrack(row + 1)

    def _is_safe(self, row, col):
        for r in range(row):
            if (self.board[r] == col or
                self.board[r] - r == col - row or
                self.board[r] + r == col + row):
                return False
        return True

    def _find_unique_solutions(self):
        unique_boards = set()

        for solution in self.solutions:
            variants = self._generate_variants(solution)
            variant_tuples = {tuple(v) for v in variants}

            if not any(v in unique_boards for v in variant_tuples):
                unique_boards.update(variant_tuples)
                self.unique_solutions.append(solution)

    def _generate_variants(self, board):
        variants = [board]

        current = board
        for _ in range(3):
            current = self._rotate_90(current)
            variants.append(current)

        variants.append(self._reflect_horizontal(board))
        variants.append(self._reflect_vertical(board))
        variants.append(self._reflect_diagonal(board))
        variants.append(self._reflect_anti_diagonal(board))

        unique_variants = []
        for v in variants:
            if v not in unique_variants:
                unique_variants.append(v)

        return unique_variants

    def _rotate_90(self, board):
        new_board = [-1] * self.n
        for row in range(self.n):
            new_board[board[row]] = self.n - 1 - row
        return new_board

    def _reflect_horizontal(self, board):
        return [self.n - 1 - col for col in board]

    def _reflect_vertical(self, board):
        return board[::-1]

    def _reflect_diagonal(self, board):
        new_board = [-1] * self.n
        for row, col in enumerate(board):
            new_board[col] = row
        return new_board

    def _reflect_anti_diagonal(self, board):
        return self._reflect_diagonal(self._reflect_horizontal(board))


class NQueensGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("N 皇后问题-黄斌-2024120483")
        self.root.geometry("800x600")

        self.font_family = "SimHei"

        self.current_solution_index = 0
        self.current_solutions = []

        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.input_frame = ttk.LabelFrame(self.main_frame, text="输入参数", padding="10")
        self.input_frame.pack(fill=tk.X, pady=5)

        ttk.Label(self.input_frame, text="棋盘大小 (N ≥ 4):", font=(self.font_family, 10)).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.n_var = tk.IntVar(value=8)
        self.n_entry = ttk.Entry(self.input_frame, textvariable=self.n_var, width=5, font=(self.font_family, 10))
        self.n_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.solve_button = ttk.Button(self.input_frame, text="求解", command=self.solve_n_queens, width=10)
        self.solve_button.grid(row=0, column=2, padx=5, pady=5)

        self.solution_type = tk.StringVar(value="all")
        style = ttk.Style()
        style.configure("TRadiobutton", font=(self.font_family, 10))
        ttk.Radiobutton(self.input_frame, text="所有解法", variable=self.solution_type, value="all", style="TRadiobutton").grid(row=0, column=3, padx=5, pady=5)
        ttk.Radiobutton(self.input_frame, text="独立解法", variable=self.solution_type, value="unique", style="TRadiobutton").grid(row=0, column=4, padx=5, pady=5)

        self.info_frame = ttk.LabelFrame(self.main_frame, text="结果信息", padding="10")
        self.info_frame.pack(fill=tk.X, pady=5)

        self.total_label = ttk.Label(self.info_frame, text="总解法数: 0", font=(self.font_family, 10))
        self.total_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.current_label = ttk.Label(self.info_frame, text="当前解法: 0/0", font=(self.font_family, 10))
        self.current_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.board_frame = ttk.LabelFrame(self.main_frame, text="棋盘", padding="10")
        self.board_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.canvas = tk.Canvas(self.board_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.nav_frame = ttk.Frame(self.main_frame, padding="10")
        self.nav_frame.pack(fill=tk.X, pady=5)

        self.prev_button = ttk.Button(self.nav_frame, text="上一个", command=self.prev_solution, width=10, state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(self.nav_frame, text="下一个", command=self.next_solution, width=10, state=tk.DISABLED)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.status_bar = ttk.Label(root, text="准备就绪", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.root.bind("<Configure>", self.resize_board)

    def solve_n_queens(self):
        try:
            n = self.n_var.get()
            if n < 4:
                messagebox.showerror("错误", "N 必须至少为 4")
                return

            self.status_bar.config(text=f"正在求解 {n}x{n} 皇后问题...")
            self.root.update()

            solver = NQueensSolver(n)
            all_solutions, unique_solutions = solver.solve()

            if self.solution_type.get() == "all":
                self.current_solutions = all_solutions
                total_text = f"总解法数: {len(all_solutions)}"
            else:
                self.current_solutions = unique_solutions
                total_text = f"独立解法数: {len(unique_solutions)}"

            self.total_label.config(text=total_text)

            if len(self.current_solutions) > 0:
                self.current_solution_index = 0
                self.current_label.config(text=f"当前解法: {self.current_solution_index + 1}/{len(self.current_solutions)}")
                self.prev_button.config(state=tk.DISABLED if len(self.current_solutions) == 1 else tk.NORMAL)
                self.next_button.config(state=tk.DISABLED if len(self.current_solutions) == 1 else tk.NORMAL)
                self.draw_board()
                self.status_bar.config(text=f"求解完成，共找到 {len(self.current_solutions)} 种解法")
            else:
                self.canvas.delete("all")
                self.status_bar.config(text="未找到解法")
        except Exception as e:
            messagebox.showerror("错误", f"求解过程中出错: {str(e)}")
            self.status_bar.config(text="求解失败")

    def draw_board(self):
        self.canvas.delete("all")

        if not self.current_solutions:
            return

        solution = self.current_solutions[self.current_solution_index]
        n = len(solution)

        canvas_width = self.canvas.winfo_width() - 20
        canvas_height = self.canvas.winfo_height() - 20

        cell_size = min(canvas_width // n, canvas_height // n)

        x_offset = (self.canvas.winfo_width() - cell_size * n) // 2
        y_offset = (self.canvas.winfo_height() - cell_size * n) // 2

        for row in range(n):
            for col in range(n):
                x1 = x_offset + col * cell_size
                y1 = y_offset + row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                color = "#FFFFFF" if (row + col) % 2 == 0 else "#C0C0C0"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

                if solution[row] == col:
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    radius = cell_size // 2 - 5

                    self.canvas.create_oval(
                        center_x - radius, center_y - radius,
                        center_x + radius, center_y + radius,
                        fill="red", outline="black", width=2
                    )

        for i in range(n):
            self.canvas.create_text(
                x_offset + i * cell_size + cell_size // 2,
                y_offset - 15,
                text=str(i),
                font=(self.font_family, 10, "bold")
            )

            self.canvas.create_text(
                x_offset - 15,
                y_offset + i * cell_size + cell_size // 2,
                text=str(i),
                font=(self.font_family, 10, "bold")
            )

    def prev_solution(self):
        if self.current_solution_index > 0:
            self.current_solution_index -= 1
            self.current_label.config(text=f"当前解法: {self.current_solution_index + 1}/{len(self.current_solutions)}")
            self.next_button.config(state=tk.NORMAL)
            if self.current_solution_index == 0:
                self.prev_button.config(state=tk.DISABLED)
            self.draw_board()

    def next_solution(self):
        if self.current_solution_index < len(self.current_solutions) - 1:
            self.current_solution_index += 1
            self.current_label.config(text=f"当前解法: {self.current_solution_index + 1}/{len(self.current_solutions)}")
            self.prev_button.config(state=tk.NORMAL)
            if self.current_solution_index == len(self.current_solutions) - 1:
                self.next_button.config(state=tk.DISABLED)
            self.draw_board()

    def resize_board(self, event=None):
        if self.current_solutions:
            self.draw_board()


def main():
    root = tk.Tk()
    app = NQueensGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()