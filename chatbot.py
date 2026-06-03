import tkinter as tk
from tkinter import scrolledtext
import random
from datetime import datetime


# ══════════════════════════════════════════════════════
#  BOT LOGIC  (separated from UI — easier to test/edit)
# ══════════════════════════════════════════════════════

def clean(text: str) -> str:
    """Sanitize input: lowercase + strip whitespace."""
    return text.lower().strip()


def current_time() -> str:
    return datetime.now().strftime("%I:%M %p")


def current_date() -> str:
    return datetime.now().strftime("%A, %B %d, %Y")


# ── Static responses (multiple options = variety) ─────
RESPONSES: dict[str, list[str]] = {
    "hello":             ["Hi there! 😊", "Hello! Great to see you 🌸", "Hey! How's it going?"],
    "hi":                ["Hey! How can I help you?", "Hi! What would you like to ask?"],
    "hey":               ["Hey! 👋 What's up?", "Hello there!"],
    "how are you":       ["I'm doing great, thanks for asking! 🤖",
                          "Running perfectly — like a well-oiled machine ⚙️"],
    "what is your name": ["I am RuleBot, your rule-based AI assistant! 🤖"],
    "who are you":       ["I'm RuleBot! A rule-based chatbot built for DecodeLabs Project 1."],
    "who made you":      ["I was crafted for an AI internship project at DecodeLabs. 💡"],
    "what can you do":   ["I respond to predefined inputs using rule-based logic.\n"
                          "Try: hello, time, date, about ai, joke, or help!"],
    "about ai":          ["AI enables machines to simulate human-like thinking! 🧠",
                          "Artificial Intelligence covers everything from rule-based "
                          "systems like me to deep learning models."],
    "what is ai":        ["AI stands for Artificial Intelligence — the simulation of "
                          "human intelligence in machines."],
    "help":              ["Here are things you can ask me:\n"
                          "  • hello / hi / hey\n"
                          "  • how are you\n"
                          "  • what is your name\n"
                          "  • time  /  date\n"
                          "  • about ai / what is ai\n"
                          "  • joke\n"
                          "  • thanks\n"
                          "  • bye / exit"],
    "joke":              ["Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
                          "Why did the AI break up with Python? Too many exceptions. 😄",
                          "I told my neural net a joke — it still doesn't get it."],
    "thanks":            ["You're welcome! 😊", "Happy to help!"],
    "thank you":         ["You're welcome! 😊", "Anytime! 🌟"],
    "bye":               ["Goodbye! Have a great day ✨", "See you later! 👋"],
    "exit":              ["Chatbot session ended. Goodbye! 👋"],
}

# ── FIX #1: Dynamic handlers (called fresh every time) ─
#    Previously the time was baked in at startup with an f-string.
#    Lambdas ensure the value is computed at the moment of the question.
DYNAMIC_HANDLERS: dict[str, callable] = {
    "time": lambda: f"The current time is {current_time()}. 🕐",
    "date": lambda: f"Today is {current_date()}. 📅",
}

EXIT_COMMANDS: set[str] = {"bye", "exit"}

WELCOME_MSG = (
    "Bot: Hello! I'm RuleBot 🤖 — your rule-based AI assistant.\n"
    "     Type 'help' to see what I can do!\n\n"
)


def get_response(user_input: str) -> str:
    """
    Return the bot's reply using a 3-tier lookup:
      1. Dynamic handlers  (time, date)
      2. Exact dict match  (O(1) — the professional approach)
      3. Keyword scan      (partial match for natural phrasing)
      4. Fallback message
    """
    cleaned = clean(user_input)

    # Tier 1 — dynamic (FIX #1)
    if cleaned in DYNAMIC_HANDLERS:
        return DYNAMIC_HANDLERS[cleaned]()

    # Tier 2 — exact match
    if cleaned in RESPONSES:
        return random.choice(RESPONSES[cleaned])

    # Tier 3 — FIX #2: keyword scan
    # e.g. "can you help me please" → matches key "help"
    for key in RESPONSES:
        if key in cleaned:
            return random.choice(RESPONSES[key])

    # Tier 4 — fallback
    return "Sorry, I don't understand that yet. Type 'help' to see what I can do! 🤔"


# ══════════════════════════════════════════════════════
#  GUI
# ══════════════════════════════════════════════════════

def send_message() -> None:
    user_msg = entry.get().strip()
    if not user_msg:
        return

    chat_area.config(state="normal")
    chat_area.insert(tk.END, f"You: {user_msg}\n", "user")

    reply = get_response(user_msg)
    chat_area.insert(tk.END, f"Bot: {reply}\n\n", "bot")

    chat_area.config(state="disabled")
    chat_area.see(tk.END)
    entry.delete(0, tk.END)

    if clean(user_msg) in EXIT_COMMANDS:
        root.after(1200, root.destroy)


def on_enter(event) -> None:
    send_message()


# ══════════════════════════════════════════════════════
#  WINDOW SETUP
# ══════════════════════════════════════════════════════

# FIX #5: guard prevents code running on accidental import
if __name__ == "__main__":

    root = tk.Tk()
    root.title("RuleBot — Rule-Based AI Chatbot")
    root.geometry("540x660")
    root.configure(bg="#f7e8ff")
    root.resizable(False, False)

    # ── Header ───────────────────────────────────────
    tk.Label(root, text="🤖 Rule-Based AI Chatbot",
             font=("Arial", 20, "bold"), bg="#f7e8ff", fg="#6a0dad").pack(pady=(15, 2))

    tk.Label(root, text="Internship Project 1 | DecodeLabs",
             font=("Arial", 11), bg="#f7e8ff", fg="#555").pack()

    # ── Chat area ────────────────────────────────────
    chat_area = scrolledtext.ScrolledText(
        root, wrap=tk.WORD, width=58, height=26,
        font=("Arial", 11), bg="white", fg="black", relief=tk.FLAT
    )
    chat_area.pack(padx=20, pady=15)
    chat_area.tag_config("user", foreground="#6a0dad", font=("Arial", 11, "bold"))
    chat_area.tag_config("bot",  foreground="#008060", font=("Arial", 11))

    # FIX #3: show welcome message on launch
    chat_area.config(state="normal")
    chat_area.insert(tk.END, WELCOME_MSG, "bot")
    chat_area.config(state="disabled")

    # FIX #4: input frame keeps entry + button grouped cleanly
    input_frame = tk.Frame(root, bg="#f7e8ff")
    input_frame.pack(fill=tk.X, padx=20, pady=(0, 15))

    entry = tk.Entry(
        input_frame, font=("Arial", 13),
        bg="#ffffff", fg="#333", relief=tk.FLAT
    )
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 8))
    entry.bind("<Return>", on_enter)
    entry.focus()   # cursor lands in the box immediately on launch

    send_button = tk.Button(
        input_frame, text="Send 💬", font=("Arial", 11, "bold"),
        bg="#b565f2", fg="white", relief=tk.FLAT, command=send_message
    )
    send_button.pack(side=tk.RIGHT, ipady=8, ipadx=12)

    root.mainloop()