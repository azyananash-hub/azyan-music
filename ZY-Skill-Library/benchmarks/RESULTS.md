# Hasil benchmark (label sintetis, dihitung manual)

Sumber: `benchmarks/run_benchmark.py`. Hanya yang terukur; lainnya NOT TESTED.

- Perhitungan skill: **14/14** lulus
- Ketepatan router (top-1, kueri berlabel): **21/21** dalam 82.3 ms

| Kasus | Harapan | Keluaran | Lulus |
|---|---|---|---|
| B-boiler efisiensi % (T_flue 200, ambien 25, CO2 9, rad 0.5) | 92.1111 | 92.111 | ya |
| B-cooling range C | 12.0 | 12 | ya |
| B-cooling efektivitas % | 75.0 | 75.0 | ya |
| B-cooling evaporasi m3/h | 10.0 | 10.0 | ya |
| B-RO recovery % | 60.0 | 60.0 | ya |
| B-RO rejection % | 98.0 | 98.0 | ya |
| B-RO Cc mg/L | 4940.0 | 4940.0 | ya |
| C-link parameter vertikal | 1080x1920 fps60 dur4 auto=true | 1080x1920 fps60 dur4 auto=true | ya |
| C-link kode ter-decode memuat <canvas | True | True | ya |
| E-trades expectancy | 5.0 | 5.0 | ya |
| E-trades win rate % | 50.0 | 50.0 | ya |
| E-trades profit factor | 1.3333 | 1.3333 | ya |
| E-trades max DD absolut | 60.0 | 60 | ya |
| E-position units | 0.025 | 0.025 | ya |

Waktu eksekusi fungsi (ms): B-boiler 0.03, B-cooling 0.01, B-ro 0.01, C-render-link 0.10, E-trades 0.04, E-position 0.01

## NOT TESTED
- A. AmiraVerse (desain Flutter): perlu runtime AI dengan dan tanpa skill; tidak ada proyek Flutter di repository ini.
- D. DEAMIRA (ide ke spesifikasi): perlu runtime AI dengan dan tanpa skill.
- C. Kualitas motion graphics: link dibuat dan diuji parameternya; render di server ClipACanvas tidak diuji.
- Perbandingan dengan vs tanpa skill (A/B), jumlah file yang dibaca, dan konsumsi token: tidak tersedia di runtime ini.
