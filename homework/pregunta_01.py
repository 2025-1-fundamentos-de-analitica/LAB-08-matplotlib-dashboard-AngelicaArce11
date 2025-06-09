# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

def create_visual_for_shipping_per_warehouse(df):
    # Creamos una copia del df
    df = df.copy()

    # Creamos la figura
    plt.figure()

    # Obtenemos las bodegas y la cantidad de despachos
    counts = df.Warehouse_block.value_counts()
    # Creamos el grafico de barras
    counts.plot.bar(
        title='Shipping per Warehouse',
        xlabel='Warehouse block',
        ylabel='Record Count',
        color='tab:blue',
        fontsize=8
    )

    # Ocultamos las lineas que enmarcan el grafico
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # Guardamos la imagen
    plt.savefig('docs/shipping_per_warehouse.png')

def create_visual_for_mode_of_shipment(df):
    # Creamos una copia del df
    df = df.copy()
    # Creamos el grafico
    plt.figure()

    # Contamos los registros por tipo de despacho
    counts = df.Mode_of_Shipment.value_counts()
    # Creamos el grafico de torta
    counts.plot.pie(
        title='Mode of shipment',
        wedgeprops=dict(width=0.35), # Hueco central del grafico
        ylabel='',
        colors=['tab:blue', 'tab:orange', 'tab:green']
    )

    # Guardamos la imagen
    plt.savefig('docs/mode_of_shipment.png')

def create_visual_for_average_customer_rating(df):
    # Creamos una copia del df
    df = df.copy()
    # Creamos el grafico
    plt.figure()

    # Modificamos el df, de tal forma que agrupamos por modo de despacho y sacamos cada uno de los estadisticos de customer_rating
    df = (
        df[['Mode_of_Shipment', 'Customer_rating']]
        .groupby('Mode_of_Shipment')
        .describe()
    )

    # Eliminamos un nivel, para que en en el df no salga Customer_rating arriba de los estadisticos
    df.columns = df.columns.droplevel()
    # Nos quedamos con la info que nos interesa
    df = df[['mean', 'min', 'max']]
    # Generamos el grafico de barras horizontal
    plt.barh(
        y=df.index.values,
        width=df['max'].values - 1, # Se empieza desde cero, por eso se resta 1
        left=df['min'].values,
        height=0.9,
        color='lightgray',
        alpha=0.8
    )

    # Palera de colores para el promedio
    colors = {
        'tab:green' if value >= 3.0 else 'tab:orange' for value in df['mean'].values
    }

    # Graficamos el promedio 
    plt.barh(
        y=df.index.values,
        width=df['mean'].values - 1,
        left=df['min'].values,
        height=0.5,
        color=colors,
        alpha=1.0
    )

    # Titulo de la figura
    plt.title('Average Customer Rating')
    # Ponemos en gris las lineas del eje x - y
    plt.gca().spines['left'].set_color('gray')
    plt.gca().spines['bottom'].set_color('gray')
    # Ocultamos las lineas de arriba y la derecha que enmarcan la figura
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # Guardamos la imagen
    plt.savefig('docs/average_customer_rating.png')

def create_visual_for_weight_distribution(df):
    # Creamos una copia del df
    df = df.copy()
    # Creamos el grafico
    plt.figure()

    # Hacemos un histograma para la variable
    df.Weight_in_gms.plot.hist(
        title='Shipped Weight Distribution',
        color='tab:orange',
        edgecolor='white'
    )

    # Ocultamos las lineas de arriba y la derecha que enmarcan la figura
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # Guardamos la imagen
    plt.savefig('docs/weight_distribution.png')

def pregunta_01():
    """
    El archivo `files/input/shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

    """

    # Leemos el archivo
    df = pd.read_csv('files/input/shipping-data.csv')

    # Creamos la carpeta de docs
    os.makedirs('docs', exist_ok=True)

    # Llamamos las funciones para generar las distintas imagenes
    create_visual_for_shipping_per_warehouse(df)
    create_visual_for_mode_of_shipment(df)
    create_visual_for_average_customer_rating(df)
    create_visual_for_weight_distribution(df)

    # Cuerpo del archivo html
    html_content = """
    <!DOCTYPE html>
    <html>
        <body>
            <h1>Shipping Dashboard Example</h1>
            <div style='width:45%;float:left'>
                <img src='shipping_per_warehouse.png' alt='Fig 1'>
                <img src='mode_of_shipment.png' alt='Fig 2'>   
            </div>
            <div style='width:45%;float:left'>
                <img src='average_customer_rating.png' alt='Fig 3'>
                <img src='weight_distribution.png' alt='Fig 4'>  
            </div>
        </body>
    </html>
    """

    # Creamos el archivo html
    with open('docs/index.html', "w", encoding="utf-8") as f:
        f.write(html_content)