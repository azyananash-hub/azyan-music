---
name: modbus-tcp-client
description: Read and write Modbus TCP holding registers with scaling and signed conversion using pymodbus, with explicit safety rules before any write. Use for PLC, sensor or inverter register access on isolated industrial networks.
license: MIT
compatibility: Python 3.9+; pymodbus (BSD-3-Clause)
metadata: {"category": "automation", "status": "verified", "owner": "zy"}
---

# modbus-tcp-client

## Activation Triggers
- User meminta "Modbus TCP", "baca register PLC", "setpoint PLC", atau integrasi sensor/inverter via Modbus.

## Scope dan Batas Kemampuan
- Dicakup: baca dan tulis holding register Modbus TCP, konversi skala, dan signed 16-bit.
- TIDAK dicakup: Modbus RTU/serial, autentikasi (Modbus TCP tidak punya), dan kontrol keselamatan proses.

## Required Tools
- Python 3.9+, `pymodbus` (BSD-3-Clause, diuji dengan 3.16.2).
- `scripts/modbus_client.py`

## Input dan Output Specification
Input: host, port, unit, alamat, jumlah, nilai (write), skala, signed. Output: nilai raw dan nilai teknik; exit 0 OK, 1 error register, 2 error koneksi/input.

## Execution Workflow
1. Konfirmasi alamat register dan skala dari dokumentasi perangkat.
2. Baca dulu (`read`) dan pastikan nilainya masuk akal.
3. Tulis (`write`) hanya setelah SOP dan persetujuan pemilik sistem.

## Decision Rules
- Write mengubah kondisi fisik peralatan: wajib konfirmasi eksplisit.
- Jaringan Modbus harus terisolasi atau lewat VPN karena tanpa autentikasi.

## Error Handling
- Koneksi gagal: exit 2. Error register: exit 1. Nilai di luar 0-65535: ValueError.

## Quality Control
- Round-trip write lalu read harus sama.
- Konversi signed: 0xFFF6 = -10.

## Acceptance Criteria
- Read dari server uji mengembalikan 375; write 1234 ke alamat 5 terbaca kembali 1234.

## Contoh Implementasi
```bash
python scripts/modbus_client.py read --host 192.168.1.20 --unit 1 --address 0 --count 2 --scale 0.1
```

## Test Cases
`tests/skills/test_custom_engineering.py` (ModbusTests): server pymodbus lokal, read/write, skala, validasi.

## Referensi dan Sumber
- pymodbus: https://github.com/pymodbus-dev/pymodbus (BSD-3-Clause, dikonfirmasi dari metadata PyPI).
- Datastore lama memicu deprecation warning pymodbus; migrasi ke SimDevice belum dilakukan.

## Informasi Lisensi
- Skill: MIT. Dependensi pymodbus: BSD-3-Clause.
