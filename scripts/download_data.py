"""Download one frozen Part 1 sample; re-use it unless --refresh is explicit."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import io
from urllib.request import urlopen
from pathlib import Path
import pandas as pd
import yfinance as yf
from left_tail.data import audit_series, daily_returns

ROOT = Path(__file__).resolve().parents[1]
START, END = '1993-01-01', '2026-09-16'  # end exclusive; completed days only


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--refresh', action='store_true')
    args = parser.parse_args()
    raw = ROOT / 'data/raw'
    raw.mkdir(parents=True, exist_ok=True)
    yf.set_tz_cache_location(str(ROOT / '.uv-cache/yfinance'))
    manifest_path = raw / 'manifest.json'
    if manifest_path.exists() and not args.refresh:
        manifest = json.loads(manifest_path.read_text())
        for filename, expected in manifest['sha256'].items():
            if hashlib.sha256((raw / filename).read_bytes()).hexdigest() != expected:
                raise RuntimeError(f'Snapshot checksum mismatch: {filename}')
        print('Reusing verified snapshot. Use --refresh to replace it intentionally.')
        print(json.dumps(manifest['audit'], indent=2))
        return
    series, sources, failures, hashes = {}, {}, {}, {}
    for label, ticker in [('SPY', 'SPY'), ('VIX', '^VIX'), ('VIX3M', '^VIX3M')]:
        try:
            frame = yf.download(ticker, start=START, end=END, auto_adjust=False,
                                actions=True, progress=False, threads=False,
                                keepna=True, multi_level_index=False)
            provider = 'Yahoo Finance via yfinance'
            source_url = None
            if label == 'VIX3M' and (frame is None or len(frame) < 252):
                source_url = 'https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX3M_History.csv'
                with urlopen(source_url, timeout=30) as response:
                    payload = response.read()
                (raw / 'VIX3M_cboe_download.csv').write_bytes(payload)
                hashes['VIX3M_cboe_download.csv'] = hashlib.sha256(payload).hexdigest()
                frame = pd.read_csv(io.BytesIO(payload))
                frame.columns = frame.columns.str.strip().str.title()
                frame['Date'] = pd.to_datetime(frame['Date'])
                frame = frame.set_index('Date').sort_index()
                frame = frame.loc[(frame.index >= START) & (frame.index < END)]
                provider = 'Cboe historical CSV (Yahoo returned insufficient history)'
            if frame is None or frame.empty:
                raise ValueError('Source returned no data')
            frame.index = pd.to_datetime(frame.index).tz_localize(None).normalize()
            column = 'Adj Close' if label == 'SPY' else 'Close'
            values = frame[column].astype(float).rename(label)
            audit_series(values, values.index)
            if label == 'SPY' and values.isna().any():
                raise ValueError('SPY has missing adjusted prices; investigate before fitting')
            series[label] = values
            name = f'{label}_source.csv'
            frame.to_csv(raw / name, index_label='Date')
            hashes[name] = hashlib.sha256((raw / name).read_bytes()).hexdigest()
            sources[label] = {'provider': provider, 'ticker': ticker, 'url': source_url,
                              'price_column': column, 'first_date': str(values.index.min().date()),
                              'last_date': str(values.index.max().date())}
        except Exception as exc:
            if label != 'VIX3M':
                raise
            failures[label] = str(exc)
    prices = pd.concat(series.values(), axis=1).sort_index()
    prices.to_csv(raw / 'daily_prices.csv', index_label='Date')
    hashes['daily_prices.csv'] = hashlib.sha256((raw / 'daily_prices.csv').read_bytes()).hexdigest()
    reference = series['SPY'].index
    audit = {label: audit_series(values, reference) for label, values in series.items()}
    audit['SPY']['usable_daily_returns'] = int(daily_returns(series['SPY']).notna().sum())
    manifest = {'downloaded_utc': datetime.now(timezone.utc).isoformat(),
                'requested_start': START, 'requested_end_exclusive': END,
                'sources': sources, 'optional_failures': failures, 'audit': audit, 'sha256': hashes,
                'missingness_note': 'Relative to source rows and observed SPY dates, not a verified exchange calendar. No filling. Common overlap does not constrain Part 1 SPY models.'}
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    (ROOT / 'results/tables/data_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
