USE mydatabase;
SHOW tables;
desc stocks;
select avg(price_open) as avg_price_open,
avg(price_high) as avg_price_high,
avg(price_low) as avg_price_low,
avg(price_close) as avg_price_close,
avg(volume) as avg_volume,
avg(price_adj_close) as avg_price_adj_close 
from stocks
group by exchanges,symbol;