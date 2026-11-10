# Tests question validation, including blank input and whitespace removal.

from src.css_assistant.schemas import QuestionRequest
import pytest 
from pydantic import ValidationError


def test_blank_question():
    with pytest.raises(ValidationError):
        QuestionRequest(question="   ")


def test_strip_ws():
    question = QuestionRequest(question="   What is CSS?   ")
    assert question.question == "What is CSS?"