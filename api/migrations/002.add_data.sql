WITH src(route_id) AS (
  VALUES ('102'), ('120'), ('25')
)
INSERT INTO bus (route_id, device_id)
SELECT
  s.route_id,
  s.route_id || '_' || md5(s.route_id::text)
FROM src s;

INSERT INTO camera (bus_id, position)
SELECT b.id, p.position
FROM bus b
JOIN (VALUES
      ('102','F'), ('102','B'),
      ('120','F'), ('120','M'), ('120','B'),
      ('25','F')
     ) AS p(route_id, position)
  ON p.route_id = b.route_id
ON CONFLICT (bus_id, position) DO NOTHING;

INSERT INTO info_from_camera (camera_id, ts, occupancy_pct, created_at)
SELECT
  c.id AS camera_id,
  NOW() - (gs * INTERVAL '1 minute') AS ts,
  ROUND(random()::numeric, 2)::real AS occupancy_pct,
  NOW() AS created_at
FROM camera c
CROSS JOIN generate_series(1, 50) AS gs;