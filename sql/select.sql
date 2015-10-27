select * from (
select rownum,src,dst,dep_date,flightno1,flightno2,flightno3,layover1,layover2,fare1,fare2,fare3,price,seats
from (select * from (two_good_connections))
union all
select rownum,src,dst,dep_date,flightno1,flightno2,layover1,fare1,fare2,price,seats
from (select * from (good_connections))
union all
select rownum,src,dst,dep_date,flightno1,fare1,price,seats
from (select * from (available_flights))
where src='{}' and dst='{}' and stops<='{}' and lower(to_char(dep_time, 'DD-MM-YYYY')) = '{}' order by {})