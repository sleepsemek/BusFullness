export function loadToColor(value) {
    const v = Math.max(0, Math.min(1, value))
    const hue = Math.round((1 - v) * 120)
    return `hsl(${hue}, 70%, 45%)`
}
