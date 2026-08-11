class DataContext:
    def __init__(self):
        self.tables = {}

    def add(self, name, df):
        self.tables[name] = df

    def get(self, name):
        return self.tables[name]

    def ids(self, table, column):
        return self.tables[table][column].dropna().tolist()

    def has(self, table):
        return table in self.tables

    def columns(self, table):
        return self.tables[table].columns.tolist()

    def shape(self, table):
        return self.tables[table].shape

    def summary(self):
        print("=" * 70)
        print("DATA CONTEXT SUMMARY")
        print("=" * 70)
        for name, df in self.tables.items():
            print(f"{name:<35} rows={len(df):<8} cols={len(df.columns)}")
        print("=" * 70)