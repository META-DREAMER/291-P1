select rownum, flightno1, flightno2, flightno3, dep_date1, dep_date2, dep_date3, src, dst, dep_time, arr_time,
stops, layover1*60, layover2*60, to_char(price, '999.99'), seats1, fare1, seats2, fare2, seats3, fare3
from (select * from (good_flights)
where src='{}' and dst='{}' and stops<='{}' and lower(to_char(dep_time, 'DD-MM-YYYY')) = '{}' order by {})