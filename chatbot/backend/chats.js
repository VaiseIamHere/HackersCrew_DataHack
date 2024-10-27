import Groq from "groq-sdk"
import dotenv from "dotenv"

dotenv.config()

const system_prompt = {
  "role": "system",
  "content": "You are a helpful assistant. You reply with accuracy."
}

const chat_history = [system_prompt]

const groq = new Groq(process.env.GROQ_API_KEY)

const reply = async (prompt) => {
  chat_history.push({
    "role": "user",
    "content": prompt
  })
  const completion = await groq.chat.completions.create({
      messages: chat_history,
      model: "llama3-70b-8192",
      max_tokens: 50,
      temperature: 0.9
    })
  const result = completion.choices[0].message.content
  chat_history.push({
    "role": "assistant",
    "content": result
  })
    return result
}

const chat = async (req, res) => {
    const response = await reply(req.body.msg)
    return res.status(200).send({
        response
    })
}

export default chat
