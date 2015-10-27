CREATE OR REPLACE VIEW matched_flights(flightno1, flightno2, flightno3, dep_date1, dep_date2, dep_date3, src, dst,
dep_time, arr_time, stops, layover1, layover2, price, seats1, fare1, seats2, fare2, seats3, fare3)
AS SELECT flightno1, flightno2, flightno3, dep_date1, dep_date2, dep_date3, src, dst, dep_time, arr_time, stops,
layover1, layover2, price, seats1, fare1, seats2, fare2, seats3, fare3
FROM (SELECT * FROM ((SELECT flightno AS flightno1, NULL AS flightno2, NULL AS flightno3, dep_date AS dep_date1,
NULL AS dep_date2, NULL AS dep_date3, src, dst, dep_time, arr_time, 0 AS stops,
NULL AS layover1, NULL AS layover2, price, seats AS seats1, fare AS fare1, NULL AS seats2, NULL AS fare2,
NULL AS seats3, NULL AS fare3 FROM available_flights)
UNION (SELECT flightno1, flightno2, NULL AS flightno3, dep_date1, dep_date2, NULL AS dep_date3, src, dst, dep_time,
arr_time, 1 AS stops, layover AS layover1, NULL AS layover2, price, seats1, fare1, seats2, fare2, NULL AS seats3, NULL AS fare3
FROM good_connections) UNION (SELECT flightno1, flightno2, flightno3, dep_date1, dep_date2, dep_date3, src, dst,
dep_time, arr_time, 2 AS stops, layover1, layover2, price, seats1, fare1, seats2, fare2, seats3, fare3 FROM good_connections_2S)))