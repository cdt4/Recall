"""Settings dialog for configuring model parameters and agent prompts."""
import os
import json
from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QSpinBox, QPushButton, 
    QComboBox, QCheckBox, QLabel, QDoubleSpinBox, QGroupBox, QVBoxLayout
)

PROMPT_DIR = "prompts"
SETTINGS_FILE = "settings.json"

class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.parent = parent
        self.setMinimumWidth(400)
        
        # Apply theme-appropriate styling
        self._apply_theme()
        
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Model Settings Group
        model_group = QGroupBox("Model Settings")
        model_layout = QFormLayout()
        model_group.setLayout(model_layout)
        
        self.model_input = QLineEdit()
        self.model_input.setText(parent.model)
        self.model_input.setPlaceholderText("e.g., llama3, mistral, gemma3:4b")
        model_layout.addRow("Model:", self.model_input)
        
        self.api_url_input = QLineEdit()
        self.api_url_input.setText(getattr(parent, 'api_url', 'http://localhost:11434'))
        self.api_url_input.setPlaceholderText("http://localhost:11434")
        model_layout.addRow("API URL:", self.api_url_input)
        
        main_layout.addWidget(model_group)
        
        # Memory Settings Group
        memory_group = QGroupBox("Memory Settings")
        memory_layout = QFormLayout()
        memory_group.setLayout(memory_layout)
        
        self.max_history_input = QSpinBox()
        self.max_history_input.setRange(1, 100)
        self.max_history_input.setValue(parent.max_history)
        memory_layout.addRow("Max History:", self.max_history_input)
        
        self.summary_threshold_input = QSpinBox()
        self.summary_threshold_input.setRange(5, 200)
        self.summary_threshold_input.setValue(parent.summary_threshold)
        memory_layout.addRow("Summary Threshold:", self.summary_threshold_input)
        
        self.enable_summarization = QCheckBox()
        self.enable_summarization.setChecked(getattr(parent, 'enable_summarization', True))
        memory_layout.addRow("Enable Auto-Summarization:", self.enable_summarization)
        
        main_layout.addWidget(memory_group)
        
        # Agent Settings Group
        agent_group = QGroupBox("Agent Settings")
        agent_layout = QFormLayout()
        agent_group.setLayout(agent_layout)
        
        self.agent_prompt_selector = QComboBox()
        self.prompts = self.load_prompts()
        self.prompts["none"] = ""
        for name in sorted(self.prompts.keys()):
            self.agent_prompt_selector.addItem(name)
        if parent.agent_prompt_name in self.prompts:
            self.agent_prompt_selector.setCurrentText(parent.agent_prompt_name)
        agent_layout.addRow("Agent Preset:", self.agent_prompt_selector)
        
        main_layout.addWidget(agent_group)
        
        # Generation Settings Group
        gen_group = QGroupBox("Generation Settings")
        gen_layout = QFormLayout()
        gen_group.setLayout(gen_layout)
        
        self.temperature_input = QDoubleSpinBox()
        self.temperature_input.setRange(0.0, 2.0)
        self.temperature_input.setSingleStep(0.1)
        self.temperature_input.setValue(getattr(parent, 'temperature', 0.7))
        gen_layout.addRow("Temperature:", self.temperature_input)
        
        self.top_p_input = QDoubleSpinBox()
        self.top_p_input.setRange(0.0, 1.0)
        self.top_p_input.setSingleStep(0.05)
        self.top_p_input.setValue(getattr(parent, 'top_p', 0.9))
        gen_layout.addRow("Top P:", self.top_p_input)
        
        self.max_tokens_input = QSpinBox()
        self.max_tokens_input.setRange(0, 32000)
        self.max_tokens_input.setValue(getattr(parent, 'max_tokens', 0))
        self.max_tokens_input.setSpecialValueText("unlimited")
        gen_layout.addRow("Max Tokens:", self.max_tokens_input)
        
        main_layout.addWidget(gen_group)
        
        # Buttons
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        main_layout.addWidget(save_button)

    def load_prompts(self):
        """Load all available agent prompts from prompts directory."""
        prompts = {}
        if not os.path.exists(PROMPT_DIR):
            os.makedirs(PROMPT_DIR)
        try:
            for file in os.listdir(PROMPT_DIR):
                if file.endswith(".txt"):
                    name = file[:-4]
                    path = os.path.join(PROMPT_DIR, file)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            prompts[name] = f.read().strip()
                    except Exception as e:
                        print(f"Error loading prompt {file}: {e}")
        except Exception as e:
            print(f"Error reading prompts directory: {e}")
        return prompts
    
    def _apply_theme(self):
        """Apply theme styling to dialog."""
        if getattr(self.parent, 'light_mode', False):
            self.setStyleSheet("""
                QDialog {
                    background-color: #f8f9fa;
                }
                QGroupBox {
                    font-weight: bold;
                    border: 1px solid #d0d0d0;
                    border-radius: 4px;
                    margin-top: 8px;
                    padding-top: 10px;
                    background-color: #ffffff;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }
                QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                    background-color: #ffffff;
                    color: #1a1a1a;
                    border: 1px solid #c0c0c0;
                    border-radius: 4px;
                    padding: 4px;
                }
                QLabel {
                    color: #1a1a1a;
                }
                QPushButton {
                    background-color: #f8f9fa;
                    color: #1a1a1a;
                    border: 1px solid #c0c0c0;
                    border-radius: 4px;
                    padding: 8px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #e9ecef;
                    border: 1px solid #0078d4;
                }
            """)
        else:
            self.setStyleSheet("""
                QDialog {
                    background-color: #1a1a1a;
                }
                QGroupBox {
                    font-weight: bold;
                    border: 1px solid #3a3a3a;
                    border-radius: 4px;
                    margin-top: 8px;
                    padding-top: 10px;
                    background-color: #1e1e1e;
                    color: #ffffff;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }
                QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                    background-color: #2e2e2e;
                    color: #ffffff;
                    border: 1px solid #4a4a4a;
                    border-radius: 4px;
                    padding: 4px;
                }
                QLabel {
                    color: #ffffff;
                }
                QPushButton {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    border: 1px solid #4a4a4a;
                    border-radius: 4px;
                    padding: 8px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #3a3a3a;
                    border: 1px solid #0078d4;
                }
            """)
    
    def save_settings(self):
        """Save settings to file and update parent."""
        self.parent.model = self.model_input.text().strip() or "llama3"
        self.parent.api_url = self.api_url_input.text().strip() or "http://localhost:11434"
        self.parent.max_history = self.max_history_input.value()
        self.parent.summary_threshold = self.summary_threshold_input.value()
        self.parent.enable_summarization = self.enable_summarization.isChecked()
        self.parent.temperature = self.temperature_input.value()
        self.parent.top_p = self.top_p_input.value()
        self.parent.max_tokens = self.max_tokens_input.value()
        
        selected_name = self.agent_prompt_selector.currentText()
        self.parent.agent_prompt_name = selected_name
        self.parent.agent_prompt = self.prompts.get(selected_name, "")

        settings = {
            "model": self.parent.model,
            "api_url": self.parent.api_url,
            "max_history": self.parent.max_history,
            "summary_threshold": self.parent.summary_threshold,
            "enable_summarization": self.parent.enable_summarization,
            "temperature": self.parent.temperature,
            "top_p": self.parent.top_p,
            "max_tokens": self.parent.max_tokens,
            "agent_prompt_name": self.parent.agent_prompt_name,
            "light_mode": self.parent.light_mode
        }
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
        self.accept()

