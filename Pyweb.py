import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class BrowserTab(QWidget):
    def __init__(self, url="http://google.com", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Browser view
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))
        layout.addWidget(self.browser)

        # Navigation bar
        nav_bar = QToolBar()
        layout.addWidget(nav_bar)

        back_btn = QAction("⬅ Back", self)
        back_btn.triggered.connect(self.browser.back)
        nav_bar.addAction(back_btn)

        forward_btn = QAction("➡ Forward", self)
        forward_btn.triggered.connect(self.browser.forward)
        nav_bar.addAction(forward_btn)

        reload_btn = QAction("🔄 Reload", self)
        reload_btn.triggered.connect(self.browser.reload)
        nav_bar.addAction(reload_btn)

        home_btn = QAction("🏠 Home", self)
        home_btn.triggered.connect(lambda: self.browser.setUrl(QUrl("http://google.com")))
        nav_bar.addAction(home_btn)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL and press Enter")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Pyweb")
        self.setGeometry(100, 100, 800, 600)

        # Tabs Widget
        self.tabs = QTabWidget()

        self.tabs.tabCloseRequested.connect(self.close_tab)

        # **Enable Right-Click Context Menu for Renaming Tabs**
        self.tabs.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabs.customContextMenuRequested.connect(self.rename_tab)

        self.setCentralWidget(self.tabs)

        # Navigation bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        new_tab_btn = QAction("➕ New Tab", self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab())
        navbar.addAction(new_tab_btn)

        self.showMaximized()
        self.is_fullscreen = False
        self.installEventFilter(self)

        # Create initial tab
        self.add_new_tab("http://google.com", "New Tab")

    def add_new_tab(self, url="http://google.com", title="New Tab"):
        new_tab = BrowserTab(url, self)
        self.tabs.addTab(new_tab, title)

    def close_tab(self, index):
        if self.tabs.count() > 1:  # Prevent closing last tab
            self.tabs.removeTab(index)

    def rename_tab(self, pos):
        index = self.tabs.tabBar().tabAt(pos)
        if index != -1:  # Valid tab clicked
            text, ok = QInputDialog.getText(self, "Rename Tab", "Enter new tab name:")
            if ok and text.strip():
                self.tabs.setTabText(index, text.strip())  # Set custom tab name

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_F11:
            if self.is_fullscreen:
                self.showMaximized()
            else:
                self.showFullScreen()
            self.is_fullscreen = not self.is_fullscreen
            return True
        return super().eventFilter(source, event)

app = QApplication(sys.argv)
QApplication.setApplicationName("Pyweb")
window = MainWindow()
window.show()
sys.exit(app.exec_())

