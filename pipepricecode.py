import streamlit as st
import pandas as pd
import math

# Pipe data dictionaries
B1001_data_dict = {
    'Nominal diameter (inches)': ['0.5', '0.75', '1', '1.5', '2', '3', '4', '5', '6', '8', '10', '12', '14', '16', '20'],
    'External diameter (mm)': ['21.3', '26.7', '33.4', '48.3', '60.3', '88.9', '114.3', '141.3', '168.3', '219.1', '273', '323.9', '355.6', '406.4', '508'],
    'Wall thickness (mm)': ['2.8', '2.9', '3.4', '3.7', '3.9', '5.5', '6', '6.6', '7.1', '8.2', '9.3', '9.5', '9.5', '9.5', '9.5'],
    'Weight (kg/m)': ['1.27', '1.68', '2.5', '4.05', '5.44', '11.3', '16.1', '21.8', '28.3', '42.5', '60.3', '73.8', '81.3', '93.3', '117'],
    'Cost per 100 m (Euro)': ['277', '338', '461', '707', '738', '1310', '1805', '2615', '3360', '5165', '7450', '9350', '11235', '13020', '16490'],
    'Pressure (bar)': ['215.59', '178.13', '166.95', '125.63', '106.07', '101.46', '86.09', '76.6', '69.19', '61.38', '55.87', '48.1', '43.81', '38.34', '30.67']
}

B1003_data_dict = {
    'Nominal diameter (inches)': ['0.5', '0.75', '1.0', '1.5', '2.0', '3.0', '4.0', '5.0', '6.0', '8.0', '10.0', '12.0', '14.0', '16.0', '20.0'],
    'External diameter (mm)': ['21.3', '26.7', '33.4', '48.3', '60.3', '88.9', '114.3', '141.3', '168.3', '219.1', '273.0', '323.9', '355.6', '406.4', '508.0'],
    'Wall thickness (mm)': ['3.7', '3.9', '4.5', '5.1', '5.5', '7.6', '8.6', '9.5', '11.0', '12.7', '12.7', '12.7', '12.7', '12.7', '12.7'],
    'Weight (kg/m)': ['1.62', '2.2', '3.24', '5.41', '7.48', '15.3', '22.3', '31.0', '42.6', '64.6', '81.6', '97.5', '107.0', '123.16', '155.0'],
    'Cost per 100 m (Euro)': ['315', '389', '536', '840', '1060', '1755', '2635', '3770', '4895', '8010', '10285', '12375', '14905', '17045', '21235'],
    'Pressure (bar)': ['158.27', '133.08', '122.75', '96.2', '83.1', '77.89', '68.55', '61.26', '59.55', '52.81', '42.39', '35.72', '32.54', '28.47', '22.78']
}

B1005_data_dict = {
    'Nominal diameter (inches)': ['0.5', '0.75', '1.0', '1.25', '1.5', '2.0', '2.5', '3.0', '4.0', '5.0', '6.0', '8.0', '10.0', '12.0'],
    'External diameter (mm)': ['21.34', '26.67', '33.4', '42.16', '48.26', '60.32', '73.02', '88.9', '114.3', '141.3', '168.27', '219.07', '273.05', '323.85'],
    'Wall thickness (mm)': ['2.11', '2.11', '2.77', '2.77', '2.77', '2.77', '3.05', '3.05', '3.05', '3.4', '3.4', '3.76', '4.19', '4.57'],
    'Weight (kg/m)': ['0.99', '1.27', '2.08', '2.69', '3.1', '3.92', '5.25', '6.44', '8.34', '11.56', '13.82', '19.92', '27.75', '35.96'],
    'Cost per m04 (Euro)': ['10.7', '14.0', '18.0', '22.2', '38.6', '24.0', '32.0', '40.0', '57.0', '75.0', '97.4', '104.0', '180.0', '194.0'],
    'Cost per m16 (Euro)': ['13.0', '18.0', '23.0', '26.0', '44.9', '34.0', '40.0', '49.0', '64.1', '93.0', '120.0', '133.0', '210.0', '228.0'],
    'Pressure (bar)': ['202.69', '162.19', '170.01', '134.69', '117.66', '94.14', '85.63', '70.33', '54.7', '49.33', '41.42', '35.19', '31.46', '28.93']
}

B1008_data_dict = {
    'External diameter (mm)': ['25', '32', '40', '50', '50', '63', '63', '75', '75', '90', '90', '110', '110', '125', '125', '160', '160', '200', '200', '250'],
    'Wall thickness (mm)': ['1.5', '1.8', '1.9', '1.8', '2.4', '1.8', '3.0', '2.6', '3.6', '2.7', '4.3', '3.2', '5.3', '3.7', '6.0', '4.7', '7.7', '5.4', '6.3', '7.3'],
    'Pressure (bar)': ['10', '10', '10', '6', '10', '6', '10', '6', '10', '6', '10', '6', '10', '6', '10', '6', '10', '6', '10', '6'],
    'Cost per 100 m (Euro)': ['208', '243', '312', '370', '445', '531', '658', '728', '959', '1180', '1365', '1500', '1985', '2170', '2770', '3475', '4475', '5475', '7450', '9250']
}

# Function to calculate pressure using Barlow's formula
def Barlow(S, D, t):
    P = (2 * S * t) / D
    return P

# Streamlit user inputs
def get_user_inputs1():
    pressure = st.number_input("Enter the pressure (bar):", min_value=0.0, format="%.2f")
    temperature = st.number_input("Enter the temperature (°C):", min_value=0.0, format="%.2f")
    medium = st.text_input("Enter the medium:")
    return pressure, temperature, medium

# Function to choose pipe material based on user input
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

# Pipe filter functions for each material type
def B1001_filter(P):
    B1001_data_dict['External diameter (mm)'] = list(map(float, B1001_data_dict['External diameter (mm)']))
    B1001_data_dict['Wall thickness (mm)'] = list(map(float, B1001_data_dict['Wall thickness (mm)']))
    B1001_data_dict['Cost per 100 m (Euro)'] = list(map(float, B1001_data_dict['Cost per 100 m (Euro)']))
    B1001_data_dict['Pressure (bar)'] = list(map(float, B1001_data_dict['Pressure (bar)']))

    B1001_data_dict['Cost per m (Euro)'] = [cost / 100 for cost in B1001_data_dict['Cost per 100 m (Euro)']]

    available_pipes = []
    for i in range(len(B1001_data_dict['Pressure (bar)'])):
        if B1001_data_dict['Pressure (bar)'][i] >= P:
            available_pipes.append({
                'External diameter (mm)': B1001_data_dict['External diameter (mm)'][i],
                'Wall thickness (mm)': B1001_data_dict['Wall thickness (mm)'][i],
                'Cost per m (Euro)': B1001_data_dict['Cost per m (Euro)'][i]
            })

    if not available_pipes:
        st.write(f"No pipes found for the pressure of {P} bar.")
    else:
        st.write(f"Available carbon steel pipes for {P} bar or higher pressure:")
        df = pd.DataFrame(available_pipes)
        st.dataframe(df)

# Similar filters for B1003, B1005, and B1008 (will follow the same pattern)
def B1003_filter(P):
    B1003_data_dict['External diameter (mm)'] = list(map(float, B1003_data_dict['External diameter (mm)']))
    B1003_data_dict['Wall thickness (mm)'] = list(map(float, B1003_data_dict['Wall thickness (mm)']))
    B1003_data_dict['Cost per 100 m (Euro)'] = list(map(float, B1003_data_dict['Cost per 100 m (Euro)']))
    B1003_data_dict['Pressure (bar)'] = list(map(float, B1003_data_dict['Pressure (bar)']))
    
    B1003_data_dict['Cost per m (Euro)'] = [cost / 100 for cost in B1003_data_dict['Cost per 100 m (Euro)']]

    available_pipes = []
    for i in range(len(B1003_data_dict['Pressure (bar)'])):
        if B1003_data_dict['Pressure (bar)'][i] >= P:
            available_pipes.append({
                'External diameter (mm)': B1003_data_dict['External diameter (mm)'][i],
                'Wall thickness (mm)': B1003_data_dict['Wall thickness (mm)'][i],
                'Cost per m (Euro)': B1003_data_dict['Cost per m (Euro)'][i]
            })

    if not available_pipes:
        st.write(f"No pipes found for the pressure of {P} bar.")
    else:
        st.write(f"Available carbon steel pipes for {P} bar or higher pressure:")
        df = pd.DataFrame(available_pipes)
        st.dataframe(df)

def B1005_filter(P):
    B1005_data_dict['External diameter (mm)'] = list(map(float, B1005_data_dict['External diameter (mm)']))
    B1005_data_dict['Wall thickness (mm)'] = list(map(float, B1005_data_dict['Wall thickness (mm)']))
    B1005_data_dict['Cost per m04 (Euro)'] = list(map(float, B1005_data_dict['Cost per m04 (Euro)']))
    B1005_data_dict['Pressure (bar)'] = list(map(float, B1005_data_dict['Pressure (bar)']))

    B1005_data_dict['Cost per m (Euro)'] = B1005_data_dict['Cost per m04 (Euro)']

    available_pipes = []
    for i in range(len(B1005_data_dict['Pressure (bar)'])):
        if B1005_data_dict['Pressure (bar)'][i] >= P:
            available_pipes.append({
                'External diameter (mm)': B1005_data_dict['External diameter (mm)'][i],
                'Wall thickness (mm)': B1005_data_dict['Wall thickness (mm)'][i],
                'Cost per m (Euro)': B1005_data_dict['Cost per m (Euro)'][i]
            })

    if not available_pipes:
        st.write(f"No pipes found for the pressure of {P} bar.")
    else:
        st.write(f"Available carbon steel pipes for {P} bar or higher pressure:")
        df = pd.DataFrame(available_pipes)
        st.dataframe(df)

def B1008_filter(P):
    B1008_data_dict['External diameter (mm)'] = list(map(float, B1008_data_dict['External diameter (mm)']))
    B1008_data_dict['Wall thickness (mm)'] = list(map(float, B1008_data_dict['Wall thickness (mm)']))
    B1008_data_dict['Pressure (bar)'] = list(map(float, B1008_data_dict['Pressure (bar)']))
    B1008_data_dict['Cost per 100 m (Euro)'] = list(map(float, B1008_data_dict['Cost per 100 m (Euro)']))

    B1008_data_dict['Cost per m (Euro)'] = [cost / 100 for cost in B1008_data_dict['Cost per 100 m (Euro)']]

    available_pipes = []
    for i in range(len(B1008_data_dict['Pressure (bar)'])):
        if B1008_data_dict['Pressure (bar)'][i] >= P:
            available_pipes.append({
                'External diameter (mm)': B1008_data_dict['External diameter (mm)'][i],
                'Wall thickness (mm)': B1008_data_dict['Wall thickness (mm)'][i],
                'Cost per m (Euro)': B1008_data_dict['Cost per m (Euro)'][i]
            })

    if not available_pipes:
        st.write(f"No pipes found for the pressure of {P} bar.")
    else:
        st.write(f"Available carbon steel pipes for {P} bar or higher pressure:")
        df = pd.DataFrame(available_pipes)
        st.dataframe(df)

# Function to choose pipe and filter based on material
def Pipe_finder(material, P):
    if material == 'B1001':
        B1001_filter(P)
        st.write("")
        B1003_filter(P)

    elif material == 'B1005':
        B1005_filter(P)

    elif material == 'B1008':
        B1008_filter(P)

    else:
        st.write("Material not found")

# Main function to run the app
def pipe_main():
    st.title("Pipe Selection Tool")
    try:
        P, T, M = get_user_inputs1()
        if st.button("Find Pipes"):
            Pipe_Material = choose_pipe_material(P, T, M)
            st.write(f"Selected Pipe Material: {Pipe_Material}")
            Pipe_finder(Pipe_Material, P)

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Run the main function
pipe_main()
