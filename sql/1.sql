CREATE OR REPLACE VIEW available_flights(flightno,dep_date, src,dst,dep_time,arr_time,fare,seats,price)
AS SELECT f.flightno, sf.dep_date, f.src, f.dst, f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time)),
f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time))+(f.est_dur/60+a2.tzone-a1.tzone)/24, fa.fare, fa.limit-count(tno), fa.price
FROM flights f, flight_fares fa, sch_flights sf, bookings b, airports a1, airports a2
WHERE f.flightno=sf.flightno AND f.flightno=fa.flightno AND f.src=a1.acode AND f.dst=a2.acode
AND fa.flightno=b.flightno(+) AND fa.fare=b.fare(+) AND sf.dep_date=b.dep_date(+)
GROUP BY f.flightno, sf.dep_date, f.src, f.dst, f.dep_time, f.est_dur,a2.tzone,a1.tzone, fa.fare, fa.limit, fa.price
HAVING fa.limit-count(tno) > 0