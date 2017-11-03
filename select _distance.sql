	select 
	round(ST_Distance(ST_Transform(t.coord, 26986), ST_Transform(ST_GeomFromText('POINT(76.944745 43.231877)',4326), 26986))) distance,
	ST_X(t.coord) as Lang,
	ST_Y(t.coord) as Lat,
	t.* from atm_locations t
	where ST_Distance(ST_Transform(t.coord, 26986), ST_Transform(ST_GeomFromText('POINT(76.944745 43.231877)',4326), 26986)) <2000
	order by distance 