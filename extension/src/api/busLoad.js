import {baseURL} from "../constants";

export function fetchBusLoadById(deviceId) {
    return fetch(`${baseURL}/bus/${deviceId}`)
        .then(res => {
            if (!res.ok) throw new Error(`Ошибка, статус ${res.status}`)
            return res.json()
        })
}

export function fetchBusLoadByDirection(directionId) {
    return fetch(`${baseURL}/bus/${directionId}`)
        .then(res => {
            if (!res.ok) throw new Error(`Ошибка, статус ${res.status}`)
            return res.json()
        })
}
