GET_SERVICES_OF_COMPANY = '''
SELECT
    booking.id, /* just for Django ORM */
    booking.amount,
    booking.created,
    booking.updated,
    booking.start_date,
    booking.end_date,
    (UNIX_TIMESTAMP(booking.start_date) * 1000) as start_date_stamp,
    (UNIX_TIMESTAMP(booking.end_date) * 1000) as end_date_stamp,
    booking.uuid, /* please note: when using an alias different to 'uuid', then django orm won't convert it into valid uuid with hyphens! */
    TIMESTAMPDIFF(MONTH, CURRENT_DATE(), booking.end_date) AS months_left,
    IF(CURRENT_DATE() > booking.end_date, 1000,
    (FLOOR( /* important to choose a function that returns an int, e.g. round could also return an int and will throw error in json */
       DATEDIFF(CURRENT_DATE(), booking.start_date) / 
       DATEDIFF(booking.end_date, booking.start_date)
       * 1000))) as progress,
    service.name AS service_name,
    service.price,
    service.duration,
    eq.amount AS article_amount,
    article.name AS article_name,
    article.id AS article_id,
    article.description AS art_desc,
    manu.name AS manu,
    a_group.name AS group_name
FROM
    portal_booking booking
JOIN portal_service service ON
    service.id = booking.service_id
JOIN portal_equipment eq ON
    eq.service_id = service.id
JOIN portal_article article ON
    article.id = eq.article_id
JOIN portal_articlegroup a_group ON
    a_group.id = article.group_id
JOIN portal_manufacturer manu ON
    manu.id = article.manufacturer_id
JOIN portal_company company ON
    company.id = booking.company_id
WHERE
    company.uuid = %s
ORDER BY
    end_date,
    group_name,
    article_amount,
    article_name'''

GET_SERVICES_FROM_STORE = '''
SELECT
    service.id,
    service.name AS service_name,
    service.price AS service_price,
    service.duration,
    service.id AS service_id,
    eq.amount AS article_amount,
    article.name AS article_name,
    article.id AS article_id,
    article.description AS art_desc,
    manu.name AS manu,
    a_group.name AS group_name,
    NOT(ISNULL(booking.id)) AS is_already_booked
FROM
    portal_service service
JOIN portal_equipment eq ON
    eq.service_id = service.id
JOIN portal_article article ON
    article.id = eq.article_id
JOIN portal_articlegroup a_group ON
    a_group.id = article.group_id
JOIN portal_manufacturer manu ON
    manu.id = article.manufacturer_id
LEFT JOIN portal_booking booking ON
    booking.service_id = service.id AND booking.company_id = %s
ORDER BY
    service_id,
    group_name,
    article_amount,
    article_name
'''

GET_SERVICE_DETAIL = '''
SELECT
    service.id,
    service.name AS service_name,
    service.price AS service_price,
    service.duration,
    service.id AS service_id,
    eq.amount AS article_amount,
    article.name AS article_name,
    article.id AS article_id,
    article.description AS art_desc,
    manu.name AS manu,
    a_group.name AS group_name
FROM
    portal_service service
JOIN portal_equipment eq ON
    eq.service_id = service.id
JOIN portal_article article ON
    article.id = eq.article_id
JOIN portal_articlegroup a_group ON
    a_group.id = article.group_id
JOIN portal_manufacturer manu ON
    manu.id = article.manufacturer_id
WHERE service.uuid = %s
ORDER BY
    service_id,
    group_name,
    article_amount,
    article_name
'''

GET_COMPANY_HIERARCHY = '''
WITH this AS (
SELECT id, uuid, name, city, postcode, details, mother_company_id
FROM
    portal_company this
    WHERE this.uuid = %s
)
SELECT mother.id, mother.uuid, mother.name, mother.postcode, mother.city, mother.details, 0 as level
FROM this
JOIN portal_company mother
ON mother.id = this.mother_company_id
UNION
SELECT this.id, this.uuid, this.name, this.postcode, this.city, this.details, 1 as level
FROM this
UNION
SELECT child.id, child.uuid, child.name, child.postcode, child.city, child.details, 2 as level
FROM this
JOIN portal_company child
ON child.mother_company_id = this.id
'''
