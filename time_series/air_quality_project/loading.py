def save_data(df, file_name):

    df.to_csv(file_name, index=False)

    print("Saved successfully")
