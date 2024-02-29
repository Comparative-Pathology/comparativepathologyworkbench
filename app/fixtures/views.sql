DROP VIEW matrices_bench_summary;
DROP VIEW matrices_collection_summary;
DROP VIEW matrices_environment_summary;
DROP VIEW matrices_image_summary;

CREATE OR REPLACE VIEW matrices_bench_summary AS
(SELECT  row_number() OVER (PARTITION BY true::boolean) AS id, a.id as matrix_id, a.title as matrix_title, a.description as matrix_description, a.blogpost as matrix_blogpost, a.created as matrix_created, a.modified as matrix_modified, a.height as matrix_height, a.width as matrix_width, d.username as matrix_owner, b.id as matrix_authorisation_id, e.username as matrix_authorisation_permitted, c.name as matrix_authorisation_authority
FROM public.matrices_matrix a, public.matrices_authorisation b, public.matrices_authority c, public.auth_user d, public.auth_user e
WHERE a.id = b.matrix_id AND c.id = b.authority_id AND d.id = a.owner_id AND e.id = b.permitted_id)
UNION
(SELECT  row_number() OVER (PARTITION BY true::boolean) AS id, a.id as matrix_id, a.title as matrix_title, a.description as matrix_description, a.blogpost as matrix_blogpost, a.created as matrix_created, a.modified as matrix_modified, a.height as matrix_height, a.width as matrix_width, b.username as matrix_owner, '0' as matrix_authorisation_id, b.username as matrix_authorisation_permitted, 'OWNER' as matrix_authorisation_authority
FROM public.matrices_matrix a, public.auth_user b
WHERE b.id = a.owner_id)
UNION
(SELECT  row_number() OVER (PARTITION BY true::boolean) AS id, a.id as matrix_id, a.title as matrix_title, a.description as matrix_description, a.blogpost as matrix_blogpost, a.created as matrix_created, a.modified as matrix_modified, a.height as matrix_height, a.width as matrix_width, b.username as matrix_owner, '0' as matrix_authorisation_id, b.username as matrix_authorisation_permitted, 'ADMIN' as matrix_authorisation_authority
FROM public.matrices_matrix a, public.auth_user b
WHERE b.id = a.owner_id)
ORDER BY matrix_id;

CREATE OR REPLACE VIEW matrices_collection_summary AS
(SELECT row_number() OVER (PARTITION BY true::boolean) AS id, a.id AS collection_id, a.title AS collection_title, a.description AS collection_description, b.username AS collection_owner, count(c.image_id) AS collection_image_count, d.id as collection_authorisation_id, e.username AS collection_authorisation_permitted, f.name AS collection_authorisation_authority
FROM public.auth_user b,
public.auth_user e,
public.matrices_collectionauthorisation d,
public.matrices_collectionauthority f,
public.matrices_collection a
LEFT JOIN public.matrices_collection_images c
ON c.collection_id = a.id
WHERE b.id = a.owner_id
AND d.collection_id = a.id
AND e.id = d.permitted_id
AND f.id = d.collection_authority_id
GROUP BY a.id, b.username, d.id, e.username, f.name
ORDER BY a.id)
UNION
(SELECT row_number() OVER (PARTITION BY true::boolean) AS id, a.id AS collection_id, a.title AS collection_title, a.description AS collection_description, b.username AS collection_owner, count(c.image_id) AS collection_image_count, '0' as collection_authorisation_id, b.username AS collection_authorisation_permitted, 'OWNER' AS matrix_authorisation_authority
FROM public.auth_user b,
public.matrices_collection a
LEFT JOIN public.matrices_collection_images c
ON c.collection_id = a.id
WHERE b.id = a.owner_id
GROUP BY a.id, b.username
ORDER BY a.id)
UNION
(SELECT row_number() OVER (PARTITION BY true::boolean) AS id, a.id AS collection_id, a.title AS collection_title, a.description AS collection_description, b.username AS collection_owner, count(c.image_id) AS collection_image_count, '0' as collection_authorisation_id, b.username AS collection_authorisation_permitted, 'ADMIN' AS matrix_authorisation_authority
FROM public.auth_user b,
public.matrices_collection a
LEFT JOIN public.matrices_collection_images c
ON c.collection_id = a.id
WHERE b.id = a.owner_id
GROUP BY a.id, b.username
ORDER BY a.id);

CREATE OR REPLACE VIEW matrices_environment_summary AS
SELECT row_number() OVER (PARTITION BY true::boolean) AS id, a.id AS environment_id, a.name AS environment_name, b.name AS environment_location, b.colour AS environment_colour, a.wordpress_active AS environment_wordpress_active
FROM public.matrices_environment a,
public.matrices_location b
where a.name = 'CPW'
AND a.location_id = b.id
ORDER BY a.id ASC;

CREATE OR REPLACE VIEW matrices_image_summary AS
(SELECT row_number() OVER (PARTITION BY true::boolean) AS id, a.id AS image_id, a.identifier AS image_identifier, a.name AS image_name, 
a.viewer_url AS image_viewer_url, a.birdseye_url AS image_birdseye_url, f.name AS image_server, f.id AS image_server_id, f.url_server AS image_server_url_server, 
f.uid AS image_server_uid, f.accessible AS image_server_accesible, h.name AS image_server_type_name, a.roi AS image_roi, a.comment AS image_comment, 
a.hidden AS image_hidden, g.username AS image_owner, e.id AS image_collection_id, e.title AS image_collection_title, i.username AS image_collection_owner, 
0 AS image_matrix_id, 'NONE' AS image_matrix_title, 'NONE' AS image_matrix_owner, array_to_string(ARRAY(SELECT z.id || ',' || z.name || ',' || z.slug
FROM public.matrices_image x
JOIN public.taggit_taggeditem y ON y.object_id = x.id
JOIN public.taggit_tag z ON y.tag_id = z.id
WHERE x.id = a.id), '|') AS image_tags
FROM public.matrices_image a 
LEFT JOIN public.matrices_cell b ON a.id = b.image_id
JOIN public.matrices_collection_images d ON d.image_id = a.id
JOIN public.matrices_collection e ON d.collection_id = e.id
JOIN public.matrices_server f ON a.server_id = f.id
JOIN public.auth_user g ON a.owner_id = g.id
JOIN public.matrices_type h ON f.type_id = h.id
JOIN public.auth_user i ON e.owner_id = i.id
WHERE b.image_id IS NULL
ORDER BY a.id ASC)
UNION
(SELECT row_number() OVER (PARTITION BY true::boolean) AS id, a.id AS image_id, a.identifier AS image_identifier, a.name AS image_name, 
a.viewer_url AS image_viewer_url, a.birdseye_url AS image_birdseye_url, f.name AS image_server, f.id AS image_server_id, f.url_server AS image_server_url_server, 
f.uid AS image_server_uid, f.accessible AS image_server_accesible, h.name AS image_server_type_name, a.roi AS image_roi, a.comment AS image_comment, 
a.hidden AS image_hidden, g.username AS image_owner, e.id AS image_collection_id, e.title AS image_collection_title, i.username AS image_collection_owner, 
c.id AS image_matrix_id, c.title AS image_matrix_title, j.username AS image_matrix_owner, array_to_string(ARRAY(SELECT z.id || ',' || z.name || ',' || z.slug
FROM public.matrices_image x
JOIN public.taggit_taggeditem y ON y.object_id = x.id
JOIN public.taggit_tag z ON y.tag_id = z.id
WHERE x.id = a.id), '|') AS image_tags
FROM public.matrices_image a 
JOIN public.matrices_cell b ON a.id = b.image_id
JOIN public.matrices_matrix c ON b.matrix_id = c.id
JOIN public.matrices_collection_images d ON d.image_id = a.id
JOIN public.matrices_collection e ON d.collection_id = e.id
JOIN public.matrices_server f ON a.server_id = f.id
JOIN public.auth_user g ON a.owner_id = g.id
JOIN public.matrices_type h ON f.type_id = h.id
JOIN public.auth_user i ON e.owner_id = i.id
JOIN public.auth_user j ON c.owner_id = j.id
ORDER BY a.id ASC);

GRANT ALL ON ALL TABLES IN SCHEMA public TO workbench_czi_user;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO workbench_czi_user;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO workbench_czi_user;
GRANT ALL PRIVILEGES ON DATABASE workbench_czi to workbench_czi_user;

/*GRANT ALL ON ALL TABLES IN SCHEMA public TO workbench_coeliac_user;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO workbench_coeliac_user;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO workbench_coeliac_user;
GRANT ALL PRIVILEGES ON DATABASE workbench_coeliac to workbench_coeliac_user;

GRANT ALL ON ALL TABLES IN SCHEMA public TO workbench_canada_user;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO workbench_canada_user;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO workbench_canada_user;
GRANT ALL PRIVILEGES ON DATABASE workbench_canada to workbench_canada_user;*/
