"""Build the anonymous documentary and table PDFs for the public package."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).parents[1]
SOURCES = ROOT / "sources"
FONT = Path("C:/Windows/Fonts/arial.ttf")
FONT_BOLD = Path("C:/Windows/Fonts/arialbd.ttf")

if FONT.exists() and FONT_BOLD.exists():
    try:
        pdfmetrics.registerFont(TTFont("PublicSans", FONT))
        pdfmetrics.registerFont(TTFont("PublicSans-Bold", FONT_BOLD))
        FONT_NORMAL = "PublicSans"
        FONT_STRONG = "PublicSans-Bold"
    except Exception:
        FONT_NORMAL = "Helvetica"
        FONT_STRONG = "Helvetica-Bold"
else:
    FONT_NORMAL = "Helvetica"
    FONT_STRONG = "Helvetica-Bold"


def metadata(canvas, document):
    canvas.saveState()
    canvas.setAuthor("")
    canvas.setCreator("Pacote de dados anonimizado")
    canvas.setSubject("Material científico para revisão por pares")
    canvas.restoreState()


styles = getSampleStyleSheet()
TITLE = ParagraphStyle(
    "PublicTitle",
    parent=styles["Title"],
    fontName=FONT_STRONG,
    fontSize=16,
    leading=20,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#183B4E"),
    spaceAfter=8 * mm,
)
SUBTITLE = ParagraphStyle(
    "PublicSubtitle",
    parent=styles["Heading2"],
    fontName=FONT_STRONG,
    fontSize=11,
    leading=14,
    textColor=colors.HexColor("#183B4E"),
    spaceBefore=4 * mm,
    spaceAfter=2 * mm,
)
BODY = ParagraphStyle(
    "PublicBody",
    parent=styles["BodyText"],
    fontName=FONT_NORMAL,
    fontSize=9.5,
    leading=14,
    alignment=TA_JUSTIFY,
    spaceAfter=2.5 * mm,
)
NOTE = ParagraphStyle(
    "PublicNote",
    parent=BODY,
    fontSize=8.3,
    leading=11,
    textColor=colors.HexColor("#37474F"),
)


def document(path: Path, title: str, pagesize=A4, margins=18 * mm):
    return SimpleDocTemplate(
        str(path),
        pagesize=pagesize,
        rightMargin=margins,
        leftMargin=margins,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title=title,
        author="",
        creator="Pacote de dados anonimizado",
    )


def build_table_3a():
    rows = [
        ("E01", 14, 50), ("E02", 15, 40), ("E03", 12, 37),
        ("E04", 17, 25), ("E05", 20, 19), ("E06", 17, 20),
        ("E07", 14, 22), ("E08", 17, 15), ("E09", 11, 20),
        ("E10", 14, 13), ("E11", 15, 12), ("E12", 10, 15),
        ("E13", 12, 12), ("E14", 14, 10), ("E15", 7, 8),
        ("E16", 7, 6), ("E17", 0, 10), ("E18", 6, 1),
    ]
    data = [["Agrupamento", "Eventos", "Porta a porta", "Total", "Ambas as interfaces"]]
    for code, event, door in rows:
        data.append([code, event, door, event + door, "Sim" if event and door else "Não"])
    data.append(["Total", sum(r[1] for r in rows), sum(r[2] for r in rows), 557, "17/18 (94,4%)"])

    target = ROOT / "Tabela 3-A - Sobreposicao entre agrupamentos e interface.pdf"
    doc = document(target, "Tabela 3-A - Sobreposição entre agrupamentos e interface", landscape(A4), 14 * mm)
    story = [
        Paragraph("Tabela 3-A - Sobreposição entre agrupamentos de entrevistador e interface", TITLE),
        Paragraph(
            "Diagnóstico da estrutura de agrupamento usada na covariância sanduíche dos modelos ajustados. "
            "Os códigos E01-E18 são pseudônimos opacos, sem chave nominal no pacote público.",
            BODY,
        ),
    ]
    table = Table(data, colWidths=[38 * mm, 30 * mm, 38 * mm, 28 * mm, 50 * mm], repeatRows=1)
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), FONT_NORMAL),
        ("FONTNAME", (0, 0), (-1, 0), FONT_STRONG),
        ("FONTNAME", (0, -1), (-1, -1), FONT_STRONG),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("LEADING", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCEAF0")),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#EEF4F6")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#183B4E")),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#7A8B93")),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, colors.HexColor("#F7FAFB")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
    ]))
    story.extend([
        table,
        Spacer(1, 4 * mm),
        Paragraph(
            "Fonte: regeneração da base analítica pública desidentificada. Denominadores: 222 registros em eventos e "
            "335 em coleta porta a porta/distrital. Dez formulários sem conteúdo substantivo foram excluídos antes desta contagem.",
            NOTE,
        ),
        Paragraph(
            "Nota de anonimização: o arquivo não contém nomes, contatos, microterritórios ou correspondência entre código e pessoa.",
            NOTE,
        ),
    ])
    doc.build(story, onFirstPage=metadata, onLaterPages=metadata)


def build_methodological_supplement():
    target = ROOT / "material_metodologico_complementar.pdf"
    doc = document(target, "Material metodológico complementar")
    rows = [
        ["Componente", "Tratamento público", "Limitação"],
        ["Indicadores", "Variáveis binárias e agregadas, com códigos opacos.", "Não permitem localizar pessoas ou áreas pequenas."],
        ["Interfaces", "Comparação entre coleta em espaços públicos e abordagem domiciliar.", "Diferenças são descritivas, não causais."],
        ["Calendário", "Atividade realizada em janeiro de 2026.", "Datas detalhadas não são publicadas."],
        ["Participação comunitária", "Indicador binário de participação informada.", "Não permite inferir grupos, entidades ou vínculos."],
        ["Privacidade", "Dados reduzidos, sem texto livre ou identificadores diretos.", "Combinações raras permanecem sujeitas a risco residual."],
    ]
    table = Table(
        [[Paragraph(str(cell), NOTE) for cell in row] for row in rows],
        colWidths=[43 * mm, 67 * mm, 67 * mm],
        repeatRows=1,
    )
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), FONT_STRONG),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCEAF0")),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#7A8B93")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFB")]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story = [
        Paragraph("Material metodológico complementar", TITLE),
        Paragraph(
            "Síntese pública dos procedimentos usados na operação territorial de diagnóstico socioambiental. "
            "Esta versão substitui materiais originais e não contém nomes de locais, pessoas, organizações ou calendários detalhados.",
            BODY,
        ),
        table,
    ]
    doc.build(story, onFirstPage=metadata, onLaterPages=metadata)


def build_methodological_notes():
    SOURCES.mkdir(parents=True, exist_ok=True)
    target = SOURCES / "notas_metodologicas_anonimizadas.pdf"
    doc = document(target, "Notas metodológicas anonimizadas")
    story = [
        Paragraph("Notas metodológicas anonimizadas", TITLE),
        Paragraph("Finalidade e escopo", SUBTITLE),
        Paragraph(
            "Este documento preserva somente evidências metodológicas compatíveis com a operação territorial de diagnóstico socioambiental realizada no Município A, no norte de Minas Gerais. "
            "Os materiais originais permanecem fora do pacote público por conterem identificadores, itinerários, descrições sensíveis e metadados autorais.",
            BODY,
        ),
        Paragraph("Cronologia relevante para a classificação da interface", SUBTITLE),
        Paragraph(
            "A atividade de campo ocorreu em janeiro de 2026. Foram utilizadas interfaces em espaços públicos e em abordagens domiciliares. "
            "A classificação usada no pipeline analítico preserva apenas as categorias de interface, sem calendário detalhado.",
            BODY,
        ),
        Paragraph("Mudança de estratégia", SUBTITLE),
        Paragraph(
            "A abordagem domiciliar foi considerada mais contextual e propícia à conversa do que a aplicação em locais de circulação pública. "
            "Essa percepção é tratada como evidência qualitativa situada: ela ajuda a formular mecanismos plausíveis de seleção e resposta, mas não demonstra que a interface causou as diferenças observadas.",
            BODY,
        ),
        Paragraph("Fricção do esquema", SUBTITLE),
        Paragraph(
            "A documentação metodológica indica que a pergunta sobre canais de informação não oferecia uma opção específica para redes sociais. A observação motivou a auditoria da categoria residual 'outro'. "
            "O percentual residual não é reinterpretado retrospectivamente como prevalência de uso de redes sociais; ele é evidência de perda de especificidade semântica do instrumento.",
            BODY,
        ),
        Paragraph("Caso sentinela de saneamento", SUBTITLE),
        Paragraph(
            "Registros de campo sobre esgotamento, resíduos e diferenças territoriais justificaram a escolha de saneamento como caso documental sentinela. As observações não são medidas técnicas de infraestrutura, qualidade da água ou prevalência municipal e devem ser trianguladas com registros administrativos e verificação especializada.",
            BODY,
        ),
        Paragraph("Limitações documentais", SUBTITLE),
        Paragraph(
            "As notas foram produzidas após uma operação de curta duração e não seguiram um protocolo padronizado de observação qualitativa. Elas combinam experiência direta, sínteses operacionais e relatos de terceiros. "
            "Por isso, é usado para documentar o processo de coleta e gerar perguntas analíticas, não como retrato objetivo da população nem como prova de causalidade.",
            BODY,
        ),
        Paragraph(
            "Referência cega: NOTAS METODOLÓGICAS ANONIMIZADAS. Documento de apoio referente à operação territorial de diagnóstico socioambiental realizada no Município A, no norte de Minas Gerais, em janeiro de 2026.",
            NOTE,
        ),
    ]
    doc.build(story, onFirstPage=metadata, onLaterPages=metadata)


def build_scientific_notes():
    target = SOURCES / "notas_cientificas_anonimizadas.pdf"
    doc = document(target, "Notas científicas anonimizadas e matriz de argumentos")
    rows = [
        ["Argumento", "Base científica", "Uso responsável no estudo"],
        ["Erro total de pesquisa", "Cobertura, seleção, não resposta, mensuração e processamento podem alterar a representação observada.", "Interpretar diferenças entre interfaces como relações compostas, sem isolar mecanismo causal."],
        ["Sistema sociotécnico", "Dados resultam conjuntamente de pessoas, processos, tecnologia e organização.", "Auditar coleta, esquema e percurso institucional, não apenas consistência do banco."],
        ["Validade de mensuração", "Campos e categorias definem quais fenômenos podem ser expressos de forma estruturada.", "Tratar a categoria residual como diagnóstico de esquema, não imputar retrospectivamente seu conteúdo."],
        ["Proveniência", "A rastreabilidade conecta origem, transformação, indicador e uso decisório.", "Distinguir existência de programa/orçamento de evidência explícita sobre a fonte territorial que o informou."],
        ["Privacidade", "Remover identificadores diretos não elimina todo risco de ligação por combinações raras.", "Publicar códigos opacos, dados reduzidos, agregações e uma auditoria explícita de risco residual."],
    ]
    table = Table(
        [[Paragraph(str(cell), NOTE) for cell in row] for row in rows],
        colWidths=[39 * mm, 66 * mm, 66 * mm],
        repeatRows=1,
    )
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), FONT_STRONG),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCEAF0")),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#7A8B93")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFB")]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    refs = [
        "Bostrom, R. P.; Heinen, J. S. MIS problems and failures: a socio-technical perspective. MIS Quarterly, 1977. DOI: 10.2307/248710.",
        "Bowker, G. C.; Star, S. L. Sorting Things Out: Classification and Its Consequences. MIT Press, 1999.",
        "Buneman, P.; Khanna, S.; Tan, W.-C. Why and where: a characterization of data provenance. ICDT, 2001. DOI: 10.1007/3-540-44503-X_20.",
        "Cheney, J.; Chiticariu, L.; Tan, W.-C. Provenance in databases: why, how, and where. Foundations and Trends in Databases, 2009. DOI: 10.1561/1900000006.",
        "Gebru, T. et al. Datasheets for datasets. Communications of the ACM, 2021. DOI: 10.1145/3458723.",
        "Groves, R. M. et al. Survey Methodology. 2nd ed. Wiley, 2009.",
        "Jacobs, A. Z.; Wallach, H. Measurement and fairness. FAccT, 2021. DOI: 10.1145/3442188.3445901.",
        "Moreau, L.; Missier, P. (eds.). PROV-DM: The PROV Data Model. W3C Recommendation, 2013.",
        "Selbst, A. D. et al. Fairness and abstraction in sociotechnical systems. FAT*, 2019. DOI: 10.1145/3287560.3287598.",
        "von Elm, E. et al. The STROBE statement. PLoS Medicine, 2007. DOI: 10.1371/journal.pmed.0040296.",
    ]
    story = [
        Paragraph("Notas científicas anonimizadas e matriz de argumentos", TITLE),
        Paragraph(
            "Síntese sanitizada dos fundamentos reaproveitáveis identificados nas versões anteriores do trabalho. Este arquivo não é uma versão do artigo e não contém autoria, afiliação, ORCID, e-mail ou endereço de projeto.",
            BODY,
        ),
        table,
        Spacer(1, 5 * mm),
        Paragraph("Referências científicas selecionadas", SUBTITLE),
    ]
    story.extend(Paragraph(reference, BODY) for reference in refs)
    story.extend([
        Paragraph("Critérios de exclusão", SUBTITLE),
        Paragraph(
            "Foram excluídos índices exploratórios sem validação institucional, recomendações programáticas não testadas, versões antigas do manuscrito, telas com endereço identificador e afirmações locais que não possuíam fonte documental independente.",
            BODY,
        ),
        Paragraph(
            "Proveniência: síntese derivada de documento acadêmico anterior mantido fora do repositório por conter autoria, afiliações, identificadores persistentes e contatos. Apenas argumentos e referências verificáveis foram preservados.",
            NOTE,
        ),
    ])
    doc.build(story, onFirstPage=metadata, onLaterPages=metadata)


if __name__ == "__main__":
    build_table_3a()
    build_methodological_supplement()
    build_methodological_notes()
    build_scientific_notes()
