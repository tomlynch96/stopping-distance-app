import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stopping Distance Visualiser", layout="centered")

st.title("🚗 Stopping Distance Interactive Graph with Presets")

# Custom slider styling using CSS injection
def slider_colour(slider_id, colour):
    st.markdown(f"""
    <style>
    div[data-testid="stSlider"][data-testid$="{slider_id}"] .stSlider > div {{
        background: {colour};
    }}
    </style>
    """, unsafe_allow_html=True)


# --- Parameters & Defaults ---
preset_forces = {"Normal (Dry Road)": 6000, "Wet Road": 4000, "Icy Road": 2000}
preset_masses = {"Small Car": 1000, "SUV": 1500, "Truck": 2500}
preset_speeds = {"City Driving": 15, "Rural Road": 25, "Motorway": 40}
preset_reactions = {"Alert Driver": 0.7, "Average": 1.5, "Tired/Distraction": 2.5}

# Layout
with st.sidebar:
    st.header("Adjust Parameters")

    # --- Braking Force ---
    st.subheader("Braking Force (N)")
    force = st.slider("Force", 2000, 10000, 6000, step=250, key="force_slider")
    cols = st.columns(3)
    for label, val in preset_forces.items():
        if cols[list(preset_forces.keys()).index(label)].button(label, key=f"force_{label}"):
            force = val
            st.session_state.force_slider = val  # Update slider value

    slider_colour("force_slider", "#FF4B4B")  # Red slider

    # --- Mass ---
    st.subheader("Vehicle Mass (kg)")
    mass = st.slider("Mass", 800, 2500, 1000, step=50, key="mass_slider")
    cols = st.columns(3)
    for label, val in preset_masses.items():
        if cols[list(preset_masses.keys()).index(label)].button(label, key=f"mass_{label}"):
            mass = val
            st.session_state.mass_slider = val

    slider_colour("mass_slider", "#4BFF4B")  # Green slider

    # --- Speed ---
    st.subheader("Initial Speed (m/s)")
    speed = st.slider("Speed", 10, 50, 30, step=1, key="speed_slider")
    cols = st.columns(3)
    for label, val in preset_speeds.items():
        if cols[list(preset_speeds.keys()).index(label)].button(label, key=f"speed_{label}"):
            speed = val
            st.session_state.speed_slider = val

    slider_colour("speed_slider", "#4B9BFF")  # Blue slider

    # --- Reaction Time ---
    st.subheader("Reaction Time (s)")
    reaction_time = st.slider("Reaction Time", 0.5, 3.0, 1.5, step=0.1, key="reaction_slider")
    cols = st.columns(3)
    for label, val in preset_reactions.items():
        if cols[list(preset_reactions.keys()).index(label)].button(label, key=f"reaction_{label}"):
            reaction_time = val
            st.session_state.reaction_slider = val

    slider_colour("reaction_slider", "#FFD24B")  # Yellow slider

# --- Physics Calculations ---
a = force / mass
t_brake = speed / a
t_total = reaction_time + t_brake
thinking_distance = speed * reaction_time
braking_distance = (speed ** 2) / (2 * a)
stopping_distance = thinking_distance + braking_distance

# --- Plot ---
t_think = np.linspace(0, reaction_time, 50)
t_stop = np.linspace(reaction_time, t_total, 100)
v_think = np.full_like(t_think, speed)
v_stop = speed - a * (t_stop - reaction_time)

t = np.concatenate((t_think, t_stop))
v = np.concatenate((v_think, v_stop))

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

# --- Distances Output ---
st.markdown(f"""
### Distances:
- **Thinking Distance:** {thinking_distance:.1f} m  
- **Braking Distance:** {braking_distance:.1f} m  
- **Total Stopping Distance:** {stopping_distance:.1f} m  
""")
