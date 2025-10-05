export function updateBadge(badge, avgLoad) {
    const { status, text, className } = getLoadStatus(avgLoad)
    badge.className = `load-badge ${className}`
    badge.textContent = text
    badge.dataset.status = status
}

export function getLoadStatus(avgLoad) {
    if (avgLoad < 0.2) {
        return { status: 'empty', text: 'пустой', className: 'empty' }
    } else if (avgLoad < 0.3) {
        return { status: 'light', text: 'свободный', className: 'light' }
    } else if (avgLoad < 0.6) {
        return { status: 'medium', text: 'средний', className: 'medium' }
    } else if (avgLoad < 0.7) {
        return { status: 'crowded', text: 'многолюдный', className: 'crowded' }
    } else if (avgLoad < 0.9) {
        return { status: 'full', text: 'заполненный', className: 'full' }
    } else {
        return { status: 'overcrowded', text: 'переполненный', className: 'overcrowded' }
    }
}

