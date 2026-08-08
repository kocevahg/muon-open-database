"""
Muon Spectrum Viewer  - PyQt6 desktop application
===================================================

Cross-platform replacement for the old tkinter tool. Reads the current
muon_data.db schema (theta_center / stat_error / sys_error / total_error /
momentum_min / momentum_max ...) directly, so it stays in sync with
build_database.py.

Run:
    pip install PyQt6 matplotlib numpy
    python spectrum_app.py
"""

from __future__ import annotations

import os
import sqlite3
import sys
from dataclasses import dataclass

import numpy as np

from PyQt6 import QtCore, QtGui, QtWidgets

import matplotlib
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.ticker as mticker

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
DEFAULT_DB = "muon_data.db"

RECOMMENDED_X = (1e-1, 1e5)      # momentum, GeV/c
RECOMMENDED_Y = (1e-15, 1e-2)    # intensity, (cm^2 s sr GeV/c)^-1

ERROR_CHOICES = {
    "Total (stat + sys)": "total_error",
    "Statistical only": "stat_error",
    "Systematic only": "sys_error",
}

# One colour per experiment.
EXP_COLORS = {
    "AMH":        "#0072B2",  # blue
    "DEIS":       "#D55E00",  # vermillion
    "De Pascale": "#661100",  # green
    "Kellogg":    "#CC79A7",  # purple
    "Kiel-DESY":  "#56B4E9",  # sky blue
    "L3+C":       "#E69F00",  # orange
    "MUTRON":     "#882255",  # wine
    "Nottingham": "#44AA99",  # teal
    "OKAYAMA":    "#999999",  # dark gray
}

FALLBACK_COLORS = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e",
                   "#17becf", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22"]
MARKERS = ["o", "s", "^", "D", "v", "P", "X", "*", "<", ">"]

# ---- plot colours ----
PLOT_BG = "#ffffff"       # figure + axes background
PLOT_FG = "#1c2530"       # axis labels / ticks
PLOT_MUTED = "#7a869a"    # secondary axis
PLOT_GRID = "#d3dae4"     # gridlines

# ---- accent palette ----
ACCENT = "#2563eb"        # primary action blue
ACCENT_HOVER = "#3b7bf5"
ACCENT_PRESS = "#1d4ed8"

# ---- dark stylesheet (chrome dark; white graph; buttons kept visible) ----
DARK_QSS = """
QMainWindow, QWidget { background: #1b1f27; color: #e4e8ef; }
QGroupBox {
    border: 1px solid #333b48; border-radius: 10px;
    margin-top: 14px; padding-top: 6px; background: #232833;
    font-weight: 600;
}
QGroupBox::title {
    subcontrol-origin: margin; subcontrol-position: top left;
    left: 12px; top: 2px; padding: 2px 6px; color: #7fb0e6;
}
QGroupBox::indicator { width: 15px; height: 15px; }

/* default (secondary) buttons: raised surface with a defined outline */
QPushButton {
    background: #2c3542; border: 1.5px solid #45566e; border-radius: 7px;
    padding: 7px 12px; color: #e8edf5; font-weight: 600;
}
QPushButton:hover { background: #37424f; border-color: #6ea3e6; color: #cfe0f7; }
QPushButton:pressed { background: #262f3b; border-color: #3b7bf5; }

/* primary action: solid blue, high contrast */
QPushButton#primary {
    background: #2563eb; border: 1.5px solid #2563eb; color: #ffffff; font-weight: 700;
    padding: 9px 12px;
}
QPushButton#primary:hover { background: #3b7bf5; border-color: #3b7bf5; }
QPushButton#primary:pressed { background: #1d4ed8; border-color: #1d4ed8; }

QComboBox, QDoubleSpinBox, QLineEdit {
    background: #1b1f27; border: 1px solid #3d4a5c; border-radius: 6px; padding: 4px 7px;
    color: #e4e8ef; selection-background-color: #2563eb; selection-color: #ffffff;
}
QComboBox:hover, QDoubleSpinBox:hover, QLineEdit:hover { border-color: #567296; }
QComboBox QAbstractItemView {
    background: #232833; color: #e4e8ef; selection-background-color: #2563eb;
    selection-color: #ffffff;
}
QTreeWidget, QTableWidget {
    background: #232833; border: 1px solid #333b48; border-radius: 8px;
    alternate-background-color: #262c38; color: #e4e8ef;
}
QTreeWidget::item:selected, QTableWidget::item:selected {
    background: #37507a; color: #ffffff;
}
QHeaderView::section {
    background: #2c3542; border: none; border-bottom: 1px solid #333b48;
    padding: 5px; font-weight: 600; color: #7fb0e6;
}
QCheckBox { color: #e4e8ef; spacing: 6px; }
QCheckBox::indicator {
    width: 16px; height: 16px; border: 1.5px solid #45566e; border-radius: 4px;
    background: #1b1f27;
}
QCheckBox::indicator:checked {
    background: #2563eb; border-color: #2563eb;
    image: url();
}
QCheckBox::indicator:hover { border-color: #6ea3e6; }
QLabel { color: #e4e8ef; }
QTabBar::tab {
    background: #2c3542; border: 1px solid #333b48; border-bottom: none;
    padding: 7px 16px; border-top-left-radius: 8px; border-top-right-radius: 8px;
    color: #9fb0c6;
}
QTabBar::tab:selected { background: #232833; color: #7fb0e6; font-weight: 700; }
QStatusBar { background: #232833; color: #7fb0e6; font-weight: 500; }
"""

# ---------------------------------------------------------------------------
# Data layer
# ---------------------------------------------------------------------------
@dataclass
class Point:
    theta: float
    momentum: float
    intensity: float
    xerr: float
    stat: float
    sys: float
    total: float


class MuonData:
    """Loads the whole table once; keeps points grouped by (experiment, theta)."""

    def __init__(self, db_path: str = DEFAULT_DB):
        self.db_path = db_path
        self.experiments: list[str] = []
        self.references: dict[str, str] = {}
        # {experiment: {theta: [Point, ...]}}
        self.by_exp_theta: dict[str, dict[float, list[Point]]] = {}
        self.color_of: dict[str, str] = {}
        self.marker_of: dict[str, str] = {}
        self._load()

    def _load(self):
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(
                f"Database not found: {self.db_path}\n"
                "Run build_database.py first, or open a different .db."
            )
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            "SELECT experiment, reference, theta_center, momentum, "
            "momentum_min, momentum_max, intensity, stat_error, sys_error, "
            "total_error FROM muon_data "
            "WHERE intensity IS NOT NULL AND theta_center IS NOT NULL "
            "ORDER BY experiment, theta_center, momentum"
        )
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()

        def half(r):
            lo, hi = r["momentum_min"], r["momentum_max"]
            if lo is None or hi is None:
                return 0.0
            return (hi - lo) / 2.0

        order = []
        for r in rows:
            exp = r["experiment"]
            if exp not in self.by_exp_theta:
                self.by_exp_theta[exp] = {}
                self.references[exp] = r["reference"] or ""
                order.append(exp)
            th = float(r["theta_center"])
            self.by_exp_theta[exp].setdefault(th, []).append(Point(
                theta=th,
                momentum=float(r["momentum"]),
                intensity=float(r["intensity"]),
                xerr=half(r),
                stat=_nz(r["stat_error"]),
                sys=_nz(r["sys_error"]),
                total=_nz(r["total_error"]),
            ))

        self.experiments = order
        for i, exp in enumerate(order):
            self.color_of[exp] = EXP_COLORS.get(exp, FALLBACK_COLORS[i % len(FALLBACK_COLORS)])
            self.marker_of[exp] = MARKERS[i % len(MARKERS)]

    def angles(self, exp: str) -> list[float]:
        return sorted(self.by_exp_theta.get(exp, {}).keys())


def _nz(v):
    return 0.0 if v is None else float(v)


# ---------------------------------------------------------------------------
# Plot canvas
# ---------------------------------------------------------------------------
class SpectrumCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(7, 8))
        self.fig.patch.set_facecolor(PLOT_BG)
        super().__init__(self.fig)
        self.setParent(parent)
        self.ax = self.fig.add_subplot(111)
        self.ax2 = None

    def draw_spectrum(self, series, xlim, ylim, err_attr, theta_lo, theta_hi,
                      logx=True, logy=True):
        self.fig.clear()
        self.fig.patch.set_facecolor(PLOT_BG)
        self.ax = self.fig.add_subplot(111)
        self.ax2 = None
        ax = self.ax
        ax.set_facecolor(PLOT_BG)

        for (exp, color, marker, x, y, xerr, yerr) in series:
            ax.errorbar(
                x, y,
                xerr=xerr if np.any(xerr > 0) else None,
                yerr=yerr if np.any(yerr > 0) else None,
                fmt=marker, label=exp,
                markerfacecolor="none", markeredgecolor=color,
                ecolor=color, color=color,
                capsize=2.5, elinewidth=0.6, markersize=4.5, markeredgewidth=1.0,
                linestyle="none",
            )

        ax.set_xscale("log" if logx else "linear")
        ax.set_yscale("log" if logy else "linear")
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_xlabel("Momentum  [GeV/c]", fontsize=13, color=PLOT_FG)
        ax.set_ylabel(
            r"Differential intensity  [cm$^{-2}$s$^{-1}$sr$^{-1}$(GeV/c)$^{-1}$]",
            fontsize=13, color=PLOT_FG,
        )
        ax.tick_params(axis="both", colors=PLOT_FG, which="both")
        for spine in ax.spines.values():
            spine.set_color(PLOT_GRID)
        if logy:
            ax.yaxis.set_major_locator(mticker.LogLocator(numticks=15))
            ax.yaxis.set_minor_locator(mticker.LogLocator(numticks=15, subs="auto"))
        ax.grid(True, which="major", ls="-", lw=0.4, alpha=0.45, color=PLOT_GRID)
        ax.grid(True, which="minor", ls=":", lw=0.3, alpha=0.3, color=PLOT_GRID)

        ax.text(
            0.98, 0.98, f"θ = {theta_lo:g} – {theta_hi:g}°",
            transform=ax.transAxes, fontsize=13, color=PLOT_FG,
            va="top", ha="right",
            bbox=dict(facecolor="#ffffff", edgecolor=PLOT_GRID, boxstyle="round,pad=0.3"),
        )
        handles, labels = ax.get_legend_handles_labels()
        if handles:
            # duplicate legend (one entry per experiment)
            seen = {}
            for h, l in zip(handles, labels):
                seen.setdefault(l, h)
            leg = ax.legend(list(seen.values()), list(seen.keys()), fontsize=8,
                            loc="lower left", ncol=2, framealpha=0.95,
                            facecolor="#ffffff", edgecolor=PLOT_GRID)
            for txt in leg.get_texts():
                txt.set_color(PLOT_FG)

        self.fig.tight_layout()
        self.draw_idle()


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, db_path=DEFAULT_DB):
        super().__init__()
        self.setWindowTitle("Muon Spectrum Viewer")
        self.resize(1300, 860)
        self.db_path = db_path
        self.data: MuonData | None = None
        self._plot_update_pending = False
        self._build_ui()
        self._load_db(db_path)

    # ---- UI --------------------------------------------------------------
    def _build_ui(self):
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        root = QtWidgets.QHBoxLayout(central)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        # ---- left control panel (inside a scroll area) ----
        panel = QtWidgets.QWidget()
        pl = QtWidgets.QVBoxLayout(panel)
        pl.setContentsMargins(2, 2, 10, 2)
        pl.setSpacing(12)

        # Angle window
        gb_angle = QtWidgets.QGroupBox("Zenith angle window  θ  [deg]")
        fa = QtWidgets.QFormLayout(gb_angle)
        fa.setContentsMargins(12, 16, 12, 12)
        fa.setSpacing(8)
        fa.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.theta_lo = QtWidgets.QDoubleSpinBox()
        self.theta_hi = QtWidgets.QDoubleSpinBox()
        for sb in (self.theta_lo, self.theta_hi):
            sb.setRange(0, 90); sb.setDecimals(1); sb.setSingleStep(1.0)
            sb.setMinimumHeight(28)
        self.theta_lo.setValue(0.0)
        self.theta_hi.setValue(90.0)
        fa.addRow("Min θ", self.theta_lo)
        fa.addRow("Max θ", self.theta_hi)
        pl.addWidget(gb_angle)

        # Error convention
        gb_err = QtWidgets.QGroupBox("Error bars")
        ve = QtWidgets.QVBoxLayout(gb_err)
        ve.setContentsMargins(12, 16, 12, 12)
        self.err_combo = QtWidgets.QComboBox()
        self.err_combo.addItems(list(ERROR_CHOICES.keys()))
        self.err_combo.setMinimumHeight(28)
        ve.addWidget(self.err_combo)
        pl.addWidget(gb_err)

        # Experiment -> angle tree (takes all remaining vertical space)
        gb_tree = QtWidgets.QGroupBox("Experiments  →  angles")
        vt = QtWidgets.QVBoxLayout(gb_tree)
        vt.setContentsMargins(12, 16, 12, 12)
        vt.setSpacing(8)
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setHeaderLabels(["experiment / angle", "N"])
        self.tree.setColumnWidth(0, 230)
        self.tree.setAlternatingRowColors(True)
        self.tree.setRootIsDecorated(True)
        self.tree.setMinimumHeight(320)
        self.tree.setIndentation(14)
        vt.addWidget(self.tree, stretch=1)
        self.tree.itemChanged.connect(self._on_tree_changed)
        hbtn = QtWidgets.QHBoxLayout()
        hbtn.setSpacing(8)
        b_all = QtWidgets.QPushButton("All")
        b_none = QtWidgets.QPushButton("None")
        b_col = QtWidgets.QPushButton("Collapse")
        b_all.clicked.connect(lambda: self._set_all(True))
        b_none.clicked.connect(lambda: self._set_all(False))
        b_col.clicked.connect(self.tree.collapseAll)
        for b in (b_all, b_none, b_col):
            b.setMinimumHeight(26)
            hbtn.addWidget(b)
        vt.addLayout(hbtn)
        pl.addWidget(gb_tree, stretch=1)

        # Axis ranges (checkable title collapses the box). All the fields live
        # in 1 inner container widget, so collapsing hides the whole thing
        self.gb_axes = QtWidgets.QGroupBox("Axis ranges")
        self.gb_axes.setCheckable(True)
        self.gb_axes.setChecked(False)
        gb_axes_outer = QtWidgets.QVBoxLayout(self.gb_axes)
        gb_axes_outer.setContentsMargins(10, 14, 10, 10)

        self._axes_body = QtWidgets.QWidget()
        fx = QtWidgets.QFormLayout(self._axes_body)
        fx.setContentsMargins(0, 0, 0, 0)
        fx.setSpacing(8)
        self.xmin = _SciSpin(RECOMMENDED_X[0]); self.xmax = _SciSpin(RECOMMENDED_X[1])
        self.ymin = _SciSpin(RECOMMENDED_Y[0]); self.ymax = _SciSpin(RECOMMENDED_Y[1])
        for sb in (self.xmin, self.xmax, self.ymin, self.ymax):
            sb.setMinimumHeight(28)
        fx.addRow("X min (GeV/c)", self.xmin)
        fx.addRow("X max (GeV/c)", self.xmax)
        fx.addRow("Y min", self.ymin)
        fx.addRow("Y max", self.ymax)
        self.logx = QtWidgets.QCheckBox("Log X"); self.logx.setChecked(True)
        self.logy = QtWidgets.QCheckBox("Log Y"); self.logy.setChecked(True)
        hlog = QtWidgets.QHBoxLayout()
        hlog.addWidget(self.logx); hlog.addWidget(self.logy); hlog.addStretch(1)
        fx.addRow(hlog)
        btn_reset = QtWidgets.QPushButton("Reset to recommended")
        btn_reset.setMinimumHeight(28)
        btn_reset.clicked.connect(self._reset_axes)
        fx.addRow(btn_reset)
        gb_axes_outer.addWidget(self._axes_body)

        self.gb_axes.toggled.connect(self._toggle_axis_box)
        pl.addWidget(self.gb_axes)
        self._toggle_axis_box(False)

        # Primary action
        self.btn_plot = QtWidgets.QPushButton("Update plot")
        self.btn_plot.setObjectName("primary")
        self.btn_plot.setMinimumHeight(38)
        self.btn_plot.clicked.connect(self.update_plot)
        pl.addWidget(self.btn_plot)

        # Secondary actions, two rows of two
        h2 = QtWidgets.QHBoxLayout(); h2.setSpacing(8)
        self.btn_save = QtWidgets.QPushButton("Save figure…")
        self.btn_export = QtWidgets.QPushButton("Export data…")
        self.btn_save.clicked.connect(self.save_figure)
        self.btn_export.clicked.connect(self.export_data)
        for b in (self.btn_save, self.btn_export):
            b.setMinimumHeight(30); h2.addWidget(b)
        pl.addLayout(h2)

        h3 = QtWidgets.QHBoxLayout(); h3.setSpacing(8)
        self.btn_open = QtWidgets.QPushButton("Open database…")
        self.btn_help = QtWidgets.QPushButton("Help")
        self.btn_open.clicked.connect(self.open_db)
        self.btn_help.clicked.connect(self.show_help)
        for b in (self.btn_open, self.btn_help):
            b.setMinimumHeight(30); h3.addWidget(b)
        pl.addLayout(h3)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(panel)
        scroll.setWidgetResizable(True)
        scroll.setFixedWidth(370)
        scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        root.addWidget(scroll)

        # Right: tabs
        self.tabs = QtWidgets.QTabWidget()
        plot_tab = QtWidgets.QWidget()
        pv = QtWidgets.QVBoxLayout(plot_tab)
        self.canvas = SpectrumCanvas(plot_tab)
        self.toolbar = NavigationToolbar(self.canvas, plot_tab)
        pv.addWidget(self.toolbar)
        pv.addWidget(self.canvas, stretch=1)
        self.tabs.addTab(plot_tab, "Plot")

        table_tab = QtWidgets.QWidget()
        tv = QtWidgets.QVBoxLayout(table_tab)
        self.table = QtWidgets.QTableWidget()
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        tv.addWidget(self.table)
        self.tabs.addTab(table_tab, "Data table")

        root.addWidget(self.tabs, stretch=1)
        self.status = self.statusBar()

        # live-update signals
        self.theta_lo.valueChanged.connect(self._on_theta_changed)
        self.theta_hi.valueChanged.connect(self._on_theta_changed)
        self.err_combo.currentIndexChanged.connect(self.update_plot)
        self.logx.toggled.connect(self.update_plot)
        self.logy.toggled.connect(self.update_plot)

    def _toggle_axis_box(self, on):
        #Collapse the axis box to just its title bar by hiding the whole body widget
        self._axes_body.setVisible(on)
        self.gb_axes.setMaximumHeight(16777215 if on else 40)

    # ---- DATABASE --------------------------------------------------------------
    def _load_db(self, path):
        try:
            self.data = MuonData(path)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Database error", str(e))
            return
        self.db_path = path
        self.setWindowTitle(f"Muon Spectrum Viewer - {os.path.basename(path)}")
        self._build_tree()
        self.update_plot()

    def _build_tree(self):
        self.tree.blockSignals(True)
        self.tree.clear()
        lo, hi = self.theta_lo.value(), self.theta_hi.value()
        for exp in self.data.experiments:
            angles = [a for a in self.data.angles(exp) if lo <= a <= hi]
            if not angles:
                continue
            npts_exp = sum(len(self.data.by_exp_theta[exp][a]) for a in angles)
            parent = QtWidgets.QTreeWidgetItem([f"{exp}", str(npts_exp)])
            parent.setFlags(parent.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable
                            | QtCore.Qt.ItemFlag.ItemIsAutoTristate)
            parent.setCheckState(0, QtCore.Qt.CheckState.Checked)
            parent.setForeground(0, QtGui.QBrush(QtGui.QColor(self.data.color_of[exp])))
            f = parent.font(0); f.setBold(True); parent.setFont(0, f)
            parent.setData(0, QtCore.Qt.ItemDataRole.UserRole, ("exp", exp, None))
            for a in angles:
                n = len(self.data.by_exp_theta[exp][a])
                child = QtWidgets.QTreeWidgetItem([f"θ = {a:g}°", str(n)])
                child.setFlags(child.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
                child.setCheckState(0, QtCore.Qt.CheckState.Checked)
                child.setData(0, QtCore.Qt.ItemDataRole.UserRole, ("angle", exp, a))
                parent.addChild(child)
            self.tree.addTopLevelItem(parent)
        self.tree.expandAll()
        self.tree.blockSignals(False)

    # ---- events ----------------------------------------------------------
    def _on_theta_changed(self):
        if self.theta_lo.value() > self.theta_hi.value():
            self.theta_hi.setValue(self.theta_lo.value())
        self._build_tree()
        self.update_plot()

    def _on_tree_changed(self, item, col):
        if not self._plot_update_pending:
            self._plot_update_pending = True
            QtCore.QTimer.singleShot(0, self._flush_plot_update)

    def _flush_plot_update(self):
        self._plot_update_pending = False
        self.update_plot()

    def _set_all(self, checked):
        self.tree.blockSignals(True)
        state = QtCore.Qt.CheckState.Checked if checked else QtCore.Qt.CheckState.Unchecked
        for i in range(self.tree.topLevelItemCount()):
            top = self.tree.topLevelItem(i)
            top.setCheckState(0, state)
            for j in range(top.childCount()):
                top.child(j).setCheckState(0, state)
        self.tree.blockSignals(False)
        self.update_plot()

    def _reset_axes(self):
        self.xmin.setValue(RECOMMENDED_X[0]); self.xmax.setValue(RECOMMENDED_X[1])
        self.ymin.setValue(RECOMMENDED_Y[0]); self.ymax.setValue(RECOMMENDED_Y[1])
        self.update_plot()

    # ---- selection -------------------------------------------------------
    def _selected_angles(self):
        #Return {exp: set(theta)} for every ticked angle child.
        out: dict[str, set] = {}
        for i in range(self.tree.topLevelItemCount()):
            top = self.tree.topLevelItem(i)
            for j in range(top.childCount()):
                child = top.child(j)
                if child.checkState(0) == QtCore.Qt.CheckState.Checked:
                    kind, exp, a = child.data(0, QtCore.Qt.ItemDataRole.UserRole)
                    out.setdefault(exp, set()).add(a)
        return out

    # ---- plot ------------------------------------------------------------
    def update_plot(self):
        if not self.data:
            return
        err_attr = {"total_error": "total", "stat_error": "stat",
                    "sys_error": "sys"}[ERROR_CHOICES[self.err_combo.currentText()]]
        sel = self._selected_angles()

        series = []
        table_rows = []
        for exp in self.data.experiments:
            angles = sorted(sel.get(exp, []))
            if not angles:
                continue
            pts = []
            for a in angles:
                pts.extend(self.data.by_exp_theta[exp][a])
            if not pts:
                continue
            pts.sort(key=lambda p: p.momentum)
            x = np.array([p.momentum for p in pts])
            y = np.array([p.intensity for p in pts])
            xerr = np.array([p.xerr for p in pts])
            yerr = np.array([getattr(p, err_attr) for p in pts])
            series.append((exp, self.data.color_of[exp], self.data.marker_of[exp],
                           x, y, xerr, yerr))
            for p in pts:
                table_rows.append([
                    exp, f"{p.theta:g}", f"{p.momentum:.4g}",
                    f"{p.xerr:.4g}" if p.xerr else "—",
                    f"{p.intensity:.4e}",
                    f"{p.stat:.3e}" if p.stat else "—",
                    f"{p.sys:.3e}" if p.sys else "—",
                    f"{p.total:.3e}" if p.total else "—",
                ])

        xlim = (self.xmin.value(), self.xmax.value())
        ylim = (self.ymin.value(), self.ymax.value())
        self.canvas.draw_spectrum(
            series, xlim, ylim, err_attr,
            self.theta_lo.value(), self.theta_hi.value(),
            logx=self.logx.isChecked(), logy=self.logy.isChecked(),
        )
        self._fill_table(table_rows)

        npts = sum(len(s[3]) for s in series)
        self.status.showMessage(
            f"θ = {self.theta_lo.value():g}–{self.theta_hi.value():g}°   |   "
            f"{len(series)} experiment(s), {npts} points shown"
        )

    def _fill_table(self, rows):
        cols = ["Experiment", "θ (deg)", "p (GeV/c)", "p half-width",
                "Intensity", "Stat err", "Sys err", "Total err"]
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.table.setItem(r, c, QtWidgets.QTableWidgetItem(val))
        self.table.resizeColumnsToContents()

    # ---- export / help ---------------------------------------------------
    def save_figure(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save figure", "muon_spectrum.svg",
            "SVG (*.svg);;PNG (*.png);;PDF (*.pdf)")
        if not path:
            return
        self.canvas.fig.savefig(path, dpi=600, bbox_inches="tight")
        self.status.showMessage(f"Figure saved: {path}", 5000)

    def export_data(self):
        if self.table.rowCount() == 0:
            QtWidgets.QMessageBox.warning(self, "No data", "Nothing to export.")
            return
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export data", "muon_data_export.csv",
            "CSV (*.csv);;Text (*.txt)")
        if not path:
            return
        # UTF-8 with BOM so it opens cleanly in Excel on Windows
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            headers = [self.table.horizontalHeaderItem(c).text()
                       for c in range(self.table.columnCount())]
            f.write(",".join(headers) + "\n")
            for r in range(self.table.rowCount()):
                vals = [self.table.item(r, c).text().replace("—", "")
                        for c in range(self.table.columnCount())]
                f.write(",".join(vals) + "\n")
        self.status.showMessage(f"Data exported: {path}", 5000)

    def open_db(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open database", "", "SQLite DB (*.db);;All files (*)")
        if path:
            self._load_db(path)

    def show_help(self):
        dlg = QtWidgets.QDialog(self)
        dlg.setWindowTitle("Instructions")
        dlg.resize(560, 480)
        v = QtWidgets.QVBoxLayout(dlg)
        txt = QtWidgets.QTextEdit(); txt.setReadOnly(True)
        txt.setStyleSheet("background:#ffffff; color:#1c2530; border:1px solid #d3dae4;")
        txt.setHtml("""
        <h3>Parameter selection</h3>
        <p><b>Zenith angle window (&theta;)</b> &mdash; degrees. Filters the
        experiment&rarr;angle tree to angles within [Min &theta;, Max &theta;].
        0&deg; = vertical, 90&deg; = horizontal.</p>
        <p><b>Experiments &rarr; angles tree</b> &mdash; each experiment expands
        to the individual zenith angles it provides, with the point count beside
        each. Tick a whole experiment, or expand it and tick individual angles.
        Only ticked angles are plotted and tabulated.</p>
        <p><b>X-axis (momentum)</b> &mdash; GeV/c. <b>Y-axis (intensity)</b>
        &mdash; (cm&sup2;&middot;s&middot;sr&middot;GeV/c)&#8315;&sup1;. Log X /
        Log Y toggle the scales. Axis ranges are in the collapsible
        &ldquo;Axis ranges&rdquo; box.</p>
        <p><b>Error bars</b> &mdash; choose Total (stat&oplus;sys), Statistical
        only, or Systematic only. Points whose source gives only a mean momentum
        have no horizontal bar (shown as &ldquo;&mdash;&rdquo;, not &plusmn;0).</p>
        <h3>Buttons</h3>
        <p><b>Update plot</b> redraws. <b>Save figure</b> exports SVG/PNG/PDF.
        <b>Export data</b> writes the current table to CSV (UTF-8 BOM, opens
        cleanly in Excel). <b>Open database</b> loads a different .db.</p>
        <p>The toolbar above the plot gives pan / zoom / save.</p>
        """)
        v.addWidget(txt)
        btn = QtWidgets.QPushButton("Close"); btn.clicked.connect(dlg.accept)
        v.addWidget(btn)
        dlg.exec()


# ---------------------------------------------------------------------------
# spin box for log axis limits
# ---------------------------------------------------------------------------
class _SciSpin(QtWidgets.QDoubleSpinBox):
    def __init__(self, value):
        super().__init__()
        self.setDecimals(0)
        self.setRange(-1e30, 1e30)
        self.setValue(value)

    def textFromValue(self, v):
        return "0" if v == 0 else f"{v:.0e}"

    def valueFromText(self, text):
        try:
            return float(text)
        except ValueError:
            return self.value()

    def validate(self, text, pos):
        return (QtGui.QValidator.State.Acceptable, text, pos)

    def stepBy(self, steps):
        v = self.value() or 1.0
        self.setValue(v * (10.0 ** steps))


def main():
    db = DEFAULT_DB
    if len(sys.argv) > 1:
        db = sys.argv[1]
    elif not os.path.exists(db):
        here = os.path.dirname(os.path.abspath(__file__))
        cand = os.path.join(here, DEFAULT_DB)
        if os.path.exists(cand):
            db = cand

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(DARK_QSS)
    win = MainWindow(db)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()