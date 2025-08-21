from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import io
import matplotlib.pyplot as plt
import math

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # para flash messages

def calcular_tabla(intervalos, frecuencias):
    N = sum(frecuencias)
    if N == 0:
        raise ValueError("La suma de frecuencias no puede ser cero.")

    FI = []
    acumulado = 0
    for f in frecuencias:
        acumulado += f
        FI.append(acumulado)

    marcas_clase = [(li + ls)/2 for li, ls in intervalos]

    media = sum(f * m for f, m in zip(frecuencias, marcas_clase)) / N

    def obtener_clase(pos):
        for i, fi_acum in enumerate(FI):
            if pos <= fi_acum:
                return i
        return -1

    pos_mediana = N / 2
    i_mediana = obtener_clase(pos_mediana)
    L_med = intervalos[i_mediana][0]
    F_med_anterior = 0 if i_mediana == 0 else FI[i_mediana -1]
    f_med = frecuencias[i_mediana]
    h_med = intervalos[i_mediana][1] - intervalos[i_mediana][0]

    mediana = L_med + ((pos_mediana - F_med_anterior) / f_med) * h_med

    i_moda = frecuencias.index(max(frecuencias))
    L_moda = intervalos[i_moda][0]
    f1 = frecuencias[i_moda]
    f0 = frecuencias[i_moda -1] if i_moda > 0 else 0
    f2 = frecuencias[i_moda +1] if i_moda < len(frecuencias) -1 else 0
    h_moda = intervalos[i_moda][1] - intervalos[i_moda][0]

    denom_moda = (2*f1 - f0 - f2)
    if denom_moda == 0:
        moda = None
    else:
        moda = L_moda + ((f1 - f0)/denom_moda) * h_moda

    rango = intervalos[-1][1] - intervalos[0][0]

    varianza_numerador = sum(f * (m - media)**2 for f, m in zip(frecuencias, marcas_clase))
    varianza = varianza_numerador / N
    desviacion = math.sqrt(varianza)
    cv = (desviacion / media) * 100 if media != 0 else None

    # Función para calcular cuantiles
    def calcular_cuantil(k, tipo='cuartil'):
        if tipo == 'cuartil':
            pos = (k * N) / 4
        elif tipo == 'decil':
            pos = (k * N) / 10
        elif tipo == 'percentil':
            pos = (k * N) / 100
        else:
            return None

        i_cuantil = obtener_clase(pos)
        L_c = intervalos[i_cuantil][0]
        F_ant = 0 if i_cuantil == 0 else FI[i_cuantil -1]
        f_c = frecuencias[i_cuantil]
        h_c = intervalos[i_cuantil][1] - intervalos[i_cuantil][0]

        valor = L_c + ((pos - F_ant) / f_c) * h_c
        return round(valor, 2)

    cuantiles = {
        "cuartiles": [calcular_cuantil(k, 'cuartil') for k in range(1,4)],
        "deciles": [calcular_cuantil(k, 'decil') for k in range(1,10)],
        "percentiles": {k: calcular_cuantil(k, 'percentil') for k in range(1, 100)}
    }

    return {
        "FI": FI,
        "media": media,
        "mediana": mediana,
        "moda": moda,
        "rango": rango,
        "varianza": varianza,
        "desviacion": desviacion,
        "cv": cv,
        "cuantiles": cuantiles,
        "intervalos": intervalos,
        "frecuencias": frecuencias,
        "marcas_clase": marcas_clase
    }

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            n = int(request.form.get("num_intervalos"))
            if n <= 0:
                flash("Ingrese un número válido de intervalos (mayor a 0).", "error")
                return redirect(url_for("index"))

            intervalos = []
            frecuencias = []

            for i in range(n):
                li = float(request.form.get(f"li_{i}"))
                ls = float(request.form.get(f"ls_{i}"))
                if ls <= li:
                    flash(f"El límite superior debe ser mayor que el inferior en intervalo {i+1}.", "error")
                    return redirect(url_for("index"))
                f = int(request.form.get(f"fi_{i}"))
                if f < 0:
                    flash(f"La frecuencia absoluta no puede ser negativa en intervalo {i+1}.", "error")
                    return redirect(url_for("index"))
                intervalos.append((li, ls))
                frecuencias.append(f)

            resultados = calcular_tabla(intervalos, frecuencias)

            # Guardamos los datos en session o pasamos directamente para graficar
            # Para simplicidad, guardaremos en memoria con IDs, pero aquí solo pasamos por render_template

            # Crear gráfico y generar imagen en base64 para mostrar inline
            import base64
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(7,3), dpi=100)
            intervalos_text = [f"{li}-{ls}" for li, ls in intervalos]
            ax.bar(intervalos_text, frecuencias, color="#00FFAB")
            ax.set_title("Histograma de Frecuencias", color="#00FFAB", fontsize=14)
            ax.set_xlabel("Intervalos", color="#00FFAB")
            ax.set_ylabel("Frecuencia absoluta (fi)", color="#00FFAB")
            ax.tick_params(axis='x', rotation=45, colors="#00FFAB")
            ax.tick_params(axis='y', colors="#00FFAB")
            ax.spines['bottom'].set_color("#00FFAB")
            ax.spines['left'].set_color("#00FFAB")
            ax.spines['top'].set_color("#121212")
            ax.spines['right'].set_color("#121212")
            fig.patch.set_facecolor("#121212")
            ax.set_facecolor("#121212")
            buf = io.BytesIO()
            plt.tight_layout()
            fig.savefig(buf, format='png', facecolor=fig.get_facecolor())
            buf.seek(0)
            img_base64 = base64.b64encode(buf.getvalue()).decode('utf8')
            plt.close(fig)

            return render_template("index.html", num_intervalos=n,
                                   intervalos=intervalos,
                                   frecuencias=frecuencias,
                                   resultados=resultados,
                                   img_data=img_base64)
        except Exception as e:
            flash(f"Error: {e}", "error")
            return redirect(url_for("index"))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
