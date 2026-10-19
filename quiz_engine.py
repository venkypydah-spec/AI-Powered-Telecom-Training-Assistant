"""
Quiz Engine — Parses and manages quiz state for the Telecom Training Assistant.
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class QuizQuestion:
    number: int
    question: str
    options: dict  # {"A": "...", "B": "...", "C": "...", "D": "..."}
    correct_answer: str
    explanation: str


@dataclass
class QuizSession:
    topic: str
    questions: List[QuizQuestion]
    current_index: int = 0
    score: int = 0
    answers_given: List[Optional[str]] = field(default_factory=list)
    completed: bool = False

    def __post_init__(self):
        if not self.answers_given:
            self.answers_given = [None] * len(self.questions)

    @property
    def total_questions(self) -> int:
        return len(self.questions)

    @property
    def current_question(self) -> Optional[QuizQuestion]:
        if self.current_index < self.total_questions:
            return self.questions[self.current_index]
        return None

    def submit_answer(self, answer: str) -> tuple:
        """Submit answer for current question. Returns (is_correct, explanation)."""
        q = self.current_question
        if q is None:
            return False, "No active question."

        answer = answer.strip().upper()
        is_correct = answer == q.correct_answer.upper()

        if is_correct:
            self.score += 1

        self.answers_given[self.current_index] = answer
        self.current_index += 1

        if self.current_index >= self.total_questions:
            self.completed = True

        return is_correct, q.explanation

    def get_results_summary(self) -> str:
        """Returns a formatted results summary."""
        pct = (self.score / self.total_questions) * 100
        grade = "Excellent! 🏆" if pct >= 80 else "Good Job! 👍" if pct >= 60 else "Keep Practicing! 📚"
        lines = [
            f"## Quiz Results — {self.topic}",
            f"**Score: {self.score}/{self.total_questions} ({pct:.0f}%)** — {grade}",
            "",
            "### Question Review:",
        ]
        for i, q in enumerate(self.questions):
            given = self.answers_given[i] or "Not answered"
            status = "✅" if given == q.correct_answer else "❌"
            lines.append(f"{status} **Q{q.number}.** {q.question}")
            lines.append(f"   Your answer: **{given}** | Correct: **{q.correct_answer}**")
            if given != q.correct_answer:
                lines.append(f"   _{q.explanation}_")
            lines.append("")
        return "\n".join(lines)


def parse_quiz_text(raw_text: str, topic: str) -> Optional[QuizSession]:
    """Parse LLM-generated quiz text into a QuizSession."""
    questions = []

    # Split by question markers: Q1., Q2., etc.
    question_blocks = re.split(r'\nQ\d+\.', "\n" + raw_text)
    question_blocks = [b.strip() for b in question_blocks if b.strip()]

    for i, block in enumerate(question_blocks):
        try:
            lines = [l.strip() for l in block.split("\n") if l.strip()]
            if not lines:
                continue

            # First line is the question text
            q_text = lines[0]

            options = {}
            correct = ""
            explanation = ""

            for line in lines[1:]:
                m_opt = re.match(r'^([ABCD])\)\s+(.*)', line)
                m_ans = re.match(r'^Answer:\s*([ABCD])', line, re.IGNORECASE)
                m_exp = re.match(r'^Explanation:\s*(.*)', line, re.IGNORECASE)

                if m_opt:
                    options[m_opt.group(1)] = m_opt.group(2)
                elif m_ans:
                    correct = m_ans.group(1).upper()
                elif m_exp:
                    explanation = m_exp.group(1)

            if q_text and len(options) >= 2 and correct:
                questions.append(QuizQuestion(
                    number=i + 1,
                    question=q_text,
                    options=options,
                    correct_answer=correct,
                    explanation=explanation or "See reference material for details.",
                ))
        except Exception:
            continue

    if not questions:
        return None

    return QuizSession(topic=topic, questions=questions)


def format_question_for_display(q: QuizQuestion, index: int, total: int) -> str:
    """Format a single question for display in the chatbot."""
    lines = [
        f"**Question {index}/{total}**",
        "",
        f"**{q.question}**",
        "",
    ]
    for letter, text in q.options.items():
        lines.append(f"**{letter})** {text}")
    lines.append("")
    lines.append("_Type A, B, C, or D to answer._")
    return "\n".join(lines)
