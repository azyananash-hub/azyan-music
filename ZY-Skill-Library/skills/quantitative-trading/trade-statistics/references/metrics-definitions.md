# Definisi metrik

- **Win rate** = jumlah trade PnL > 0 / total trade.
- **Expectancy** = (jumlah PnL) / (jumlah trade). Satuan sama dengan PnL input.
- **Profit factor** = total PnL positif / |total PnL negatif|. Tidak terdefinisi bila tidak ada rugi.
- **Max drawdown (absolut)** = max over t dari (peak_equity(t) - equity(t)).
- **Max drawdown (%)** = drawdown absolut / peak saat itu. Hanya dihitung bila peak > 0.

Catatan: tanpa modal awal, drawdown diukur dari nol. Persentase drawdown tidak akurat dalam kasus itu.
