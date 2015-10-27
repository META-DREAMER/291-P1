select * from (
select rownum,src,dst,dep_date,dep_time,arr_time,2 AS stops,flightno1,flightno2,flightno3,layover1*24*60 as layover1,layover2*24*60 as layover2,fare1,fare2,fare3,price,seats
from (select * from (two_good_connections))
union all
select rownum,src,dst,dep_date,dep_time,arr_time,1 AS stops,flightno1,flightno2,NULL as flightno3,layover*24*60 as layover1,NULL as layover2, fare1,fare2, NULL as fare3, price,seats
from (select * from (good_connections))
union all
select rownum,src,dst,dep_date,dep_time,arr_time,0 AS stops,flightno as flightno1,NULL as flightno2,NULL as flightno3,NULL as layover1,NULL as layover2,fare as fare1,NULL as fare2,NULL as fare3,price,seats
from (select * from (available_flights)))
where LOWER(src)=LOWER('{}') and LOWER(dst)=LOWER('{}') and stops<= {} and lower(to_char(dep_time, 'DD-MM-YYYY')) = LOWER('{}') order by {}