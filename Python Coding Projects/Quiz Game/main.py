from question_model import Question
# from data import question_data
from quiz_brain import QuizBrain
import requests
from random import choice
from ui import QuizInterface



params = {
            "amount": 10,
            "type": "boolean",
}

# def get_questions():
resp = requests.get("https://opentdb.com/api.php?amount=10&type=boolean", params=params)
resp.raise_for_status()
question_data = resp.json()
# print(question_data)
# rndm_select = choice(question_data["results"])
# rndm_quest = rndm_select["question"]
# print(rndm_quest)

question_bank = []

for question in question_data["results"]:
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)



quiz = QuizBrain(question_bank)
quiz_ui = QuizInterface(quiz)


# while quiz.still_has_questions():
#     quiz.next_question()

print("You've completed the quiz")
print(f"Your final score was: {quiz.score}/{quiz.question_number}")


