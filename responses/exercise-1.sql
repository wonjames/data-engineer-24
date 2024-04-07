SELECT
  o.locationId, SUM(items.amount) as total_amount, DATE_FORMAT(t.datetime, '%m-%y') as month_year
FROM bp_data_exercise.transactions as t, JSON_TABLE(t.details, '$.items[*]' COLUMNS (id  INT PATH '$.id', amount INT PATH '$.amount')) items
INNER JOIN bp_data_exercise.orderItems as o ON o.id = items.id
GROUP BY o.locationId,
MONTH(t.datetime)
ORDER BY MIN(t.datetime) ASC;
