
import tkinter as tk
from tkinter import messagebox, font
import random
import time

GRID = 4
TILE_SIZE = 110
PAD = 8
WINDOW_W = GRID * TILE_SIZE + (GRID + 1) * PAD
WINDOW_H = WINDOW_W + 160

BG_COLOR      = "#1a1a2e"
BOARD_BG      = "#16213e"
TILE_COLOR    = "#0f3460"
TILE_HOVER    = "#e94560"
TILE_TEXT     = "#ffffff"
EMPTY_COLOR   = "#0d0d1a"
BTN_COLOR     = "#e94560"
BTN_TEXT      = "#ffffff"
HEADER_TEXT   = "#e94560"
INFO_TEXT     = "#a8b2d8"
WIN_COLOR     = "#4ade80"

class PuzzleModel:
    def __init__(self, size=4):
        self.size = size
        self.reset()

    def reset(self):
        self.board = list(range(1, self.size * self.size)) + [0]  
        self.moves = 0
        self.start_time = None
        self.finished = False
        self._shuffle()

    def _find_zero(self):
        return self.board.index(0)

    def _shuffle(self):
    
        for _ in range(1000):
            zero = self._find_zero()
            neighbors = self._get_neighbors(zero)
            swap = random.choice(neighbors)
            self.board[zero], self.board[swap] = self.board[swap], self.board[zero]
        
        while self.is_solved():
            self._shuffle()

    def _get_neighbors(self, pos):
        row, col = divmod(pos, self.size)
        neighbors = []
        if row > 0: neighbors.append(pos - self.size)
        if row < self.size - 1: neighbors.append(pos + self.size)
        if col > 0: neighbors.append(pos - 1)
        if col < self.size - 1: neighbors.append(pos + 1)
        return neighbors

    def can_move(self, tile_pos):
        zero = self._find_zero()
        return tile_pos in self._get_neighbors(zero)

    def move_tile(self, tile_pos):
       
        if not self.can_move(tile_pos):
            return False
        zero = self._find_zero()
        self.board[zero], self.board[tile_pos] = self.board[tile_pos], self.board[zero]
        self.moves += 1
        if self.start_time is None:
            self.start_time = time.time()
        if self.is_solved():
            self.finished = True
        return True

    def is_solved(self):
        return self.board == list(range(1, self.size * self.size)) + [0]

    def get_elapsed(self):
        if self.start_time is None:
            return 0
        return int(time.time() - self.start_time)

    def get_tile_at(self, row, col):
        return self.board[row * self.size + col]


class PuzzleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("15 Puzzle")
        self.resizable(False, False)
        self.configure(bg=BG_COLOR)
        self.model = PuzzleModel(GRID)
        self._build_ui()
        self._draw_board()
        self._tick()

    def _build_ui(self):
        bold_font  = font.Font(family="Segoe UI", size=14, weight="bold")
        title_font = font.Font(family="Segoe UI", size=22, weight="bold")
        info_font  = font.Font(family="Segoe UI", size=12)
        btn_font   = font.Font(family="Segoe UI", size=11, weight="bold")

        tk.Label(self, text="15 PUZZLE", font=title_font,
                 bg=BG_COLOR, fg=HEADER_TEXT).pack(pady=(18, 4))

        info_frame = tk.Frame(self, bg=BG_COLOR)
        info_frame.pack(fill="x", padx=24, pady=4)

        self.moves_var = tk.StringVar(value="Harakatlar: 0")
        self.time_var  = tk.StringVar(value="Vaqt: 0s")

        tk.Label(info_frame, textvariable=self.moves_var,
                 font=info_font, bg=BG_COLOR, fg=INFO_TEXT).pack(side="left")
        tk.Label(info_frame, textvariable=self.time_var,
                 font=info_font, bg=BG_COLOR, fg=INFO_TEXT).pack(side="right")

        board_size = GRID * TILE_SIZE + (GRID + 1) * PAD
        self.canvas = tk.Canvas(self, width=board_size, height=board_size,
                                bg=BOARD_BG, highlightthickness=0,
                                bd=0, relief="flat")
        self.canvas.pack(padx=24, pady=10)
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<Motion>",   self._on_hover)

        self._hover_pos = None

        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=12)

        tk.Button(btn_frame, text="🔄  Yangi O'yin", font=btn_font,
                  bg=BTN_COLOR, fg=BTN_TEXT, activebackground="#c73652",
                  activeforeground="white", relief="flat", padx=18, pady=8,
                  cursor="hand2", command=self._new_game).pack(side="left", padx=8)

        tk.Button(btn_frame, text="💡  Yechim", font=btn_font,
                  bg="#0f3460", fg=BTN_TEXT, activebackground="#1a5276",
                  activeforeground="white", relief="flat", padx=18, pady=8,
                  cursor="hand2", command=self._show_solution).pack(side="left", padx=8)

    def _draw_board(self):
        self.canvas.delete("all")
        self._tile_rects = {}

        for row in range(GRID):
            for col in range(GRID):
                val = self.model.get_tile_at(row, col)
                x1 = PAD + col * (TILE_SIZE + PAD)
                y1 = PAD + row * (TILE_SIZE + PAD)
                x2 = x1 + TILE_SIZE
                y2 = y1 + TILE_SIZE
                pos = row * GRID + col

                if val == 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2,
                                                 fill=EMPTY_COLOR, outline="",
                                                 tags=f"cell_{pos}")
                    continue
                
                color = TILE_HOVER if pos == self._hover_pos and self.model.can_move(pos) \
                        else TILE_COLOR

                r = self.canvas.create_rectangle(x1+4, y1+4, x2-4, y2-4,
                                                 fill=color, outline="",
                                                 tags=f"cell_{pos}")
               
                self.canvas.create_rectangle(x1+4, y1+4, x2-4, y2-4,
                                             fill="", outline="#2a4a7f",
                                             width=2, tags=f"cell_{pos}")

                
                cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                fsize = 28 if val < 10 else 22
                self.canvas.create_text(cx, cy, text=str(val),
                                        font=("Segoe UI", fsize, "bold"),
                                        fill=TILE_TEXT, tags=f"cell_{pos}")

                self._tile_rects[pos] = (x1, y1, x2, y2)

        self.moves_var.set(f"Harakatlar: {self.model.moves}")

    def _pos_from_xy(self, x, y):
        col = (x - PAD) // (TILE_SIZE + PAD)
        row = (y - PAD) // (TILE_SIZE + PAD)
        if 0 <= row < GRID and 0 <= col < GRID:
            return int(row) * GRID + int(col)
        return None

    def _on_click(self, event):
        if self.model.finished:
            return
        pos = self._pos_from_xy(event.x, event.y)
        if pos is None:
            return
        moved = self.model.move_tile(pos)
        if moved:
            self._draw_board()
            if self.model.finished:
                self._celebrate()

    def _on_hover(self, event):
        pos = self._pos_from_xy(event.x, event.y)
        if pos != self._hover_pos:
            self._hover_pos = pos
            self._draw_board()

    def _tick(self):
        """Har soniyada vaqt yangilanadi."""
        elapsed = self.model.get_elapsed()
        m, s = divmod(elapsed, 60)
        if m:
            self.time_var.set(f"Vaqt: {m}d {s:02d}s")
        else:
            self.time_var.set(f"Vaqt: {s}s")
        self.after(1000, self._tick)

    def _new_game(self):
        self._hover_pos = None
        self.model.reset()
        self._draw_board()

    def _celebrate(self):
        elapsed = self.model.get_elapsed()
        m, s = divmod(elapsed, 60)
        time_str = f"{m} daqiqa {s} soniya" if m else f"{s} soniya"
        msg = (f"🎉 Tabriklaymiz!\n\n"
               f"Taxtachani yig'dingiz!\n\n"
               f"⏱  Vaqt: {time_str}\n"
               f"🔢  Harakatlar: {self.model.moves}")
        messagebox.showinfo("G'ALABA!", msg)

    def _show_solution(self):
        messagebox.showinfo(
            "Maslahat 💡",
            "15-Puzzle yechim strategiyasi:\n\n"
            "1️⃣  Avval 1-qatorni (1,2,3,4) yig'ing\n"
            "2️⃣  Keyin 2-qatorni (5,6,7,8) yig'ing\n"
            "3️⃣  Qolgan 3x2 blokni aylantirish\n"
            "     usuli bilan yig'ing\n\n"
            "Bo'sh katakni doim maqsad plita\n"
            "yoniga olib keling, so'ng siljiting."
        )


if __name__ == "__main__":
    app = PuzzleApp()
    app.mainloop()
