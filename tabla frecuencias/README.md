🚀 ¿Cómo usar la aplicación?
1. Ingreso al sistema

Usa pip install flask y ejecuta

Si estás corriendo la aplicación localmente, asegúrate de tener Flask instalado y ejecutar python nombre_del_archivo.py.

Accede a la aplicación a través del navegador en:

http://127.0.0.1:5000


2. Ingresar datos
Paso 1: Especificar número de intervalos

En el campo “Número de intervalos”, escribe cuántos intervalos vas a utilizar.

Debe ser un número entre 1 y 50.

Paso 2: Generar campos de entrada

Haz clic en “Generar entradas”.

Se mostrarán las cajas para ingresar:

Límite Inferior (LI)

Límite Superior (LS)

Frecuencia Absoluta (fi)

Paso 3: Ingresar los intervalos y frecuencias

Llena cada fila con los datos correspondientes a cada clase.

Asegúrate de que:

LS > LI en cada intervalo.

Frecuencia (fi) ≥ 0.

Paso 4: Calcular resultados

Haz clic en “Calcular y Mostrar Resultados”.

Si los datos son válidos, se generará automáticamente el análisis.

📊 Resultados mostrados
1. Tabla de Frecuencias
Intervalo	fi	FI
Ej: 0-10	5	5

fi: Frecuencia absoluta

FI: Frecuencia acumulada

2. Medidas de Posición

Media: Promedio ponderado.

Mediana: Valor central estimado de la distribución.

Moda: Valor de la clase con mayor frecuencia.

Cuartiles: Q1, Q2 (mediana), Q3.

Deciles: D1 a D9.

Percentiles: P1 a P99.

Valores redondeados a 2 o 3 cifras decimales para mayor claridad.

3. Medidas de Dispersión

Rango: Diferencia entre el límite superior del último intervalo y el inferior del primero.

Varianza: Medida de dispersión respecto a la media.

Desviación estándar: Raíz cuadrada de la varianza.

Coeficiente de variación (CV): Medida relativa de dispersión (%).

4. Histograma de Frecuencias

Se presenta un gráfico de barras con cada intervalo y su correspondiente frecuencia absoluta.

🧪 Validaciones y Mensajes de Error

La aplicación mostrará errores si:

El número de intervalos es menor que 1 o mayor que 50.

Un límite superior es menor o igual al inferior.

Una frecuencia es negativa.

La suma total de frecuencias es cero.

Los errores aparecen en cuadros rojos en la parte superior del formulario