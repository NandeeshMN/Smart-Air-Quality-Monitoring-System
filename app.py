import serial
import time
import re
from collections import deque
import plotly.graph_objs as go
from dash import Dash, dcc, html
from dash.dependencies import Output, Input
from fuzzy_aqi import get_air_quality_status

# ---------------- Serial Configuration ----------------
PORT = "COM5"
BAUD_RATE = 9600

def connect_to_arduino(port, baud_rate, retries=5):
    for attempt in range(retries):
        try:
            ser = serial.Serial(port, baud_rate, timeout=1)
            time.sleep(2)
            ser.reset_input_buffer()
            print("✅ Connected to Arduino")
            return ser
        except serial.SerialException as e:
            print(f"Attempt {attempt+1} failed:", e)
            time.sleep(2)

    print("⚠ Running without Arduino")
    return None

ser = connect_to_arduino(PORT, BAUD_RATE)

# ---------------- Dash App ----------------
app = Dash(__name__)

raw_data = deque(maxlen=100)
fuzzy_data = deque(maxlen=100)
recent_values = deque(maxlen=10)

# State variables
last_average = None
last_aqi = 0
last_status = "Waiting..."
last_color = "white"
last_measures = []
first_value_processed = False

# ---------------- Layout ----------------
app.layout = html.Div(
    style={'fontFamily': 'Arial', 'textAlign': 'center', 'padding': '20px'},
    children=[
        html.H1("🌿 Smart Air Quality Monitoring System"),

        html.Div(id='status-text',
                 style={'fontSize': '32px', 'fontWeight': 'bold'}),

        html.Div(id='aqi-value',
                 style={'fontSize': '24px'}),

        html.Div(id='avg-value',
                 style={'fontSize': '18px', 'color': '#666'}),

        html.H3("🛡️ Safety Measures"),

        html.Ul(
            id='safety-measures',
            style={
                'listStylePosition': 'inside',
                'textAlign': 'left',
                'width': 'fit-content',
                'margin': '0 auto'
            }
        ),

        dcc.Graph(id='live-graph'),

        dcc.Interval(id='interval', interval=1000, n_intervals=0)
    ]
)

# ---------------- Serial Read ----------------
def read_sensor_value():
    if ser and ser.in_waiting:
        try:
            line = ser.readline().decode(errors='ignore').strip()
            print("Received:", line)

            match = re.search(r"MQ135 Value:\s*(\d+)", line)
            if match:
                return int(match.group(1))

        except Exception as e:
            print("Serial read error:", e)

    return None

# ---------------- Callback ----------------
@app.callback(
    [
        Output('live-graph', 'figure'),
        Output('status-text', 'children'),
        Output('status-text', 'style'),
        Output('aqi-value', 'children'),
        Output('avg-value', 'children'),
        Output('safety-measures', 'children')
    ],
    Input('interval', 'n_intervals')
)
def update_dashboard(n):
    global last_average, last_aqi, last_status, last_color
    global last_measures, first_value_processed

    try:
        value = read_sensor_value()

        if value is not None:
            raw_data.append(value)
            recent_values.append(value)

            # ✅ FIRST VALUE → immediate result
            if not first_value_processed:
                result = get_air_quality_status(value)

                last_average = value
                last_aqi = result["aqi"]
                last_status = result["status"]
                last_color = result["color"]
                last_measures = result["measures"]

                fuzzy_data.append(last_aqi)
                first_value_processed = True

            # ✅ AFTER 10 VALUES → update
            elif len(recent_values) == 10:
                avg = sum(recent_values) / len(recent_values)

                result = get_air_quality_status(avg)

                last_average = avg
                last_aqi = result["aqi"]
                last_status = result["status"]
                last_color = result["color"]
                last_measures = result["measures"]

                fuzzy_data.append(last_aqi)
                recent_values.clear()

        # ---------------- Graph ----------------
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            y=list(raw_data),
            mode='lines+markers',
            name='Raw MQ135',
            line=dict(color='red', dash='dot')
        ))

        fig.add_trace(go.Scatter(
            y=list(fuzzy_data),
            mode='lines+markers',
            name='Fuzzy AQI',
            line=dict(color='cyan', width=3)
        ))

        fig.update_layout(
            title='Raw MQ135 vs Fuzzy AQI',
            template='plotly_dark'
        )

        # ---------------- UI ----------------
        measures_list = [html.Li(m) for m in last_measures]

        return (
            fig,
            f"Air Quality: {last_status}",
            {'color': last_color, 'fontSize': '32px', 'fontWeight': 'bold'},
            f"Fuzzy AQI: {last_aqi}",
            f"Average MQ135: {round(last_average,2) if last_average else '--'}",
            measures_list
        )

    except Exception as e:
        print("❌ CALLBACK ERROR:", e)

        return (
            go.Figure(),
            "Error",
            {'color': 'red'},
            "Error",
            "Error",
            []
        )

# ---------------- Run ----------------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)