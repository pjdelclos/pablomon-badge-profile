import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os

# Define badge categories and tiers
BADGE_CATEGORIES = [
    'Writing (Quill)',
    'Exams (Brain)',
    'Math (Spark)',
    'Timeliness (Hourglass)',
    'Creative (Dragon)',
    'Participation (Speech)'
]

BADGE_ICON_FILES = [
    'quill_icon.png',
    'brain_icon.png',
    'spark_icon.png',
    'hourglass_icon.png',
    'dragon_icon.png',
    'speech_icon.png'
]

TIER_LEVELS = {
    "None": 0,
    "Bronze": 1,
    "Silver": 2,
    "Gold": 3
}

# Load individual badge icons
@st.cache_data
def load_individual_icons():
    icons = []
    for file in BADGE_ICON_FILES:
        if os.path.exists(file):
            icon = Image.open(file).resize((40, 40))
            icons.append(icon)
        else:
            icons.append(None)
    return icons

st.title("Pablómon Badge Profile Generator")
st.markdown("Select your current tier for each badge below. A radar chart will be generated based on your selections.")

badge_icons = load_individual_icons()

# Collect badge tiers from user
badge_tiers = {}
for badge in BADGE_CATEGORIES:
    tier = st.selectbox(f"{badge} Tier:", options=list(TIER_LEVELS.keys()), key=badge)
    badge_tiers[badge] = TIER_LEVELS[tier]

if st.button("Generate Badge Profile Chart"):
    labels = list(badge_tiers.keys())
    stats = list(badge_tiers.values())
    stats += stats[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, stats, color='green', linewidth=2)
    ax.fill(angles, stats, color='green', alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([''] * len(labels))
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(['None', 'Bronze', 'Silver', 'Gold'])
    ax.set_ylim(0, 3)

    # Add individual badge icons directly to radar chart
    for i, angle in enumerate(angles[:-1]):
        icon = badge_icons[i]
        if icon:
            img_arr = np.array(icon)
            imagebox = OffsetImage(img_arr, zoom=0.2)
            ab = AnnotationBbox(
                imagebox,
                (angle, 3.2),  # Position outside the outer ring
                frameon=False,
                xycoords='polar'
            )
            ax.add_artist(ab)

    st.pyplot(fig)
