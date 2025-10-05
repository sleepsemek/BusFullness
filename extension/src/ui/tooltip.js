import {cardClassNames} from "../constants";
import {loadToColor} from "../utils/colors";

export function updateTooltip(tooltip, loads) {
    const zones = ['Задняя', 'Средняя', 'Передняя']

    const tooltipTitle = Object.assign(
        document.createElement('div'),
        {
            className: cardClassNames.tooltipClassNames.tooltipTitle,
            textContent: 'Загруженность по зонам'
        }
    )

    const tooltipZones = Object.assign(
        document.createElement('div'),
        { className: cardClassNames.tooltipClassNames.tooltipZones }
    )

    loads.forEach((load, index) => {
        const zoneContainer = Object.assign(
            document.createElement('div'),
            { className: cardClassNames.tooltipClassNames.tooltipZone }
        )

        const zoneLabel = Object.assign(
            document.createElement('div'),
            {
                className: cardClassNames.tooltipClassNames.tooltipZoneLabel,
                textContent: zones[index]
            }
        )

        const zoneBarContainer = Object.assign(
            document.createElement('div'),
            { className: cardClassNames.tooltipClassNames.tooltipZoneBarContainer }
        )

        const zoneFill = Object.assign(
            document.createElement('div'),
            {
                className: cardClassNames.tooltipClassNames.tooltipZoneBarFill,
                style: `width: ${load * 100}%; background: ${loadToColor(load)}`
            }
        )

        const zonePercent = Object.assign(
            document.createElement('div'),
            {
                className: cardClassNames.tooltipClassNames.tooltipZonePercentage,
                textContent: `${Math.round(load * 100)}%`
            }
        )

        zoneBarContainer.appendChild(zoneFill)
        zoneContainer.append(zoneLabel, zoneBarContainer, zonePercent)
        tooltipZones.appendChild(zoneContainer)
    })

    tooltip.innerHTML = ''
    tooltip.append(tooltipTitle, tooltipZones)
}