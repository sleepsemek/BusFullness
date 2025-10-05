import { injectScript } from './observer'
import {renderCourse, insertRouteContainers} from './ui/render'

let routeData = null
let courseData = null

window.addEventListener('message', (event) => {
    if (event.source !== window) return

    const msg = event.data
    if (!msg) return

    switch (msg.type) {
        case 'ROUTE_RESPONSE':
            try {
                routeData = msg.payload
                insertRouteContainers(routeData)
            } catch (e) {
                console.error('prepareRouteContainers error', e)
            }
            break
        case 'ROUTING_API_RESPONSE':
            try {
                courseData = msg.payload
                setTimeout(() => {
                    renderCourse(courseData)
                }, 200)

            } catch (e) {
                console.error('prepareCourseContainers error', e)
            }
            break
    }
}, false)

;(function init() {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectScript)
    } else {
        injectScript()
    }
})()

