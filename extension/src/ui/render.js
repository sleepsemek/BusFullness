import {drawCard, updateCard} from "./routeCard";
import {groupByDirection} from "../utils/groupBy";
import {
    cardClassNames,
    routePageElementSelectors,
} from "../constants";

export function insertRouteContainers(latestData) {
    const headers = Array.from(document.querySelectorAll(routePageElementSelectors.header))
    if (!headers.length) return

    const groups = latestData ? groupByDirection(latestData.devices || []) : new Map()

    for (const header of headers) {
        const directionId = String(header.dataset.directionId).trim()

        let host = header.nextSibling

        const directionGroup = groups.get(directionId)
        if (!directionGroup) continue

        renderDirection(host, directionId, directionGroup)
    }
}

function renderDirection(host, directionId, buses) {
    const stations = Array.from(host.querySelectorAll(routePageElementSelectors.station))
    const untouchedStations = []

    let currentMaxTime = -1
    let currentMissingCount = 0

    let busIndex = 0
    let nodeColor = stations[0].firstElementChild.firstElementChild.style.backgroundColor

    if (!buses || !buses.length) {
        untouchedStations.push(...stations)
        clearPreviousCards(untouchedStations)

        return
    }

    for (const station of stations) {
        const timeElement = station.querySelector(routePageElementSelectors.activeTime)
        if (!timeElement) {
            untouchedStations.push(station)
            currentMissingCount++

            continue
        }

        const timeValue = parseInt(timeElement.textContent.replace(' мин', '').trim())

        const currentBus = buses[busIndex]
        if (!currentBus) {
            untouchedStations.push(station)

            continue
        }

        if (currentMissingCount >= 3 || currentMaxTime === -1 || timeValue < currentMaxTime) {
            const existingCard = station.previousElementSibling?.classList.contains(cardClassNames.card) ? station.previousElementSibling : false

            if (existingCard) {
                updateCard(existingCard, currentBus)
            } else {
                station.parentNode.insertBefore(drawCard(currentBus, nodeColor), station)
            }
            currentMaxTime = timeValue
            busIndex++
        } else {
            currentMaxTime = timeValue
            untouchedStations.push(station)
        }

        currentMissingCount = 0
    }

    clearPreviousCards(untouchedStations)

    function clearPreviousCards(untouchedStations) {
        for (const station of untouchedStations) {
            const previousElement = station.previousElementSibling

            const isCard = previousElement?.classList.contains(cardClassNames.card) ?? false

            if (isCard) {
                previousElement.remove()
            }
        }
    }
}