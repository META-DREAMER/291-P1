SELECT rownum, flightno1, flightno2, flightno3, dep_date1, dep_date2, dep_date3, src, dst, dep_time, arr_time,
stops, layover1*60, layover2*60, to_char(price, '000.00'), seats1, fare1, seats2, fare2, seats3, fare3
FROM (SELECT * FROM (matched_flights) WHERE src = '{}' AND dst = '{}' AND stops <= '{}' AND LOWER(to_char(dep_time, 'DD-MM-YYYY')) = '{}'
ORDER BY {})