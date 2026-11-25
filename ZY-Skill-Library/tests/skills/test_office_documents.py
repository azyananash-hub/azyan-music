"""Uji fungsional skill dokumen (IMPORTED dari anthropics/skills, Apache-2.0).

Setiap test membuat input sendiri di folder sementara, menjalankan script upstream
apa adanya (tidak dimodifikasi), lalu memverifikasi file keluarannya.
Membutuhkan: pypdf, reportlab, openpyxl, python-pptx, python-docx, PIL, dan
LibreOffice (soffice) untuk xlsx/pptx. Test yang dependensinya hilang di-skip dengan alasan jelas.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from _helpers import LIBRARY_ROOT

SKILLS = os.path.join(LIBRARY_ROOT, "skills", "office-documents")
PDF_SCRIPTS = os.path.join(SKILLS, "pdf", "scripts")
XLSX_SCRIPTS = os.path.join(SKILLS, "xlsx", "scripts")
PPTX_SCRIPTS = os.path.join(SKILLS, "pptx", "scripts")
DOCX_SCRIPTS = os.path.join(SKILLS, "docx", "scripts")


def _has(module: str) -> bool:
    try:
        __import__(module)
        return True
    except ImportError:
        return False


def _run(args, cwd=None, timeout=240):
    return subprocess.run([sys.executable, *args], cwd=cwd, capture_output=True, text=True, timeout=timeout)


@unittest.skipUnless(_has("pypdf") and _has("reportlab"), "butuh pypdf dan reportlab")
class PdfSkillTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()

    def _fillable_pdf(self, path):
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(path)
        c.drawString(72, 740, "Formulir uji ZY")
        c.drawString(72, 700, "Nama lengkap:")
        c.acroForm.textfield(name="full_name", tooltip="Nama", x=200, y=690, width=250, height=24,
                             borderStyle="inset", forceBorder=True)
        c.save()

    def test_detects_fillable_fields(self):
        pdf = os.path.join(self.tmp, "form.pdf")
        self._fillable_pdf(pdf)
        r = _run([os.path.join(PDF_SCRIPTS, "check_fillable_fields.py"), pdf])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("has fillable form fields", r.stdout)

    def test_detects_non_fillable(self):
        from reportlab.pdfgen import canvas

        pdf = os.path.join(self.tmp, "plain.pdf")
        c = canvas.Canvas(pdf)
        c.drawString(72, 700, "Tidak ada field")
        c.save()
        r = _run([os.path.join(PDF_SCRIPTS, "check_fillable_fields.py"), pdf])
        self.assertIn("does not have fillable form fields", r.stdout)

    def test_extract_then_fill_roundtrip(self):
        from pypdf import PdfReader

        pdf = os.path.join(self.tmp, "form.pdf")
        info = os.path.join(self.tmp, "fields.json")
        out = os.path.join(self.tmp, "filled.pdf")
        self._fillable_pdf(pdf)

        r = _run([os.path.join(PDF_SCRIPTS, "extract_form_field_info.py"), pdf, info], cwd=PDF_SCRIPTS)
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(info, encoding="utf-8") as fh:
            fields = json.load(fh)
        ids = [f["field_id"] for f in fields]
        self.assertIn("full_name", ids)

        # Isi nilai lalu tulis ulang PDF
        for f in fields:
            if f["field_id"] == "full_name":
                f["page"] = f.get("page", 1)
                f["value"] = "Zyan"
        fields_path = os.path.join(self.tmp, "values.json")
        with open(fields_path, "w", encoding="utf-8") as fh:
            json.dump(fields, fh)
        r = _run([os.path.join(PDF_SCRIPTS, "fill_fillable_fields.py"), pdf, fields_path, out], cwd=PDF_SCRIPTS)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        values = PdfReader(out).get_fields()
        self.assertEqual(str(values["full_name"].get("/V")), "Zyan")


@unittest.skipUnless(_has("openpyxl") and shutil.which("soffice"), "butuh openpyxl dan LibreOffice")
class XlsxSkillTests(unittest.TestCase):
    def test_recalc_writes_formula_results(self):
        import openpyxl

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "budget.xlsx")
            wb = openpyxl.Workbook()
            ws = wb.active
            ws["A1"], ws["B1"] = 1200, 350.5
            ws["C1"] = "=A1+B1"
            ws["C2"] = "=C1*2"
            wb.save(path)
            r = _run([os.path.join(XLSX_SCRIPTS, "recalc.py"), path], timeout=400)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            values = openpyxl.load_workbook(path, data_only=True).active
            self.assertAlmostEqual(values["C1"].value, 1550.5)
            self.assertAlmostEqual(values["C2"].value, 3101.0)
            formulas = openpyxl.load_workbook(path).active
            self.assertEqual(formulas["C1"].value, "=A1+B1")  # formula tetap ada


@unittest.skipUnless(_has("pptx") and _has("PIL") and shutil.which("soffice"), "butuh python-pptx, PIL, LibreOffice")
class PptxSkillTests(unittest.TestCase):
    def test_thumbnail_grid_is_created(self):
        from PIL import Image
        from pptx import Presentation
        from pptx.util import Inches

        with tempfile.TemporaryDirectory() as tmp:
            deck = os.path.join(tmp, "deck.pptx")
            prs = Presentation()
            for title in ("Pengantar", "Data", "Kesimpulan"):
                slide = prs.slides.add_slide(prs.slide_layouts[5])
                slide.shapes.title.text = title
            prs.save(deck)
            prefix = os.path.join(tmp, "grid")
            r = _run([os.path.join(PPTX_SCRIPTS, "thumbnail.py"), deck, prefix, "--cols", "3"], timeout=400)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            out = prefix + ".jpg"
            self.assertTrue(os.path.isfile(out), f"grid tidak dibuat: {os.listdir(tmp)}")
            with Image.open(out) as img:
                self.assertGreater(img.width, 300)


@unittest.skipUnless(_has("docx"), "butuh python-docx")
class DocxSkillTests(unittest.TestCase):
    VALIDATE = os.path.join(DOCX_SCRIPTS, "office", "validate.py")

    def _make(self, tmp):
        from docx import Document

        path = os.path.join(tmp, "surat.docx")
        doc = Document()
        doc.add_heading("Laporan uji", level=1)
        doc.add_paragraph("Paragraf pertama untuk validasi.")
        doc.save(path)
        return path

    def test_validator_reports_schema_issue_in_default_template(self):
        # Temuan nyata: template default python-docx melewatkan atribut wajib pada settings.xml
        # (w:zoom tanpa w:percent). Validator upstream harus melaporkannya, bukan meloloskannya.
        with tempfile.TemporaryDirectory() as tmp:
            path = self._make(tmp)
            r = _run([self.VALIDATE, path])
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("settings.xml", r.stdout)

    def test_validator_rejects_corrupted_document(self):
        import zipfile

        with tempfile.TemporaryDirectory() as tmp:
            path = self._make(tmp)
            broken = os.path.join(tmp, "rusak.docx")
            with zipfile.ZipFile(path) as src, zipfile.ZipFile(broken, "w", zipfile.ZIP_DEFLATED) as dst:
                for item in src.infolist():
                    data = src.read(item.filename)
                    if item.filename == "word/document.xml":
                        data = data.replace(b"<w:body>", b"<w:body><w:bogusElement/>", 1)
                    dst.writestr(item, data)
            r = _run([self.VALIDATE, broken])
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("document.xml", r.stdout)


if __name__ == "__main__":
    unittest.main()
