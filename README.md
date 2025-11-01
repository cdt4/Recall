# Recall

A clean, desktop chat interface for Ollama with persistent conversation memory and session management.

Recall provides a lightweight GUI to interact with local LLM models through Ollama, with the unique ability to maintain conversation context across sessions. Each chat is automatically saved, allowing you to pick up conversations exactly where you left off.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.5+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features

- **Session-Based Memory** - Each conversation is saved automatically and can be resumed anytime
- **Multiple Chat Sessions** - Create, rename, and delete separate conversation threads
- **Light & Dark Themes** - Choose your preferred visual style
- **File Drag & Drop** - Include text file contents directly in your messages
- **Customizable Agent Prompts** - Define different AI personalities for different use cases
- **Smart Context Management** - Auto-summarization keeps conversations performant as they grow
- **Advanced Model Settings** - Fine-tune temperature, top_p, token limits, and context window size
- **Local & Private** - All conversations stay on your machine using Ollama

## Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and running locally
- At least one Ollama model downloaded (e.g., `ollama pull llama3`)

## Installation

1. **Clone or download this repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure Ollama is running**
   ```bash
   ollama serve
   ```

4. **Download a model (if not already done)**
   ```bash
   ollama pull llama3
   ```

## Usage

### Starting the Application

```bash
python gui.py
```

### Basic Operations

- **New Chat**: Click the "+ New Chat" button to create a new conversation session
- **Switch Sessions**: Click on any session name in the sidebar to switch to it
- **Send Messages**: Type your message in the input box and press Enter
- **Attach Files**: Drag and drop text files into the window to include them in your message
- **Settings**: Click "Settings" to configure the model and other parameters
- **Toggle Theme**: Click "Light Mode" / "Dark Mode" to switch themes

### Session Management

Right-click on any session in the sidebar to:
- **Delete Session**: Remove the session and its history
- **Rename Session**: Change the session name

## Configuration

### Settings

Access settings via the Settings button. You can configure:

**Model Settings:**
- **Model**: The Ollama model to use (e.g., `llama3`, `mistral`, `gemma3:4b`)
- **API URL**: Ollama API endpoint (default: `http://localhost:11434`)

**Memory Settings:**
- **Max History**: Number of recent messages to keep in context (default: 5)
- **Summary Threshold**: Number of messages before auto-summarization triggers (default: 20)
- **Enable Auto-Summarization**: Toggle automatic conversation summarization

**Agent Settings:**
- **Agent Preset**: Select a custom agent prompt from the `prompts/` directory

**Generation Settings:**
- **Temperature**: Controls randomness (0.0-2.0, default: 0.7)
- **Top P**: Nucleus sampling threshold (0.0-1.0, default: 0.9)
- **Max Tokens**: Maximum response length (0 = unlimited)

### Custom Agent Prompts

Create custom agent personalities by adding `.txt` files to the `prompts/` directory:

1. Create a file: `prompts/helpful_coder.txt`
2. Add your prompt:
   ```
   You are an expert programmer who provides clear, concise code examples with explanations.
   ```
3. Restart the app or reopen settings to see the new preset

## Project Structure

```
recall/
├── gui.py                  # Main application entry point
├── main.py                 # Core chat logic and Ollama API integration
├── chat_area.py           # Chat display and input handling
├── sidebar.py             # Session management sidebar
├── settings_dialog.py     # Settings configuration dialog
├── requirements.txt       # Python dependencies
├── memory_*.json         # Session conversation histories (auto-generated)
├── settings.json         # User settings (auto-generated)
└── prompts/              # Custom agent prompts directory
    └── *.txt             # Individual prompt files
```

## How It Works

### Session-Based Conversations

Recall organizes chats into sessions, each saved as a separate JSON file. This means:
- Every message you send and receive is automatically saved
- You can create unlimited sessions for different topics or projects
- Sessions can be renamed or deleted at any time
- Switch between sessions instantly without losing context

### Context Management

To keep conversations fast and efficient:
- **Max History** determines how many recent messages are sent to the model
- **Summary Threshold** triggers automatic summarization when conversations grow long
- When triggered, older messages are condensed into a summary while recent messages remain intact
- This maintains context while preventing slowdowns from very long conversations

### File Integration

Drag and drop text files directly into the window:
- File contents are automatically read and included in your message
- Multiple files can be attached at once
- Perfect for discussing code, logs, or documents with the AI

## Troubleshooting

### Ollama Connection Issues

If you see "Request Error" or "HTTP Error" messages:
1. Ensure Ollama is running: `ollama serve`
2. Check that Ollama is listening on `http://localhost:11434`
3. Verify your model is downloaded: `ollama list`

### Model Not Found

If you get a model not found error:
```bash
ollama pull <model-name>
```

### GUI Not Starting

Ensure PySide6 is properly installed:
```bash
pip install --upgrade PySide6
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Why Recall?

Recall was built to solve a simple problem: existing Ollama interfaces don't remember your conversations. Every time you restart them, you lose all context. Recall changes that by automatically saving every conversation, making it perfect for:

- Long-term projects where you need to maintain context over days or weeks
- Managing multiple separate topics without mixing contexts
- Reviewing past conversations to understand how solutions evolved
- Working with code and documents that span multiple interactions

## Built With

- [Ollama](https://ollama.ai/) - Local LLM inference
- [PySide6](https://wiki.qt.io/Qt_for_Python) - Cross-platform GUI framework
- Python 3.8+ - Core implementation
