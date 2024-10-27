from flask import Flask, json , jsonify
app = Flask(__name__)

no_of_questions = 15
batch = 3
visited = 0
def choice_question(results):
    pass
def send_question(i):
    pass
def evaluate_question(ans,i):
    pass
@app.route("/generate/questions")
def generate_question():
   results = []
   questions = choice_question(results)
   for i in range(5):
        for i in questions:
            ans = send_question(i)
            results = results.append(evaluate_question(ans,i))
        questions = choice_question(results)
        results = []


if __name__ == "__main__":
    app.run(debug=True)