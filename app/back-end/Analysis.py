# pip install flask streamlit pandas plotly openpyxl psutil
# streamlit run Analysis.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os
#Define basePath
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
@st.cache_data(hash_funcs={"_thread.RLock": lambda _: None})
def read_file(file_path):
    if os.path.exists(file_path):
        return pd.read_excel(file_path, engine='openpyxl')
    else:
        return pd.DataFrame()  #Return 1DataFrameNUll if arqv n exist
#Modifctn t/Read Excel fromFolder'files'w/ name fix
file_path = os.path.join(base_path, 'files', 'file.xlsx')
df = read_file(file_path)
if df.empty:
    st.warning('Nenhum arquivo encontrado para análise. Por favor, importe uma planilha.')
else:
    #Move infos t/t-line Above, except'Gás'
    cols_to_shift = ['Dif Km', 'Dif Hr', 'Km/Lt', 'Hr/Lt', '(Hr/Lt)Gás']
    for col in cols_to_shift:
        if col in df.columns:
            df[col] = df[col].shift(-1)
    for col in cols_to_shift:
        if col in df.columns:
            df.iloc[-1, df.columns.get_loc(col)] = None
    #New lógic t/coluns added
    df['$PreçoMin'] = df['(Hr/Lt)Gás'] * df['Dif Hr']
    df['Tanque'] = 290
    df['Tq-Lt'] = df['Tanque'] - df['Litros']
    df['Km/TqLt'] = df['Dif Km'] / df['Tq-Lt']
    df['Hr/TqLt'] = df['Tq-Lt'] / df['Dif Hr']
    df['MáxKmLt'] = df['Km/Lt'] + df['Km/TqLt']
    df['KmMáx'] = df['Tanque'] * df['MáxKmLt']
    #Corection t/consider leftOvers d'combustv
    df['Sobra Combustível'] = df.apply(lambda row: row['Dif Km'] - (row['Dif Hr'] * row['Km/Lt']), axis=1)
    df['Km/Lt Real'] = df.apply(lambda row: row['Dif Km'] / (row['Litros'] + row['Sobra Combustível']), axis=1)
    #New Calculs Bysteps
    df['KmMx/HTL'] = df['KmMáx'] / df['Hr/TqLt']
    df['Máx(Hr/Lt)'] = df['Hr/TqLt'] + df['Hr/Lt']
    df['Tq/(MáxH/L)'] = df['Tanque'] / df['Máx(Hr/Lt)']
    df['Simulação'] = df['KmMáx'] / df['MáxKmLt'] / df['Máx(Hr/Lt)']
    df['Simulação/Realidade'] = df['Simulação'] / df['Hr/Lt'] / df['Km/Lt']
    #Simulatio with especific values of Litros
    df['Tanque 200'] = 200
    df['Km/Tq200'] = df['Dif Km'] / df['Tanque 200']
    df['Hr/Tq200'] = df['Tanque 200'] / df['Dif Hr']
    df['Tanque 150'] = 150
    df['Km/Tq150'] = df['Dif Km'] / df['Tanque 150']
    df['Hr/Tq150'] = df['Tanque 150'] / df['Dif Hr']
    df['Tanque 100'] = 100
    df['Km/Tq100'] = df['Dif Km'] / df['Tanque 100']
    df['Hr/Tq100'] = df['Tanque 100'] / df['Dif Hr']
    df['Tanque 225'] = 225
    df['Km/Tq225'] = df['Dif Km'] / df['Tanque 225']
    df['Hr/Tq225'] = df['Tanque 225'] / df['Dif Hr']
    #Round t-values
    cols_to_round = ['$PreçoMin', 'Km/TqLt', 'Hr/TqLt', 'Km/Tq200', 'Hr/Tq200', 'Km/Tq150', 'Hr/Tq150', 'Km/Tq100', 'Hr/Tq100', 'Km/Tq225', 'Hr/Tq225', 'MáxKmLt', 'KmMáx', 'Sobra Combustível', 'Km/Lt Real', 'KmMx/HTL', 'Máx(Hr/Lt)', 'Tq/(MáxH/L)', 'Simulação', 'Simulação/Realidade']
    df[cols_to_round] = df[cols_to_round].round(2)
    #Filtr t/caminhões betoneira
    filtro_betoneiras = df[df['Veículo/Equip.'].str.startswith('BT')]
    #Reorganiz as coluns
    cols_to_export = [
        'Data', 'Motorista', 'PLACA/', '$PreçoMin', '(Hr/Lt)Gás', 'Km/Lt', 'Hr/Lt', 'Km/TqLt', 'Hr/TqLt', 'Km/Tq200', 'Hr/Tq200', 'Km/Tq150', 'Hr/Tq150', 'Km/Tq100', 'Hr/Tq100', 'Km/Tq225', 'Hr/Tq225', 'Dif Km', 'Dif Hr', 'KmAtual', 'Horas', 'Custo Gás',
        'Veículo/Equip.', 'Litros', 'Gás', 'Tanque', 'Tq-Lt', 'MáxKmLt', 'KmMáx', 'KmMx/HTL',
        'Máx(Hr/Lt)', 'Tq/(MáxH/L)', 'Simulação', 'Simulação/Realidade', 'Sobra Combustível', 'Km/Lt Real', 'Modelo'
    ]
    df_export = filtro_betoneiras[cols_to_export]
    #Remov coluns Unwantd d'Visualizaç
    cols_to_display = [
        'Data', 'Motorista', 'PLACA/', '$PreçoMin', '(Hr/Lt)Gás', 'Km/Lt', 'Hr/Lt', 'Km/TqLt', 'Hr/TqLt', 'Km/Tq200', 'Hr/Tq200', 'Km/Tq150', 'Hr/Tq150', 'Km/Tq100', 'Hr/Tq100', 'Km/Tq225', 'Hr/Tq225', 'Dif Km', 'Dif Hr', 'KmAtual', 'Horas',
        'Custo Gás', 'Veículo/Equip.', 'Litros', 'Gás', 'Tanque', 'Tq-Lt', 'MáxKmLt', 'KmMáx', 'KmMx/HTL', 'Máx(Hr/Lt)', 'Tq/(MáxH/L)', 'Simulação', 'Simulação/Realidade', 'Km/Lt Real', 'Modelo'
    ]
    df_display = filtro_betoneiras[cols_to_display]
    st.title('Análise de Desempenho dos Caminhões Betoneira')
    st.sidebar.header('Filtrar os Dados')
    st.write("Tabela de Dados Filtrados:")
    st.write(df_display)
    fig = px.histogram(df_display, x='Veículo/Equip.', y='Km/Lt Real', color='Motorista', hover_data=['Data', 'PLACA/'])
    fig.update_layout(
        title="Desempenho das Betoneiras por Motorista",
        xaxis_title="Veículo/Equipamento",
        yaxis_title="Km/Lt Real"
    )
    st.plotly_chart(fig)
    #Export Data t/Excel
    if st.button('Exportar Dados Filtrados para Excel'):
        with pd.ExcelWriter(os.path.join(base_path, 'files', 'dados_filtrados.xlsx'), engine='openpyxl') as writer:
            df_export.to_excel(writer, index=False, sheet_name='Dados Filtrados')
        st.write('Dados exportados para Excel com sucesso!')
        with open(os.path.join(base_path, 'files', 'dados_filtrados.xlsx'), 'rb') as f:
            st.download_button('Baixar Dados Filtrados', f, file_name='dados_filtrados.xlsx')
    #Functn t/Remov arqvs
    if st.button('Limpar'):
        dir_path = os.path.join(base_path, 'files')
        for f in os.listdir(dir_path):
            os.remove(os.path.join(dir_path, f))
        st.write('Arquivos limpos com sucesso!')