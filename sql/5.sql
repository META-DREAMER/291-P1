create or replace view available_flights(flightno,dep_date,src,dst,dep_time,arr_time,fare,seats,price) as
  select fl.flightno, sf.dep_date, fl.src, fl.dst, fl.dep_time+(trunc(sf.dep_date)-trunc(fl.dep_time)),
  fl.dep_time+(trunc(sf.dep_date)-trunc(fl.dep_time))+((fl.est_dur/60+a2.tzone-a1.tzone)/24),
  fa.fare, fa.limit-count(tno), fa.price
  from flights fl, flight_fares fa, sch_flights sf, bookings b, airports a1, airports a2
  where fl.flightno=sf.flightno and fl.flightno=fa.flightno and fl.src=a1.acode and
	fl.dst=a2.acode and fa.flightno=b.flightno(+) and fa.fare=b.fare(+) and
	sf.dep_date=b.dep_date(+)
  group by fl.flightno, sf.dep_date, fl.src, fl.dst, fl.dep_time, fl.est_dur,a2.tzone,
	a1.tzone, fa.fare, fa.limit, fa.price
  having fa.limit-count(tno) > 0