import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stopping Distance Visualiser", layout="centered")

st.title("🚗 Stopping Distance Interactive Graph")

st.markdown(
    """
    Adjust the sliders to see how speed, reaction time, mass, and braking force affect stopping distance.
    """
)

# Sidebar Controls
st.sidebar.header("Adjust Parameters")

# --- Braking Force ---
st.sidebar.subheader("Braking Force (N)")
F = st.sidebar.slider('Force', min_value=2000, max_value=10000, value=6000, step=250)
st.sidebar.caption("Typical values:\n- Normal (Dry Road): 6000 N\n- Wet Road: 4000 N\n- Icy Road: 2000 N")

# --- Mass ---
st.sidebar.subheader("Vehicle Mass (kg)")
m = st.sidebar.slider('Mass', min_value=800, max_value=2500, value=1000, step=50)
st.sidebar.caption("Typical values:\n- Small Car: 1000 kg\n- SUV: 1500 kg\n- Truck: 2500 kg")

# --- Speed ---
st.sidebar.subheader("Initial Speed (m/s)")
v0 = st.sidebar.slider('Speed', min_value=10, max_value=50, value=30, step=1)
st.sidebar.caption("Typical values:\n- City Driving: 15 m/s (54 km/h)\n- Rural Road: 25 m/s (90 km/h)\n- Motorway: 40 m/s (144 km/h)")

# --- Reaction Time ---
st.sidebar.subheader("Reaction Time (s)")
reaction_time = st.sidebar.slider('Reaction Time', min_value=0.5, max_value=3.0, value=1.5, step=0.1)
st.sidebar.caption("Typical values:\n- Alert Driver: 0.7 s\n- Average: 1.5 s\n- Tired/Distraction: 2.5 s")

# Physics calculations
a = F / m
t_brake = v0 / a
t_total = reaction_time + t_brake
thinking_distance = v0 * reaction_time
braking_distance = (v0 ** 2) / (2 * a)
stopping_distance = thinking_distance + braking_distance

# Time and velocity arrays
t_think = np.linspace(0, reaction_time, 50)
t_stop = np.linspace(reaction_time, t_total, 100)
v_think = np.full_like(t_think, v0)
v_stop = v0 - a * (t_stop - reaction_time)

t = np.concatenate((t_think, t_stop))
v = np.concatenate((v_think, v_stop))

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(t, v, color='blue', linewidth=2, label='Velocity')
ax.fill_between(t_think, 0, v_think, color='orange', alpha=0.3, label='Thinking Distance')
ax.fill_between(t_stop, 0, v_stop, color='purple', alpha=0.3, label='Braking Distance')

ax.set_title('Velocity vs Time for a Stopping Vehicle')
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Velocity (m/s)')
ax.grid(which='major', linestyle='-', linewidth=0.8)
ax.grid(which='minor', linestyle=':', linewidth=0.5, alpha=0.7)
ax.minorticks_on()
ax.set_xlim(0, 10)
ax.set_ylim(0, 55)
ax.legend()

st.pyplot(fig)

# Display distances
st.markdown(
    f"""
    ### Distances:
    
    - **Thinking Distance:** {thinking_distance:.1f} m  
    - **Braking Distance:** {braking_distance:.1f} m  
    - **Total Stopping Distance:** {stopping_distance:.1f} m  
    """
)

