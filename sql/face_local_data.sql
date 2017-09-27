create extension hstore;

create table face_local_data
(
	id serial not null
		constraint face_local_data_pkey
			primary key,
	name varchar not null,
	feature integer[],
	status integer default 0 not null,
	face_img varchar,
	attended_at integer
)
;

create unique index face_local_data_name_uindex
	on face_local_data (name)
;

# face distance compare
CREATE EXTENSION IF NOT EXISTS cube;

DROP FUNCTION IF EXISTS rogue_public_compare_face(target_feature INTEGER[128], OUT target_id INTEGER, OUT targer_diff NUMERIC);
CREATE FUNCTION rogue_public_compare_face(target_feature INTEGER[128], OUT target_id INTEGER, OUT targer_diff NUMERIC) AS $$
DECLARE
    face_recrod RECORD;
BEGIN
    SELECT id, feature INTO face_recrod FROM public.face_local_data ORDER BY cube(feature) <-> cube(target_feature) LIMIT 1;
    target_id = face_recrod.id;
    targer_diff = cube(face_recrod.feature) <-> cube(target_feature);
END;
$$ LANGUAGE plpgsql;

# random face vector
DROP FUNCTION IF EXISTS random_face(line_count INTEGER);
CREATE FUNCTION random_face(line_count INTEGER) RETURNS void AS $$
DECLARE
    random_array INTEGER[128];
BEGIN
    FOR line IN 1..$1 LOOP
        FOR i IN 1..128 LOOP
            random_array[i] = random() * (5000 - (-5000) +1) + (-5000);
        END LOOP;
        INSERT INTO public.face_local_data(name, feature) VALUES ('test' || line, random_array);
    END LOOP;
END;
$$ LANGUAGE plpgsql;