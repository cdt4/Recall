"""Recall - Core functionality for chat with persistent memory."""
import requests
import json
import os
from typing import List, Dict, Any

def chat_with_memory(user_input: str, session: str = "default", model: str = "llama3",
                     max_history: int = 5, summary_threshold: int = 20, agent_prompt: str = "") -> str:
    """Chat with Ollama model while maintaining conversation memory.
    
    Args:
        user_input: The user's message
        session: Session name for memory persistence
        model: Ollama model name
        max_history: Maximum number of recent messages to keep
        summary_threshold: Number of messages before triggering summarization
        agent_prompt: System prompt to prepend to conversation
        
    Returns:
        The assistant's response
    """
    MEMORY_FILE = f"memory_{session}.json"

    # Load memory
    memory = load_memory(session)

    # Add new user message
    memory.append({"role": "user", "content": user_input})

    # Summarize older messages if too long
    if len(memory) > summary_threshold:
        old_messages = memory[:-max_history]
        old_text = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in old_messages])
        summary_prompt = f"Summarize the following conversation in a few sentences to preserve context:\n{old_text}\nSummary:"
        summary = generate_text(summary_prompt, model=model)
        memory = [{"role": "system", "content": summary}] + memory[-max_history:]

    # Build prompt from memory
    context_messages = memory[-max_history:]
    if agent_prompt:
        context_messages = [{"role": "system", "content": agent_prompt}] + context_messages

    context = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in context_messages])
    context += "\nAssistant:"

    # Generate assistant response
    assistant_reply = generate_text(context, model=model)
    
    if not assistant_reply or assistant_reply.startswith(("HTTP Error:", "Request Error:", "Unexpected Error:")):
        return assistant_reply

    # Save memory
    memory.append({"role": "assistant", "content": assistant_reply})
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving memory: {e}")

    return assistant_reply

def generate_text(prompt: str, model: str = "llama3") -> str:
    """Generate text using Ollama API.
    
    Args:
        prompt: The prompt to send to the model
        model: Ollama model name
        
    Returns:
        The generated text or error message
    """
    url = "http://localhost:11434/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False}

    try:
        r = requests.post(url, json=payload)
        r.raise_for_status()
        data = r.json()
        return data.get("response", "")
    except requests.HTTPError as e:
        return f"HTTP Error: {e}, {r.text}"
    except requests.RequestException as e:
        return f"Request Error: {e}"
    except Exception as e:
        return f"Unexpected Error: {e}"

def load_memory(session: str = "default") -> List[Dict[str, str]]:
    """Load chat memory for a given session.
    
    Args:
        session: Session name
        
    Returns:
        List of message dictionaries with 'role' and 'content' keys
    """
    MEMORY_FILE = f"memory_{session}.json"
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                memory = json.load(f)
                if not isinstance(memory, list):
                    print(f"Invalid memory format in {MEMORY_FILE}")
                    return []
                return memory
        except json.JSONDecodeError as e:
            print(f"JSON decode error loading memory: {e}")
            return []
        except Exception as e:
            print(f"Error loading memory: {e}")
            return []
    return []
