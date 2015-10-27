create or replace view good_three_connections (src,dst,dep_date1,dep_date2, dep_date3, dep_time,arr_time,flightno1,flightno2,flightno3,layover1,layover2,price,seats1, fare1,seats2,fare2,seats3,fare3)
as select a1.src, a3.dst, a1.dep_date, a2.dep_date, a3.dep_date, a1.dep_time, a3.arr_time, a1.flightno, a2.flightno, a3.flightno, (a2.dep_time-a1.arr_time)*24,
(a3.dep_time-a2.arr_time)*24,min(a1.price+a2.price+a3.price), a1.seats, a1.fare, a2.seats, a2.fare, a3.seats, a3.fare
from available_flights a1, available_flights a2, available_flights a3
where a1.dst=a2.src and a1.arr_time +1.5/24 <=a2.dep_time and a1.arr_time +5/24 >=a2.dep_time
and a2.dst=a3.src and a2.arr_time +1.5/24 <=a3.dep_time and a2.arr_time +5/24 >=a3.dep_time
group by a1.src, a3.dst, a1.dep_date, a2.dep_date, a3.dep_date, a1.dep_time, a3.arr_time, a1.flightno,
a2.flightno, a3.flightno, a2.dep_time, a1.arr_time, a3.dep_time, a2.arr_time, a1.seats, a1.fare, a2.seats, a2.fare, a3.seats, a3.fare