create or replace view good_flights(flightno1, flightno2, flightno3, dep_date1, dep_date2, dep_date3, src, dst, dep_time, arr_time, stops, layover1, layover2, price, seats1, fare1, seats2, fare2, seats3, fare3)
as select flightno1, flightno2, flightno3, dep_date1, dep_date2, dep_date3, src, dst, dep_time, arr_time, stops, layover1, layover2, price, seats1, fare1, seats2, fare2, seats3, fare3
from (select * from
((select flightno as flightno1, null as flightno2, null as flightno3, dep_date as dep_date1, null as dep_date2, null as dep_date3, src, dst, dep_time, arr_time, 0 as stops,
null as layover1, null as layover2, price, seats as seats1, fare as fare1, null as seats2, null as fare2, null as seats3, null as fare3 from available_flights)
union (select flightno1, flightno2, null as flightno3, dep_date1, dep_date2, null as dep_date3, src, dst, dep_time, arr_time, 1 as stops, layover as layover1,
null as layover2, price, seats1, fare1, seats2, fare2, null as seats3, null as fare3 from good_connections)
union (select flightno1, flightno2, flightno3, dep_date1, dep_date2, dep_date3, src, dst, dep_time, arr_time, 2 as stops, layover1, layover2,
price, seats1, fare1, seats2, fare2, seats3, fare3 from good_three_connections)))