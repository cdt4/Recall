"""Chat area widget for displaying conversation and handling user input."""
from PySide6.QtWidgets import QVBoxLayout, QTextEdit, QLineEdit
from main import chat_with_memory, load_memory
import os
import html

class ChatArea:
    def __init__(self, parent):
        self.parent = parent
        self.layout = QVBoxLayout()

        # Chat display
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.layout.addWidget(self.chat_area)

        # Input box
        self.input_box = QLineEdit()
        self.input_box.returnPressed.connect(self.send_message)
        self.layout.addWidget(self.input_box)

        # Files dropped to attach
        self.dropped_files = []

        # Initialize theme
        self.update_theme(self.parent.light_mode)

    def update_theme(self, light_mode: bool):
        """Update colors for light or dark mode"""
        if light_mode:
            self.chat_area.setStyleSheet("""
                QTextEdit {
                    font-size: 16px;
                    background-color: #ffffff;
                    color: #1a1a1a;
                    border: 1px solid #d0d0d0;
                    border-radius: 4px;
                    padding: 8px;
                }
            """)
            self.input_box.setStyleSheet("""
                QLineEdit {
                    font-size: 16px;
                    background-color: #ffffff;
                    color: #1a1a1a;
                    border: 2px solid #c0c0c0;
                    border-radius: 4px;
                    padding: 8px;
                }
                QLineEdit:focus {
                    border: 2px solid #0078d4;
                }
            """)
        else:
            self.chat_area.setStyleSheet("""
                QTextEdit {
                    font-size: 16px;
                    background-color: #1e1e1e;
                    color: #ffffff;
                    border: 1px solid #3a3a3a;
                    border-radius: 4px;
                    padding: 8px;
                }
            """)
            self.input_box.setStyleSheet("""
                QLineEdit {
                    font-size: 16px;
                    background-color: #2e2e2e;
                    color: #ffffff;
                    border: 2px solid #4a4a4a;
                    border-radius: 4px;
                    padding: 8px;
                }
                QLineEdit:focus {
                    border: 2px solid #0078d4;
                }
            """)

    def load_session_chat(self, session=None):
        """Load and display chat history for a session."""
        if session:
            self.parent.current_session = session
        self.chat_area.clear()
        memory = load_memory(self.parent.current_session)
        for m in memory:
            role = m.get('role', 'unknown').capitalize()
            content = html.escape(m.get('content', ''))
            
            if self.parent.light_mode:
                role_color = "#1565c0" if role == 'User' else "#2c2c2c"
                text_color = "#1a1a1a"
            else:
                role_color = "#66b3ff" if role == 'User' else "#ffffff"
                text_color = "#e0e0e0"
            
            if role == 'User':
                self.chat_area.append(f'<div style="text-align:right; margin-bottom:16px;"><b style="color:{role_color};">{role}:</b> <span style="color:{text_color};">{content}</span></div>')
            else:
                self.chat_area.append(f'<div style="text-align:left; margin-bottom:16px; margin-right:auto;"><b style="color:{role_color};">{role}:</b> <span style="color:{text_color};">{content}</span></div>')
        self.chat_area.verticalScrollBar().setValue(self.chat_area.verticalScrollBar().maximum())

    def send_message(self):
        """Handle sending user message and getting AI response."""
        user_text = self.input_box.text().strip()
        if not user_text and not self.dropped_files:
            return

        # Display user message
        display_text = html.escape(user_text)
        if self.dropped_files:
            display_text += " [Attached: " + html.escape(", ".join(os.path.basename(f) for f in self.dropped_files)) + "]"
        
        if self.parent.light_mode:
            role_color = "#1565c0"
            text_color = "#1a1a1a"
        else:
            role_color = "#66b3ff"
            text_color = "#e0e0e0"
        
        self.chat_area.append(f'<div style="text-align:right; margin-bottom:16px;"><b style="color:{role_color};">You:</b> <span style="color:{text_color};">{display_text}</span></div>')
        self.input_box.clear()

        # Combine file contents
        combined_input = user_text
        for file_path in self.dropped_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
                    combined_input += f"\n\n--- File: {os.path.basename(file_path)} ---\n{file_content}"
            except UnicodeDecodeError:
                self.chat_area.append(f'<div style="color:red;"><b>Error:</b> Cannot read binary file {os.path.basename(file_path)}</div>')
            except Exception as e:
                self.chat_area.append(f'<div style="color:red;"><b>Error reading file:</b> {html.escape(str(e))}</div>')
        self.dropped_files = []

        # Generate AI response (agent_prompt is passed correctly now)
        assistant_reply = chat_with_memory(
            combined_input,
            self.parent.current_session,
            model=self.parent.model,
            max_history=self.parent.max_history,
            summary_threshold=self.parent.summary_threshold,
            agent_prompt=self.parent.agent_prompt
        )

        # Display assistant message
        if self.parent.light_mode:
            role_color = "#2c2c2c"
            text_color = "#1a1a1a"
        else:
            role_color = "#ffffff"
            text_color = "#e0e0e0"
        
        self.chat_area.append(f'<div style="text-align:left; margin-bottom:16px; margin-right:auto;"><b style="color:{role_color};">Assistant:</b> <span style="color:{text_color};">{html.escape(assistant_reply)}</span></div>')
        self.chat_area.verticalScrollBar().setValue(self.chat_area.verticalScrollBar().maximum())
