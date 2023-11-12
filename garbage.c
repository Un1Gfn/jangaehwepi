
return (
  ( ((int64_t)random())<<32 | random() )
  % 1*1000*1000*1000
  + 1*1000*1000*1000
);

return (
  (random()%2) ?
  INT64_MAX :
  INT64_MIN
);
