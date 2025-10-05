export function groupByDirection(devices) {
    const map = new Map()
    for (const device of devices) {
        const key = String(device.direction_id).trim()
        if (!map.has(key)) map.set(key, [])
        map.get(key).push(device)
    }
    return map
}
