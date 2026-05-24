import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# -----------------------------
# FUZZY VARIABLES
# -----------------------------
mq135 = ctrl.Antecedent(np.arange(0, 501, 1), 'mq135')
aqi = ctrl.Consequent(np.arange(0, 301, 1), 'aqi')

# Membership functions (Input)
mq135['low'] = fuzz.trimf(mq135.universe, [0, 0, 200])
mq135['medium'] = fuzz.trimf(mq135.universe, [150, 250, 350])
mq135['high'] = fuzz.trimf(mq135.universe, [300, 500, 500])

# Membership functions (Output)
aqi['good'] = fuzz.trimf(aqi.universe, [0, 0, 100])
aqi['moderate'] = fuzz.trimf(aqi.universe, [100, 150, 200])
aqi['poor'] = fuzz.trimf(aqi.universe, [200, 300, 300])

# -----------------------------
# FUZZY RULES
# -----------------------------
rule1 = ctrl.Rule(mq135['low'], aqi['good'])
rule2 = ctrl.Rule(mq135['medium'], aqi['moderate'])
rule3 = ctrl.Rule(mq135['high'], aqi['poor'])

aqi_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])


# -----------------------------
# FUZZY AQI CALCULATION
# -----------------------------
def get_fuzzy_aqi(sensor_value):
    sim = ctrl.ControlSystemSimulation(aqi_ctrl)  # FIXED (no reuse bug)
    sim.input['mq135'] = sensor_value
    sim.compute()
    return sim.output['aqi']


# -----------------------------
# GOVERNMENT-STYLE CONTROL MEASURES
# -----------------------------
def get_control_measures(status):
    measures = {
        "GOOD": [
            "Air quality is safe.",
            "Promote green practices like planting trees."
        ],

        "MODERATE": [
            "Sensitive individuals should limit outdoor exposure.",
            "Reduce prolonged physical activity outdoors.",
            "Use masks if necessary.",
            "Avoid burning waste or pollutants."
        ],

        "POOR": [
            "Avoid outdoor activities.",
            "Stay indoors as much as possible.",
            "Keep windows and doors closed.",
            "Use air purifier if available.",
            "Wear N95 mask when going outside.",
            "Avoid vehicle usage and reduce emissions.",
            "Follow government health advisories."
        ]
    }
    return measures.get(status, [])


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def get_air_quality_status(sensor_value):
    aqi_value = get_fuzzy_aqi(sensor_value)

    # Classification
    if aqi_value <= 100:
        status = "GOOD"
        color = "green"
    elif aqi_value <= 200:
        status = "MODERATE"
        color = "orange"
    else:
        status = "POOR"
        color = "red"

    measures = get_control_measures(status)

    return {
        "sensor_value": sensor_value,
        "aqi": round(aqi_value, 2),
        "status": status,
        "color": color,
        "measures": measures
    }


# -----------------------------
# TESTING
# -----------------------------
if __name__ == "__main__":
    value = 320  # sample MQ135 value
    result = get_air_quality_status(value)

    print("Sensor Value:", result["sensor_value"])
    print("AQI:", result["aqi"])
    print("Status:", result["status"])
    print("Color:", result["color"])
    print("Control Measures:")
    for m in result["measures"]:
        print("-", m)