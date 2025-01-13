import streamlit as st
import numpy as np
from PIL import Image

class Neuron:
    def __init__(self, weights, bias, func="sigmoid"):
        self.weights = np.array(weights)
        self.bias = bias
        self.func = func.lower()
        
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def tanh(self, x):
        return np.tanh(x)
    
    def run(self, input_data):
        input_data = np.array(input_data)
        if len(input_data) != len(self.weights):
            raise ValueError("Input data must have same length as weights")
        
        z = np.dot(self.weights, input_data) + self.bias
        
        if self.func == "sigmoid":
            return self.sigmoid(z)
        elif self.func == "relu":
            return self.relu(z)
        elif self.func == "tanh":
            return self.tanh(z)
        else:
            raise ValueError("Unknown activation function")
    
    def changeWeights(self, new_weights):
        if len(new_weights) != len(self.weights):
            raise ValueError("New weights must have same length as current weights")
        self.weights = np.array(new_weights)
    
    def changeBias(self, new_bias):
        self.bias = new_bias

# Configuración de la página
st.set_page_config(
    page_title="Simulador de Neurona",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Aplicar estilo CSS personalizado
st.markdown("""
    <style>
        .block-container {
            padding-left: 5rem !important;
            padding-right: 5rem !important;
            max-width: 1000px !important;
            margin: auto !important;
        }
        .stImage {
            margin: 2rem auto !important;
            display: block !important;
            max-width: 600px !important;
        }
        .output-container {
            background-color: #f0f8ff !important;
            padding: 2rem !important;
            border-radius: 10px !important;
            border: 2px solid #4a90e2 !important;
            margin: 2rem 0 !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        }
        .output-value {
            font-size: 1.5em !important;
            text-align: center !important;
            color: #2c5282 !important;
            background-color: white !important;
            padding: 1rem !important;
            border-radius: 5px !important;
            margin-top: 1rem !important;
            border: 1px solid #e2e8f0 !important;
        }
        .centered-image {
            text-align: center !important;
        }
        .stMarkdown {
            margin-bottom: 1rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# Título y descripción
st.title("🧠 Neurona Artificial 2.0")

# Cargar y mostrar la imagen
image = Image.open("neurona.jpg")
st.markdown('<div class="centered-image">', unsafe_allow_html=True)
st.image(image, width=400)
st.markdown('</div>', unsafe_allow_html=True)

st.write("Una herramienta interactiva para simular el comportamiento de una neurona artificial")

# Selector del número de entradas/pesos
num_inputs = st.slider(
    "Elige el número de entradas/pesos que tendrá la neurona",
    min_value=1,
    max_value=10,
    value=2,
    help="Este valor determina cuántas entradas y pesos tendrá la neurona"
)

# Crear columnas para pesos y entradas
st.subheader("Pesos (w)")
weight_cols = st.columns(num_inputs)
weights = []

for i in range(num_inputs):
    with weight_cols[i]:
        w = st.number_input(
            f"w{i}",
            value=0.00,
            format="%.2f",
            step=0.1
        )
        weights.append(w)

st.write(f"w = {weights}")

# Entradas
st.subheader("Entradas (x)")
input_cols = st.columns(num_inputs)
inputs = []

for i in range(num_inputs):
    with input_cols[i]:
        x = st.number_input(
            f"x{i}",
            value=0.00,
            format="%.2f",
            step=0.1
        )
        inputs.append(x)

st.write(f"x = {inputs}")

# Sesgo y función de activación
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sesgo (b)")
    bias = st.number_input(
        "Introduce el valor del sesgo",
        value=0.00,
        format="%.2f",
        step=0.1
    )

with col2:
    st.subheader("Función de Activación")
    activation_function = st.selectbox(
        "Elige la función de activación",
        ["Sigmoide", "ReLU", "Tangente Hiperbólica"]
    )

# Botón de cálculo
if st.button("Calcular Salida", type="primary"):
    # Convertir nombre de función de activación al formato de la clase
    func_map = {
        "Sigmoide": "sigmoid",
        "ReLU": "relu",
        "Tangente Hiperbólica": "tanh"
    }
    
    # Crear instancia de neurona y calcular salida
    neuron = Neuron(weights=weights, bias=bias, func=func_map[activation_function])
    output = neuron.run(inputs)
    
    # Mostrar resultados en el contenedor personalizado
    st.markdown("""
        <div class="output-container">
            <h3 style="color: #2c5282; margin: 0 0 0.5rem 0;">🔢 Resultados del Cálculo</h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Suma Ponderada (z):**")
        weighted_sum = np.dot(weights, inputs) + bias
        st.latex(f"z = \sum_i w_i x_i + b = {weighted_sum:.4f}")
        
    with col2:
        st.write("**Función de Activación:**")
        formulas = {
            "sigmoid": "σ(z) = 1 / (1 + e^{-z})",
            "relu": "ReLU(z) = max(0, z)",
            "tanh": "tanh(z) = \\frac{e^z - e^{-z}}{e^z + e^{-z}}"
        }
        st.latex(formulas[func_map[activation_function]])
    
    # Mostrar la salida de manera destacada
    st.markdown("""
        <div class="output-value">
            <h3 style="color: #2c5282; margin: 0;">🎯 Salida de la Neurona (y)</h3>
    """, unsafe_allow_html=True)
    st.latex(f"y = {output:.4f}")
    st.markdown('</div></div>', unsafe_allow_html=True)