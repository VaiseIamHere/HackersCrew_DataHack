import express from "express"
import cors from "cors"
import chat from "./chats.js"

const app = express()

app.use(cors())
app.use(express.json())
app.use(express.urlencoded({ extended: false}))

app.listen(4000, () => {
    console.log("Started Listening !!")
})

app.get('/', async (req, res) => {
    res.send("Server Connected")
})

app.post('/chat', chat)
