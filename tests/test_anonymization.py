import re
import unittest
from pathlib import Path

import pandas as pd

from analysis.regenerate_analysis import assign_ranked_codes


ROOT = Path(__file__).parents[1]


class AnonymousPublicationTest(unittest.TestCase):
    def test_ranked_codes_are_stable_and_do_not_preserve_labels(self):
        labels = pd.Series(["Pessoa Alfa", "Pessoa Beta", "Pessoa Alfa", "Pessoa Gama"])
        coded = assign_ranked_codes(labels, prefix="E")

        self.assertEqual(coded.tolist(), ["E01", "E02", "E01", "E03"])
        self.assertFalse(any("pessoa" in value.lower() for value in coded))

    def test_public_dataset_has_only_approved_columns_and_codes(self):
        dataset = ROOT / "analysis" / "public_analytic_data.csv"
        self.assertTrue(dataset.exists(), "a base analítica pública deve ser gerada")
        frame = pd.read_csv(dataset)

        forbidden_fragments = ("nome", "contato", "email", "uuid", "telefone", "coorden")
        self.assertFalse(
            any(fragment in column.lower() for column in frame.columns for fragment in forbidden_fragments)
        )
        self.assertTrue(frame["interviewer"].dropna().str.fullmatch(r"E\d{2}").all())
        self.assertTrue(frame["territory"].dropna().str.fullmatch(r"T\d{2}").all())

        text = "\n".join(frame.select_dtypes(include=["object", "string"]).fillna("").astype(str).stack())
        self.assertIsNone(re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", text))
        self.assertIsNone(
            re.search(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", text, re.I)
        )

    def test_synthetic_interviewers_are_codes(self):
        workbook = ROOT / "analysis" / "synthetic_data.xlsx"
        frame = pd.read_excel(workbook)
        values = frame.iloc[:, 180].dropna().astype(str)
        self.assertTrue(values.str.fullmatch(r"E\d{2}").all())

    def test_public_source_does_not_contain_a_nominal_alias_table(self):
        source = (ROOT / "analysis" / "regenerate_analysis.py").read_text(encoding="utf-8")
        self.assertNotIn("INTERVIEWER_ALIASES", source)
        self.assertNotRegex(source, r"Outro rotulo:")


if __name__ == "__main__":
    unittest.main()
