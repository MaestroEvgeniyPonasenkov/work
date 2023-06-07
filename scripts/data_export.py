def export_to_xlsx(df, fname):
    df.to_excel(f'{fname}.xlsx', index=False)