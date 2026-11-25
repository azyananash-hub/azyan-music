---
name: portfolio-metrics-quantstats
description: Compute historical portfolio metrics (cumulative return, Sharpe ratio, maximum drawdown, annualized volatility) from a daily returns CSV using quantstats. Use for evaluating past performance; never a profit guarantee.
license: MIT
compatibility: Python 3.9+; quantstats (Apache-2.0), pandas, numpy
metadata: {"category": "finance", "status": "verified", "owner": "zy"}
---

# portfolio-metrics-quantstats

## Activation Triggers
- User meminta "Sharpe", "max drawdown", "volatility portofolio", atau "metrik return harian".

## Scope dan Batas Kemampuan
- Dicakup: metrik deskriptif dari return harian historis.
- TIDAK dicakup: pengambilan data pasar, prediksi, dan rekomendasi investasi.

## Required Tools
- Python 3.9+, quantstats (Apache-2.0), pandas, numpy.
- `scripts/portfolio_metrics.py`

## Input dan Output Specification
Input: CSV dengan kolom `return` (desimal per hari, mis. 0.01 = 1 %). Output JSON: n_days, cumulative_return_pct, sharpe_rf0, max_drawdown_pct, volatility_ann_pct.

## Execution Workflow
1. Pastikan return sudah net biaya dan dalam desimal. 2. Jalankan script. 3. Laporkan jumlah hari bersama setiap metrik.

## Decision Rules
- Sampel kecil: tampilkan peringatan dan jangan menarik kesimpulan kuat.
- Jangan mengubah periode anualisasi tanpa alasan.

## Error Handling
- Kolom tidak ada atau nilai non-finite: ValueError, exit 2.

## Quality Control
- Drawdown dari return [+10 %, -50 %] = 50 %; cumulative = -45 %.

## Acceptance Criteria
- Test PortfolioTests lulus pada seri acuan di atas.

## Contoh Implementasi
```bash
python scripts/portfolio_metrics.py returns.csv
```

## Test Cases
`tests/skills/test_new_skills.py` (PortfolioTests).

## Referensi dan Sumber
- quantstats: https://github.com/ranaroussi/quantstats (Apache-2.0; LICENSE.txt dan registry).

## Informasi Lisensi
- Skill: MIT. Dependensi quantstats: Apache-2.0.
