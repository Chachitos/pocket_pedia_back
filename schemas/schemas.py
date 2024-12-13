from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, Enum, ForeignKey, DECIMAL
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

#ENUMS
class LessonDifficulty(enum.Enum):
    basic = "basic"
    intermediate = "intermediate"
    advanced = "advanced"

class QuestionType(enum.Enum):
    multiple_choice = "multiple_choice"
    true_false = "true_false"
    fill_in_the_blank = "fill_in_the_blank"

class QuizDifficultyLevel(enum.Enum):
    basic = "basic"
    intermediate = "intermediate"
    advanced = "advanced"

class ContentType(enum.Enum):
    lesson = "lesson"
    quiz = "quiz"


class Student(Base):
    __tablename__ = "student"
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    user_trakcing_id = Column(Integer)
    name = Column(String)
    email = Column(String, unique=True)
    cellphone = Column(Integer)

    
    lesson_progress = relationship("Lesson_Progress", back_populates="student")
    quiz_attempts = relationship("Quiz_Attempt", back_populates="student")
    quiz_progress = relationship("Quiz_Progress", back_populates="student")
    question_tracking = relationship("Question_Tracking", back_populates="student")
    study_history = relationship("Study_History", back_populates="student")
    spaced_repetition = relationship("Spaced_Repetition_Schedule", back_populates="student")
    user_tracking = relationship("User_Tracking", back_populates="student")

class Lesson(Base):
    __tablename__ = "lesson"
    lesson_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(Text)
    content_md = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow)
    difficulty = Column(Enum(LessonDifficulty))
    quiz_id = Column(Integer, ForeignKey("quiz.quiz_id"))
    creator_id = Column(Integer)  

    
    quiz = relationship("Quiz", back_populates="lesson")
    images = relationship("Lesson_Image", back_populates="lesson")
    lesson_progress = relationship("Lesson_Progress", back_populates="lesson")
    study_history = relationship("Study_History", back_populates="lesson")
    user_tracking = relationship("User_Tracking", back_populates="lesson")
    lesson_categories = relationship("Lesson_Category", back_populates="lesson")

class Lesson_Image(Base):
    __tablename__ = "lesson_image"
    image_id = Column(Integer, primary_key=True, autoincrement=True)
    lesson_id = Column(Integer, ForeignKey("lesson.lesson_id"))
    image_url = Column(String)
    description = Column(String)
    line_where_to_display = Column(Integer)

    
    lesson = relationship("Lesson", back_populates="images")

class Lesson_Progress(Base):
    __tablename__ = "lesson_progress"
    progress_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("student.student_id"))
    lesson_id = Column(Integer, ForeignKey("lesson.lesson_id"))
    lesson_completed = Column(Boolean)
    quiz_completed = Column(Boolean)
    start_date = Column(DateTime, default=datetime.utcnow)
    completion_date = Column(DateTime)

    
    student = relationship("Student", back_populates="lesson_progress")
    lesson = relationship("Lesson", back_populates="lesson_progress")

class Quiz(Base):
    __tablename__ = "quiz"
    quiz_id = Column(Integer, primary_key=True, autoincrement=True)
    lesson_id = Column(Integer, ForeignKey("lesson.lesson_id"))
    title = Column(String)
    description = Column(Text)
    difficulty_level = Column(Enum(QuizDifficultyLevel))
    estimated_time = Column(Integer)
    attempts_allowed = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    
    lesson = relationship("Lesson", back_populates="quiz")
    questions = relationship("Question", back_populates="quiz")
    quiz_attempts = relationship("Quiz_Attempt", back_populates="quiz")
    quiz_progress = relationship("Quiz_Progress", back_populates="quiz")
    user_tracking = relationship("User_Tracking", back_populates="quiz")
    study_history = relationship("Study_History", back_populates="quiz")
    quiz_categories = relationship("Quiz_Category", back_populates="quiz")

class Question(Base):
    __tablename__ = "question"
    question_id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey("quiz.quiz_id"))
    question_text = Column(Text)
    question_number = Column(Integer)
    question_type = Column(Enum(QuestionType))
    weight = Column(DECIMAL)

    
    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("Option", back_populates="question")
    answers = relationship("Answer", back_populates="question")
    question_tracking = relationship("Question_Tracking", back_populates="question")
    spaced_repetition = relationship("Spaced_Repetition_Schedule", back_populates="question")

class Option(Base):
    __tablename__ = "option"
    option_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("question.question_id"))
    option_text = Column(String)
    is_correct = Column(Boolean)

    
    question = relationship("Question", back_populates="options")

class Quiz_Attempt(Base):
    __tablename__ = "quiz_attempt"
    quiz_attempt_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("student.student_id"))
    quiz_id = Column(Integer, ForeignKey("quiz.quiz_id"))
    completion_date = Column(DateTime)
    score = Column(DECIMAL)
    attempts = Column(Integer)

    
    student = relationship("Student", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="quiz_attempts")
    answers = relationship("Answer", back_populates="quiz_attempt")

class Answer(Base):
    __tablename__ = "answer"
    answer_id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_attempt_id = Column(Integer, ForeignKey("quiz_attempt.quiz_attempt_id"))
    question_id = Column(Integer, ForeignKey("question.question_id"))
    option_id = Column(Integer, ForeignKey("option.option_id"))
    is_correct = Column(Boolean)
    reviewed_at = Column(DateTime)
    next_review = Column(DateTime)

    
    quiz_attempt = relationship("Quiz_Attempt", back_populates="answers")
    question = relationship("Question", back_populates="answers")

class User_Tracking(Base):
    __tablename__ = "user_tracking"
    tracking_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("student.student_id"))
    lesson_id = Column(Integer, ForeignKey("lesson.lesson_id"))
    last_quiz_id = Column(Integer, ForeignKey("quiz.quiz_id"))
    total_quizzes_completed = Column(Integer)
    average_score = Column(DECIMAL)
    last_activity = Column(DateTime)
    next_repetition = Column(DateTime)
    next_question_id = Column(Integer) 
    total_time_spent = Column(Integer)

    
    student = relationship("Student", back_populates="user_tracking")
    lesson = relationship("Lesson", back_populates="user_tracking")
    quiz = relationship("Quiz", back_populates="user_tracking")

class Quiz_Progress(Base):
    __tablename__ = "quiz_progress"
    quiz_progress_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("student.student_id"))
    quiz_id = Column(Integer, ForeignKey("quiz.quiz_id"))
    score = Column(DECIMAL)
    attempts = Column(Integer)
    time_spent = Column(Integer)
    last_completed = Column(DateTime)
    accuracy_rate = Column(DECIMAL)

    
    student = relationship("Student", back_populates="quiz_progress")
    quiz = relationship("Quiz", back_populates="quiz_progress")

class Question_Tracking(Base):
    __tablename__ = "question_tracking"
    question_tracking_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("student.student_id"))
    question_id = Column(Integer, ForeignKey("question.question_id"))
    times_answered = Column(Integer)
    times_answered_correctly = Column(Integer)
    last_answered = Column(DateTime)
    next_review = Column(DateTime)
    is_due = Column(Boolean)

    
    student = relationship("Student", back_populates="question_tracking")
    question = relationship("Question", back_populates="question_tracking")

class Study_History(Base):
    __tablename__ = "study_history"
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("student.student_id"))
    lesson_id = Column(Integer, ForeignKey("lesson.lesson_id"))
    quiz_id = Column(Integer, ForeignKey("quiz.quiz_id"))
    session_date = Column(DateTime)
    time_spent = Column(Integer)
    content_type = Column(Enum(ContentType))
    success_rate = Column(DECIMAL)

    
    student = relationship("Student", back_populates="study_history")
    lesson = relationship("Lesson", back_populates="study_history")
    quiz = relationship("Quiz", back_populates="study_history")

class Spaced_Repetition_Schedule(Base):
    __tablename__ = "spaced_repetition_schedule"
    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("student.student_id"))
    question_id = Column(Integer, ForeignKey("question.question_id"))
    due_date = Column(DateTime)
    review_interval = Column(Integer)
    times_repeated = Column(Integer)
    easiness_factor = Column(DECIMAL)

    
    student = relationship("Student", back_populates="spaced_repetition")
    question = relationship("Question", back_populates="spaced_repetition")

class Category(Base):
    __tablename__ = "category"
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String)
    category_description = Column(Text)
    icon_url = Column(String)

    
    lesson_categories = relationship("Lesson_Category", back_populates="category")
    quiz_categories = relationship("Quiz_Category", back_populates="category")

class Lesson_Category(Base):
    __tablename__ = "lesson_category"
    lesson_id = Column(Integer, ForeignKey("lesson.lesson_id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("category.category_id"), primary_key=True)

    
    lesson = relationship("Lesson", back_populates="lesson_categories")
    category = relationship("Category", back_populates="lesson_categories")

class Quiz_Category(Base):
    __tablename__ = "quiz_category"
    quiz_id = Column(Integer, ForeignKey("quiz.quiz_id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("category.category_id"), primary_key=True)

    
    quiz = relationship("Quiz", back_populates="quiz_categories")
    category = relationship("Category", back_populates="quiz_categories")
