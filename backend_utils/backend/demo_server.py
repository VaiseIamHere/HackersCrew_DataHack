from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from flask_cors import CORS
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from prompts import *
from flask import Flask , json, jsonify, request , render_template
from recommend import Recommend
app = Flask(__name__)
CORS(app)
@app.route('/')
def normal():
    return "Hello user !!!"
load_dotenv()

db = {

}
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

start_session_prompt_template = PromptTemplate(
      input_variables=["chat_history"],
      template=start_session_prompt
   )
question_rating_prompt = PromptTemplate(
      input_variables=["chat_history","rating"],
      template=start_session_prompt
   )


memory = ConversationBufferMemory(memory_key="chat_history")
def gemini_generate(diff, chat_history):
    return llm.invoke(question_rating_prompt.format(chat_history=chat_history, rating=diff)).content

def get_diff(results):
    return Recommend().predict_next_difficulty(results)

@app.route("/api/postcontext/<string:user>", methods=['POST'])
def post_content(user):
    res = request.get_json()
    db[user] = {
        "content": res.get("context"),
        "result": []
    }
    return jsonify({"status": db[user]["content"]}), 200

@app.route("/api/getquestion/<string:user>", methods=['GET'])
def get_question(user):
    if user not in db or "result" not in db[user]:
        return jsonify({"error": "User not found or no results available"}), 404

    diff = get_diff(db[user]["result"])
    question = gemini_generate(diff, db[user]["content"])
    return jsonify({"question": question}), 200

@app.route("/api/postanswer/<string:user>", methods=['POST'])
def post_answer(user):
    if user not in db:
        return jsonify({"error": "User not found"}), 404

    res = request.get_json()
    db[user]["result"].append((res.get("rating"), res.get("response")))
    return jsonify({"status": "success"}), 200

@app.route("/api/xai")
def home():
   return render_template('index.html')

@app.route("/api/refs/<string:user>")
def refs(user):
   return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)
