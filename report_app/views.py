import pandas as pd
from django.shortcuts import render
from .forms import UploadFileForm

def calculate_overdue(df):
    df.columns = df.columns.str.strip()
    df.columns = [c.replace(" ", "_") for c in df.columns]

    df['Просроченная_задолженность_на_конец_периода'] = (
        df['Дебиторская_задолженность_на_конец_периода'] -
        df['Кредиторская_задолженность_на_конец_периода'] -
        df['Начислено_за_период']
    ).clip(lower=0)

    aggregated = df.groupby('РСО')['Просроченная_задолженность_на_конец_периода'].sum().reset_index()
    aggregated.columns = [c.replace(" ", "_") for c in aggregated.columns]

    return aggregated

def upload_file(request):
    file_data_rows = []
    file_headers = []
    result_rows = []
    result_headers = ["РСО", "Просроченная_задолженность_на_конец_периода"]
    file_error = False

    form = UploadFileForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        excel_file = request.FILES['file']
        try:
            df = pd.read_excel(excel_file, engine='openpyxl')
            df.columns = df.columns.str.strip()
            df.columns = [c.replace(" ", "_") for c in df.columns]
            df = df.fillna("")

            for col in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    df[col] = df[col].astype(str)

            file_headers = list(df.columns)
            file_data_rows = df.values.tolist()

            if "Просроченная_задолженность_на_конец_периода" in file_headers:
                idx = file_headers.index("Просроченная_задолженность_на_конец_периода")
                file_headers.pop(idx)
                for i in range(len(file_data_rows)):
                    file_data_rows[i].pop(idx)

            aggregated = calculate_overdue(df)
            aggregated = aggregated.fillna(0)
            result_rows = aggregated.values.tolist()

        except Exception:
            file_data_rows = []
            file_headers = []
            result_rows = []
            file_error = True

    return render(request, 'report_app/upload.html', {
        'form': form,
        'file_headers': file_headers,
        'file_data_rows': file_data_rows,
        'result_data_rows': result_rows,
        'result_headers': result_headers,
        'file_error': file_error
    })
