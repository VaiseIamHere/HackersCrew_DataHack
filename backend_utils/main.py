import os
import PyPDF2
from dotenv import load_dotenv
import google.generativeai as genai
import asyncio
import json
from datetime import datetime
import logging
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict

# Load environment variables
load_dotenv()

class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    FILL_IN_BLANK = "fill_in_blank"
    TRUE_FALSE = "true_false"
    WH_QUESTION = "wh_question"
    DEFINITION = "definition"

@dataclass
class Question:
    text: str
    answer: str
    question_type: QuestionType
    difficulty: str
    options: List[str] = None
    explanation: str = None
    subtopic: str = None
    context: str = None
    metadata: Dict = None

class HybridQuizGenerator:
    def __init__(self, gemini_api_key: str):
        """Initialize the hybrid quiz generator using only Gemini API."""
        # Configure Gemini
        genai.configure(api_key=gemini_api_key)
        self.gemini = genai.GenerativeModel('gemini-pro')
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF file using PyPDF2."""
        text = ""
        try:
            with open(pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page_num in range(len(reader.pages)):
                    text += reader.pages[page_num].extract_text() + "\n"
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF: {str(e)}")
        return text

    async def generate_gemini_questions(self, context: str, subtopic: str) -> List[Question]:
        """Generate questions using Gemini API."""
        prompt = f"""
You are an advanced educational content creator. Based on the following context and subtopic, generate a diverse set of quiz questions that assess different levels of understanding and types of knowledge.

Context: {context}
Subtopic: {subtopic}

Requirements:
1. Create **5 multiple choice questions** with:
   - 4 answer options each
   - Indicate the correct answer and provide a brief explanation for why it's correct.
2. Create **3 true/false questions** with clear statements that can be evaluated as true or false.
3. Create **2 fill-in-the-blank questions** where a key term or concept is missing.
4. Create **2 definition questions** that ask for the definition of a specific term found in the context.
5. Create **1 analytical question** that requires critical thinking or application of concepts.

Format your response as a JSON array of questions, with the following fields:
- `question_text`: The text of the question.
- `correct_answer`: The correct answer.
- `question_type`: The type of the question (e.g., "multiple_choice", "true_false", "fill_in_blank", "definition", "analytical").
- `difficulty`: Difficulty level (e.g., "easy", "medium", "hard").
- `options`: An array of answer options (for multiple choice).
- `explanation`: A brief explanation for the correct answer (for multiple choice and definition questions).

Example output:
[
    {
        "question_text": "What is the primary function of a neural network?",
        "correct_answer": "To approximate complex functions",
        "question_type": "definition",
        "difficulty": "medium",
        "options": null,
        "explanation": "Neural networks can learn from data to make predictions or classifications."
    },
    ...
    GIVE ONLY THE JSON NOTHING ELSE
]
"""

        
        try:
            response = await asyncio.to_thread(
                lambda: self.gemini.generate_content(prompt).text
            )
            questions_data = json.loads(response)
            
            questions = []
            for q_data in questions_data:
                questions.append(Question(
                    text=q_data['question_text'],
                    answer=q_data['correct_answer'],
                    question_type=QuestionType(q_data['question_type']),
                    difficulty=q_data['difficulty'],
                    options=q_data.get('options'),
                    explanation=q_data.get('explanation'),
                    subtopic=subtopic,
                    context=context
                ))
            
            return questions
        except Exception as e:
            self.logger.error(f"Error generating Gemini questions: {str(e)}")
            return []

    async def generate_hybrid_quiz(self, pdf_path: str, subtopic: str, num_questions: int = 10) -> Dict:
        """Generate quiz using only Gemini API with context from a PDF."""
        # Extract context from the provided PDF
        context = self.extract_text_from_pdf(pdf_path)
        if not context:
            self.logger.error("No text extracted from the PDF.")
            return {}

        all_questions = await self.generate_gemini_questions(context, subtopic)
        
        # Select best questions
        selected_questions = self._select_best_questions(all_questions, num_questions)
        
        # Create quiz data
        quiz_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'num_questions': len(selected_questions),
                'question_types': self._get_question_type_distribution(selected_questions),
                'difficulty_distribution': self._get_difficulty_distribution(selected_questions)
            },
            'questions': [self._question_to_dict(q) for q in selected_questions]
        }
        
        return quiz_data

    def _select_best_questions(self, questions: List[Question], num_questions: int) -> List[Question]:
        """Select best questions based on diversity and quality."""
        selected = []
        questions = sorted(questions, key=lambda x: (x.difficulty, x.question_type.value))
        
        # Ensure diversity in question types and difficulty
        difficulty_counts = {'easy': 0, 'medium': 0, 'hard': 0}
        type_counts = {qt: 0 for qt in QuestionType}
        
        while len(selected) < num_questions and questions:
            for q in questions[:]:
                if (difficulty_counts[q.difficulty] < num_questions // 3 and
                    type_counts[q.question_type] < num_questions // len(QuestionType)):
                    selected.append(q)
                    difficulty_counts[q.difficulty] += 1
                    type_counts[q.question_type] += 1
                    questions.remove(q)
                    
                    if len(selected) >= num_questions:
                        break
        
        return selected

    def _question_to_dict(self, question: Question) -> Dict:
        """Convert Question object to dictionary."""
        return {
            'text': question.text,
            'answer': question.answer,
            'type': question.question_type.value,
            'difficulty': question.difficulty,
            'options': question.options,
            'explanation': question.explanation,
            'subtopic': question.subtopic,
            'context': question.context
        }

    def _get_question_type_distribution(self, questions: List[Question]) -> Dict[str, int]:
        """Get the distribution of question types in the selected questions."""
        distribution = {qt.value: 0 for qt in QuestionType}
        for question in questions:
            distribution[question.question_type.value] += 1
        return distribution

    def _get_difficulty_distribution(self, questions: List[Question]) -> Dict[str, int]:
        """Get the distribution of difficulty levels in the selected questions."""
        distribution = {'easy': 0, 'medium': 0, 'hard': 0}
        for question in questions:
            distribution[question.difficulty] += 1
        return distribution

    async def save_quiz(self, quiz_data: Dict, output_path: str):
        """Save quiz data to JSON file."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(quiz_data, f, indent=2)
            self.logger.info(f"Quiz saved to {output_path}")
        except Exception as e:
            self.logger.error(f"Error saving quiz: {str(e)}")
            raise

if __name__ == "__main__":
    async def main():
        api_key = os.getenv("API_KEY")
        generator = HybridQuizGenerator(api_key)
        
        # Provide the PDF path and subtopic for question generation
        pdf_path = "dsa1.pdf"
        subtopic = "DSA"
        
        quiz_data = await generator.generate_hybrid_quiz(pdf_path, subtopic, num_questions=10)
        await generator.save_quiz(
            quiz_data,
            f"quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        print("Quiz generated successfully!")

    asyncio.run(main())
