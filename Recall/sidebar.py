"""Sidebar widget for session management and settings."""
import os
import re
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QListWidget, QMenu, QMessageBox, QInputDialog
from PySide6.QtCore import Qt

class Sidebar:
    def __init__(self, parent):
        self.parent = parent
        self.layout = QVBoxLayout()
        self.layout.setSpacing(5)

        # New Chat button
        self.new_chat_button = QPushButton("+ New Chat")
        self.new_chat_button.clicked.connect(self.create_new_chat)
        self.layout.addWidget(self.new_chat_button)

        # Session list
        self.session_list = QListWidget()
        self.session_list.setStyleSheet("font-size:16px;")
        self.session_list.itemClicked.connect(self.change_session)
        self.session_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.session_list.customContextMenuRequested.connect(self.show_session_menu)
        self.layout.addWidget(QLabel("Sessions"))
        self.layout.addWidget(self.session_list)

        # Settings button
        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.parent.open_settings)
        self.layout.addWidget(self.settings_button)

        # Light/Dark Mode toggle button at bottom
        self.theme_button = QPushButton("Light Mode")
        self.theme_button.clicked.connect(self.toggle_theme)
        self.layout.addWidget(self.theme_button, alignment=Qt.AlignRight)

        self.load_sessions()
        self.update_theme()

    def load_sessions(self):
        self.session_list.clear()
        for file in os.listdir("."):
            if file.startswith("memory_") and file.endswith(".json"):
                session_name = file[len("memory_"):-5]
                self.session_list.addItem(session_name)
        if self.session_list.count() == 0:
            self.session_list.addItem("default")

    def create_new_chat(self):
        """Create a new chat session."""
        name, ok = QInputDialog.getText(self.parent, "New Chat", "Enter new chat name:")
        if ok and name:
            # Sanitize session name
            name = re.sub(r'[<>:"/\\|?*]', '_', name).strip()
            if not name:
                QMessageBox.warning(self.parent, "Invalid Name", "Session name cannot be empty.")
                return
            if not any(self.session_list.item(i).text() == name for i in range(self.session_list.count())):
                self.session_list.addItem(name)
                self.parent.load_session_chat(name)
            else:
                QMessageBox.warning(self.parent, "Duplicate Name", "A session with this name already exists.")

    def change_session(self, item):
        self.parent.load_session_chat(item.text())

    def show_session_menu(self, pos):
        item = self.session_list.itemAt(pos)
        if item:
            menu = QMenu()
            delete_action = menu.addAction("Delete Session")
            rename_action = menu.addAction("Rename Session")
            action = menu.exec(self.session_list.mapToGlobal(pos))
            if action == delete_action:
                reply = QMessageBox.question(self.parent, "Confirm Delete",
                                             f"Delete session '{item.text()}'?",
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    try:
                        os.remove(f"memory_{item.text()}.json")
                    except FileNotFoundError:
                        pass
                    self.load_sessions()
                    self.parent.load_session_chat("default")
            elif action == rename_action:
                new_name, ok = QInputDialog.getText(self.parent, "Rename Chat", "New name:", text=item.text())
                if ok and new_name:
                    # Sanitize session name
                    new_name = re.sub(r'[<>:"/\\|?*]', '_', new_name).strip()
                    if not new_name:
                        QMessageBox.warning(self.parent, "Invalid Name", "Session name cannot be empty.")
                        return
                    if any(self.session_list.item(i).text() == new_name for i in range(self.session_list.count())):
                        QMessageBox.warning(self.parent, "Duplicate Name", "A session with this name already exists.")
                        return
                    old_file = f"memory_{item.text()}.json"
                    new_file = f"memory_{new_name}.json"
                    try:
                        if os.path.exists(old_file):
                            os.rename(old_file, new_file)
                        item.setText(new_name)
                        self.parent.load_session_chat(new_name)
                    except Exception as e:
                        QMessageBox.critical(self.parent, "Rename Error", f"Failed to rename session: {e}")

    def toggle_theme(self):
        self.parent.light_mode = not getattr(self.parent, "light_mode", False)
        self.update_theme()
        self.parent.chat_area.update_theme(self.parent.light_mode)
        self.parent._update_window_theme()

    def update_theme(self):
        if getattr(self.parent, "light_mode", False):
            # Light theme - modern, clean design
            self.session_list.setStyleSheet("""
                QListWidget {
                    font-size: 16px;
                    background-color: #ffffff;
                    color: #1a1a1a;
                    border: 1px solid #d0d0d0;
                    border-radius: 4px;
                    padding: 4px;
                }
                QListWidget::item {
                    padding: 8px;
                    border-radius: 4px;
                    margin: 2px;
                }
                QListWidget::item:hover {
                    background-color: #f0f0f0;
                }
                QListWidget::item:selected {
                    background-color: #e3f2fd;
                    color: #1565c0;
                }
            """)
            button_style = """
                QPushButton {
                    background-color: #f8f9fa;
                    color: #1a1a1a;
                    font-size: 14px;
                    border: 1px solid #c0c0c0;
                    border-radius: 4px;
                    padding: 8px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #e9ecef;
                    border: 1px solid #0078d4;
                }
                QPushButton:pressed {
                    background-color: #dee2e6;
                }
            """
            self.new_chat_button.setStyleSheet(button_style)
            self.settings_button.setStyleSheet(button_style)
            self.theme_button.setStyleSheet(button_style)
            self.theme_button.setText("Dark Mode")
        else:
            # Dark theme
            self.session_list.setStyleSheet("""
                QListWidget {
                    font-size: 16px;
                    background-color: #1e1e1e;
                    color: #ffffff;
                    border: 1px solid #3a3a3a;
                    border-radius: 4px;
                    padding: 4px;
                }
                QListWidget::item {
                    padding: 8px;
                    border-radius: 4px;
                    margin: 2px;
                }
                QListWidget::item:hover {
                    background-color: #2a2a2a;
                }
                QListWidget::item:selected {
                    background-color: #1a3a52;
                    color: #b3d9ff;
                }
            """)
            button_style = """
                QPushButton {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    font-size: 14px;
                    border: 1px solid #4a4a4a;
                    border-radius: 4px;
                    padding: 8px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #3a3a3a;
                    border: 1px solid #0078d4;
                }
                QPushButton:pressed {
                    background-color: #262626;
                }
            """
            self.new_chat_button.setStyleSheet(button_style)
            self.settings_button.setStyleSheet(button_style)
            self.theme_button.setStyleSheet(button_style)
            self.theme_button.setText("Light Mode")
