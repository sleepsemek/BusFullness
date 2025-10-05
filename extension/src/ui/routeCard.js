import {updateBadge} from "./badge";
import {updateTooltip} from "./tooltip";
import {fetchBusLoadById} from "../api/busLoad";
import {loadToColor} from "../utils/colors";
import {cardClassNames, cardClassNameSelectors, transportTypeMap} from "../constants";

export function drawCard(bus, nodeColor) {
    const card = document.createElement('div')
    card.className = cardClassNames.card
    card.dataset.directionId = bus.direction_id
    card.dataset.deviceId = bus.device_id

    const busHeader = Object.assign(
        document.createElement('div'),
        { className: cardClassNames.cardHeader }
    )

    const loadIndicator = Object.assign(
        document.createElement('div'),
        { className: cardClassNames.cardLoadIndicator }
    )

    const busText = Object.assign(
        document.createElement('div'),
        {
            className: cardClassNames.cardHeaderText,
            textContent: `${transportTypeMap[bus.transport_type]} ${bus.route_name}`
        }
    )

    busHeader.append(loadIndicator, busText)

    const bars = Object.assign(
        document.createElement('div'),
        { className: cardClassNames.cardLoadBar }
    )

    const zone = Object.assign(
        document.createElement('div'),
        { className: cardClassNames.cardLoadZoneBackground }
    )

    const zoneForeground = Object.assign(
        document.createElement('div'),
        { className: cardClassNames.cardLoadZoneForeground }
    )
    zone.appendChild(zoneForeground)
    bars.appendChild(zone)

    const tooltip = Object.assign(
        document.createElement('div'),
        {
            className: cardClassNames.tooltipClassNames.tooltip,
            textContent: 'Пожалуйста, подождите...'
        }
    )
    bars.appendChild(tooltip)

    const descriptionContainer = Object.assign(
        document.createElement('div'),
        { className: cardClassNames.cardDescriptionContainer }
    )

    const descriptionText = Object.assign(
        document.createElement('div'),
        {
            className: cardClassNames.cardDescription,
            textContent: 'Загруженность:'
        }
    )

    const badge = Object.assign(
        document.createElement('div'),
        {
            className: cardClassNames.cardLoadBadge,
            textContent: 'Загрузка...'
        }
    )

    descriptionContainer.append(descriptionText, badge)

    const footer = Object.assign(
        document.createElement('div'),
        { className: cardClassNames.cardFooter }
    )

    footer.textContent = `Устройство: ${bus.device_id}`

    fetchBusLoadById(bus.device_id).then(loads => {
        applyGradient(zone, loads)
        updateBadgeAndTooltip(badge, tooltip, loads)
    })

    card.append(busHeader, bars, descriptionContainer, footer)
    card.style.setProperty('--bus-line-color', nodeColor)

    return card
}

export function updateCard(card, bus) {
    card.dataset.directionId = bus.direction_id
    card.dataset.deviceId = bus.device_id

    const busText = card.querySelector(cardClassNameSelectors.cardHeaderText)
    if (busText) {
        busText.textContent = `${transportTypeMap[bus.transport_type]} ${bus.route_name}`
    }

    const zone = card.querySelector(cardClassNameSelectors.cardLoadZoneBackground)
    const badge = card.querySelector(cardClassNameSelectors.cardLoadBadge)
    const tooltip = card.querySelector(cardClassNameSelectors.tooltipClassNames.tooltip)
    const footer = card.querySelector(cardClassNameSelectors.cardFooter)

    if (footer) {
        footer.textContent = `Устройство: ${bus.device_id}`
    }

    fetchBusLoadById(bus.device_id).then(loads => {
        applyGradient(zone, loads)
        updateBadgeAndTooltip(badge, tooltip, loads)
    })
}

function updateBadgeAndTooltip(badge, tooltip, loads) {
    if (!loads.length) return

    const avgLoad = loads.reduce((a, b) => a + b, 0) / loads.length

    updateBadge(badge, avgLoad)
    updateTooltip(tooltip, loads)
}

function applyGradient(zone, loads) {
    if (!loads.length) return

    const min = Math.min(...loads)
    const avg = loads.reduce((a, b) => a + b, 0) / loads.length

    const colorMin = loadToColor(min)
    const colorAvg = loadToColor(avg)
    let foreground = zone.querySelector(cardClassNameSelectors.cardLoadZoneForeground)

    let backgroundGradient = `radial-gradient(circle at center,
        ${colorAvg} 30%,
        ${colorMin} 100%
    )`

    foreground.style.backgroundImage = backgroundGradient
    foreground.style.opacity = '0.8'

    setTimeout(() => {
        zone.style.backgroundImage = backgroundGradient
        foreground.style.opacity = '0'
    }, 1000)
}
