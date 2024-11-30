import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px 

# Cargar los datos
df = pd.read_csv('Base__FS__limpia_MPAC.csv')

# CSS para ampliar el ancho del contenido y mostrar las métricas en una sola fila
st.markdown("""
    <style>
    .main .block-container {
        max-width: 60%;
        padding-top: 0; /* Quitar el espacio superior */
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .metric-container {
        display: flex;
        justify-content: flex-start;
        gap: 20px;
        flex-wrap: nowrap; /* Evitar que se vayan a una segunda fila */
    }
    .metric-box {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        color: white;
        font-family: sans-serif;
        width: 220px; /* Ancho fijo para que ocupen una fila */
        text-align: left;
    }
    .metric-title {
        font-size: 1rem;
        color: #ffa500;
        font-weight: bold;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Configuración del título del dashboard
st.title("Dashboard de Análisis de Desarrolladores FS")

# Botones en la barra lateral
vista_general = st.sidebar.button("Vista General")
vista_filtrada = st.sidebar.button("Vista Filtrada")

# Vista General
if vista_general or not vista_filtrada:
    # Cuadros de métricas personalizados en una sola fila
    total_empleados = len(df)
    edad_promedio = f"{df['Edad'].mean():.1f}"
    salario_promedio = f"${df['Salario'].mean():,.2f}"
    experiencia_promedio = f"{df['Años_De_Experiencia'].mean():.1f}"

    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-box">
                <div class="metric-title">Total de Empleados</div>
                <div class="metric-value">{total_empleados}</div>
            </div>
            <div class="metric-box">
                <div class="metric-title">Edad Promedio</div>
                <div class="metric-value">{edad_promedio}</div>
            </div>
            <div class="metric-box">
                <div class="metric-title">Salario Promedio</div>
                <div class="metric-value">{salario_promedio}</div>
            </div>
            <div class="metric-box">
                <div class="metric-title">Años de Experiencia Promedio</div>
                <div class="metric-value">{experiencia_promedio}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Gráficos distribuidos en dos filas y cuatro columnas, alineados a la izquierda
    
    # Primera fila de gráficos
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        # Gráfico de Distribución de Edad
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.histplot(df['Edad'], bins=30, kde=True, ax=ax)
        ax.set_title("Distribución de Edad", fontsize=14, color='blue')

        st.pyplot(fig)

    with col2:
        # Gráfico de Distribución de Salario
        fig, ax = plt.subplots(figsize=(6, 3))
        #sns.histplot(df['Salario'], bins=30, kde=True, color="blue", ax=ax)
        sns.boxplot(x=df['Salario'], patch_artist=True, notch=True,
              boxprops=dict(facecolor='lightblue', color='orange'
              ), vert=False)
        ax.set_title("Distribución de Salario", fontsize=14, color='blue')

        st.pyplot(fig)
   
    with col3:
        # Gráfico de "Distribución por Genero"
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.countplot(data=df, x='Genero', ax=ax, palette="Set2")
        ax.set_title("Distribución por Género")
        ax.set_xlabel("Género")
        ax.set_ylabel("Frecuencia")
        #ax.get_yaxis().set_visible(False)

        st.pyplot(fig)
   
    with col4:
        # Gráfico de barras para Nivel_Educativo
        dfedu = df['Nivel_Educativo'].value_counts().nlargest(10)

        # Definir una lista de colores para las barras
        colors = plt.cm.inferno(np.linspace(0, 0.8, len(dfedu)))

        # Gráfico de "Distribución por Nivel_Educativo"
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.countplot(data=df, y='Nivel_Educativo', palette=colors)
        ax.set_title("Distribución por Nivel_Educativo")
        ax.set_xlabel('Frecuencia', fontsize=12)
        ax.set_ylabel('Nivel_Educativo', fontsize=12)
        #ax.get_yaxis().set_visible(False)
        
        # Invertir el eje Y para que la barra más alta esté en la parte superior
        #ax.invert_yaxis()

        st.pyplot(fig)

    # Segunda fila de gráficos
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        # Definir una lista de colores para las barras
        colors = plt.cm.viridis(np.linspace(0, 0.8, len(dfedu)))

        # Gráfico de Salario por Genero
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.boxplot(data=df, x='Genero', y='Salario', ax=ax, palette=colors)
        ax.set_title("Salario por Genero")
        st.pyplot(fig)

    with col2:
        # Gráfico de Salario por Nivel_Educativo
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.boxplot(data=df, x='Salario', y='Nivel_Educativo', ax=ax, palette="Set2")
        ax.set_title("Salario por Nivel_Educativo")
        st.pyplot(fig)

    with col3:
        # Gráfico de Comparación entre Edad y Salario
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.scatterplot(data=df, x='Edad', y='Salario', ax=ax, color="purple")
        ax.set_title("Comparación de Edad y Salario")
        st.pyplot(fig)

    with col4:
        # Gráfico de Años_De_Experiencia vs Salario
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.scatterplot(data=df, x='Años_De_Experiencia', y='Salario', ax=ax, color="orange")
        ax.set_title("Años_De_Experiencia vs Salario")

        st.pyplot(fig)

    # Tercera fila de gráficos
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Dashboard con gráficos interactivos
        fig = px.histogram(df, x='Genero', color='Edad', title="Distribución de Género por Edad")
        ax.set_xlabel('Género', fontsize=12)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        # Dashboard con gráficos interactivos
        fig = px.histogram(df, x='Salario', color='Edad', title="Distribución de Salario por Edad")
        st.plotly_chart(fig, use_container_width=True)
        


    # Gráfico de correlación entre todas las variables numéricas
    st.header("Correlación entre Variables Numéricas")
    df_numeric = df[['Edad', 'Salario', 'Años_De_Experiencia']] # Solo variables numéricas para correlación
    correlation_matrix = df_numeric.corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    ax.set_title("Matriz de Correlación")

    st.pyplot(fig)

# Vista Filtrada
elif vista_filtrada:
    st.header("Vista Filtrada - Análisis Detallado")

    # Filtros en la barra lateral para la vista filtrada
    genero_seleccionado = st.sidebar.selectbox("Selecciona el género", df['Genero'].unique())
    nivel_educativo_seleccionado = st.sidebar.selectbox("Selecciona el nivel educativo", df['Nivel_Educativo'].unique())
    edad_seleccionada = st.sidebar.slider("Selecciona el rango de edad",
                                          int(df['Edad'].min()),
                                          int(df['Edad'].max()),
                                          (int(df['Edad'].min()), int(df['Edad'].max())))

    # Filtrar el DataFrame con los criterios seleccionados
    df_filtrado = df[(df['Genero'] == genero_seleccionado) &
                     (df['Nivel_Educativo'] == nivel_educativo_seleccionado) &
                     (df['Edad'] >= edad_seleccionada[0]) &
                     (df['Edad'] <= edad_seleccionada[1])]

    # Panel General de la Vista Filtrada
    st.subheader("Estadísticas Generales")
    st.metric("Total de Empleados", len(df_filtrado))
    st.metric("Edad Promedio", f"{df_filtrado['Edad'].mean():.1f}")
    st.metric("Salario Promedio", f"${df_filtrado['Salario'].mean():,.2f}")
    st.metric("Años_De_Experiencia Promedio", f"{df_filtrado['Años_De_Experiencia'].mean():.1f}")

