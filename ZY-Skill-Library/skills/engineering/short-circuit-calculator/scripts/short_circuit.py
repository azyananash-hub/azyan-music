"""Simplified symmetrical three-phase short-circuit calculator.

Scope (sengaja dibatasi):
  - Hanya gangguan tiga fasa simetris pada satu bus.
  - Sumber direpresentasikan sebagai impedansi ekivalen dari MVA hubung singkat.
  - Transformator direpresentasikan dari impedansi persen (Z%) pada MVA ratingnya.
  - Puncak arus mengikuti bentuk faktor kappa IEC 60909 (aproksimasi).
  - TIDAK memperhitungkan kontribusi motor, gangguan tak-simetris, atau
    impedansi urutan nol. Gunakan software studi (mis. pandapower) untuk studi penuh.

Semua hasil adalah estimasi untuk analisis/pre-check, bukan dasar operasi peralatan.

Satuan:
  V dalam kV (line-to-line), S dalam MVA, Z dalam ohm, arus dalam kA.
"""

from __future__ import annotations

import argparse
import cmath
import json
import math
import sys


SQRT3 = math.sqrt(3.0)


def _check_positive(name: str, value: float) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(f"{name} harus berupa angka, bukan {type(value).__name__}")
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} harus > 0 dan finite, dapat {value}")


def source_impedance_ohm(v_kv: float, s_sc_mva: float, x_r_ratio: float = 10.0) -> complex:
    """Impedansi ekivalen sumber (ohm, sisi tegangan v_kv).

    |Z| = V^2 / S_sc. Komponen R dan X dipisah menggunakan rasio X/R.
    """
    _check_positive("v_kv", v_kv)
    _check_positive("s_sc_mva", s_sc_mva)
    _check_positive("x_r_ratio", x_r_ratio)
    z_mag = v_kv**2 / s_sc_mva
    x = z_mag * x_r_ratio / math.sqrt(1.0 + x_r_ratio**2)
    r = x / x_r_ratio
    return complex(r, x)


def transformer_impedance_ohm(
    v_sec_kv: float, s_rated_mva: float, z_percent: float, x_r_ratio: float = 10.0
) -> complex:
    """Impedansi transformator (ohm, referensi sisi sekunder v_sec_kv).

    Z_ohm = (Z% / 100) * V^2 / S_rated.
    """
    _check_positive("v_sec_kv", v_sec_kv)
    _check_positive("s_rated_mva", s_rated_mva)
    _check_positive("z_percent", z_percent)
    _check_positive("x_r_ratio", x_r_ratio)
    z_mag = (z_percent / 100.0) * v_sec_kv**2 / s_rated_mva
    x = z_mag * x_r_ratio / math.sqrt(1.0 + x_r_ratio**2)
    r = x / x_r_ratio
    return complex(r, x)


def three_phase_fault_current_ka(v_kv: float, z_total_ohm: complex) -> float:
    """Arus gangguan simetris tiga fasa (kA rms): I = V / (sqrt(3) * |Z|)."""
    _check_positive("v_kv", v_kv)
    z_abs = abs(z_total_ohm)
    if z_abs == 0:
        raise ValueError("impedansi total nol: arus gangguan tak terhingga, periksa input")
    return v_kv / (SQRT3 * z_abs)


def iec_kappa(r_over_x: float) -> float:
    """Faktor kappa IEC 60909: kappa = 1.02 + 0.98 * exp(-3 R/X)."""
    if not math.isfinite(r_over_x) or r_over_x < 0:
        raise ValueError("R/X harus >= 0")
    return 1.02 + 0.98 * math.exp(-3.0 * r_over_x)


def peak_current_ka(ik_ka: float, r_over_x: float) -> float:
    """Arus puncak ip = sqrt(2) * kappa * Ik (kA)."""
    _check_positive("ik_ka", ik_ka)
    return math.sqrt(2.0) * iec_kappa(r_over_x) * ik_ka


def analyse(
    v_sec_kv: float,
    s_sc_mva: float,
    transformer_mva: float | None = None,
    transformer_z_percent: float | None = None,
    x_r_ratio_source: float = 10.0,
    x_r_ratio_transformer: float = 10.0,
    v_hv_kv: float | None = None,
) -> dict:
    """Hitung arus gangguan di bus sekunder.

    Jika transformator diberikan, sumber dikonversi dari sisi HV ke sisi sekunder
    menggunakan rasio tegangan (v_hv_kv / v_sec_kv)^2 — sumber MVA dan impedansi
    sumber diasumsikan dinyatakan pada tegangan sisi HV.
    """
    if (transformer_mva is None) != (transformer_z_percent is None):
        raise ValueError("transformer_mva dan transformer_z_percent harus diisi bersama")

    # Sumber dinyatakan pada tegangan sisi sekunder bila tidak ada transformator.
    z_source = source_impedance_ohm(v_sec_kv, s_sc_mva, x_r_ratio_source)
    if transformer_mva is None:
        z_total = z_source
        z_transformer = complex(0, 0)
    else:
        if v_hv_kv is None:
            raise ValueError("v_hv_kv wajib diisi bila transformator dimodelkan")
        _check_positive("v_hv_kv", v_hv_kv)
        # Sumber di sisi HV: impedansi sumber dirujuk ke sisi sekunder dengan (V_sec/V_hv)^2
        z_source_hv = source_impedance_ohm(v_hv_kv, s_sc_mva, x_r_ratio_source)
        z_source = z_source_hv * (v_sec_kv / v_hv_kv) ** 2
        z_transformer = transformer_impedance_ohm(
            v_sec_kv, transformer_mva, transformer_z_percent, x_r_ratio_transformer
        )
        z_total = z_source + z_transformer

    ik = three_phase_fault_current_ka(v_sec_kv, z_total)
    r_over_x = z_total.real / z_total.imag if z_total.imag != 0 else 0.0
    ip = peak_current_ka(ik, r_over_x)
    return {
        "v_sec_kv": v_sec_kv,
        "z_source_ohm": [round(z_source.real, 6), round(z_source.imag, 6)],
        "z_transformer_ohm": [round(z_transformer.real, 6), round(z_transformer.imag, 6)],
        "z_total_ohm": [round(z_total.real, 6), round(z_total.imag, 6)],
        "z_total_abs_ohm": round(abs(z_total), 6),
        "ik_kA_rms": round(ik, 4),
        "kappa": round(iec_kappa(abs(r_over_x)), 4),
        "ip_kA_peak": round(peak_current_ka(ik, abs(r_over_x)), 4),
        "scope_note": "Gangguan 3 fasa simetris, aproksimasi IEC 60909; bukan studi lengkap.",
    }


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--v-sec-kv", type=float, required=True, help="Tegangan bus sekunder (kV, LL)")
    p.add_argument("--s-sc-mva", type=float, required=True, help="MVA hubung singkat sumber")
    p.add_argument("--v-hv-kv", type=float, help="Tegangan sisi HV sumber (kV), wajib bila ada trafo")
    p.add_argument("--trafo-mva", type=float, help="MVA rating transformator")
    p.add_argument("--trafo-z-percent", type=float, help="Impedansi transformator (%)")
    p.add_argument("--xr-source", type=float, default=10.0, help="Rasio X/R sumber (default 10)")
    p.add_argument("--xr-trafo", type=float, default=10.0, help="Rasio X/R transformator (default 10)")
    p.add_argument("--json", action="store_true", help="Keluarkan JSON")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        result = analyse(
            v_sec_kv=args.v_sec_kv,
            s_sc_mva=args.s_sc_mva,
            transformer_mva=args.trafo_mva,
            transformer_z_percent=args.trafo_z_percent,
            x_r_ratio_source=args.xr_source,
            x_r_ratio_transformer=args.xr_trafo,
            v_hv_kv=args.v_hv_kv,
        )
    except (ValueError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Ik''  (rms simetris) : {result['ik_kA_rms']} kA")
        print(f"ip    (puncak)       : {result['ip_kA_peak']} kA  (kappa={result['kappa']})")
        print(f"|Z| total           : {result['z_total_abs_ohm']} ohm")
        print(result["scope_note"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
