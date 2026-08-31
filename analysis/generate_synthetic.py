import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def main():
    # Number of records to generate
    N = 20
    
    # Create empty dataframe with 185 columns to be safe
    # We name them "col0", "col1", etc., except for specific required named columns
    cols = [f"col{i}" for i in range(185)]
    
    # regenerate_analysis.py requires a column named '_submission_time'
    # Actually, let's just make the 5th column '_submission_time' to simulate some position
    cols[5] = "_submission_time"
    
    df = pd.DataFrame(index=range(N), columns=cols)
    
    # 1. Submission Time (Mix of January 2026, some before 17th - evento, some after 19th - porta_a_porta)
    # Let's generate dates: 
    # 10 records for "evento" (Jan 10, 2026)
    # 10 records for "porta_a_porta" (Jan 20, 2026)
    jan_evento = "2026-01-10T14:30:00Z"
    jan_porta = "2026-01-20T09:15:00Z"
    
    df.loc[0:9, "_submission_time"] = jan_evento
    df.loc[10:19, "_submission_time"] = jan_porta
    
    # 2. Fill specific columns accessed by index in regenerate_analysis.Columns
    
    # col 4: TERRITORY
    territories = ["T01", "T01", "T02", "T02", "T03", "T03", "T04", "T04", "T05", None]
    df.iloc[:, 4] = np.tile(territories, 2)
    
    # col 6: HOUSEHOLD_SIZE
    df.iloc[:, 6] = ["3", "Moro eu e mais 2", "1 pessoa", "4", "5", "Nenhum", "2", "6", "10", "3"] * 2
    
    # col 7: ELDERLY
    df.iloc[:, 7] = ["Nenhum", "1", "2 idosos", "Nenhum", "1", "3", "Nenhum", "1", "Nenhum", "Nenhum"] * 2
    
    # col 10: UNEMPLOYED
    df.iloc[:, 10] = ["Nenhum", "1 desempregado", "Nenhum", "2", "Nenhum", "1", "Nenhum", "3", "Nenhum", "1"] * 2
    
    # col 11: BENEFITS
    df.iloc[:, 11] = ["Nao recebe", "Recebe", "Nao sabe", "Bolsa Familia", "BPC", "Nao recebe", "Recebe", "Outro", "Nao recebe", "Recebe"] * 2
    
    # col 14, 15, 18: Transferencias
    df.iloc[:, 14] = [1, 0, 0, 1, 0, 1, 0, 0, 1, 0] * 2  # BOLSA_FAMILIA
    df.iloc[:, 15] = [0, 1, 0, 0, 0, 0, 1, 0, 0, 1] * 2  # BPC
    df.iloc[:, 18] = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0] * 2  # OTHER_BENEFIT
    
    # col 21: CADUNICO
    df.iloc[:, 21] = ["Sim", "Não", "Sim", "Não", "Nao sabe", "Sim", "Sim", "Não", "Não", "Sim"] * 2
    
    # col 23: INCOME
    df.iloc[:, 23] = ["Menor que um salario", "Igual a um salario", "Mais de um", "Menor", "Igual", "Mais", "Menor", "Igual", "Menor", "Mais"] * 2
    
    # col 43: GARDEN
    df.iloc[:, 43] = ["Sim", "Não", "Sim", "Não", "Sim", "Não", "Não", "Sim", "Sim", "Não"] * 2
    
    # col 46-50: HOUSING_RISK_ANY (Booleanos)
    df.iloc[:, 46] = [1, 0, 0, 1, 0, 0, 1, 0, 0, 0] * 2
    df.iloc[:, 47] = [0, 1, 0, 0, 0, 0, 0, 1, 0, 0] * 2
    df.iloc[:, 48] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] * 2
    df.iloc[:, 49] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] * 2
    df.iloc[:, 50] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] * 2
    
    # col 54: WATER_NETWORK
    df.iloc[:, 54] = [1, 1, 1, 0, 1, 1, 1, 1, 1, 1] * 2
    
    # col 62: ELECTRIC_NETWORK
    df.iloc[:, 62] = [1, 1, 1, 1, 1, 1, 1, 1, 0, 1] * 2
    
    # col 69: SEWER_NETWORK
    df.iloc[:, 69] = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0] * 2
    
    # col 71: SEPTIC
    df.iloc[:, 71] = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1] * 2
    
    # col 76: MUNICIPAL_TRASH
    df.iloc[:, 76] = [1, 1, 1, 0, 1, 1, 1, 0, 1, 1] * 2
    
    # col 79: BURNING
    df.iloc[:, 79] = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0] * 2
    
    # col 84: WASTE_SEPARATION
    df.iloc[:, 84] = ["Sim", "Não", "Sim", "Não", "Não", "Sim", "Sim", "Não", "Não", "Não"] * 2
    
    # col 117: HEALTH_NONE
    df.iloc[:, 117] = [0, 1, 0, 0, 1, 0, 0, 1, 0, 1] * 2
    
    # col 118: HYPERTENSION
    df.iloc[:, 118] = [1, 0, 1, 0, 0, 1, 0, 0, 1, 0] * 2
    
    # col 119: DIABETES
    df.iloc[:, 119] = [0, 0, 1, 0, 0, 0, 1, 0, 0, 0] * 2
    
    # col 136: DOMESTIC_VIOLENCE
    df.iloc[:, 136] = ["Nao", "Nao", "Sim", "Nao", "Nao", "Nao", "Sim", "Nao", "Nao", "Nao"] * 2
    
    # col 139: COMMUNITY_ENGAGEMENT
    df.iloc[:, 139] = ["Sim", "Não", "Sim", "Não", "Nao sabe", "Sim", "Sim", "Não", "Não", "Sim"] * 2
    
    # col 162: SOCIAL_PROJECT
    df.iloc[:, 162] = ["Sim", "Não", "Não", "Sim", "Não", "Sim", "Não", "Não", "Sim", "Não"] * 2
    
    # col 180: INTERVIEWER
    df.iloc[:, 180] = ["E01", "E02", "E03", "E04", "E05"] * 4
    
    # Ensure there are some "substantive" answers (columns 6 to 179) so they are _valid
    # The columns we just filled are well within 6 to 179.
    
    # Export to Excel
    out_path = Path(__file__).parent / "synthetic_data.xlsx"
    df.to_excel(out_path, index=False)
    print(f"{out_path.name} gerado com sucesso! (N=20)")

if __name__ == "__main__":
    from pathlib import Path
    main()
