import json

with open('manifest.json') as f:
    weeks = json.load(f)

weeks_sorted = list(reversed(weeks))  # most recent first
latest = weeks_sorted[0]

def week_sort_key(w):
    # "P4W2" -> (4, 2)
    p, wk = w['week'][1:].split('W')
    return (int(p), int(wk))

max_pipe = max(max(w['aid_pipeline'] for w in weeks), max(w['do_pipeline'] for w in weeks))

def sparkline(values, color, height=44):
    if len(values) < 2:
        return ''
    w, h = 260, height
    pad = 6
    lo, hi = min(values), max(values)
    span = (hi - lo) or 1
    pts = []
    for i, v in enumerate(values):
        x = pad + i * (w - 2*pad) / (len(values)-1)
        y = h - pad - (v - lo) / span * (h - 2*pad)
        pts.append(f"{x:.1f},{y:.1f}")
    path = " ".join(pts)
    last_x, last_y = pts[-1].split(',')
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" height="{h}" preserveAspectRatio="none">'
            f'<polyline points="{path}" fill="none" stroke="{color}" stroke-width="2.5" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="{last_x}" cy="{last_y}" r="3.5" fill="{color}"/></svg>')

aid_spark = sparkline([w['aid_pipeline'] for w in weeks], '#86BC25')
do_spark = sparkline([w['do_pipeline'] for w in weeks], '#00A3E0')
ytd_spark = sparkline([w['ytd_operate'] for w in weeks], '#005587')

rows_html = ''
for i, w in enumerate(weeks_sorted):
    is_latest = (i == 0)
    badge = '<span class="latest-badge">LATEST</span>' if is_latest else ''
    rows_html += f'''
      <a class="week-card{' latest' if is_latest else ''}" href="{w['filename']}">
        <div class="wc-top">
          <span class="wc-week">{w['week']}</span>
          {badge}
        </div>
        <div class="wc-metrics">
          <div class="wc-metric"><span class="wc-label">AI&amp;D Pipeline</span><span class="wc-val">${w['aid_pipeline']:.1f}M</span></div>
          <div class="wc-metric"><span class="wc-label">DataOps Pipeline</span><span class="wc-val">${w['do_pipeline']:.1f}M</span></div>
          <div class="wc-metric"><span class="wc-label">Operate YTD</span><span class="wc-val">${w['ytd_operate']:.1f}M</span></div>
        </div>
        <div class="wc-open">Open dashboard &rarr;</div>
      </a>'''

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI&amp;D FY27 Pipeline &amp; Performance — Weekly Archive</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: Arial, Helvetica, sans-serif; background: #FAFAF8; color: #1A1A18; }}
  .hero {{ background: #282728; color: #fff; padding: 40px 32px 32px; }}
  .hero .eyebrow {{ font-size: 11px; letter-spacing: .5px; color: #86BC25; font-weight: 700; }}
  .hero h1 {{ font-size: 26px; font-weight: 800; margin-top: 6px; }}
  .hero .sub {{ font-size: 13px; color: rgba(255,255,255,.65); margin-top: 6px; }}

  .wrap {{ max-width: 1100px; margin: 0 auto; padding: 28px 32px 60px; }}

  .trend-section {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 32px; }}
  .trend-card {{ background: #fff; border: 1px solid #eee; border-radius: 10px; padding: 16px 18px; }}
  .trend-card .tc-label {{ font-size: 11px; font-weight: 700; color: #666; text-transform: uppercase; letter-spacing: .3px; }}
  .trend-card .tc-val {{ font-size: 22px; font-weight: 800; margin-top: 4px; }}
  .trend-card .tc-chart {{ margin-top: 10px; }}

  .section-label {{ font-size: 13px; font-weight: 700; color: #444; margin: 8px 0 14px; text-transform: uppercase; letter-spacing: .3px; }}

  .weeks-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 14px; }}
  .week-card {{ display: block; background: #fff; border: 1px solid #eee; border-radius: 10px; padding: 16px 18px;
                text-decoration: none; color: inherit; transition: box-shadow .15s, transform .1s; }}
  .week-card:hover {{ box-shadow: 0 4px 14px rgba(0,0,0,.08); transform: translateY(-1px); }}
  .week-card.latest {{ border-color: #86BC25; box-shadow: 0 0 0 1px #86BC25 inset; }}
  .wc-top {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }}
  .wc-week {{ font-size: 17px; font-weight: 800; }}
  .latest-badge {{ font-size: 9px; font-weight: 700; background: #86BC25; color: #fff; padding: 3px 7px; border-radius: 4px; letter-spacing: .3px; }}
  .wc-metrics {{ display: flex; flex-direction: column; gap: 5px; margin-bottom: 12px; }}
  .wc-metric {{ display: flex; justify-content: space-between; font-size: 12px; }}
  .wc-label {{ color: #888; }}
  .wc-val {{ font-weight: 700; }}
  .wc-open {{ font-size: 11px; font-weight: 700; color: #86BC25; }}

  footer {{ text-align: center; font-size: 11px; color: #999; padding: 24px; }}
</style>
</head>
<body>

  <div class="hero">
    <div class="eyebrow">DELOITTE · APPLICATION OPERATIONS</div>
    <h1>AI&amp;D FY27 Pipeline &amp; Performance</h1>
    <div class="sub">Weekly dashboard archive · updated {latest['week']}</div>
  </div>

  <div class="wrap">

    <div class="section-label">Trend across all weeks</div>
    <div class="trend-section">
      <div class="trend-card">
        <div class="tc-label">AI&amp;D Operate Pipeline</div>
        <div class="tc-val" style="color:#86BC25;">${latest['aid_pipeline']:.1f}M</div>
        <div class="tc-chart">{aid_spark}</div>
      </div>
      <div class="trend-card">
        <div class="tc-label">DataOps Pipeline</div>
        <div class="tc-val" style="color:#00A3E0;">${latest['do_pipeline']:.1f}M</div>
        <div class="tc-chart">{do_spark}</div>
      </div>
      <div class="trend-card">
        <div class="tc-label">FY27 Operate YTD</div>
        <div class="tc-val" style="color:#005587;">${latest['ytd_operate']:.1f}M</div>
        <div class="tc-chart">{ytd_spark}</div>
      </div>
    </div>

    <div class="section-label">All weeks ({len(weeks)})</div>
    <div class="weeks-grid">
      {rows_html}
    </div>

  </div>

  <footer>Source: Jupiter CRM &middot; Generated automatically from weekly AI&amp;E Jupiter dataset exports</footer>

</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("index.html generated,", len(weeks), "weeks listed, latest =", latest['week'])
