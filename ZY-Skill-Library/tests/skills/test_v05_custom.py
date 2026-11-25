"""Uji terarah v0.5: 7 skill custom industri/narasi. Nilai acuan dihitung manual di tiap test."""
import importlib.util
import os
import shutil
import subprocess
import tempfile
import unittest

from _helpers import LIBRARY_ROOT

SK = os.path.join(LIBRARY_ROOT, "skills")


def mod(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(SK, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


relay = mod("relay_curve", "engineering/overcurrent-relay-curves/scripts/relay_curve.py")
xf = mod("transformer_calc", "engineering/transformer-rating-regulation/scripts/transformer_calc.py")
motor = mod("motor_calc", "engineering/motor-starting-sizing/scripts/motor_calc.py")
loop = mod("loop_calc", "industrial-utility/instrument-loop-calc/scripts/loop_calc.py")
rel = mod("reliability", "industrial-utility/reliability-pm-metrics/scripts/reliability.py")
energy = mod("energy_metrics", "industrial-utility/industrial-energy-metrics/scripts/energy_metrics.py")
sub = mod("subtitle_sync", "creative-production/narration-subtitle-sync/scripts/subtitle_sync.py")


class RelayTests(unittest.TestCase):
    def test_very_inverse_exact_value(self):
        """VI, TMS 1, I/Is = 10: t = 13.5 / (10 - 1) = 1.5 s."""
        self.assertAlmostEqual(relay.operate_time_s(10, 1, "VI"), 1.5, places=9)

    def test_faster_at_higher_multiple_and_rejects_pickup(self):
        self.assertGreater(relay.operate_time_s(2, 1), relay.operate_time_s(5, 1))
        with self.assertRaises(ValueError):
            relay.operate_time_s(1.0, 1)


class TransformerTests(unittest.TestCase):
    def test_rated_current_and_regulation(self):
        """1000 kVA, 20 kV: I = 1e6/(sqrt3*20000) = 28.868 A.
        Z=6 %, X/R=10: R=5.970/... = 0.59701 %, X=5.9701 %; dV = 0.59701*0.8 + 5.9701*0.6 = 4.0597 %."""
        r = xf.analyse(1000, 20000, 6.0, 10, 0.8)
        self.assertAlmostEqual(r["i_rated_a"], 28.868, places=3)
        self.assertAlmostEqual(r["voltage_regulation_pct"], 4.0597, places=3)

    def test_invalid_pf(self):
        with self.assertRaises(ValueError):
            xf.analyse(1000, 20000, 6, 10, 1.5)


class MotorTests(unittest.TestCase):
    def test_flc_and_star_delta(self):
        """75 kW, 400 V, PF 0.85, eta 0.93: FLC = 75000/(sqrt3*400*0.85*0.93) = 136.92 A.
        LRC/FLC = 7 -> DOL 958.4 A; star-delta = 319.5 A."""
        r = motor.analyse(75, 400, 0.85, 0.93, 7.0)
        self.assertAlmostEqual(r["flc_a"], 136.92, places=1)
        self.assertAlmostEqual(r["star_delta_start_current_a"], r["dol_start_current_a"] / 3, places=2)

    def test_requires_nameplate_ratio(self):
        with self.assertRaises(ValueError):
            motor.analyse(75, 400, 0.85, 0.93, 1.0)


class LoopTests(unittest.TestCase):
    def test_scaling_and_fault_window(self):
        """12 mA pada span 0-100: 50 %; 3.5 mA dan 21.5 mA adalah fault (NAMUR NE43)."""
        r = loop.ma_to_value(12, 0, 100)
        self.assertAlmostEqual(r["value"], 50.0)
        self.assertFalse(r["fault_namur_ne43"])
        self.assertTrue(loop.ma_to_value(3.5, 0, 100)["fault_namur_ne43"])
        self.assertTrue(loop.ma_to_value(21.5, 0, 100)["fault_namur_ne43"])

    def test_pt100_known_point_and_round_trip(self):
        """Pt100 pada 100 C = 138.5055 ohm (Callendar-Van Dusen)."""
        self.assertAlmostEqual(loop.pt100_resistance(100), 138.5055, places=3)
        self.assertAlmostEqual(loop.pt100_temperature(138.5055), 100.0, places=3)


class ReliabilityTests(unittest.TestCase):
    def test_availability_and_weibull(self):
        """MTBF 100 h, MTTR 2 h: A = 100/102 = 0.980392. R(eta) = e^-1 = 0.367879."""
        self.assertAlmostEqual(rel.availability(100, 2), 0.980392, places=6)
        self.assertAlmostEqual(rel.weibull_reliability(1000, 1000, 2.5), 0.367879, places=6)


class EnergyTests(unittest.TestCase):
    def test_pfc_kvar(self):
        """100 kW, PF 0.70 -> 0.95: tan(phi1)=1.020204, tan(phi2)=0.328684, Qc = 69.152 kvar."""
        self.assertAlmostEqual(energy.pfc_kvar(100, 0.70, 0.95), 69.152, places=2)

    def test_kwh_per_unit(self):
        self.assertAlmostEqual(energy.intensity(1200, 400), 3.0)


class SubtitleTests(unittest.TestCase):
    SRT = "1\n00:00:00,000 --> 00:00:02,000\nHalo dunia\n\n2\n00:00:02,000 --> 00:00:04,000\nSelamat datang\n"

    def test_roundtrip_and_scale(self):
        cues = sub.parse_srt(self.SRT)
        self.assertEqual(sub.to_srt(cues).count("-->"), 2)
        scaled = sub.scale_to_duration(cues, 8000)
        self.assertEqual(scaled[-1]["end"], 8000)

    def test_overlap_detected(self):
        cues = [{"start": 0, "end": 3000, "text": "a"}, {"start": 2000, "end": 4000, "text": "b"}]
        self.assertTrue(any("overlap" in i for i in sub.validate(cues)))

    def test_loudness_with_real_ffmpeg(self):
        if not shutil.which("ffmpeg"):
            self.skipTest("butuh ffmpeg")
        with tempfile.TemporaryDirectory() as tmp:
            wav = os.path.join(tmp, "n.wav")
            subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "sine=frequency=1000:duration=3",
                            wav], check=True)
            m = sub.loudness(wav)
            self.assertTrue(-70 < m["integrated_lufs"] < 0)
            self.assertLessEqual(m["true_peak_dbtp"], 0.5)


if __name__ == "__main__":
    unittest.main()
