# Лабораторная работа 8: Красно-черные деревья
import tkinter as tk
from tkinter import messagebox

RED, BLACK = True, False


class Node:
    def __init__(self, key, color=RED):
        self.key, self.color = key, color
        self.left = self.right = self.parent = None


class RedBlackTree:
    def __init__(self):
        self.NIL = Node(None, BLACK)
        self.root = self.NIL

    def _rot(self, x, left=True):
        y = x.right if left else x.left
        if left:
            x.right = y.left
            if y.left != self.NIL: y.left.parent = x
        else:
            x.left = y.right
            if y.right != self.NIL: y.right.parent = x

        y.parent = x.parent
        if not x.parent: self.root = y
        elif x == x.parent.left: x.parent.left = y
        else: x.parent.right = y

        if left: y.left, x.parent = x, y
        else: y.right, x.parent = x, y

    def insert(self, key):
        if self.find(key) != self.NIL: return False
        node = Node(key)
        node.left = node.right = self.NIL
        p, cur = None, self.root

        while cur != self.NIL:
            p = cur
            cur = cur.left if key < cur.key else cur.right

        node.parent = p
        if not p: self.root = node
        elif key < p.key: p.left = node
        else: p.right = node

        if not node.parent:
            node.color = BLACK
            return True

        self._fix_insert(node)
        return True

    def _fix_insert(self, k):
        while k.parent and k.parent.color == RED:
            p, g = k.parent, k.parent.parent
            is_right = (p == g.right)
            u = g.left if is_right else g.right

            if u.color == RED:
                u.color = p.color = BLACK
                g.color = RED
                k = g
            else:
                if k == (p.left if is_right else p.right):
                    k = p
                    self._rot(k, left=not is_right)
                k.parent.color = BLACK
                k.parent.parent.color = RED
                self._rot(k.parent.parent, left=is_right)
            if k == self.root: break
        self.root.color = BLACK

    def _transplant(self, u, v):
        if not u.parent: self.root = v
        elif u == u.parent.left: u.parent.left = v
        else: u.parent.right = v
        v.parent = u.parent

    def delete(self, key):
        z = self.find(key)
        if z == self.NIL: return False
        y, orig_color = z, z.color

        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = z.right
            while y.left != self.NIL: y = y.left
            orig_color = y.color
            x = y.right
            if y.parent == z: x.parent = y
            else:
                self._transplant(y, y.right)
                y.right, y.right.parent = z.right, y
            self._transplant(z, y)
            y.left, y.left.parent = z.left, y
            y.color = z.color

        if orig_color == BLACK:
            self._fix_delete(x)
        return True

    def _fix_delete(self, x):
        while x != self.root and x.color == BLACK:
            is_left = (x == x.parent.left)
            s = x.parent.right if is_left else x.parent.left

            if s.color == RED:
                s.color, x.parent.color = BLACK, RED
                self._rot(x.parent, left=is_left)
                s = x.parent.right if is_left else x.parent.left

            if s.left.color == BLACK and s.right.color == BLACK:
                s.color = RED
                x = x.parent
            else:
                far = s.right if is_left else s.left
                if far.color == BLACK:
                    near = s.left if is_left else s.right
                    near.color, s.color = BLACK, RED
                    self._rot(s, left=not is_left)
                    s = x.parent.right if is_left else x.parent.left
                s.color = x.parent.color
                x.parent.color = BLACK
                (s.right if is_left else s.left).color = BLACK
                self._rot(x.parent, left=is_left)
                x = self.root
        x.color = BLACK

    def find(self, key):
        cur = self.root
        while cur != self.NIL and key != cur.key:
            cur = cur.left if key < cur.key else cur.right
        return cur




class TreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Красно-черное дерево | Лабораторная 8")
        self.root.geometry("900x600")
        self.tree = RedBlackTree()

        # Панель управления
        panel = tk.Frame(root, bg="#f5f5f5", pady=8)
        panel.pack(fill=tk.X)

        tk.Label(panel, text="Числа:", font=("Arial", 10), bg="#f5f5f5").pack(side=tk.LEFT, padx=5)
        self.entry = tk.Entry(panel, font=("Arial", 10), width=24)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind("<Return>", lambda e: self.act_insert())

        tk.Button(panel, text="Добавить", bg="#4CAF50", fg="white", command=self.act_insert).pack(side=tk.LEFT, padx=3)
        tk.Button(panel, text="Удалить", bg="#f44336", fg="white", command=self.act_delete).pack(side=tk.LEFT, padx=3)
        tk.Button(panel, text="Очистить", bg="#757575", fg="white", command=self.act_clear).pack(side=tk.LEFT, padx=3)

        self.status = tk.Label(panel, text="Готово", font=("Arial", 9, "italic"), bg="#f5f5f5")
        self.status.pack(side=tk.RIGHT, padx=10)

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def parse_keys(self):
        txt = self.entry.get().strip()
        if not txt: return []
        try:
            return [int(x) for x in txt.split()]
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целые числа через пробел!")
            return None

    def act_insert(self):
        keys = self.parse_keys()
        if keys is None or not keys: return
        added = [k for k in keys if self.tree.insert(k)]
        self.status.config(text=f"Добавлено: {added}" if added else "Все узлы уже есть")
        self.entry.delete(0, tk.END)
        self.render()

    def act_delete(self):
        keys = self.parse_keys()
        if keys is None or not keys: return
        deleted = [k for k in keys if self.tree.delete(k)]
        self.status.config(text=f"Удалено: {deleted}" if deleted else "Узлы не найдены")
        self.entry.delete(0, tk.END)
        self.render()

    def act_clear(self):
        self.tree = RedBlackTree()
        self.status.config(text="Дерево очищено")
        self.render()

    def render(self):
        self.canvas.delete("all")
        if self.tree.root == self.tree.NIL: return
        w = self.canvas.winfo_width() or 900
        self._draw(self.tree.root, w // 2, 40, w // 4)

    def _draw(self, node, x, y, dx):
        r, dy = 16, 55
        for child, nx in ((node.left, x - dx), (node.right, x + dx)):
            if child != self.tree.NIL:
                self.canvas.create_line(x, y, nx, y + dy, width=2, fill="#999")
                self._draw(child, nx, y + dy, max(dx // 2, 20))

        color = "#e53935" if node.color == RED else "#263238"
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="white", width=2)
        self.canvas.create_text(x, y, text=str(node.key), fill="white", font=("Arial", 10, "bold"))


if __name__ == "__main__":
    tk_root = tk.Tk()
    app = TreeApp(tk_root)
    tk_root.mainloop()