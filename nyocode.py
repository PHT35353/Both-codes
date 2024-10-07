import pandas as pd
import streamlit as st
import math

# Hardcoded pipe data from CSVs
pipe_data = {
    "B1001": [
        {"Nominal diameter (inches)": 0.5, "External diameter (mm)": 21.3, "Wall thickness (mm)": 2.8, "Weight (kg/m)": 1.27, "Cost per 100 m (Euro)": 277, "Pressure (bar)": 215.59},
        {"Nominal diameter (inches)": 0.75, "External diameter (mm)": 26.7, "Wall thickness (mm)": 2.9, "Weight (kg/m)": 1.68, "Cost per 100 m (Euro)": 338, "Pressure (bar)": 178.13},
        {"Nominal diameter (inches)": 1, "External diameter (mm)": 33.4, "Wall thickness (mm)": 3.4, "Weight (kg/m)": 2.5, "Cost per 100 m (Euro)": 461, "Pressure (bar)": 166.95},
        {"Nominal diameter (inches)": 1.5, "External diameter (mm)": 48.3, "Wall thickness (mm)": 3.7, "Weight (kg/m)": 4.05, "Cost per 100 m (Euro)": 707, "Pressure (bar)": 125.63},
        {"Nominal diameter (inches)": 2, "External diameter (mm)": 60.3, "Wall thickness (mm)": 3.9, "Weight (kg/m)": 5.44, "Cost per 100 m (Euro)": 738, "Pressure (bar)": 106.07},
        
    ],
    "B1003": [
        {"Nominal diameter (inches)": 0.5, "External diameter (mm)": 21.3, "Wall thickness (mm)": 3.7, "Weight (kg/m)": 1.62, "Cost per 100 m (Euro)": 315, "Pressure (bar)": 158.27},
        {"Nominal diameter (inches)": 0.75, "External diameter (mm)": 26.7, "Wall thickness (mm)": 3.9, "Weight (kg/m)": 2.2, "Cost per 100 m (Euro)": 389, "Pressure (bar)": 133.08},
        {"Nominal diameter (inches)": 1.0, "External diameter (mm)": 33.4, "Wall thickness (mm)": 4.5, "Weight (kg/m)": 3.24, "Cost per 100 m (Euro)": 536, "Pressure (bar)": 122.75},
        {"Nominal diameter (inches)": 1.5, "External diameter (mm)": 48.3, "Wall thickness (mm)": 5.1, "Weight (kg/m)": 5.41, "Cost per 100 m (Euro)": 840, "Pressure (bar)": 96.2},
        {"Nominal diameter (inches)": 2.0, "External diameter (mm)": 60.3, "Wall thickness (mm)": 5.5, "Weight (kg/m)": 7.48, "Cost per 100 m (Euro)": 1060, "Pressure (bar)": 83.1},
        
    ],
    "B1005": [
        {"Nominal diameter (inches)": 0.5, "External diameter (mm)": 21.34, "Wall thickness (mm)": 2.11, "Weight (kg/m)": 0.99, "Cost per m (304 L)": 10.7, "Cost per m (316 L)": 13.0, "Pressure (bar)": 202.69},
        {"Nominal diameter (inches)": 0.75, "External diameter (mm)": 26.67, "Wall thickness (mm)": 2.11, "Weight (kg/m)": 1.27, "Cost per m (304 L)": 14.0, "Cost per m (316 L)": 18.0, "Pressure (bar)": 162.19},
        {"Nominal diameter (inches)": 1.0, "External diameter (mm)": 33.4, "Wall thickness (mm)": 2.77, "Weight (kg/m)": 2.08, "Cost per m (304 L)": 18.0, "Cost per m (316 L)": 23.0, "Pressure (bar)": 170.01},
        {"Nominal diameter (inches)": 1.25, "External diameter (mm)": 42.16, "Wall thickness (mm)": 2.77, "Weight (kg/m)": 2.69, "Cost per m (304 L)": 22.2, "Cost per m (316 L)": 26.0, "Pressure (bar)": 134.69},
        {"Nominal diameter (inches)": 1.5, "External diameter (mm)": 48.26, "Wall thickness (mm)": 2.77, "Weight (kg/m)": 3.1, "Cost per m (304 L)": 38.6, "Cost per m (316 L)": 44.9, "Pressure (bar)": 117.66},
       
    ],
    "B1008": [
        {"External diameter (mm)": 25, "Wall thickness (mm)": 1.5, "Pressure (bar)": 10, "Cost per 100 m (Euro)": 208},
        {"External diameter (mm)": 32, "Wall thickness (mm)": 1.8, "Pressure (bar)": 10, "Cost per 100 m (Euro)": 243},
        {"External diameter (mm)": 40, "Wall thickness (mm)": 1.9, "Pressure (bar)": 10, "Cost per 100 m (Euro)": 312},
        {"External diameter (mm)": 50, "Wall thickness (mm)": 1.8, "Pressure (bar)": 6, "Cost per 100 m (Euro)": 370},
        {"External diameter (mm)": 50, "Wall thickness (mm)": 2.4, "Pressure (bar)": 10, "Cost per 100 m (Euro)": 445},
        
    ]
}


# Barlow's equation for calculating pressure
def Barlow(S, D, t):
    P = (2 * S * t) / D
    return P

# Streamlit input function to get user inputs
def get_user_inputs1():
    pressure = st.number_input("Enter the pressure (bar):", min_value=0.0, format="%.2f")
    temperature = st.number_input("Enter the temperature (°C):", min_value=0.0, format="%.2f")
    medium = st.text_input("Enter the medium (e.g., steam, water-glycol):")
    return pressure, temperature, medium

# Choose pipe material based on inputs
def choose_pipe_material(P, T, M):
    if M.lower() in ('water glycol', 'water-glycol', 'pressurized water', 'pressurized-water'):
        if P > 10 and T > 425:
            return 'B1005'
        else:
            return 'B1008'

    if P <= 10:
        if T <= 60:
            return 'B1008'
        elif 60 <= T <= 425:
            return 'B1001'
        else:
            return 'B1008'
    else:
        if T <= 425:
            return 'B1001'
        else:
            return 'B1005'

# Function to filter pipes based on pressure
def filter_pipes(P, material):
    available_pipes = [pipe for pipe in pipe_data[material] if pipe['Pressure (bar)'] >= P]
    if not available_pipes:
        st.write(f"No pipes found for the pressure of {P} bar.")
    else:
        st.write(f"Available pipes for {P} bar or higher pressure:")
        df = pd.DataFrame(available_pipes)
        st.dataframe(df[['External diameter (mm)', 'Wall thickness (mm)', 'Cost per 100 m (Euro)']])

# Function to choose and display available pipes
def Pipe_finder(material, P):
    if material in pipe_data:
        filter_pipes(P, material)
    else:
        st.write("Material not found")

# Main function for the Streamlit app
def pipe_main():
    st.title("Pipe Selection Tool")
    
    # Get user inputs
    P, T, M = get_user_inputs1()
    
    if st.button("Find Pipe"):
        # Choose pipe material based on inputs
        Pipe_Material = choose_pipe_material(P, T, M)
        st.write(f"Chosen pipe material: {Pipe_Material}")
        
        # Find and display the available pipes
        Pipe_finder(Pipe_Material, P)

if __name__ == '__main__':
    pipe_main()
