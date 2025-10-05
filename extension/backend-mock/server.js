import express from "express"
import cors from "cors"

const app = express()
app.use(cors())

const port = 3000

const buses = new Map()

function generateTarget() {
    const base = Math.random()
    return [
        Math.min(1, Math.max(0, base)),
        Math.min(1, Math.max(0, base + (Math.random() * 0.2 - 0.1))),
        Math.min(1, Math.max(0, base + (Math.random() * 0.2 - 0.1)))
    ]
}

function getBusLoad(deviceId) {
    let state = buses.get(deviceId)

    if (!state) {
        const start = generateTarget()
        state = {
            current: start,
            target: generateTarget(),
            stepsLeft: 5
        }
        buses.set(deviceId, state)
    }

    if (state.stepsLeft <= 0) {
        state.target = generateTarget()
        state.stepsLeft = 5
    }

    const next = state.current.map((val, i) => {
        const diff = (state.target[i] - val) / state.stepsLeft
        return val + diff
    })

    state.current = next
    state.stepsLeft--

    return next
}

app.get("/bus/:deviceId", (req, res) => {
    const { deviceId } = req.params
    const loads = getBusLoad(deviceId)
    res.json(loads)
})

app.listen(port, () => {
    console.log(`Бэкенд запущен на порту ${port}`)
})
