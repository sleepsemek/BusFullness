-- Buses
CREATE TABLE bus
(
    id         BIGSERIAL PRIMARY KEY,
    device_id  TEXT        NOT NULL UNIQUE,
    route_id   TEXT        NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Cameras
CREATE TABLE camera
(
    id         BIGSERIAL PRIMARY KEY,
    bus_id     BIGINT      NOT NULL REFERENCES bus (id) ON DELETE CASCADE,
    position   CHAR(1)     NOT NULL CHECK (position IN ('F', 'M', 'B')), -- F=Front, M=Middle, B=Back
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (bus_id, position)                                            -- one camera per position in a bus
);

-- Measurements from cameras
CREATE TABLE info_from_camera
(
    id            BIGSERIAL PRIMARY KEY,
    camera_id     BIGINT      NOT NULL REFERENCES camera (id) ON DELETE CASCADE,
    ts            TIMESTAMPTZ NOT NULL, -- event time (UTC)
    occupancy_pct REAL        NOT NULL CHECK (occupancy_pct BETWEEN 0 AND 1),
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);