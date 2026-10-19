"""
AI-Powered Telecom Training Assistant
Gradio Chatbot Interface with pure-Python CLI fallback.
"""

import os
os.environ.setdefault("GRADIO_ANALYTICS_ENABLED", "False")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("DO_NOT_TRACK", "1")

import logging
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpx2").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
from typing import List, Tuple, Optional

from rag_pipeline import rag_pipeline
from llm_engine import granite_llm
from quiz_engine import parse_quiz_text, format_question_for_display, QuizSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── Available Telecom Topics ──────────────────────────────────────────────────
TELECOM_TOPICS = [
    "5G Network Architecture",
    "LTE and 4G Technology",
    "OSI Model and Network Protocols",
    "Wireless Communication Fundamentals",
    "Network Security in Telecom",
    "Cloud, SDN and NFV in Telecom",
    "Fiber Optics and Transmission Systems",
    "IoT and M2M Communications",
]

# ─── Shared Application State ─────────────────────────────────────────────────
class AppState:
    def __init__(self):
        self.quiz_session: Optional[QuizSession] = None
        self.chat_history: List[Tuple[str, str]] = []

    def reset_quiz(self):
        self.quiz_session = None

app_state = AppState()


def initialize_rag() -> str:
    """Initialize the RAG pipeline."""
    try:
        rag_pipeline.initialize()
        return f"✅ Knowledge base loaded — mode: {rag_pipeline.mode}"
    except Exception as e:
        logger.error(f"RAG init error: {e}")
        return f"⚠️ RAG initialization failed: {e}"


# ─── Core Processing Functions (shared by Gradio and CLI) ─────────────────────

def handle_explain(topic: str, history: list) -> Tuple[list, str]:
    if not topic.strip():
        history.append({"role": "assistant", "content": "⚠️ Please enter a topic to explain."})
        return history, ""
    history.append({"role": "user", "content": f"📖 Explain: **{topic}**"})
    history.append({"role": "assistant", "content": "⏳ Retrieving materials and generating explanation..."})
    try:
        _, context = rag_pipeline.retrieve(topic)
        explanation = granite_llm.explain_concept(topic, context)
        app_state.chat_history.append(("user", f"Explain: {topic}"))
        app_state.chat_history.append(("assistant", explanation))
        history[-1] = {"role": "assistant", "content": f"### 📡 {topic}\n\n{explanation}"}
    except Exception as e:
        logger.error(f"Explain error: {e}")
        history[-1] = {"role": "assistant", "content": f"❌ Error: {e}"}
    return history, ""


def handle_chat(user_message: str, history: list) -> Tuple[list, str]:
    if not user_message.strip():
        return history, ""

    # ── Quiz answer mode ───────────────────────────────────────────────────────
    if app_state.quiz_session and not app_state.quiz_session.completed:
        session = app_state.quiz_session
        answer = user_message.strip().upper()
        history.append({"role": "user", "content": user_message})

        if answer == "QUIT":
            app_state.quiz_session = None
            history.append({"role": "assistant", "content": "Quiz ended. Ask me anything!"})
            return history, ""

        if answer not in ["A", "B", "C", "D"]:
            history.append({"role": "assistant", "content": "⚠️ Please answer with **A**, **B**, **C**, or **D** (or type QUIT to end)."})
            return history, ""

        is_correct, explanation = session.submit_answer(answer)
        feedback = "✅ **Correct!**" if is_correct else f"❌ **Incorrect.** Correct: **{session.questions[session.current_index - 1].correct_answer}**."
        msg = f"{feedback}\n\n_{explanation}_"

        if session.completed:
            msg += "\n\n" + session.get_results_summary()
            msg += "\n\n---\n_Quiz complete! You can start a new quiz or ask more questions._"
            app_state.quiz_session = None
        else:
            q = session.current_question
            msg += "\n\n---\n\n" + format_question_for_display(
                q, session.current_index, session.total_questions
            )
        history.append({"role": "assistant", "content": msg})
        return history, ""

    # ── Normal Q&A mode ────────────────────────────────────────────────────────
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": "⏳ Thinking..."})
    try:
        _, context = rag_pipeline.retrieve(user_message)
        response = granite_llm.answer_question(user_message, context, app_state.chat_history)
        app_state.chat_history.append(("user", user_message))
        app_state.chat_history.append(("assistant", response))
        history[-1] = {"role": "assistant", "content": response}
    except Exception as e:
        logger.error(f"Chat error: {e}")
        history[-1] = {"role": "assistant", "content": f"❌ Error: {e}"}
    return history, ""


def handle_quiz(topic: str, num_q: int, history: list) -> Tuple[list, str]:
    if not topic.strip():
        history.append({"role": "assistant", "content": "⚠️ Please select a topic."})
        return history, ""
    if app_state.quiz_session and not app_state.quiz_session.completed:
        history.append({"role": "assistant", "content": "⚠️ A quiz is already in progress. Answer it or type QUIT."})
        return history, ""

    history.append({"role": "user", "content": f"🧪 Start quiz: **{topic}** ({int(num_q)} questions)"})
    history.append({"role": "assistant", "content": f"⏳ Generating {int(num_q)}-question quiz on **{topic}**..."})
    try:
        _, context = rag_pipeline.retrieve(topic)
        raw_quiz = granite_llm.generate_quiz(topic, context, int(num_q))
        session = parse_quiz_text(raw_quiz, topic)
        if session is None or session.total_questions == 0:
            history[-1] = {"role": "assistant", "content": f"❌ Could not parse quiz output:\n```\n{raw_quiz[:500]}\n```"}
            return history, ""
        app_state.quiz_session = session
        q = session.current_question
        msg = (
            f"✅ Quiz ready! **{session.total_questions} questions** on **{topic}**.\n\n"
            "Type **A**, **B**, **C**, or **D** to answer. Type **QUIT** to exit quiz.\n\n"
            "---\n\n"
            + format_question_for_display(q, 1, session.total_questions)
        )
        history[-1] = {"role": "assistant", "content": msg}
    except Exception as e:
        logger.error(f"Quiz error: {e}")
        history[-1] = {"role": "assistant", "content": f"❌ Quiz error: {e}"}
    return history, ""


def handle_summary(topic: str, history: list) -> Tuple[list, str]:
    if not topic.strip():
        history.append({"role": "assistant", "content": "⚠️ Please enter a topic."})
        return history, ""
    history.append({"role": "user", "content": f"📋 Summary: **{topic}**"})
    history.append({"role": "assistant", "content": "⏳ Generating study summary..."})
    try:
        _, context = rag_pipeline.retrieve(topic)
        summary = granite_llm.generate_summary(topic, context)
        history[-1] = {"role": "assistant", "content": f"### 📋 Study Summary: {topic}\n\n{summary}"}
    except Exception as e:
        history[-1] = {"role": "assistant", "content": f"❌ Error: {e}"}
    return history, ""


def handle_learning_path(topic: str, history: list) -> Tuple[list, str]:
    if not topic.strip():
        history.append({"role": "assistant", "content": "⚠️ Please enter a topic."})
        return history, ""
    history.append({"role": "user", "content": f"🗺️ Learning path: **{topic}**"})
    history.append({"role": "assistant", "content": "⏳ Building learning path..."})
    try:
        _, context = rag_pipeline.retrieve(topic)
        path = granite_llm.suggest_learning_path(topic, context)
        history[-1] = {"role": "assistant", "content": f"### 🗺️ Learning Path: {topic}\n\n{path}"}
    except Exception as e:
        history[-1] = {"role": "assistant", "content": f"❌ Error: {e}"}
    return history, ""


# ─── Gradio UI ─────────────────────────────────────────────────────────────────

WELCOME_MSG = """
# 📡 AI-Powered Telecom Training Assistant

Welcome! I'm your intelligent telecom learning companion powered by **IBM Granite 4** and **watsonx.ai**.

## What I can do:
- 📖 **Explain** complex telecom concepts in simple terms
- 🧪 **Quiz** you with interactive multiple-choice questions
- 💬 **Answer** your telecom questions in real time
- 📋 **Summarize** topics into concise study notes
- 🗺️ **Suggest** personalized learning paths

**Try asking:** _"Explain 5G network slicing"_, _"What is beamforming?"_, or use the controls!
"""

CSS = """
.gradio-container { max-width: 1100px !important; margin: auto; }
#chatbot { height: 520px; }
footer { display: none !important; }
"""


def build_gradio_ui():
    import gradio as gr

    with gr.Blocks(
        title="📡 Telecom Training Assistant",
    ) as demo:

        gr.Markdown("# 📡 AI-Powered Telecom Training Assistant")
        gr.Markdown("*Powered by IBM Granite 4 · watsonx.ai · RAG*")

        with gr.Row():
            # ── Left Sidebar ──────────────────────────────────────────────────
            with gr.Column(scale=1):
                gr.Markdown("### ⚙️ Setup")
                rag_status = gr.Textbox(
                    label="Knowledge Base Status",
                    value="Click Initialize to load...",
                    interactive=False,
                )
                init_btn = gr.Button("🔌 Initialize Knowledge Base", variant="primary")

                gr.Markdown("---")
                gr.Markdown("### 📚 Topic")
                topic_dropdown = gr.Dropdown(
                    choices=TELECOM_TOPICS,
                    label="Select Topic",
                    value=TELECOM_TOPICS[0],
                )
                topic_input = gr.Textbox(
                    label="Or type custom topic",
                    placeholder="e.g., OFDM, network slicing, SS7...",
                )
                explain_btn = gr.Button("📖 Explain Topic", variant="secondary")
                summary_btn = gr.Button("📋 Study Summary", variant="secondary")
                path_btn = gr.Button("🗺️ Learning Path", variant="secondary")

                gr.Markdown("---")
                gr.Markdown("### 🧪 Quiz")
                quiz_topic = gr.Dropdown(
                    choices=TELECOM_TOPICS,
                    label="Quiz Topic",
                    value=TELECOM_TOPICS[0],
                )
                num_questions = gr.Slider(
                    minimum=3, maximum=10, value=5, step=1,
                    label="Number of Questions",
                )
                quiz_btn = gr.Button("🧪 Start Quiz", variant="primary")

                gr.Markdown("---")
                clear_btn = gr.Button("🗑️ Clear Chat", variant="stop")

            # ── Main Chat Area ────────────────────────────────────────────────
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    value=[{"role": "assistant", "content": WELCOME_MSG}],
                    elem_id="chatbot",
                    label="Telecom Training Chat",
                )
                with gr.Row():
                    msg_input = gr.Textbox(
                        placeholder="Ask a question, answer quiz (A/B/C/D), or type freely...",
                        label="Your Message",
                        scale=5,
                        container=False,
                    )
                    send_btn = gr.Button("Send ➤", variant="primary", scale=1)
                gr.Markdown("*💡 Use the controls on the left to explain topics, start quizzes, or get summaries.*")

        # ── Quick Topic Buttons ────────────────────────────────────────────────
        gr.Markdown("### ⚡ Quick Topics")
        with gr.Row():
            for topic in TELECOM_TOPICS[:4]:
                gr.Button(topic, size="sm").click(
                    fn=lambda h, t=topic: handle_explain(t, h),
                    inputs=[chatbot], outputs=[chatbot, msg_input],
                )
        with gr.Row():
            for topic in TELECOM_TOPICS[4:]:
                gr.Button(topic, size="sm").click(
                    fn=lambda h, t=topic: handle_explain(t, h),
                    inputs=[chatbot], outputs=[chatbot, msg_input],
                )

        # ── Event Wiring ───────────────────────────────────────────────────────
        def get_topic(dropdown_val, custom_val):
            return custom_val.strip() if custom_val.strip() else dropdown_val

        init_btn.click(fn=initialize_rag, outputs=[rag_status])

        explain_btn.click(
            fn=lambda d, c, h: handle_explain(get_topic(d, c), h),
            inputs=[topic_dropdown, topic_input, chatbot],
            outputs=[chatbot, msg_input],
        )
        summary_btn.click(
            fn=lambda d, c, h: handle_summary(get_topic(d, c), h),
            inputs=[topic_dropdown, topic_input, chatbot],
            outputs=[chatbot, msg_input],
        )
        path_btn.click(
            fn=lambda d, c, h: handle_learning_path(get_topic(d, c), h),
            inputs=[topic_dropdown, topic_input, chatbot],
            outputs=[chatbot, msg_input],
        )
        quiz_btn.click(
            fn=handle_quiz,
            inputs=[quiz_topic, num_questions, chatbot],
            outputs=[chatbot, msg_input],
        )
        send_btn.click(
            fn=handle_chat,
            inputs=[msg_input, chatbot],
            outputs=[chatbot, msg_input],
        )
        msg_input.submit(
            fn=handle_chat,
            inputs=[msg_input, chatbot],
            outputs=[chatbot, msg_input],
        )
        clear_btn.click(
            fn=lambda h: ([], ""),
            inputs=[chatbot],
            outputs=[chatbot, msg_input],
        )

    return demo


# ─── CLI Fallback (no Gradio required) ────────────────────────────────────────

def run_cli():
    """Interactive CLI fallback when Gradio is not available."""
    print("\n" + "=" * 65)
    print("  📡  AI-Powered Telecom Training Assistant  (CLI Mode)")
    print("  Powered by IBM Granite 4 · watsonx.ai · RAG")
    print("=" * 65)

    print("\nInitializing knowledge base...")
    msg = initialize_rag()
    print(msg)

    print("\nCommands:")
    print("  explain <topic>   — Explain a telecom concept")
    print("  quiz <topic>      — Start a quiz (5 questions)")
    print("  summary <topic>   — Get a study summary")
    print("  path <topic>      — Get a learning path")
    print("  help              — Show available topics")
    print("  quit              — Exit")
    print("-" * 65)

    history = []

    def show(msgs):
        for role, text in msgs[-2:]:
            prefix = "🧑 You" if role == "user" else "🤖 Assistant"
            print(f"\n{prefix}:\n{text}")

    while True:
        try:
            raw = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not raw:
            continue

        low = raw.lower()

        if low in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        elif low == "help":
            print("\nAvailable topics:")
            for i, t in enumerate(TELECOM_TOPICS, 1):
                print(f"  {i}. {t}")
        elif low.startswith("explain "):
            topic = raw[8:].strip()
            history, _ = handle_explain(topic, history)
            show(history)
        elif low.startswith("quiz "):
            topic = raw[5:].strip()
            history, _ = handle_quiz(topic, 5, history)
            show(history)
        elif low.startswith("summary "):
            topic = raw[8:].strip()
            history, _ = handle_summary(topic, history)
            show(history)
        elif low.startswith("path "):
            topic = raw[5:].strip()
            history, _ = handle_learning_path(topic, history)
            show(history)
        else:
            # Free chat or quiz answer
            history, _ = handle_chat(raw, history)
            show(history)


# ─── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    use_cli = "--cli" in sys.argv

    if not use_cli:
        try:
            import threading
            import gradio as gr  # noqa
            print("🚀 Starting Telecom Training Assistant (Gradio UI)...")
            print("📡 Initializing knowledge base...")
            initialize_rag()
            # Pre-warm IAM token in background so first LLM call is instant
            threading.Thread(target=granite_llm._get_iam_token, daemon=True).start()
            demo = build_gradio_ui()
            demo.launch(
                server_name="127.0.0.1", server_port=7860, share=False, show_error=True,
                theme=gr.themes.Soft(primary_hue="blue", secondary_hue="indigo"),
                css=CSS,
            )
            demo.block_thread()
        except ImportError:
            print("⚠️  Gradio not available — falling back to CLI mode.")
            print("   Install Gradio for the web UI: pip install gradio")
            run_cli()
    else:
        run_cli()
