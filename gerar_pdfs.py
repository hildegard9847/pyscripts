import pandas as pd
import os
import shutil
from pathlib import Path
import win32com.client as win32

# === CONFIGURAÇÕES ===
# Caminho dos arquivos
arquivo_base = "Planilha de Análise Centro de Custo. dt.xlsx"
arquivo_cc = "Centro de Custo.xlsx"

# Pasta de saída dos PDFs
saida_dir = Path("PDFs_Gerados")
saida_dir.mkdir(exist_ok=True)

# Lê a lista de centros de custo com responsáveis
df_cc = pd.read_excel(arquivo_cc)

# Inicializa o Excel com automação via COM
excel = win32.gencache.EnsureDispatch("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False

# Loop por cada centro de custo da tabela
for _, row in df_cc.iterrows():
    centro = str(row[0]).strip()
    responsavel = str(row[1]).strip().replace(" ", "")  # tira espaços do nome

    # Copia o arquivo modelo para edição temporária
    temp_path = Path(f"temp_{centro}.xlsx")
    shutil.copy(arquivo_base, temp_path)

    # Abre o arquivo temporário no Excel
    wb = excel.Workbooks.Open(str(temp_path.resolve()))
    try:
        # Acessa a aba "Lista não encontrados" e altera B1
        ws = wb.Worksheets("Lista não encontrados")
        ws.Range("B1").Value = centro

        # Salva como PDF (todas as abas)
        nome_pdf = f"{responsavel}.{centro}.pdf"
        destino_pdf = str((saida_dir / nome_pdf).resolve())

        wb.ExportAsFixedFormat(0, destino_pdf)  # 0 = PDF

    finally:
        # Fecha o workbook sem salvar alterações no .xlsx
        wb.Close(SaveChanges=False)

    # Remove o arquivo temporário
    temp_path.unlink(missing_ok=True)

# Encerra o Excel
excel.Quit()

print("PDFs gerados com sucesso!")
