"""Main GUI application for Recall."""
import sys
import os
import json
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout
from settings_dialog import SettingsDialog
from sidebar import Sidebar
from chat_area import ChatArea

SETTINGS_FILE = "settings.json"

class ChatGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recall")
        self.resize(900, 700)
        self.setAcceptDrops(True)
        
        # Set window background
        self.setStyleSheet("QWidget { background-color: #f8f9fa; }")

        # Light/Dark mode flag
        self.light_mode = False  # default to dark mode

        # Default settings
        self.model = "llama3"
        self.api_url = "http://localhost:11434"
        self.max_history = 5
        self.summary_threshold = 20
        self.enable_summarization = True
        self.temperature = 0.7
        self.top_p = 0.9
        self.max_tokens = 0
        self.agent_prompt_name = "none"
        self.agent_prompt = ""

        # Load settings.json if it exists
        self._load_settings()
        self._load_agent_prompt()

        # Current session
        self.current_session = "default"

        # Main layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Sidebar
        self.sidebar = Sidebar(self)
        main_layout.addLayout(self.sidebar.layout, 1)

        # Chat area
        self.chat_area = ChatArea(self)
        main_layout.addLayout(self.chat_area.layout, 4)
        
        # Apply initial theme
        self._update_window_theme()

    def _load_settings(self):
        """Load settings from settings.json."""
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    self.model = settings.get("model", self.model)
                    self.api_url = settings.get("api_url", self.api_url)
                    self.max_history = settings.get("max_history", self.max_history)
                    self.summary_threshold = settings.get("summary_threshold", self.summary_threshold)
                    self.enable_summarization = settings.get("enable_summarization", self.enable_summarization)
                    self.temperature = settings.get("temperature", self.temperature)
                    self.top_p = settings.get("top_p", self.top_p)
                    self.max_tokens = settings.get("max_tokens", self.max_tokens)
                    self.agent_prompt_name = settings.get("agent_prompt_name", self.agent_prompt_name)
                    self.light_mode = settings.get("light_mode", self.light_mode)
            except json.JSONDecodeError as e:
                print(f"JSON decode error loading settings: {e}")
            except Exception as e:
                print(f"Error loading settings: {e}")

    def _load_agent_prompt(self):
        """Load agent prompt from prompts directory."""
        prompt_file = os.path.join("prompts", f"{self.agent_prompt_name}.txt")
        if os.path.exists(prompt_file):
            try:
                with open(prompt_file, "r", encoding="utf-8") as f:
                    self.agent_prompt = f.read().strip()
            except Exception as e:
                print(f"Error loading agent prompt: {e}")

    def open_settings(self):
        """Open settings dialog."""
        dlg = SettingsDialog(self)
        if dlg.exec():
            # Reload agent prompt after settings change
            self._load_agent_prompt()

    def load_session_chat(self, session=None):
        """Load chat for specified session."""
        self.chat_area.load_session_chat(session)
    
    def _update_window_theme(self):
        """Update main window background color based on theme."""
        if self.light_mode:
            self.setStyleSheet("QWidget { background-color: #f8f9fa; }")
        else:
            self.setStyleSheet("QWidget { background-color: #1a1a1a; }")

    # Drag and drop events to attach files
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isfile(file_path):
                self.chat_area.dropped_files.append(file_path)
        if self.chat_area.dropped_files:
            file_names = ", ".join(os.path.basename(f) for f in self.chat_area.dropped_files)
            current_text = self.chat_area.input_box.text()
            if current_text:
                self.chat_area.input_box.setText(current_text + f" [Attached: {file_names}]")
            else:
                self.chat_area.input_box.setText(f"[Attached: {file_names}]")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatGUI()
    window.show()
    sys.exit(app.exec())
