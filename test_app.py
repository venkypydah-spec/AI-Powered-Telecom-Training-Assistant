"""
Tests for the Telecom Training Assistant components.
Run with: python test_app.py
"""

import sys
import unittest
from unittest.mock import patch, MagicMock


class TestQuizEngine(unittest.TestCase):
    """Test the quiz parsing and session management."""

    SAMPLE_QUIZ = """
Q1. What does 5G stand for?
A) Fifth Generation
B) Fast Generation
C) Fiber Gateway
D) Frequency Generator
Answer: A
Explanation: 5G stands for Fifth Generation wireless technology.

Q2. Which multiplexing technique does 5G NR use in the downlink?
A) FDMA
B) TDMA
C) OFDMA
D) CDMA
Answer: C
Explanation: 5G NR uses OFDMA (Orthogonal Frequency Division Multiple Access) in the downlink, same as LTE.

Q3. What is the name of the 5G base station?
A) eNodeB
B) gNodeB
C) NodeB
D) BTS
Answer: B
Explanation: The 5G base station is called gNodeB (gNB), while 4G uses eNodeB (eNB).
"""

    def test_parse_quiz_text(self):
        from quiz_engine import parse_quiz_text
        session = parse_quiz_text(self.SAMPLE_QUIZ, "5G Technology")
        self.assertIsNotNone(session)
        self.assertEqual(session.total_questions, 3)
        self.assertEqual(session.questions[0].correct_answer, "A")
        self.assertEqual(session.questions[1].correct_answer, "C")
        self.assertEqual(session.questions[2].correct_answer, "B")
        print("✅ Quiz parsing: PASSED")

    def test_quiz_session_correct_answer(self):
        from quiz_engine import parse_quiz_text
        session = parse_quiz_text(self.SAMPLE_QUIZ, "5G Technology")
        is_correct, explanation = session.submit_answer("A")
        self.assertTrue(is_correct)
        self.assertEqual(session.score, 1)
        self.assertEqual(session.current_index, 1)
        print("✅ Quiz correct answer: PASSED")

    def test_quiz_session_wrong_answer(self):
        from quiz_engine import parse_quiz_text
        session = parse_quiz_text(self.SAMPLE_QUIZ, "5G Technology")
        is_correct, explanation = session.submit_answer("B")
        self.assertFalse(is_correct)
        self.assertEqual(session.score, 0)
        print("✅ Quiz wrong answer: PASSED")

    def test_quiz_completion(self):
        from quiz_engine import parse_quiz_text
        session = parse_quiz_text(self.SAMPLE_QUIZ, "5G Technology")
        session.submit_answer("A")  # correct
        session.submit_answer("C")  # correct
        session.submit_answer("B")  # correct
        self.assertTrue(session.completed)
        self.assertEqual(session.score, 3)
        summary = session.get_results_summary()
        self.assertIn("3/3", summary)
        print("✅ Quiz completion and scoring: PASSED")

    def test_format_question(self):
        from quiz_engine import parse_quiz_text, format_question_for_display
        session = parse_quiz_text(self.SAMPLE_QUIZ, "5G Technology")
        display = format_question_for_display(session.questions[0], 1, 3)
        self.assertIn("Question 1/3", display)
        self.assertIn("A)", display)
        print("✅ Question formatting: PASSED")


class TestKnowledgeBase(unittest.TestCase):
    """Test the telecom knowledge base."""

    def test_knowledge_base_loads(self):
        from knowledge_base import get_all_documents
        docs = get_all_documents()
        self.assertGreater(len(docs), 0)
        self.assertEqual(len(docs), 8)
        print(f"✅ Knowledge base: {len(docs)} documents loaded")

    def test_document_has_content(self):
        from knowledge_base import get_all_documents
        docs = get_all_documents()
        for title, content in docs:
            self.assertTrue(len(title) > 0, f"Empty title found")
            self.assertTrue(len(content) > 100, f"Content too short for: {title}")
        print("✅ All documents have valid content: PASSED")


class TestConfig(unittest.TestCase):
    """Test configuration values."""

    def test_config_values(self):
        from config import (
            WATSONX_API_KEY, WATSONX_PROJECT_ID, WATSONX_URL,
            GRANITE_MODEL_ID, CHUNK_SIZE, CHUNK_OVERLAP, TOP_K_RETRIEVAL
        )
        self.assertTrue(len(WATSONX_API_KEY) > 10, "API key missing")
        self.assertTrue(len(WATSONX_PROJECT_ID) > 10, "Project ID missing")
        self.assertIn("ml.cloud.ibm.com", WATSONX_URL)
        self.assertIn("granite", GRANITE_MODEL_ID.lower())
        self.assertGreater(CHUNK_SIZE, 0)
        self.assertGreater(TOP_K_RETRIEVAL, 0)
        print("✅ Configuration values: PASSED")


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Telecom Training Assistant — Unit Tests")
    print("=" * 60)
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestKnowledgeBase))
    suite.addTests(loader.loadTestsFromTestCase(TestQuizEngine))
    
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print(f"✅ All {result.testsRun} tests passed!")
    else:
        print(f"❌ {len(result.failures)} failures, {len(result.errors)} errors")
    print("=" * 60)
    sys.exit(0 if result.wasSuccessful() else 1)
