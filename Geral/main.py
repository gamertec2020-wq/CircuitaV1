import json
import math
import re
import textwrap
import tkinter as tk
import webbrowser
from copy import deepcopy
from tkinter import filedialog, messagebox, ttk

from lessons import BREADBOARD_INTRO, LESSONS, SAFETY_INTRO


APP_TITLE = "Circuita - Laboratorio de Circuitos"
CREDITS_URL = "https://www.instagram.com/Hikaru_Labs/"

COMPONENTS = {
    "battery": {"label": "Pilha / conjunto", "pins": ["+", "-"], "size": (120, 58), "color": "#e6a23c"},
    "resistor": {"label": "Resistor", "pins": ["A", "B"], "size": (110, 58), "color": "#d6b566"},
    "capacitor": {"label": "Capacitor", "pins": ["A", "B"], "size": (110, 58), "color": "#75a7d8"},
    "led": {"label": "LED", "pins": ["A", "K"], "size": (100, 58), "color": "#f16b65"},
    "diode": {"label": "Diodo", "pins": ["A", "K"], "size": (100, 58), "color": "#88c6ff"},
    "button": {"label": "Botao", "pins": ["A", "B"], "size": (100, 58), "color": "#a78bda"},
    "display": {"label": "Tela LCD", "pins": ["VCC", "GND", "SDA", "SCL"], "size": (200, 120), "color": "#65b98b"},
    "arduino": {
        "label": "Arduino Uno",
        "pins": ["VCC", "GND", "D13", "A0", "A4", "A5"],
        "size": (166, 104),
        "color": "#4eae9b",
    },
    "potentiometer": {"label": "Potenciometro", "pins": ["A", "W", "B"], "size": (124, 64), "color": "#e0a65c"},
    "buzzer": {"label": "Buzzer", "pins": ["+", "-"], "size": (104, 64), "color": "#d982b5"},
    "motor": {"label": "Motor DC", "pins": ["+", "-"], "size": (104, 64), "color": "#78aee0"},
    "lamp": {"label": "Lampada", "pins": ["A", "B"], "size": (104, 64), "color": "#e8d06e"},
}

DEFAULTS = {
    "battery": {"voltage": 4.5, "format": "AA", "cells": 3},
    "resistor": {"resistance": 220.0},
    "capacitor": {"capacitance": 100.0},
    "led": {"forward_voltage": 2.0, "resistance": 20.0},
    "diode": {"forward_voltage": 0.7, "resistance": 10.0},
    "button": {"closed": False},
    "display": {"text": "Aguardando script"},
    "arduino": {"pin13": 5.0},
    "potentiometer": {"resistance": 10000.0, "wiper": 50.0},
    "buzzer": {"resistance": 32.0},
    "motor": {"resistance": 100.0},
    "lamp": {"resistance": 100.0},
}

BG = "#11171d"
PANEL = "#192129"
PANEL_LIGHT = "#202a34"
TEXT = "#e6edf3"
MUTED = "#90a0ad"
ACCENT = "#50d9b0"
WIRE = "#65b9ff"
CANVAS_BG = "#0d141a"
COMPONENT_BG = "#1a2731"


def terminal_id(component, pin):
    return f"{component}:{pin}"


def parse_number(value, label):
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{label}: informe um numero valido.")
    if not math.isfinite(number):
        raise ValueError(f"{label}: o valor precisa ser finito.")
    return number


def solve_linear(matrix, vector):
    size = len(vector)
    augmented = [row[:] + [vector[index]] for index, row in enumerate(matrix)]
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1e-14:
            raise ValueError("Circuito sem uma solucao numerica estavel.")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        for item in range(column, size + 1):
            augmented[column][item] /= divisor
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor:
                for item in range(column, size + 1):
                    augmented[row][item] -= factor * augmented[column][item]
    return [augmented[index][size] for index in range(size)]


class UnionFind:
    def __init__(self, items):
        self.parent = {item: item for item in items}

    def find(self, item):
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, first, second):
        first_root = self.find(first)
        second_root = self.find(second)
        if first_root != second_root:
            self.parent[second_root] = first_root


class CircuitaApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_TITLE} | por @Hikaru_Labs")
        self.root.geometry("1320x820")
        self.root.minsize(1000, 650)
        self.root.configure(bg=BG)
        self.components = []
        self.wires = []
        self.next_id = 1
        self.selected_id = None
        self.pending_terminal = None
        self.drag_state = None
        self.simulation_running = False
        self.last_voltages = {}
        self.last_currents = {}
        self.manual_window = None
        self._build_ui()
        self._draw_canvas()

    def _build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", background=PANEL_LIGHT, foreground=TEXT, padding=(9, 6), borderwidth=0)
        style.map("TButton", background=[("active", "#2c3a47")])
        style.configure("TLabel", background=PANEL, foreground=TEXT)
        style.configure("TEntry", fieldbackground="#10161c", foreground=TEXT, insertcolor=TEXT)
        style.configure(
            "TScrollbar",
            background="#2b3944",
            troughcolor="#10161c",
            bordercolor=PANEL,
            arrowcolor=MUTED,
        )
        style.configure(
            "TCombobox",
            fieldbackground="#10161c",
            background=PANEL_LIGHT,
            foreground=TEXT,
            arrowcolor=ACCENT,
        )
        style.map("TCombobox", fieldbackground=[("readonly", "#10161c")],
                  foreground=[("readonly", TEXT)])
        self.root.option_add("*TCombobox*Listbox.background", PANEL_LIGHT)
        self.root.option_add("*TCombobox*Listbox.foreground", TEXT)
        self.root.option_add("*TCombobox*Listbox.selectBackground", "#2c6e5a")
        self.root.option_add("*TCombobox*Listbox.selectForeground", TEXT)

        toolbar = tk.Frame(self.root, bg="#151d25", height=58)
        toolbar.pack(side="top", fill="x")
        toolbar.pack_propagate(False)
        logo = tk.Canvas(toolbar, width=32, height=32, bg="#151d25", highlightthickness=0)
        logo.pack(side="left", padx=(16, 8))
        logo.create_rectangle(2, 2, 30, 30, fill="#1d332f", outline="#347e68", width=1)
        logo.create_line(8, 16, 14, 16, 14, 9, 22, 9, fill=ACCENT, width=2)
        logo.create_line(14, 16, 14, 23, 23, 23, fill=ACCENT, width=2)
        logo.create_oval(5, 13, 11, 19, fill=ACCENT, outline="")
        logo.create_oval(20, 6, 26, 12, fill="#70c8ff", outline="")
        logo.create_oval(20, 20, 26, 26, fill="#70c8ff", outline="")
        tk.Label(toolbar, text="CIRCUITA", bg="#151d25", fg=ACCENT,
                 font=("Segoe UI", 14, "bold")).pack(side="left", padx=(0, 18))
        self._tool_button(toolbar, "▶  Simular", self.start_simulation, accent=True)
        self._tool_button(toolbar, "■  Parar", self.stop_simulation)
        self._tool_button(toolbar, "＋ Exemplo Arduino", self.load_example)
        self._tool_button(toolbar, "📖 Manual", self.open_manual)
        self._tool_button(toolbar, "Salvar", self.save_project)
        self._tool_button(toolbar, "Abrir", self.open_project)
        self._tool_button(toolbar, "Limpar", self.clear_project)
        self.status_var = tk.StringVar(value="Pronto para montar")
        status = tk.Frame(toolbar, bg="#202a34")
        status.pack(side="right", padx=13, pady=13)
        self.status_dot = tk.Canvas(status, width=12, height=12, bg="#202a34", highlightthickness=0)
        self.status_dot.pack(side="left", padx=(8, 2))
        self.status_dot.create_oval(2, 2, 10, 10, fill="#738291", outline="")
        tk.Label(status, textvariable=self.status_var, bg="#202a34", fg="#c4d0da",
                 font=("Segoe UI", 8)).pack(side="left", padx=(1, 9), pady=5)

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=10, pady=(10, 0))

        toolbox = tk.Frame(body, bg=PANEL, width=184)
        toolbox.pack(side="left", fill="y", padx=(0, 10))
        toolbox.pack_propagate(False)
        self.toolbox_frame = toolbox
        toolbox_canvas = tk.Canvas(toolbox, bg=PANEL, highlightthickness=0, width=184)
        self.toolbox_canvas = toolbox_canvas
        toolbox_scrollbar = ttk.Scrollbar(toolbox, orient="vertical", command=toolbox_canvas.yview)
        toolbox_canvas.configure(yscrollcommand=toolbox_scrollbar.set)
        toolbox_scrollbar.pack(side="right", fill="y")
        toolbox_canvas.pack(side="left", fill="both", expand=True)
        toolbox_content = tk.Frame(toolbox_canvas, bg=PANEL)
        toolbox_window = toolbox_canvas.create_window((0, 0), window=toolbox_content, anchor="nw")
        toolbox_content.bind(
            "<Configure>",
            lambda _event: toolbox_canvas.configure(scrollregion=toolbox_canvas.bbox("all")),
        )
        toolbox_canvas.bind(
            "<Configure>",
            lambda event: toolbox_canvas.itemconfigure(toolbox_window, width=event.width),
        )
        self.root.bind_all("<MouseWheel>", self._scroll_toolbox, add="+")
        self.root.bind_all("<Button-4>", self._scroll_toolbox, add="+")
        self.root.bind_all("<Button-5>", self._scroll_toolbox, add="+")
        toolbox = toolbox_content
        self._section_label(toolbox, "BIBLIOTECA")
        tk.Label(toolbox, text="Clique para adicionar ao quadro", bg=PANEL, fg=MUTED, wraplength=155,
                 justify="left", font=("Segoe UI", 9)).pack(anchor="w", padx=13, pady=(0, 12))
        for kind, definition in COMPONENTS.items():
            button = tk.Button(
                toolbox,
                text=f"+  {definition['label']}",
                command=lambda component_type=kind: self.add_component(component_type),
                bg=PANEL_LIGHT,
                fg=TEXT,
                activebackground="#2c3a47",
                activeforeground=TEXT,
                relief="flat",
                anchor="w",
                padx=12,
                pady=9,
                font=("Segoe UI", 9),
                cursor="hand2",
            )
            button.pack(fill="x", padx=9, pady=3)
        self._section_label(toolbox, "CONEXOES")
        tk.Label(
            toolbox,
            text="Clique em um terminal e depois em outro para criar um fio. Clique em um botao para alternar seu estado.",
            bg=PANEL,
            fg=MUTED,
            wraplength=156,
            justify="left",
            font=("Segoe UI", 9),
        ).pack(anchor="w", padx=13, pady=(0, 10))

        work = tk.Frame(body, bg=BG)
        work.pack(side="left", fill="both", expand=True)
        self.canvas = tk.Canvas(work, bg=CANVAS_BG, highlightthickness=1, highlightbackground="#34424e")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self._canvas_click)
        self.canvas.bind("<B1-Motion>", self._canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self._canvas_release)
        self.canvas.bind("<Configure>", lambda _event: self._draw_canvas())
        self.root.bind("<Delete>", lambda _event: self.delete_selected())

        inspector = tk.Frame(body, bg=PANEL, width=270)
        inspector.pack(side="right", fill="y", padx=(10, 0))
        inspector.pack_propagate(False)
        self._section_label(inspector, "PROPRIEDADES")
        self.inspector_body = tk.Frame(inspector, bg=PANEL)
        self.inspector_body.pack(fill="x", padx=12)
        self._show_empty_inspector()
        tk.Frame(inspector, bg="#2b3742", height=1).pack(fill="x", padx=12, pady=14)
        self._section_label(inspector, "TESTE RAPIDO")
        tk.Label(
            inspector,
            text='Comandos suportados:\nDISPLAY texto\nDIGITAL_WRITE 13 HIGH|LOW\nREAD A0\nWAIT ms',
            bg=PANEL,
            fg=MUTED,
            justify="left",
            font=("Consolas", 8),
        ).pack(anchor="w", padx=13, pady=(0, 7))
        self.script = tk.Text(
            inspector,
            height=8,
            bg="#10161c",
            fg="#c8e6d4",
            insertbackground=TEXT,
            relief="flat",
            font=("Consolas", 9),
            padx=8,
            pady=8,
            wrap="word",
        )
        self.script.pack(fill="x", padx=10)
        self.script.insert("1.0", "DIGITAL_WRITE 13 HIGH\nDISPLAY Oi, circuito!\nREAD A0")
        self._tool_button(inspector, "Executar teste", self.run_script, fill=True)
        tk.Label(
            inspector,
            text="Simulacao eletrica DC didatica. Nao conecte componentes reais com base apenas neste resultado.",
            bg=PANEL,
            fg="#d9a35c",
            wraplength=235,
            justify="left",
            font=("Segoe UI", 8),
        ).pack(anchor="w", padx=13, pady=(12, 8))

        self.output = tk.Text(
            self.root,
            height=5,
            bg="#0b1015",
            fg="#c0ccd6",
            insertbackground=TEXT,
            relief="flat",
            font=("Cascadia Mono", 9),
            padx=10,
            pady=7,
            state="disabled",
        )
        self.output.pack(fill="x", padx=10, pady=10)
        credits = tk.Label(
            self.root,
            text="Desenvolvido por @Hikaru_Labs  ·  Instagram",
            bg=BG,
            fg="#83d9bd",
            cursor="hand2",
            font=("Segoe UI", 9, "underline"),
            padx=12,
            pady=3,
        )
        credits.pack(side="bottom", anchor="e", padx=10, pady=(0, 5))
        credits.bind("<Button-1>", lambda _event: webbrowser.open(CREDITS_URL))
        credits.bind("<Enter>", lambda _event: credits.configure(fg="#b4f1dc"))
        credits.bind("<Leave>", lambda _event: credits.configure(fg="#83d9bd"))
        self._log("Bem-vindo! Adicione componentes ou carregue o exemplo Arduino.")

    def _tool_button(self, parent, label, command, accent=False, fill=False):
        button = tk.Button(
            parent,
            text=label,
            command=command,
            bg=ACCENT if accent else PANEL_LIGHT,
            fg="#10161c" if accent else TEXT,
            activebackground="#70dbb9" if accent else "#2c3a47",
            activeforeground="#10161c" if accent else TEXT,
            relief="flat",
            padx=11,
            pady=6,
            font=("Segoe UI", 9, "bold" if accent else "normal"),
            cursor="hand2",
        )
        button.pack(side="top" if fill else "left",
                    fill="x" if fill else None, padx=4, pady=7)
        return button

    def _section_label(self, parent, text):
        tk.Label(parent, text=text, bg=PANEL, fg=ACCENT, font=("Segoe UI", 9, "bold")).pack(
            anchor="w", padx=13, pady=(14, 8)
        )

    def _show_empty_inspector(self):
        for child in self.inspector_body.winfo_children():
            child.destroy()
        tk.Label(
            self.inspector_body,
            text="Selecione um componente para editar seus valores.",
            bg=PANEL,
            fg=MUTED,
            wraplength=220,
            justify="left",
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=6)

    def _selected_component(self):
        return next((item for item in self.components if item["id"] == self.selected_id), None)

    def _show_properties(self):
        for child in self.inspector_body.winfo_children():
            child.destroy()
        component = self._selected_component()
        if component is None:
            self._show_empty_inspector()
            return
        tk.Label(
            self.inspector_body,
            text=f"{COMPONENTS[component['type']]['label']}  #{component['id']}",
            bg=PANEL,
            fg=TEXT,
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", pady=(2, 10))
        if component["type"] in ("battery", "resistor", "led", "diode", "button", "buzzer", "motor", "lamp"):
            current = self.last_currents.get(component["id"])
            pins = COMPONENTS[component["type"]]["pins"][:2]
            first = self.last_voltages.get(terminal_id(component["id"], pins[0]))
            second = self.last_voltages.get(terminal_id(component["id"], pins[1]))
            if current is not None and first is not None and second is not None:
                tk.Label(
                    self.inspector_body,
                    text=f"Simulacao: {abs(current) * 1000:.2f} mA | {abs(first - second):.2f} V",
                    bg=PANEL,
                    fg=ACCENT,
                    font=("Segoe UI", 9, "bold"),
                ).pack(anchor="w", pady=(0, 8))
        elif component["type"] == "capacitor" and self.last_voltages:
            tk.Label(
                self.inspector_body,
                text="Corrente DC: 0 mA (modelo em regime permanente)",
                bg=PANEL,
                fg=MUTED,
                wraplength=220,
                justify="left",
                font=("Segoe UI", 8),
            ).pack(anchor="w", pady=(0, 8))
        entries = {}
        field_labels = {
            "resistance": "Resistencia (ohms)",
            "capacitance": "Capacitancia (uF)",
            "forward_voltage": "Queda do LED (V)",
            "wiper": "Posicao do cursor (%)",
        }
        if component["type"] == "battery":
            tk.Label(
                self.inspector_body,
                text="Formato de cada pilha alcalina",
                bg=PANEL,
                fg=MUTED,
                font=("Segoe UI", 8),
            ).pack(anchor="w")
            battery_format = ttk.Combobox(
                self.inspector_body,
                values=("A", "AA", "AAA"),
                state="readonly",
            )
            battery_format.set(component.get("format", "AA"))
            battery_format.pack(fill="x", pady=(2, 8))
            entries["format"] = battery_format
            field_labels["cells"] = "Quantidade em serie (1-24)"
            tk.Label(
                self.inspector_body,
                text=f"Tensao nominal do conjunto: {component.get('voltage', 1.5):g} V",
                bg=PANEL,
                fg=ACCENT,
                font=("Segoe UI", 9, "bold"),
            ).pack(anchor="w", pady=(0, 8))
        else:
            field_labels["voltage"] = "Tensao (V)"
        if component["type"] == "diode":
            field_labels["forward_voltage"] = "Queda direta (V)"
        keys = [
            key for key in field_labels
            if key in component and key != "wiper" and key not in entries
        ]
        if "wiper" in component:
            keys.append("wiper")
        for key in keys:
            tk.Label(self.inspector_body, text=field_labels[key], bg=PANEL, fg=MUTED, font=("Segoe UI", 8)).pack(
                anchor="w"
            )
            entry = ttk.Entry(self.inspector_body)
            entry.insert(0, str(component[key]))
            entry.pack(fill="x", pady=(2, 8))
            entries[key] = entry
        if component["type"] == "battery":
            tk.Label(
                self.inspector_body,
                text="Este desenho representa uma pilha ou conjunto de pilhas em serie. Pilhas alcalinas: cerca de 1,5 V cada; NiMH recarregaveis: geralmente 1,2 V cada. Confira a embalagem.",
                bg=PANEL,
                fg=MUTED,
                wraplength=225,
                justify="left",
                font=("Segoe UI", 8),
            ).pack(anchor="w", pady=(0, 8))

        if component["type"] == "button":
            state = "Fechado (passa corrente)" if component.get("closed") else "Aberto"
            tk.Label(self.inspector_body, text=f"Estado: {state}", bg=PANEL, fg=MUTED).pack(anchor="w", pady=5)
            self._tool_button(
                self.inspector_body,
                "Alternar botao",
                lambda: self.toggle_button(component["id"]),
                fill=True,
            )
        elif component["type"] == "display":
            tk.Label(self.inspector_body, text="Texto atual:", bg=PANEL, fg=MUTED).pack(anchor="w")
            tk.Label(
                self.inspector_body,
                text=component.get("text", ""),
                bg="#10161c",
                fg="#9fe7bb",
                wraplength=210,
                justify="left",
                padx=7,
                pady=7,
            ).pack(fill="x", pady=4)
        elif component["type"] == "arduino":
            tk.Label(
                self.inspector_body,
                text=f"Pino D13: {component.get('pin13', 0):.1f} V",
                bg=PANEL,
                fg=MUTED,
            ).pack(anchor="w", pady=5)

        if entries:
            self._tool_button(
                self.inspector_body,
                "Aplicar valores",
                lambda: self.apply_properties(component, entries),
                fill=True,
            )
        self._tool_button(
            self.inspector_body,
            "Excluir componente",
            self.delete_selected,
            fill=True,
        )

    def add_component(self, kind, x=None, y=None, **values):
        component_id = self.next_id
        self.next_id += 1
        component = {
            "id": component_id,
            "type": kind,
            "x": x if x is not None else 120 + (component_id % 4) * 36,
            "y": y if y is not None else 100 + (component_id % 5) * 34,
        }
        component.update(DEFAULTS[kind])
        component.update(values)
        self.components.append(component)
        self.selected_id = component_id
        self._show_properties()
        self._draw_canvas()
        self.status_var.set(f"{COMPONENTS[kind]['label']} adicionado.")

    def apply_properties(self, component, entries):
        try:
            updated_values = {}
            for key, entry in entries.items():
                if key == "format":
                    value = entry.get()
                    if value not in ("A", "AA", "AAA"):
                        raise ValueError("Selecione o formato A, AA ou AAA.")
                    updated_values[key] = value
                    continue
                value = parse_number(entry.get(), key)
                if key == "cells":
                    if value != int(value) or not 1 <= value <= 24:
                        raise ValueError("A quantidade de pilhas precisa ser um numero inteiro entre 1 e 24.")
                    updated_values[key] = int(value)
                    continue
                if key in ("resistance", "capacitance") and value <= 0:
                    raise ValueError(f"{key}: o valor precisa ser maior que zero.")
                if key == "wiper" and not 0 <= value <= 100:
                    raise ValueError("A posicao do cursor precisa ficar entre 0 e 100%.")
                if key == "voltage" and value < 0:
                    raise ValueError("A tensao do conjunto de pilhas nao pode ser negativa.")
                if key == "forward_voltage" and value <= 0:
                    raise ValueError("A queda de tensao do LED precisa ser maior que zero.")
                updated_values[key] = value
        except ValueError as error:
            messagebox.showerror("Valor invalido", str(error), parent=self.root)
            return
        component.update(updated_values)
        if component["type"] == "battery" and "cells" in updated_values:
            component["voltage"] = updated_values["cells"] * 1.5
        self._draw_canvas()
        self.status_var.set("Propriedades atualizadas.")
        self._show_properties()
        if self.simulation_running:
            self.simulate()

    def _scroll_toolbox(self, event):
        pointer_x, pointer_y = self.root.winfo_pointerxy()
        left = self.toolbox_frame.winfo_rootx()
        top = self.toolbox_frame.winfo_rooty()
        right = left + self.toolbox_frame.winfo_width()
        bottom = top + self.toolbox_frame.winfo_height()
        if not (left <= pointer_x < right and top <= pointer_y < bottom):
            return None
        if getattr(event, "num", None) == 4:
            units = -1
        elif getattr(event, "num", None) == 5:
            units = 1
        else:
            delta = getattr(event, "delta", 0)
            units = int(-delta / 120)
            if units == 0 and delta:
                units = -1 if delta > 0 else 1
        if units:
            self.toolbox_canvas.yview_scroll(units, "units")
        return "break"

    def _terminal_positions(self, component):
        x, y = component["x"], component["y"]
        width, height = COMPONENTS[component["type"]]["size"]
        pins = COMPONENTS[component["type"]]["pins"]
        if len(pins) == 2:
            return {pins[0]: (x - width / 2, y), pins[1]: (x + width / 2, y)}
        if component["type"] == "arduino":
            return {
                "VCC": (x - width / 2, y - height / 2),
                "GND": (x - width / 2, y + height / 2),
                "D13": (x + width / 2, y - height / 2),
                "A0": (x + width / 2, y + height / 2),
                "A4": (x - width / 2, y),
                "A5": (x + width / 2, y),
            }
        if component["type"] == "display":
            return {
                "VCC": (x - width / 2, y - height / 2),
                "GND": (x - width / 2, y + height / 2),
                "SDA": (x + width / 2, y - height / 2),
                "SCL": (x + width / 2, y + height / 2),
            }
        if component["type"] == "potentiometer":
            return {
                "A": (x - width / 2, y - height / 2),
                "W": (x + width / 2, y),
                "B": (x - width / 2, y + height / 2),
            }
        return {
            "VCC": (x - width / 2, y - height / 2),
            "GND": (x - width / 2, y + height / 2),
            "D13": (x + width / 2, y - height / 2),
            "A0": (x + width / 2, y + height / 2),
        }

    def _draw_canvas(self):
        if not hasattr(self, "canvas"):
            return
        self.canvas.delete("all")
        width = max(self.canvas.winfo_width(), 400)
        height = max(self.canvas.winfo_height(), 300)
        for x in range(10, width, 24):
            for y in range(10, height, 24):
                self.canvas.create_oval(x, y, x + 1, y + 1, fill="#26323c", outline="")

        if not self.components:
            center_x, center_y = width / 2, height / 2
            self.canvas.create_oval(
                center_x - 32, center_y - 94, center_x + 32, center_y - 30,
                fill="#17251f", outline="#2f755d", width=2,
            )
            self.canvas.create_line(
                center_x - 17, center_y - 62, center_x - 2, center_y - 62,
                center_x - 2, center_y - 78, center_x + 15, center_y - 78,
                fill=ACCENT, width=3,
            )
            self.canvas.create_line(
                center_x - 2, center_y - 62, center_x - 2, center_y - 46,
                center_x + 15, center_y - 46, fill=ACCENT, width=3,
            )
            self.canvas.create_oval(center_x - 22, center_y - 68, center_x - 12, center_y - 58,
                                    fill=ACCENT, outline="")
            self.canvas.create_oval(center_x + 10, center_y - 83, center_x + 20, center_y - 73,
                                    fill="#70c8ff", outline="")
            self.canvas.create_oval(center_x + 10, center_y - 51, center_x + 20, center_y - 41,
                                    fill="#70c8ff", outline="")
            self.canvas.create_text(
                center_x, center_y - 8, text="SEU LABORATORIO, SEU CIRCUITO",
                fill="#d5e3ec", font=("Segoe UI", 14, "bold"),
            )
            self.canvas.create_text(
                center_x, center_y + 23,
                text="Escolha um componente na biblioteca ou carregue um projeto guiado pelo Manual.",
                fill=MUTED, font=("Segoe UI", 9), width=max(280, width - 48),
            )
            self.canvas.create_text(
                center_x, center_y + 58,
                text="Clique nos terminais para conectar  ·  Arraste os componentes para organizar",
                fill="#6f8190", font=("Segoe UI", 8), width=max(260, width - 48),
            )

        positions = {}
        for component in self.components:
            for pin, point in self._terminal_positions(component).items():
                positions[terminal_id(component["id"], pin)] = point
        for first, second in self.wires:
            if first in positions and second in positions:
                self.canvas.create_line(*positions[first], *positions[second],
                                        fill="#071019", width=8, capstyle="round")
                self.canvas.create_line(*positions[first], *positions[second],
                                        fill=WIRE, width=3, capstyle="round")

        for component in self.components:
            self._draw_component(component)
        if self.pending_terminal and self.pending_terminal in positions:
            x, y = positions[self.pending_terminal]
            self.canvas.create_oval(x - 9, y - 9, x + 9, y + 9, outline=ACCENT, width=2)

    def _draw_component(self, component):
        kind = component["type"]
        definition = COMPONENTS[kind]
        x, y = component["x"], component["y"]
        width, height = definition["size"]
        left, top = x - width / 2, y - height / 2
        selected = component["id"] == self.selected_id
        border = ACCENT if selected else "#354552"
        fill = COMPONENT_BG
        self.canvas.create_rectangle(
            left + 3, top + 4, left + width + 3, top + height + 4,
            fill="#080d12", outline="",
        )
        if selected:
            self.canvas.create_rectangle(left - 3, top - 3, left + width + 3, top + height + 3,
                                         outline="#296d58", width=1)
        self.canvas.create_rectangle(left, top, left + width, top + height, fill=fill, outline=border, width=2)

        if kind == "battery":
            self.canvas.create_line(x - 12, y - 14, x - 12, y + 14, fill=definition["color"], width=4)
            self.canvas.create_line(x + 1, y - 9, x + 1, y + 9, fill=definition["color"], width=3)
            label = f"{component.get('cells', 1)}x {component.get('format', 'AA')} | conjunto {component['voltage']:g} V"
            self.canvas.create_text(x, top + 10, text=label, fill=TEXT, font=("Segoe UI", 7))
        elif kind == "resistor":
            points = [x - 25, y, x - 17, y - 9, x - 7, y + 9, x + 3, y - 9, x + 13, y + 9, x + 25, y]
            self.canvas.create_line(*points, fill=definition["color"], width=3)
            self.canvas.create_text(x, top + 10, text=f"{component['resistance']:g} ohm", fill=TEXT,
                                    font=("Segoe UI", 8))
        elif kind == "capacitor":
            self.canvas.create_line(x - 7, y - 14, x - 7, y + 14, fill=definition["color"], width=3)
            self.canvas.create_line(x + 7, y - 14, x + 7, y + 14, fill=definition["color"], width=3)
            self.canvas.create_text(x, top + 10, text=f"{component['capacitance']:g} uF", fill=TEXT,
                                    font=("Segoe UI", 8))
        elif kind == "led":
            lit = self.last_currents.get(component["id"], 0.0) > 0.001
            color = "#ff6464" if lit else "#733e43"
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=color, outline="#ff9b92", width=2)
            self.canvas.create_line(x + 13, y - 12, x + 23, y - 18, fill=definition["color"], width=2)
            self.canvas.create_line(x + 18, y - 4, x + 28, y - 10, fill=definition["color"], width=2)
            if lit:
                self.canvas.create_oval(x - 16, y - 16, x + 16, y + 16, outline="#ff8e72", width=1)
            self.canvas.create_text(x, top + 10, text="LIGADO" if lit else "LED", fill=TEXT,
                                    font=("Segoe UI", 8))
        elif kind == "diode":
            self.canvas.create_line(x - 23, y, x - 9, y, fill=definition["color"], width=2)
            self.canvas.create_polygon(
                x - 9, y - 12, x - 9, y + 12, x + 7, y,
                fill=definition["color"], outline=definition["color"]
            )
            self.canvas.create_line(x + 9, y - 13, x + 9, y + 13, fill=definition["color"], width=3)
            self.canvas.create_line(x + 9, y, x + 23, y, fill=definition["color"], width=2)
            self.canvas.create_text(x, top + 10, text="DIODO", fill=TEXT, font=("Segoe UI", 8))
        elif kind == "button":
            closed = component.get("closed", False)
            self.canvas.create_line(x - 20, y, x - 6, y, fill=definition["color"], width=3)
            self.canvas.create_line(x + 6, y, x + 20, y, fill=definition["color"], width=3)
            self.canvas.create_line(x - 6, y, x + (6 if closed else 2), y + (0 if closed else -9),
                                    fill=definition["color"], width=3)
            self.canvas.create_text(x, top + 10, text="FECHADO" if closed else "ABERTO", fill=TEXT,
                                    font=("Segoe UI", 8))
        elif kind == "potentiometer":
            self.canvas.create_arc(x - 24, y - 18, x + 24, y + 18, start=15, extent=150,
                                   style="arc", outline=definition["color"], width=4)
            self.canvas.create_line(x, y + 1, x + 10, y - 10, fill=definition["color"], width=3)
            self.canvas.create_text(x + 24, y - 14, text=f"{component['wiper']:g}%", fill=TEXT,
                                    font=("Segoe UI", 8))
        elif kind == "buzzer":
            sounding = self.last_currents.get(component["id"], 0.0) > 0.001
            self.canvas.create_oval(x - 19, y - 19, x + 19, y + 19, fill="#392536",
                                    outline="#ff83c5" if sounding else definition["color"], width=3)
            self.canvas.create_text(x, y, text="♪", fill="#ff83c5" if sounding else definition["color"],
                                    font=("Segoe UI", 17, "bold"))
            self.canvas.create_text(x, top + 10, text=f"{component['resistance']:g} ohm", fill=TEXT,
                                    font=("Segoe UI", 8))
        elif kind == "motor":
            running = self.last_currents.get(component["id"], 0.0) > 0.001
            self.canvas.create_oval(x - 19, y - 19, x + 19, y + 19, fill="#263444",
                                    outline="#8bd0ff" if running else definition["color"], width=3)
            self.canvas.create_text(x, y, text="M", fill="#8bd0ff" if running else definition["color"],
                                    font=("Segoe UI", 15, "bold"))
            self.canvas.create_text(x, top + 10, text=f"{component['resistance']:g} ohm", fill=TEXT,
                                    font=("Segoe UI", 8))
        elif kind == "lamp":
            lit = self.last_currents.get(component["id"], 0.0) > 0.001
            self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15,
                                    fill="#ffe995" if lit else "#554c2e", outline=definition["color"], width=2)
            self.canvas.create_line(x - 9, y - 9, x + 9, y + 9, fill="#241f12", width=2)
            self.canvas.create_line(x - 9, y + 9, x + 9, y - 9, fill="#241f12", width=2)
            self.canvas.create_text(x, top + 10, text="LIGADA" if lit else "LAMPADA", fill=TEXT,
                                    font=("Segoe UI", 8))
        elif kind == "display":
            powered = self._display_powered(component)
            text = component.get("text", "Aguardando script")
            display_text = "\n".join(textwrap.wrap(text[:32], width=16)[:2]) or " "
            self.canvas.create_rectangle(left + 14, top + 24, left + width - 14, top + height - 10,
                                         fill="#102b26" if powered else "#17201e", outline="#397459")
            self.canvas.create_text(x, y + 9, text=display_text, fill="#92f5b5" if powered else "#72847b",
                                    font=("Consolas", 10), width=width - 38, justify="center")
            self.canvas.create_text(x, top + 13, text="TELA LCD 16x2", fill=TEXT, font=("Segoe UI", 9))
        elif kind == "arduino":
            self.canvas.create_rectangle(left + 26, top + 15, left + width - 12, top + height - 12,
                                         fill="#147968", outline="#58cbb1", width=2)
            self.canvas.create_text(x + 10, y, text="UNO", fill="white", font=("Segoe UI", 16, "bold"))
            self.canvas.create_text(x + 8, top + 10, text="ARDUINO", fill=TEXT, font=("Segoe UI", 8, "bold"))
            self.canvas.create_text(x + 7, y + 20, text="D13 / A0 / A4 / A5", fill="#bcebe1",
                                    font=("Segoe UI", 7))

        for pin, (px, py) in self._terminal_positions(component).items():
            terminal = terminal_id(component["id"], pin)
            connected = any(terminal in wire for wire in self.wires)
            color = ACCENT if terminal == self.pending_terminal else (WIRE if connected else "#d6e0e8")
            self.canvas.create_oval(px - 5, py - 5, px + 5, py + 5, fill=color, outline="#10161c", width=1)
            if len(definition["pins"]) == 2:
                label_x = px + (10 if px < x else -10)
                anchor = "w" if px < x else "e"
                self.canvas.create_text(label_x, py, text=pin, fill=MUTED, anchor=anchor, font=("Segoe UI", 7))
            else:
                anchor = "e" if px < x else "w"
                label_x = px - 8 if px < x else px + 8
                self.canvas.create_text(label_x, py, text=pin, fill=MUTED, anchor=anchor, font=("Segoe UI", 7))

    def _canvas_click(self, event):
        closest = self._find_terminal(event.x, event.y)
        if closest:
            if self.pending_terminal is None:
                self.pending_terminal = closest
            elif self.pending_terminal != closest:
                self.wires.append((self.pending_terminal, closest))
                self.pending_terminal = None
                self.status_var.set("Fio conectado.")
                if self.simulation_running:
                    self.simulate()
            else:
                self.pending_terminal = None
            self._draw_canvas()
            return

        component = self._find_component(event.x, event.y)
        if component:
            self.selected_id = component["id"]
            if component["type"] == "button":
                self.toggle_button(component["id"])
            else:
                self._show_properties()
                self.drag_state = (component["id"], event.x - component["x"], event.y - component["y"])
                self._draw_canvas()
        else:
            self.selected_id = None
            self.pending_terminal = None
            self._show_properties()
            self._draw_canvas()

    def _canvas_drag(self, event):
        if not self.drag_state:
            return
        component_id, offset_x, offset_y = self.drag_state
        component = next((item for item in self.components if item["id"] == component_id), None)
        if component:
            component["x"] = max(85, event.x - offset_x)
            component["y"] = max(55, event.y - offset_y)
            self._draw_canvas()

    def _canvas_release(self, _event):
        self.drag_state = None

    def _find_terminal(self, x, y):
        for component in self.components:
            for pin, (px, py) in self._terminal_positions(component).items():
                if math.hypot(px - x, py - y) <= 10:
                    return terminal_id(component["id"], pin)
        return None

    def _find_component(self, x, y):
        for component in reversed(self.components):
            width, height = COMPONENTS[component["type"]]["size"]
            if abs(component["x"] - x) <= width / 2 and abs(component["y"] - y) <= height / 2:
                return component
        return None

    def toggle_button(self, component_id):
        component = next((item for item in self.components if item["id"] == component_id), None)
        if component:
            component["closed"] = not component.get("closed", False)
            self._show_properties()
            self._draw_canvas()
            if self.simulation_running:
                self.simulate()

    def delete_selected(self):
        if self.selected_id is None:
            return
        prefix = f"{self.selected_id}:"
        self.components = [item for item in self.components if item["id"] != self.selected_id]
        self.wires = [wire for wire in self.wires if not wire[0].startswith(prefix) and not wire[1].startswith(prefix)]
        self.selected_id = None
        self._show_properties()
        self._draw_canvas()
        self.status_var.set("Componente removido.")

    def clear_project(self):
        if self.components and not messagebox.askyesno("Limpar quadro", "Remover todos os componentes e fios?"):
            return
        self.stop_simulation()
        self.components.clear()
        self.wires.clear()
        self.selected_id = None
        self.pending_terminal = None
        self._show_properties()
        self._draw_canvas()
        self.status_var.set("Quadro limpo.")

    def load_example(self):
        self.stop_simulation()
        self.components.clear()
        self.wires.clear()
        self.next_id = 1
        board = self._add_raw("arduino", 170, 250, pin13=5.0)
        resistor = self._add_raw("resistor", 365, 220, resistance=220.0)
        button = self._add_raw("button", 540, 220, closed=True)
        led = self._add_raw("led", 710, 220)
        screen = self._add_raw("display", 500, 420)
        self._connect(board, "D13", resistor, "A")
        self._connect(resistor, "B", button, "A")
        self._connect(button, "B", led, "A")
        self._connect(led, "K", board, "GND")
        self._connect(board, "VCC", screen, "VCC")
        self._connect(board, "GND", screen, "GND")
        self.selected_id = board
        self.simulation_running = True
        self.simulate()
        self._show_properties()
        self._draw_canvas()
        self.status_var.set("Exemplo ligado: clique no botao para abrir ou fechar o circuito.")
        self._log("Exemplo: Arduino D13 -> resistor 220 ohms -> botao -> LED -> GND; tela ligada em 5 V.")

    def open_manual(self):
        if self.manual_window is not None and self.manual_window.winfo_exists():
            self.manual_window.deiconify()
            self.manual_window.lift()
            return

        window = tk.Toplevel(self.root)
        window.title("Circuita - Manual e projetos para aprender")
        window.geometry("1050x740")
        window.minsize(820, 600)
        window.configure(bg=BG)
        self.manual_window = window
        window.protocol("WM_DELETE_WINDOW", self._close_manual)

        warning = tk.Label(
            window,
            text=SAFETY_INTRO,
            bg="#3a2a1d",
            fg="#ffe0a3",
            justify="left",
            anchor="w",
            wraplength=980,
            padx=14,
            pady=12,
            font=("Segoe UI", 9, "bold"),
        )
        warning.pack(fill="x", padx=12, pady=12)

        content = tk.Frame(window, bg=BG)
        content.pack(fill="both", expand=True, padx=12)
        lesson_frame = tk.Frame(content, bg=PANEL, width=280)
        lesson_frame.pack(side="left", fill="y", padx=(0, 10))
        lesson_frame.pack_propagate(False)
        tk.Label(lesson_frame, text="AULAS PRATICAS", bg=PANEL, fg=ACCENT,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=12, pady=12)
        list_frame = tk.Frame(lesson_frame, bg=PANEL)
        list_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        list_scroll = ttk.Scrollbar(list_frame, orient="vertical")
        self.lesson_list = tk.Listbox(
            list_frame,
            bg="#10161c",
            fg=TEXT,
            selectbackground="#176c59",
            selectforeground="white",
            relief="flat",
            font=("Segoe UI", 9),
            activestyle="none",
            yscrollcommand=list_scroll.set,
        )
        list_scroll.configure(command=self.lesson_list.yview)
        list_scroll.pack(side="right", fill="y")
        self.lesson_list.pack(side="left", fill="both", expand=True)
        for lesson in LESSONS:
            self.lesson_list.insert("end", lesson["title"])
        self.lesson_list.bind("<<ListboxSelect>>", self._show_lesson)

        guide = tk.Frame(content, bg=PANEL)
        guide.pack(side="left", fill="both", expand=True)
        tk.Label(guide, text="MANUAL DE ELETRONICA PARA INICIANTES",
                 bg=PANEL, fg=ACCENT, font=("Segoe UI", 10, "bold")).pack(
                     anchor="w", padx=12, pady=(12, 6)
                 )
        guide_text_frame = tk.Frame(guide, bg=PANEL)
        guide_text_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        guide_scroll = ttk.Scrollbar(guide_text_frame, orient="vertical")
        self.lesson_text = tk.Text(
            guide_text_frame,
            bg="#10161c",
            fg=TEXT,
            relief="flat",
            wrap="word",
            padx=14,
            pady=12,
            spacing1=2,
            spacing3=5,
            font=("Segoe UI", 10),
            yscrollcommand=guide_scroll.set,
        )
        guide_scroll.configure(command=self.lesson_text.yview)
        guide_scroll.pack(side="right", fill="y")
        self.lesson_text.pack(side="left", fill="both", expand=True)
        self.lesson_text.tag_configure("title", foreground=ACCENT, font=("Segoe UI", 15, "bold"), spacing3=10)
        self.lesson_text.tag_configure("heading", foreground="#83d9bd", font=("Segoe UI", 10, "bold"), spacing1=8)
        self.lesson_text.tag_configure("safety", foreground="#ffd08a")
        self.lesson_text.configure(state="disabled")

        footer = tk.Frame(window, bg=BG)
        footer.pack(fill="x", padx=12, pady=12)
        self.lesson_status = tk.StringVar(value="Selecione uma aula e monte o projeto para acompanha-la no quadro.")
        tk.Label(footer, textvariable=self.lesson_status, bg=BG, fg=MUTED,
                 font=("Segoe UI", 9)).pack(side="left", fill="x", expand=True)
        self._tool_button(footer, "Aula anterior", lambda: self._step_lesson(-1))
        self._tool_button(footer, "Montar projeto da aula", self._load_selected_lesson, accent=True)
        self._tool_button(footer, "Proxima aula", lambda: self._step_lesson(1))
        self.lesson_list.selection_set(0)
        self.lesson_list.activate(0)
        self._show_lesson()

    def _close_manual(self):
        if self.manual_window is not None and self.manual_window.winfo_exists():
            self.manual_window.destroy()
        self.manual_window = None

    def _selected_lesson_index(self):
        if not hasattr(self, "lesson_list") or not self.lesson_list.winfo_exists():
            return 0
        selection = self.lesson_list.curselection()
        return selection[0] if selection else 0

    def _show_lesson(self, _event=None):
        if not hasattr(self, "lesson_text") or not self.lesson_text.winfo_exists():
            return
        lesson = LESSONS[self._selected_lesson_index()]
        lines = []

        def heading(text):
            lines.append((text, "heading"))

        lines.append((lesson["title"], "title"))
        heading("Como funciona a protoboard")
        lines.append((BREADBOARD_INTRO, "body"))
        heading("O que vamos aprender")
        lines.append((lesson["goal"], "body"))
        heading("Materiais")
        lines.append((lesson["parts"], "body"))
        heading("Seguranca - leia antes de montar")
        lines.append((lesson["safety"], "safety"))
        heading("Monte com a fonte desconectada")
        for number, step in enumerate(lesson["steps"], start=1):
            lines.append((f"{number}. {step}", "body"))
        heading("O que deve acontecer")
        lines.append((lesson["observe"], "body"))
        heading("Como montar no Circuita e o que o modelo nao simula")
        lines.append((lesson["real"], "body"))
        lines.append(("", "body"))
        self.lesson_text.configure(state="normal")
        self.lesson_text.delete("1.0", "end")
        for text, tag in lines:
            self.lesson_text.insert("end", text + "\n", tag)
        self.lesson_text.configure(state="disabled")
        self.lesson_text.yview_moveto(0)
        self.lesson_status.set(
            f"Aula {self._selected_lesson_index() + 1} de {len(LESSONS)}. "
            "Desconecte a fonte real antes de alterar a montagem."
        )

    def _step_lesson(self, offset):
        index = self._selected_lesson_index()
        index = (index + offset) % len(LESSONS)
        self.lesson_list.selection_clear(0, "end")
        self.lesson_list.selection_set(index)
        self.lesson_list.activate(index)
        self.lesson_list.see(index)
        self._show_lesson()

    def _load_selected_lesson(self):
        index = self._selected_lesson_index()
        lesson = LESSONS[index]
        if self.components and not messagebox.askyesno(
            "Carregar projeto da aula",
            "O projeto atual no quadro sera substituido. Salve-o antes se quiser guarda-lo.",
            parent=self.manual_window,
        ):
            return
        self.stop_simulation()
        self.components = []
        self.wires = deepcopy(lesson["project"]["wires"])
        for item in lesson["project"]["components"]:
            component = deepcopy(item)
            component_type = component["type"]
            component.update(DEFAULTS[component_type])
            component.update(item)
            self.components.append(component)
        self.next_id = max((item["id"] for item in self.components), default=0) + 1
        self.selected_id = next(
            (item["id"] for item in self.components if item["type"] == "arduino"),
            self.components[0]["id"] if self.components else None,
        )
        self.pending_terminal = None
        self.script.delete("1.0", "end")
        self.script.insert("1.0", lesson["project"].get("script", ""))
        self.last_voltages = {}
        self.last_currents = {}
        self._show_properties()
        self._draw_canvas()
        self.simulation_running = True
        self.simulate()
        self.status_var.set(f"Projeto carregado: {lesson['title']}. Siga as instrucoes do manual.")
        self.lesson_status.set(f"Projeto da aula {index + 1} carregado no quadro.")
        self._log(f"Manual: carregado projeto '{lesson['title']}'.")

    def _add_raw(self, kind, x, y, **values):
        component_id = self.next_id
        self.next_id += 1
        component = {"id": component_id, "type": kind, "x": x, "y": y}
        component.update(DEFAULTS[kind])
        component.update(values)
        self.components.append(component)
        return component_id

    def _connect(self, first_component, first_pin, second_component, second_pin):
        self.wires.append((terminal_id(first_component, first_pin), terminal_id(second_component, second_pin)))

    def save_project(self):
        path = filedialog.asksaveasfilename(
            parent=self.root,
            title="Salvar circuito",
            defaultextension=".circuita",
            filetypes=[("Projeto Circuita", "*.circuita"), ("JSON", "*.json")],
        )
        if not path:
            return
        project = {"version": 1, "components": self.components, "wires": self.wires, "script": self.script.get("1.0", "end-1c")}
        try:
            with open(path, "w", encoding="utf-8") as project_file:
                json.dump(project, project_file, indent=2, ensure_ascii=False)
        except OSError as error:
            messagebox.showerror("Erro ao salvar", str(error), parent=self.root)
            return
        self.status_var.set(f"Projeto salvo: {path}")

    def open_project(self):
        path = filedialog.askopenfilename(
            parent=self.root,
            title="Abrir circuito",
            filetypes=[("Projeto Circuita", "*.circuita *.json"), ("Todos os arquivos", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as project_file:
                project = json.load(project_file)
            components = project.get("components")
            wires = project.get("wires")
            if not isinstance(components, list) or not isinstance(wires, list):
                raise ValueError("O arquivo nao contem um projeto Circuita valido.")
            valid_ids = set()
            for index, component in enumerate(components):
                if not isinstance(component, dict):
                    raise ValueError("O projeto contem um componente invalido.")
                if component.get("type") not in COMPONENTS or not isinstance(component.get("id"), int):
                    raise ValueError("O projeto contem um componente desconhecido.")
                component_type = component["type"]
                defaults = dict(DEFAULTS[component_type])
                defaults.update(component)
                if component_type == "battery":
                    if "cells" not in component:
                        defaults["cells"] = max(1, min(24, round(defaults["voltage"] / 1.5)))
                    if defaults.get("format") not in ("A", "AA", "AAA"):
                        raise ValueError("Formato de pilha invalido. Use A, AA ou AAA.")
                    cells = defaults.get("cells")
                    if not isinstance(cells, int) or not 1 <= cells <= 24:
                        raise ValueError("Quantidade de pilhas invalida. Use um numero inteiro entre 1 e 24.")
                components[index] = defaults
                valid_ids.add(component["id"])
            for wire in wires:
                if not isinstance(wire, list) or len(wire) != 2:
                    raise ValueError("O projeto contem uma conexao invalida.")
                for terminal in wire:
                    component_part, separator, pin = terminal.partition(":")
                    if not separator or not component_part.isdigit():
                        raise ValueError("O projeto contem um terminal invalido.")
                    component = next((item for item in components if item["id"] == int(component_part)), None)
                    if component is None or pin not in COMPONENTS[component["type"]]["pins"]:
                        raise ValueError("O projeto conecta um terminal inexistente.")
        except (OSError, json.JSONDecodeError, ValueError, AttributeError) as error:
            messagebox.showerror("Erro ao abrir", str(error), parent=self.root)
            return
        self.stop_simulation()
        self.components = components
        self.wires = [tuple(wire) for wire in wires]
        self.next_id = max(valid_ids, default=0) + 1
        self.selected_id = None
        self.pending_terminal = None
        self.script.delete("1.0", "end")
        self.script.insert("1.0", project.get("script", ""))
        self._show_properties()
        self._draw_canvas()
        self.status_var.set(f"Projeto aberto: {path}")

    def start_simulation(self):
        self.simulation_running = True
        self.simulate()

    def stop_simulation(self):
        self.simulation_running = False
        self.last_currents = {}
        self._draw_canvas()
        if hasattr(self, "status_var"):
            self._set_status("Simulacao parada", "#738291")

    def _set_status(self, message, color):
        self.status_var.set(message)
        self.status_dot.itemconfigure(1, fill=color)

    def _run_solver(self):
        terminals = []
        for component in self.components:
            terminals.extend(terminal_id(component["id"], pin) for pin in COMPONENTS[component["type"]]["pins"])
        union = UnionFind(terminals)
        for first, second in self.wires:
            if first in union.parent and second in union.parent:
                union.union(first, second)
        roots = list(dict.fromkeys(union.find(terminal) for terminal in terminals))
        if not roots:
            return {}, {}

        ground_terminal = next(
            (
                terminal_id(component["id"], pin)
                for component in self.components
                for pin in (["-", "GND"] if component["type"] in ("battery", "arduino", "display") else [])
                if pin in COMPONENTS[component["type"]]["pins"]
            ),
            terminals[0],
        )
        ground = union.find(ground_terminal)
        node_roots = [root for root in roots if root != ground]
        node_index = {root: index for index, root in enumerate(node_roots)}
        semiconductor_states = {
            component["id"]: False
            for component in self.components
            if component["type"] in ("led", "diode")
        }
        voltages = {}

        def node_voltage(root, solution):
            return 0.0 if root == ground else solution[node_index[root]]

        for _iteration in range(8):
            size = len(node_roots)
            matrix = [[0.0] * size for _ in range(size)]
            vector = [0.0] * size
            conductances = {}

            def branch(first_terminal, second_terminal, resistance, source_voltage=0.0, key=None):
                first = union.find(first_terminal)
                second = union.find(second_terminal)
                resistance = max(float(resistance), 1e-9)
                conductance = 1.0 / resistance
                conductances[key] = conductance
                first_index = node_index.get(first)
                second_index = node_index.get(second)
                if first_index is not None:
                    matrix[first_index][first_index] += conductance
                    vector[first_index] += source_voltage * conductance
                if second_index is not None:
                    matrix[second_index][second_index] += conductance
                    vector[second_index] -= source_voltage * conductance
                if first_index is not None and second_index is not None:
                    matrix[first_index][second_index] -= conductance
                    matrix[second_index][first_index] -= conductance

            for index in range(size):
                matrix[index][index] += 1e-9

            for component in self.components:
                kind = component["type"]
                first = terminal_id(component["id"], COMPONENTS[kind]["pins"][0])
                second = terminal_id(component["id"], COMPONENTS[kind]["pins"][1])
                if kind == "resistor":
                    branch(first, second, component["resistance"], key=component["id"])
                elif kind == "battery":
                    branch(first, second, 0.05, component["voltage"], key=component["id"])
                elif kind == "button" and component.get("closed"):
                    branch(first, second, 0.02, key=component["id"])
                elif kind in ("led", "diode"):
                    forward = component.get("forward_voltage", 2.0) if semiconductor_states[component["id"]] else 0.0
                    resistance = component.get("resistance", 20.0) if semiconductor_states[component["id"]] else 1e6
                    branch(first, second, resistance, forward, key=component["id"])
                elif kind in ("buzzer", "motor", "lamp"):
                    branch(first, second, component["resistance"], key=component["id"])
                elif kind == "potentiometer":
                    total_resistance = component["resistance"]
                    position = component["wiper"] / 100.0
                    branch(
                        terminal_id(component["id"], "A"),
                        terminal_id(component["id"], "W"),
                        max(total_resistance * position, 0.01),
                        key=(component["id"], "aw"),
                    )
                    branch(
                        terminal_id(component["id"], "W"),
                        terminal_id(component["id"], "B"),
                        max(total_resistance * (1.0 - position), 0.01),
                        key=(component["id"], "wb"),
                    )
                elif kind == "arduino":
                    branch(
                        terminal_id(component["id"], "VCC"),
                        terminal_id(component["id"], "GND"),
                        0.1,
                        5.0,
                        key=(component["id"], "vcc"),
                    )
                    branch(
                        terminal_id(component["id"], "D13"),
                        terminal_id(component["id"], "GND"),
                        0.1,
                        component.get("pin13", 0.0),
                        key=(component["id"], "d13"),
                    )
                    branch(
                        terminal_id(component["id"], "A0"),
                        terminal_id(component["id"], "GND"),
                        10_000_000.0,
                        key=(component["id"], "a0"),
                    )

            solution = solve_linear(matrix, vector) if size else []
            voltages = {root: node_voltage(root, solution) for root in roots}
            changed = False
            for component in self.components:
                if component["type"] not in ("led", "diode"):
                    continue
                first = union.find(terminal_id(component["id"], "A"))
                second = union.find(terminal_id(component["id"], "K"))
                forward_voltage = voltages[first] - voltages[second]
                conducting = forward_voltage > component.get("forward_voltage", 2.0)
                if conducting != semiconductor_states[component["id"]]:
                    semiconductor_states[component["id"]] = conducting
                    changed = True
            if not changed:
                break

        currents = {}
        for component in self.components:
            kind = component["type"]
            if kind not in (
                "resistor", "led", "diode", "button", "battery", "buzzer", "motor", "lamp", "potentiometer"
            ):
                continue
            if kind == "potentiometer":
                first = terminal_id(component["id"], "A")
                second = terminal_id(component["id"], "B")
                resistance = component["resistance"]
            else:
                first, second = COMPONENTS[kind]["pins"][:2]
                first = terminal_id(component["id"], first)
                second = terminal_id(component["id"], second)
            difference = voltages[union.find(first)] - voltages[union.find(second)]
            if kind == "resistor":
                resistance = component["resistance"]
            elif kind == "battery":
                resistance = 0.05
                difference -= component["voltage"]
            elif kind == "button":
                if not component.get("closed"):
                    currents[component["id"]] = 0.0
                    continue
                resistance = 0.02
            else:
                resistance = component.get("resistance", 20.0)
                if kind in ("led", "diode") and not semiconductor_states[component["id"]]:
                    resistance = 1e6
                if kind in ("led", "diode") and semiconductor_states[component["id"]]:
                    difference -= component.get("forward_voltage", 2.0 if kind == "led" else 0.7)
            currents[component["id"]] = difference / resistance
        terminal_voltages = {terminal: voltages[union.find(terminal)] for terminal in terminals}
        return terminal_voltages, currents

    def _display_powered(self, component):
        if not self.last_voltages:
            return False
        terminals = [terminal_id(component["id"], pin) for pin in ("VCC", "GND")]
        values = [self.last_voltages.get(terminal) for terminal in terminals]
        if None in values:
            return False
        return values[0] - values[1] >= 2.7

    def simulate(self):
        try:
            self.last_voltages, self.last_currents = self._run_solver()
        except (ValueError, ZeroDivisionError) as error:
            self._set_status("Falha na simulacao", "#ff6678")
            self._log(f"Erro: {error}")
            return False
        self._draw_canvas()
        active_loads = sum(
            1 for item in self.components
            if item["type"] in ("led", "lamp", "buzzer", "motor")
            and self.last_currents.get(item["id"], 0.0) > 0.001
        )
        self._set_status(
            f"Simulando circuito DC | Cargas ativas: {active_loads}",
            ACCENT if active_loads else "#70c8ff",
        )
        if active_loads:
            self._log(f"Simulacao concluida: {active_loads} carga(s) ativa(s).")
        else:
            self._log("Simulacao concluida: nenhuma carga ativa. Confira a fonte, os fios e a polaridade.")
        self._show_properties()
        return True

    def run_script(self):
        commands = self.script.get("1.0", "end-1c").splitlines()
        messages = []
        read_a0 = False
        try:
            for number, raw_command in enumerate(commands, start=1):
                command = raw_command.strip()
                if not command or command.startswith("#"):
                    continue
                match = re.fullmatch(r"DISPLAY\s+(.+)", command, re.IGNORECASE)
                if match:
                    text = match.group(1).strip().strip('"')
                    screens = [item for item in self.components if item["type"] == "display"]
                    if not screens:
                        raise ValueError(f"Linha {number}: adicione uma Tela LCD antes de usar DISPLAY.")
                    screens[0]["text"] = text[:32]
                    messages.append(f'Tela: "{text[:32]}"')
                    continue
                match = re.fullmatch(r"DIGITAL_WRITE\s+13\s+(HIGH|LOW)", command, re.IGNORECASE)
                if match:
                    boards = [item for item in self.components if item["type"] == "arduino"]
                    if not boards:
                        raise ValueError(f"Linha {number}: adicione um Arduino Uno antes de usar DIGITAL_WRITE.")
                    boards[0]["pin13"] = 5.0 if match.group(1).upper() == "HIGH" else 0.0
                    messages.append(f"Pino D13 definido como {match.group(1).upper()}.")
                    continue
                if re.fullmatch(r"READ\s+A0", command, re.IGNORECASE):
                    if not any(item["type"] == "arduino" for item in self.components):
                        raise ValueError(f"Linha {number}: adicione um Arduino Uno antes de usar READ A0.")
                    read_a0 = True
                    continue
                match = re.fullmatch(r"WAIT\s+(\d+)", command, re.IGNORECASE)
                if match:
                    delay = int(match.group(1))
                    if delay > 60000:
                        raise ValueError(f"Linha {number}: WAIT aceita no maximo 60000 ms.")
                    messages.append(f"WAIT {delay} ms (tempo logico; sem atraso na interface).")
                    continue
                raise ValueError(
                    f"Linha {number}: comando desconhecido. Use DISPLAY, DIGITAL_WRITE, READ A0 ou WAIT."
                )
        except ValueError as error:
            messagebox.showerror("Erro no script", str(error), parent=self.root)
            return
        self.simulation_running = True
        if not self.simulate():
            return
        for message in messages:
            self._log(message)
        if read_a0:
            board = next(item for item in self.components if item["type"] == "arduino")
            voltage = self.last_voltages.get(terminal_id(board["id"], "A0"), 0.0)
            analog_value = round(min(max(voltage, 0.0), 5.0) * 1023 / 5.0)
            self._log(f"Leitura A0: {voltage:.2f} V ({analog_value}/1023).")
        for component in self.components:
            if component["type"] == "display":
                self._log(f'Tela LCD: "{component["text"]}" '
                           f'({"alimentada" if self._display_powered(component) else "sem alimentacao"}).')
        self._show_properties()

    def _log(self, text):
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n")
        lines = int(self.output.index("end-1c").split(".")[0])
        if lines > 100:
            self.output.delete("1.0", f"{lines - 100}.0")
        self.output.see("end")
        self.output.configure(state="disabled")


def main():
    root = tk.Tk()
    CircuitaApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
