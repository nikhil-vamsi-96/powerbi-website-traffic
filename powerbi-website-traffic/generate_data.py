"""
Generates a synthetic website traffic dataset modeled on the schema
of a Google Analytics export (session-level rows), since GA's live
dataset isn't downloadable from this environment.

Simulates 6 months of daily sessions across traffic sources, device
categories, and countries, with realistic relationships:
- Weekday traffic higher than weekends
- Organic/Direct traffic converts better than Paid/Social
- Mobile has higher bounce rate than Desktop
- A gradual growth trend plus seasonal dips
"""
import numpy as np, pandas as pd
from datetime import datetime, timedelta

rng = np.random.default_rng(33)

start = datetime(2024,1,1)
n_days = 210  # ~7 months
dates = [start + timedelta(days=i) for i in range(n_days)]

sources = ['Organic Search','Direct','Paid Search','Social','Referral','Email']
source_weights = [0.34,0.22,0.16,0.14,0.09,0.05]
devices = ['Desktop','Mobile','Tablet']
device_weights = [0.46,0.47,0.07]
countries = ['India','United States','United Kingdom','Germany','Canada','Australia','Brazil','Other']
country_weights = [0.38,0.22,0.09,0.07,0.06,0.05,0.05,0.08]

source_conv_rate = {'Organic Search':0.034,'Direct':0.041,'Paid Search':0.028,
                     'Social':0.014,'Referral':0.022,'Email':0.052}
source_bounce_base = {'Organic Search':0.42,'Direct':0.38,'Paid Search':0.48,
                       'Social':0.58,'Referral':0.44,'Email':0.35}
device_bounce_mult = {'Desktop':0.85,'Mobile':1.20,'Tablet':1.05}

rows = []
session_id = 1
for i, d in enumerate(dates):
    dow = d.weekday()  # 0=Mon
    weekday_mult = 1.15 if dow < 5 else 0.75
    trend = 1 + i*0.0016  # gradual growth over 7 months
    # occasional campaign spike
    campaign_spike = 1.6 if d.strftime('%Y-%m-%d') in ['2024-03-15','2024-05-20','2024-06-10'] else 1.0
    base_sessions = 340 * weekday_mult * trend * campaign_spike

    daily_sessions = int(rng.normal(base_sessions, base_sessions*0.08))
    daily_sessions = max(50, daily_sessions)

    src_alloc = rng.multinomial(daily_sessions, source_weights)
    for src, cnt in zip(sources, src_alloc):
        if cnt == 0: continue
        dev_alloc = rng.multinomial(cnt, device_weights)
        for dev, dcnt in zip(devices, dev_alloc):
            if dcnt == 0: continue
            ctry_alloc = rng.multinomial(dcnt, country_weights)
            for ctry, ccnt in zip(countries, ctry_alloc):
                if ccnt == 0: continue
                for _ in range(ccnt):
                    bounce_p = np.clip(source_bounce_base[src]*device_bounce_mult[dev] + rng.normal(0,0.05), 0.1, 0.9)
                    is_bounce = rng.random() < bounce_p
                    pageviews = 1 if is_bounce else rng.poisson(3.4)+1
                    duration = 0 if is_bounce else int(rng.gamma(2, 80))
                    conv_p = source_conv_rate[src] * (0.5 if is_bounce else 1.3)
                    converted = rng.random() < conv_p
                    rows.append([
                        session_id, d.strftime('%Y-%m-%d'), src, dev, ctry,
                        pageviews, duration, int(is_bounce), int(converted)
                    ])
                    session_id += 1

df = pd.DataFrame(rows, columns=[
    'SessionID','Date','TrafficSource','Device','Country',
    'Pageviews','SessionDurationSec','IsBounce','Converted'
])
df.to_csv('website_sessions.csv', index=False)
print(f"Generated {len(df):,} sessions across {n_days} days")
print(f"Overall bounce rate: {df['IsBounce'].mean():.1%}")
print(f"Overall conversion rate: {df['Converted'].mean():.2%}")
