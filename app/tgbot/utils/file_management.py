from datetime import datetime
import pandas as pd
import os
from fpdf import FPDF


def get_pdf_path(df: pd.DataFrame) -> str:

    df["Дата начала"] = pd.to_datetime(df["Дата начала"]).dt.strftime("%Y-%m-%d")
    df["Дата окончания"] = pd.to_datetime(df["Дата окончания"]).dt.strftime("%Y-%m-%d")

    # Создание PDF
    pdf_path = "events.pdf"
    pdf = FPDF()
    pdf.add_page()

    # Добавление шрифта, поддерживающего кириллицу
    pdf.add_font("DejaVuSans", "", "app/tgbot/utils/DejaVuSans.ttf", uni=True)  # Убедитесь, что файл шрифта находится в той же папке
    pdf.set_font("DejaVuSans", size=12)

    # Установка цвета фона (светло-серый)
    pdf.set_fill_color(240, 240, 240)

    # Добавление заголовка
    pdf.cell(200, 10, text="Список событий", new_x="LMARGIN", new_y="NEXT", align="C", fill=True)

    # Добавление данных из DataFrame
    for index, row in df.iterrows():
        # Дата и название события
        pdf.cell(200, 10, text=f"{row['Дата начала']} - {row['Дата окончания']}: {row['Название события']}", new_x="LMARGIN", new_y="NEXT", fill=True)
        # Место проведения
        pdf.cell(200, 10, text=f"Место: {row['Место проведения']} ({row['Время события']})", new_x="LMARGIN", new_y="NEXT", fill=True)
        # Описание
        pdf.multi_cell(200, 10, text=f"Описание: {row['Описание']}", new_x="LMARGIN", new_y="NEXT", fill=True)
        # Пустая строка для разделения событий
        pdf.cell(200, 10, text="", new_x="LMARGIN", new_y="NEXT")

    # Сохранение PDF
    pdf.output(pdf_path)

    return pdf_path
