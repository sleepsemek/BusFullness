export const routePageElementSelectors = {
    header: 'div._1sv3x8qq[data-direction-id], div._6xulm8t[data-direction-id]',
    station: 'div._15nfxwn',
    activeTime: '._mgulo2d, ._psoawlx'
}

export const coursePageElementSelectors = {
    list: '._awwm2v',
    cardContent: '._1a1fu9m',
}

export const cardClassNames = {
    card: 'gis-bus-card',
    cardHeader: 'bus-header',
    cardHeaderText: 'bus-header-text',
    cardLoadIndicator: 'load-indicator',
    cardLoadBar: 'load-bars',
    cardLoadZoneBackground: 'load-zone',
    cardLoadZoneForeground: 'load-zone-foreground',
    tooltipClassNames: {
        tooltip: 'load-tooltip',
        tooltipTitle: 'tooltip-title',
        tooltipZones: 'tooltip-zones',
        tooltipZone: 'tooltip-zone',
        tooltipZoneLabel: 'zone-label',
        tooltipZoneBarContainer: 'zone-bar-container',
        tooltipZoneBarFill: 'zone-fill',
        tooltipZonePercentage: 'zone-percent'
    },
    cardDescriptionContainer: 'zone-description-container',
    cardDescription: 'zone-description',
    cardLoadBadgeWrapper: 'gis-course-load-badge-wrapper',
    cardLoadBadge: 'load-badge',
    cardLoadBadgeCourse: 'load-badge load-badge--course',
    cardFooter: 'load-footer',
}

const createClassNameSelectors = (classNames) => {
    const result = {};

    for (const [key, value] of Object.entries(classNames)) {
        if (typeof value === 'object' && value !== null) {
            result[key] = createClassNameSelectors(value);
        } else {
            result[key] = `.${value}`;
        }
    }

    return result;
}

export const cardClassNameSelectors = createClassNameSelectors(cardClassNames);

export const transportTypeMap = {
    bus: "Автобус",
    trolleybus: "Троллейбус",
    tram: "Трамвай",
    shuttle_bus: "Маршрутка"
}

export const baseURL = 'http://localhost:3000'