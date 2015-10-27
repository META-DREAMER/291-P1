create or replace view two_good_connections (src,dst,dep_date,dep_time,arr_time,flightno1,flightno2,flightno3,layover1,layover2,fare1,fare2,fare3,price,seats) as
  select a1.src,a3.dst,a1.dep_date,a1.dep_time, a3.arr_time,a1.flightno,a2.flightno,a3.flightno,a2.dep_time-a1.arr_time,a3.dep_time-a2.arr_time,a1.fare,a2.fare,a3.fare,min(a1.price+a2.price+a3.price),least(a1.seats,a2.seats,a3.seats)
  from available_flights a1, available_flights a2, available_flights a3
  where a1.dst=a2.src and a2.dst=a3.src and a1.arr_time +1.5/24 <=a2.dep_time and a1.arr_time +5/24 >=a2.dep_time
  and a2.arr_time +1.5/24 <=a3.dep_time and a2.arr_time +5/24 >=a3.dep_time
  group by a1.src,a3.dst,a1.dep_date,a1.dep_time, a3.arr_time,a1.flightno,a2.flightno,a3.flightno,a2.dep_time,a1.arr_time,a3.dep_time,a2.arr_time,a1.fare,a2.fare,a3.fare,a1.seats,a2.seats,a3.seats