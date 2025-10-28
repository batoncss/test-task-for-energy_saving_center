import pandas as pd
from django.shortcuts import render
from .forms import UploadFileForm


def calculate_overdue_debt(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Рассчитывает просроченную задолженность по каждому РСО."""
    dataframe.columns = dataframe.columns.str.strip().str.replace(" ", "_")

    dataframe["Просроченная_задолженность_на_конец_периода"] = (
        dataframe["Дебиторская_задолженность_на_конец_периода"]
        - dataframe["Кредиторская_задолженность_на_конец_периода"]
        - dataframe["Начислено_за_период"]
    ).clip(lower=0)

    aggregated = (
        dataframe.groupby("РСО")["Просроченная_задолженность_на_конец_периода"]
        .sum()
        .reset_index()
    )

    aggregated.columns = aggregated.columns.str.replace(" ", "_")
    return aggregated


def upload_report_view(request):
    """Представление для загрузки Excel-файла и отображения результата расчёта."""
    form = UploadFileForm(request.POST or None, request.FILES or None)
    context = {
        "form": form,
        "file_headers": [],
        "file_data_rows": [],
        "result_headers": ["РСО", "Просроченная_задолженность_на_конец_периода"],
        "result_data_rows": [],
        "file_error": False,
    }

    if request.method == "POST" and form.is_valid():
        excel_file = request.FILES.get("file")

        try:
            df = pd.read_excel(excel_file, engine="openpyxl").fillna("")
            df.columns = df.columns.str.strip().str.replace(" ", "_")

            for col in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    df[col] = df[col].astype(str)

            context["file_headers"] = list(df.columns)
            context["file_data_rows"] = df.values.tolist()

            overdue_col = "Просроченная_задолженность_на_конец_периода"
            if overdue_col in context["file_headers"]:
                idx = context["file_headers"].index(overdue_col)
                context["file_headers"].pop(idx)
                for row in context["file_data_rows"]:
                    row.pop(idx)
            aggregated = calculate_overdue_debt(df).fillna(0)
            context["result_data_rows"] = aggregated.values.tolist()

        except Exception as exc:
            context.update({
                "file_headers": [],
                "file_data_rows": [],
                "result_data_rows": [],
                "file_error": True,
            })

    return render(request, "report_app/upload.html", context)
