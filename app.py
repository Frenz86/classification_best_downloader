import streamlit as st
import pandas as pd
from joblib import load

import streamlit as st
import base64
from io import BytesIO

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index = False, sheet_name='Sheet1',float_format="%.2f")
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="Result.xlsx">Download Results </a>' # decode b'abc' => abc


def main():
    st.button("Re-run")
    st.markdown("Inserire un dataset con 5 colonne")

with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center ; color: black;'>Machine Learning App</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center ; color: black;'><strong>Creating your prediction app  </h3>", unsafe_allow_html=True)



    uploaded_file = st.file_uploader("Choose a XLSX file", type="xlsx")

    if uploaded_file:
        df = pd.read_excel(uploaded_file,engine='openpyxl')

        st.dataframe(df)
        #st.table(df.head(20))
        model = load("model_5LR.pkl")
        #model.predict([[3243,3434,65656,7676,45445]])
        X = df
        y_predict = model.predict(X)
        df['prediction'] = y_predict
        st.markdown(get_table_download_link(df), unsafe_allow_html=True)
        st.dataframe(df['prediction'])
        
        
if __name__ == "__main__":
    main()