"""Regenerate manuscript statistics from the local XLSX source."""

from __future__ import annotations

import re
import unicodedata
from datetime import datetime
import json
import math
from pathlib import Path
from statistics import NormalDist
from typing import Any, Iterable, Mapping, Optional

import numpy as np
import pandas as pd


def normalize_text(value: Any) -> str:
    """Return a canonical lower-case, accent-free text label."""
    if value is None:
        return ""
    text = unicodedata.normalize("NFKD", str(value))
    text = "".join(char for char in text if not unicodedata.combining(char))
    return re.sub(r"\s+", " ", text).strip().lower()


def classify_interface(submission_time: Any) -> Optional[str]:
    """Classify January 2026 records by the documented collection windows."""
    if submission_time is None:
        return None
    parsed = datetime.fromisoformat(str(submission_time).replace("Z", "+00:00"))
    if parsed.year != 2026 or parsed.month != 1:
        return None
    if parsed.day <= 17:
        return "evento"
    if parsed.day >= 19:
        return "porta_a_porta"
    return None


def row_has_substantive_answer(
    row: Mapping[str, Any], substantive_columns: Iterable[str]
) -> bool:
    """Return whether a record answers at least one substantive questionnaire item."""
    for column in substantive_columns:
        value = row.get(column)
        if value is not None and str(value).strip() != "":
            return True
    return False


def assign_ranked_codes(values: pd.Series, prefix: str) -> pd.Series:
    """Replace labels with deterministic frequency-ranked anonymous codes.

    Ties are resolved by normalized label only during the private transformation;
    the correspondence table is never written to the public package.
    """
    normalized = values.map(normalize_text).replace("", pd.NA)
    counts = normalized.value_counts(dropna=True)
    ordered = sorted(counts.index, key=lambda label: (-int(counts[label]), label))
    mapping = {
        label: f"{prefix}{position:02d}"
        for position, label in enumerate(ordered, start=1)
    }
    return normalized.map(mapping).astype("string")


def regenerate(source: Path, output: Path) -> dict[str, Any]:
    """Regenerate the public report from the desidentified analytic CSV."""
    if source.suffix.lower() == ".csv":
        return regenerate_public(source, output)
    raise ValueError(
        "The public pipeline accepts only public_analytic_data.csv; "
        "the identifiable workbook is intentionally outside the review package."
    )


def regenerate_public(source: Path, output: Path) -> dict[str, Any]:
    """Write all public statistics from the reduced analytic dataset."""
    frame = pd.read_csv(source)
    january = frame.loc[frame["wave"].eq("janeiro_2026")].copy()
    july = frame.loc[frame["wave"].eq("julho_2026")].copy()
    studies = _run_public_studies(january, july)
    report = {
        "provenance": {
            "source": source.name,
            "public_records": int(len(frame)),
            "january_valid_records": int(len(january)),
            "january_event_records": int((january["interface"] == "evento").sum()),
            "january_door_to_door_records": int(
                (january["interface"] == "porta_a_porta").sum()
            ),
            "july_records": int(len(july)),
        },
        "descriptive": _descriptive(january),
        "studies": studies,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def _regenerate_private_workbook(source: Path, output: Path) -> dict[str, Any]:
    """Private compatibility helper; not called by the public interface."""
    frame = pd.read_excel(source)
    submitted = pd.to_datetime(frame["_submission_time"], errors="coerce")
    january = frame.loc[(submitted.dt.year == 2026) & (submitted.dt.month == 1)].copy()
    january["_submitted_at"] = submitted.loc[january.index]
    substantive_columns = list(frame.columns[6:179])
    january["_valid"] = january[substantive_columns].notna().any(axis=1)
    january["interface"] = january["_submitted_at"].map(classify_interface)
    analytic = january.loc[january["_valid"] & january["interface"].notna()]
    studies = _run_studies(frame, submitted, analytic)
    report = {
        "provenance": {
            "source": source.name,
            "source_records": int(len(frame)),
            "january_raw_records": int(len(january)),
            "january_empty_records": int((~january["_valid"]).sum()),
            "january_valid_records": int(len(analytic)),
            "january_event_records": int((analytic["interface"] == "evento").sum()),
            "january_door_to_door_records": int(
                (analytic["interface"] == "porta_a_porta").sum()
            ),
        },
        "descriptive": _descriptive(_derive(analytic, analytic["_submitted_at"])),
        "studies": studies,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


NORMAL = NormalDist()


class Columns:
    """Stable positions from the exported Kobo workbook, documented in README."""

    HOUSEHOLD_SIZE = 6
    ELDERLY = 7
    UNEMPLOYED = 10
    BENEFITS = 11
    RETIREMENT = 12
    BOLSA_FAMILIA = 14
    BPC = 15
    OTHER_BENEFIT = 18
    CADUNICO = 21
    COMMERCE = 22
    INCOME = 23
    HOUSING_RISK = 44
    HOUSING_RISK_ANY = (46, 47, 48, 49, 50)
    ACCESS = 52
    WATER_NETWORK = 54
    ELECTRIC_NETWORK = 62
    SEWER_NETWORK = 69
    SEPTIC = 71
    MUNICIPAL_TRASH = 76
    BURNING = 79
    WASTE_SEPARATION = 84
    RECYCLING = 85
    GARDEN = 43
    MANUAL_SKILL = 94
    MANUAL_SKILL_NONE = 95
    ARTISTIC_SKILL = 106
    ARTISTIC_SKILL_NONE = 107
    HEALTH = 116
    HEALTH_NONE = 117
    HYPERTENSION = 118
    DIABETES = 119
    CONTROLLED_MEDICINE = 130
    CIGARETTE = 126
    ALCOHOL = 128
    PHYSICAL_DISABILITY = 134
    MENTAL_DISABILITY = 135
    DOMESTIC_VIOLENCE = 136
    COMMUNITY_ENGAGEMENT = 139
    SOCIAL_PROJECT = 162
    IMPROVEMENT_REQUEST = 163
    NEWS_OTHER = 159
    TERRITORY = 4
    INTERVIEWER = 180


def _column(frame: pd.DataFrame, position: int) -> str:
    return str(frame.columns[position])


def _binary(frame: pd.DataFrame, position: int) -> pd.Series:
    values = pd.to_numeric(frame.iloc[:, position], errors="coerce")
    return values.where(values.isna(), (values > 0).astype(float))


def _text_answer(frame: pd.DataFrame, position: int) -> pd.Series:
    raw = frame.iloc[:, position]
    cleaned = raw.map(normalize_text)
    missing = raw.isna() | cleaned.eq("") | cleaned.str.contains("nao sabe", na=False)
    return cleaned.where(~missing)


def _yes_no(frame: pd.DataFrame, position: int) -> pd.Series:
    answer = _text_answer(frame, position)
    return answer.map(lambda value: np.nan if pd.isna(value) else float(not value.startswith("nao")))


def _territory(value: Any) -> Optional[str]:
    label = normalize_text(value)
    return label.upper() if re.fullmatch(r"t\d{2}", label) else None


def _interviewer(value: Any) -> str:
    label = normalize_text(value)
    return label.upper() if re.fullmatch(r"e\d{2}", label) else "Nao informado"


def _derive(frame: pd.DataFrame, submitted: pd.Series) -> pd.DataFrame:
    data = frame.copy()
    data["_submitted_at"] = submitted
    data["interface"] = submitted.map(classify_interface)
    data["territory"] = data.iloc[:, Columns.TERRITORY].map(_territory)
    data["interviewer"] = data.iloc[:, Columns.INTERVIEWER].map(_interviewer)
    data["submission_hour"] = submitted.dt.hour.astype(float)
    data["septic"] = _binary(data, Columns.SEPTIC)
    data["sewer_network"] = _binary(data, Columns.SEWER_NETWORK)
    data["municipal_trash"] = _binary(data, Columns.MUNICIPAL_TRASH)
    data["burning"] = _binary(data, Columns.BURNING)
    data["water_network"] = _binary(data, Columns.WATER_NETWORK)
    data["electric_network"] = _binary(data, Columns.ELECTRIC_NETWORK)
    data["waste_separation"] = _yes_no(data, Columns.WASTE_SEPARATION)
    data["recycling"] = _yes_no(data, Columns.RECYCLING)
    data["cadunico"] = _yes_no(data, Columns.CADUNICO)
    data["commerce"] = _yes_no(data, Columns.COMMERCE)
    data["garden"] = _yes_no(data, Columns.GARDEN)
    data["manual_skill"] = _binary(data, Columns.MANUAL_SKILL_NONE).map(
        lambda value: np.nan if pd.isna(value) else 1.0 - value
    )
    data["artistic_skill"] = _binary(data, Columns.ARTISTIC_SKILL_NONE).map(
        lambda value: np.nan if pd.isna(value) else 1.0 - value
    )
    data["community_engagement"] = _yes_no(data, Columns.COMMUNITY_ENGAGEMENT)
    data["health_problem"] = _binary(data, Columns.HEALTH_NONE).map(
        lambda value: np.nan if pd.isna(value) else 1.0 - value
    )
    data["hypertension"] = _binary(data, Columns.HYPERTENSION)
    data["diabetes"] = _binary(data, Columns.DIABETES)
    data["domestic_violence"] = _yes_no(data, Columns.DOMESTIC_VIOLENCE)
    data["controlled_medicine"] = _binary(data, Columns.CONTROLLED_MEDICINE)
    data["cigarette"] = _binary(data, Columns.CIGARETTE)
    data["alcohol"] = _binary(data, Columns.ALCOHOL)
    data["physical_disability"] = _yes_no(data, Columns.PHYSICAL_DISABILITY)
    data["mental_disability"] = _yes_no(data, Columns.MENTAL_DISABILITY)
    data["social_project"] = _yes_no(data, Columns.SOCIAL_PROJECT)
    improvement = _text_answer(data, Columns.IMPROVEMENT_REQUEST)
    data["improvement_request"] = improvement.map(
        lambda value: np.nan if pd.isna(value) else float(not value.startswith("nenhum"))
    )
    data["news_other"] = _binary(data, Columns.NEWS_OTHER)
    income = _text_answer(data, Columns.INCOME)
    data["low_income"] = income.map(
        lambda value: np.nan
        if pd.isna(value)
        else float(value.startswith("menor") or value.startswith("igual"))
    )
    unemployed = _text_answer(data, Columns.UNEMPLOYED)
    data["unemployed"] = unemployed.map(
        lambda value: np.nan if pd.isna(value) else float(not value.startswith("nenhum"))
    )
    benefits = _text_answer(data, Columns.BENEFITS)
    benefit_columns = list(range(Columns.RETIREMENT, Columns.OTHER_BENEFIT + 1))
    benefit_components = pd.concat(
        [_binary(data, column) for column in benefit_columns], axis=1
    )
    data["benefit_or_retirement"] = benefit_components.max(
        axis=1, skipna=True
    ).where(benefits.notna())
    transfer_columns = list(range(Columns.BOLSA_FAMILIA, Columns.OTHER_BENEFIT + 1))
    transfer = pd.concat([_binary(data, column) for column in transfer_columns], axis=1)
    data["social_transfer"] = transfer.max(axis=1, skipna=True).where(benefits.notna())
    access = _text_answer(data, Columns.ACCESS)
    data["difficult_access"] = access.map(
        lambda value: np.nan
        if pd.isna(value)
        else float("terra" in value or "dificil" in value or "outro" in value)
    )
    risk = pd.concat([_binary(data, column) for column in Columns.HOUSING_RISK_ANY], axis=1)
    data["housing_risk"] = risk.max(axis=1, skipna=True)
    data["elderly"] = _text_answer(data, Columns.ELDERLY).map(
        lambda value: np.nan if pd.isna(value) else float(not value.startswith("nenhum"))
    )
    household = _text_answer(data, Columns.HOUSEHOLD_SIZE)
    data["household_size"] = household.map(_household_size)
    return data


def _household_size(value: Any) -> float:
    if value is None or pd.isna(value):
        return np.nan
    match = re.search(r"\d+", str(value))
    if not match:
        return np.nan
    return float(match.group())


def _proportion(series: pd.Series) -> dict[str, float | int]:
    observed = series.dropna()
    count = int(observed.sum())
    total = int(len(observed))
    return {"n": total, "count": count, "proportion": count / total if total else np.nan}


def _wilson(count: int, total: int, alpha: float = 0.05) -> tuple[float, float]:
    if not total:
        return (np.nan, np.nan)
    z = NORMAL.inv_cdf(1 - alpha / 2)
    p = count / total
    denom = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / denom
    margin = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denom
    return centre - margin, centre + margin


def _two_proportion(left: pd.Series, right: pd.Series) -> dict[str, float | int]:
    left_clean = left.dropna()
    right_clean = right.dropna()
    a, n_a = int(left_clean.sum()), int(len(left_clean))
    b, n_b = int(right_clean.sum()), int(len(right_clean))
    p_a, p_b = a / n_a, b / n_b
    pooled = (a + b) / (n_a + n_b)
    se = math.sqrt(pooled * (1 - pooled) * (1 / n_a + 1 / n_b))
    z = (p_b - p_a) / se if se else 0.0
    p_value = math.erfc(abs(z) / math.sqrt(2))
    low_a, high_a = _wilson(a, n_a)
    low_b, high_b = _wilson(b, n_b)
    return {
        "event_n": n_a,
        "event_proportion": p_a,
        "door_n": n_b,
        "door_proportion": p_b,
        "difference": p_b - p_a,
        "ci_low": low_b - high_a,
        "ci_high": high_b - low_a,
        "p": p_value,
        "cramers_v": math.sqrt(z * z / (n_a + n_b)),
    }


def _bh(values: list[float]) -> list[float]:
    size = len(values)
    order = sorted(range(size), key=lambda index: values[index])
    adjusted = [0.0] * size
    running = 1.0
    for rank in range(size, 0, -1):
        index = order[rank - 1]
        running = min(running, values[index] * size / rank)
        adjusted[index] = min(running, 1.0)
    return adjusted


def _design_matrix(data: pd.DataFrame, extras: list[str] | None = None) -> tuple[np.ndarray, list[str]]:
    columns = [np.ones(len(data)), (data["interface"] == "porta_a_porta").astype(float).to_numpy()]
    names = ["intercept", "interface_porta_a_porta"]
    for variable in ("territory", "interviewer"):
        categories = sorted(data[variable].astype(str).unique())
        for category in categories[1:]:
            columns.append((data[variable] == category).astype(float).to_numpy())
            names.append(variable + "=" + category)
    hour = data["submission_hour"].astype(float)
    columns.append((hour - hour.mean()).to_numpy())
    names.append("submission_hour_centered")
    for variable in extras or []:
        series = data[variable].astype(float)
        columns.append((series - series.mean()).to_numpy())
        names.append(variable + "_centered")
    return np.column_stack(columns), names


def _cluster_logit(data: pd.DataFrame, outcome: str, extras: list[str] | None = None) -> dict[str, Any]:
    required = [outcome, "interface", "territory", "interviewer", "submission_hour"] + (extras or [])
    model_data = data.dropna(subset=required).copy()
    y = model_data[outcome].astype(float).to_numpy()
    x, names = _design_matrix(model_data, extras)
    beta = np.zeros(x.shape[1])
    for _ in range(100):
        eta = np.clip(x @ beta, -30, 30)
        probability = 1 / (1 + np.exp(-eta))
        weights = np.clip(probability * (1 - probability), 1e-8, None)
        score = x.T @ (y - probability)
        information = x.T @ (weights[:, None] * x)
        update = np.linalg.pinv(information) @ score
        beta_next = beta + update
        if np.max(np.abs(beta_next - beta)) < 1e-8:
            beta = beta_next
            break
        beta = beta_next
    probability = 1 / (1 + np.exp(-np.clip(x @ beta, -30, 30)))
    weights = np.clip(probability * (1 - probability), 1e-8, None)
    bread = np.linalg.pinv(x.T @ (weights[:, None] * x))
    meat = np.zeros((x.shape[1], x.shape[1]))
    for _, group in model_data.groupby("interviewer", sort=False):
        positions = group.index
        row_index = model_data.index.get_indexer(positions)
        score = x[row_index].T @ (y[row_index] - probability[row_index])
        meat += np.outer(score, score)
    cluster_count = int(model_data["interviewer"].nunique())
    correction = 1.0
    if cluster_count > 1 and len(model_data) > x.shape[1]:
        correction = cluster_count / (cluster_count - 1) * (len(model_data) - 1) / (len(model_data) - x.shape[1])
    covariance = correction * bread @ meat @ bread
    position = names.index("interface_porta_a_porta")
    estimate = float(beta[position])
    std_error = float(math.sqrt(max(covariance[position, position], 0)))
    z = estimate / std_error if std_error else np.nan
    return {
        "n": int(len(model_data)),
        "clusters": cluster_count,
        "or": math.exp(estimate),
        "ci_low": math.exp(estimate - 1.96 * std_error),
        "ci_high": math.exp(estimate + 1.96 * std_error),
        "p": math.erfc(abs(z) / math.sqrt(2)) if not math.isnan(z) else np.nan,
        "converged": True,
    }


STUDY_1_OUTCOMES = [
    ("septic", "Fossa"),
    ("sewer_network", "Rede publica de esgoto"),
    ("benefit_or_retirement", "Algum beneficio ou aposentadoria"),
    ("social_transfer", "Transferencia social"),
    ("low_income", "Renda ate R$ 1.500"),
    ("unemployed", "Ao menos um adulto desempregado"),
    ("cadunico", "Inscricao no CadUnico"),
    ("difficult_access", "Acesso dificil"),
    ("health_problem", "Problema de saude"),
    ("community_engagement", "Participacao comunitaria"),
    ("manual_skill", "Habilidade manual"),
    ("housing_risk", "Algum risco habitacional"),
    ("domestic_violence", "Violencia domestica"),
    ("waste_separation", "Separacao de residuos"),
    ("hypertension", "Hipertensao"),
    ("recycling", "Reaproveitamento de reciclaveis"),
    ("artistic_skill", "Habilidade artistica"),
    ("water_network", "Agua de rede publica"),
    ("burning", "Queima de residuos"),
    ("diabetes", "Diabetes"),
]


def _study_1(january: pd.DataFrame) -> dict[str, Any]:
    event = january.loc[january["interface"] == "evento"]
    door = january.loc[january["interface"] == "porta_a_porta"]
    rows = []
    for column, label in STUDY_1_OUTCOMES:
        row = _two_proportion(event[column], door[column])
        row.update({"outcome": column, "label": label})
        rows.append(row)
    q_values = _bh([float(row["p"]) for row in rows])
    for row, q_value in zip(rows, q_values):
        row["q"] = q_value
    return {"comparisons": rows}


def _descriptive(january: pd.DataFrame) -> dict[str, Any]:
    selected = [
        ("low_income", "Renda ate R$ 1.500"),
        ("unemployed", "Ao menos um adulto desempregado"),
        ("cadunico", "Inscricao no CadUnico"),
        ("social_transfer", "Transferencia social"),
        ("benefit_or_retirement", "Algum beneficio ou aposentadoria"),
        ("water_network", "Agua de rede publica"),
        ("sewer_network", "Rede publica de esgoto"),
        ("septic", "Fossa"),
        ("municipal_trash", "Coleta municipal de residuos"),
        ("burning", "Queima de residuos"),
        ("waste_separation", "Separacao de residuos"),
        ("health_problem", "Problema de saude no domicilio"),
        ("hypertension", "Hipertensao"),
        ("diabetes", "Diabetes"),
    ]
    return {
        column: {"label": label, **_proportion(january[column])}
        for column, label in selected
    }


def _study_2(january: pd.DataFrame) -> dict[str, Any]:
    common = january.loc[january["territory"].notna()].copy()
    outcomes = STUDY_1_OUTCOMES[:6]
    results = []
    for outcome, label in outcomes:
        result = _cluster_logit(common, outcome)
        result.update({"outcome": outcome, "label": label})
        results.append(result)
    return {
        "model": "logit(outcome ~ interface + territory + interviewer + submission_hour)",
        "sample": "five normalized territories with support in both interfaces",
        "standard_errors": "sandwich covariance clustered by normalized interviewer",
        "results": results,
    }


def _rank(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(len(values), dtype=float)
    start = 0
    while start < len(values):
        end = start + 1
        while end < len(values) and values[order[end]] == values[order[start]]:
            end += 1
        ranks[order[start:end]] = (start + 1 + end) / 2
        start = end
    return ranks


def _pearson(left: np.ndarray, right: np.ndarray) -> float:
    if len(left) < 3:
        return np.nan
    return float(np.corrcoef(left, right)[0, 1])


def _mean_with_minimum(data: pd.DataFrame, minimum: int) -> pd.Series:
    """Mean rows only when the documented minimum item count is observed."""
    mean = data.mean(axis=1)
    return mean.where(data.notna().sum(axis=1) >= minimum)


def _study_3(january: pd.DataFrame, july: pd.DataFrame) -> dict[str, Any]:
    outcomes = STUDY_1_OUTCOMES + [
        ("municipal_trash", "Coleta municipal de residuos"),
        ("garden", "Horta"),
        ("news_other", "Outro como canal de informacao"),
    ]
    rows = []
    for column, label in outcomes:
        comparison = _two_proportion(january[column], july[column])
        comparison.update({"outcome": column, "label": label})
        rows.append(comparison)
    q_values = _bh([float(row["p"]) for row in rows])
    for row, q_value in zip(rows, q_values):
        row["q"] = q_value
    jan_values = np.array([row["event_proportion"] for row in rows], dtype=float)
    jul_values = np.array([row["door_proportion"] for row in rows], dtype=float)
    return {
        "n_january": int(len(january)),
        "n_july": int(len(july)),
        "pearson": _pearson(jan_values, jul_values),
        "spearman": _pearson(_rank(jan_values), _rank(jul_values)),
        "mean_absolute_difference": float(np.mean(np.abs(jul_values - jan_values))),
        "comparisons": rows,
    }


def _mvce_r(january: pd.DataFrame) -> dict[str, Any]:
    data = january.copy()
    vulnerable_domains = pd.DataFrame(
        {
            "economy": _mean_with_minimum(data[["low_income", "unemployed", "cadunico", "social_transfer"]], 2),
            "housing_mobility": _mean_with_minimum(data[["housing_risk", "difficult_access"]], 1),
            "sanitation_utilities": _mean_with_minimum(pd.DataFrame(
                {
                    "no_water": 1 - data["water_network"],
                    "no_sewer": 1 - data["sewer_network"],
                    "burning": data["burning"],
                    "no_electricity": 1 - data["electric_network"],
                }
            ), 2),
            "health_exposure": _mean_with_minimum(data[[
                "health_problem", "controlled_medicine", "cigarette", "alcohol",
                "physical_disability", "mental_disability", "domestic_violence",
            ]], 3),
        }
    )
    capacity_domains = pd.DataFrame(
        {
            "productive": _mean_with_minimum(data[["commerce", "manual_skill", "artistic_skill"]], 2),
            "socioenvironmental": _mean_with_minimum(data[["garden", "waste_separation", "recycling"]], 2),
            "collective_civic": _mean_with_minimum(data[["community_engagement", "social_project", "improvement_request"]], 2),
        }
    )
    data["vulnerability"] = vulnerable_domains.mean(axis=1)
    data["capacity"] = capacity_domains.mean(axis=1)
    complete = data.dropna(subset=["vulnerability", "capacity"])
    threshold = complete["vulnerability"].quantile(0.75)
    high = complete.loc[complete["vulnerability"] >= threshold]
    rng = np.random.default_rng(20260823)
    vulnerability_rank_correlations = []
    capacity_rank_correlations = []
    for _ in range(5000):
        v_weights = rng.dirichlet(np.ones(vulnerable_domains.shape[1]))
        c_weights = rng.dirichlet(np.ones(capacity_domains.shape[1]))
        v_score = vulnerable_domains.loc[complete.index].to_numpy() @ v_weights
        c_score = capacity_domains.loc[complete.index].to_numpy() @ c_weights
        vulnerability_rank_correlations.append(_pearson(_rank(complete["vulnerability"].to_numpy()), _rank(v_score)))
        capacity_rank_correlations.append(_pearson(_rank(complete["capacity"].to_numpy()), _rank(c_score)))
    return {
        "domain_rules": {
            "vulnerability_economy": 2,
            "vulnerability_housing_mobility": 1,
            "vulnerability_sanitation_utilities": 2,
            "vulnerability_health_exposure": 3,
            "capacity_productive": 2,
            "capacity_socioenvironmental": 2,
            "capacity_collective_civic": 2,
        },
        "n": int(len(complete)),
        "pearson": _pearson(complete["vulnerability"].to_numpy(), complete["capacity"].to_numpy()),
        "high_vulnerability_n": int(len(high)),
        "high_vulnerability_any_capacity": float((high["capacity"] > 0).mean()),
        "high_vulnerability_capacity_mean": float(high["capacity"].mean()),
        "weight_sensitivity_median_spearman_vulnerability": float(np.median(vulnerability_rank_correlations)),
        "weight_sensitivity_median_spearman_capacity": float(np.median(capacity_rank_correlations)),
    }


def _run_studies(frame: pd.DataFrame, submitted: pd.Series, analytic: pd.DataFrame) -> dict[str, Any]:
    january_data = _derive(analytic, analytic["_submitted_at"])
    july_mask = (submitted.dt.year == 2026) & (submitted.dt.month == 7)
    july_raw = frame.loc[july_mask].copy()
    july_submitted = submitted.loc[july_mask]
    july_data = _derive(july_raw, july_submitted)
    study_1 = _study_1(january_data)
    study_2 = _study_2(january_data)
    study_3 = _study_3(january_data, july_data)
    study_4 = {
        "january": _proportion(january_data["news_other"]),
        "july": _proportion(july_data["news_other"]),
    }
    septic_health = _cluster_logit(
        january_data.loc[january_data["territory"].notna()],
        "health_problem",
        extras=["septic", "elderly", "household_size", "low_income"],
    )
    return {
        "study_1": study_1,
        "study_2": study_2,
        "study_3": study_3,
        "study_4": study_4,
        "mvce_r": _mvce_r(january_data),
        "septic_health": septic_health,
    }


def _run_public_studies(january_data: pd.DataFrame, july_data: pd.DataFrame) -> dict[str, Any]:
    """Run the documented studies on already-derived, anonymous columns."""
    study_1 = _study_1(january_data)
    study_2 = _study_2(january_data)
    study_3 = _study_3(january_data, july_data)
    study_4 = {
        "january": _proportion(january_data["news_other"]),
        "july": _proportion(july_data["news_other"]),
    }
    septic_health = _cluster_logit(
        january_data.loc[january_data["territory"].notna()],
        "health_problem",
        extras=["septic", "elderly", "household_size", "low_income"],
    )
    return {
        "study_1": study_1,
        "study_2": study_2,
        "study_3": study_3,
        "study_4": study_4,
        "mvce_r": _mvce_r(january_data),
        "septic_health": septic_health,
    }
