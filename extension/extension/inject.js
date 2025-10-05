(function() {
    const XHR = XMLHttpRequest.prototype;
    const origOpen = XHR.open;
    const origSend = XHR.send;


    XHR.open = function(method, url) {
        this._url = url;
        this._method = method;
        return origOpen.apply(this, arguments);
    };

    XHR.send = function(body) {
        this.addEventListener("load", function() {
            try {
                if (this._method === "POST" && this._url.includes('/v2/points/directions')) {
                    let data;
                    try { data = JSON.parse(this.responseText); }
                    catch { data = this.responseText; }

                    window.postMessage({
                        type: "ROUTE_RESPONSE",
                        payload: data
                    }, "*");
                }

                if (this._url.includes('routing.api.2gis.com') && !this._url.includes('search_schedule')) {
                    let data;
                    try { data = JSON.parse(this.responseText); }
                    catch { data = this.responseText; }

                    window.postMessage({
                        type: "ROUTING_API_RESPONSE",
                        payload: data
                    }, "*");
                }
            } catch(e) { console.error(e); }
        });
        return origSend.apply(this, arguments);
    };
})();
