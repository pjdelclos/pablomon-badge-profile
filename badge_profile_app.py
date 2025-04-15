import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io

# Define badge categories and tiers
BADGE_CATEGORIES = [
    'Writing (Quill)',
    'Exams (Brain)',
    'Math (Spark)',
    'Timeliness (Hourglass)',
    'Creative (Dragon)',
    'Participation (Speech)'
]

TIER_LEVELS = {
    "None": 0,
    "Bronze": 1,
    "Silver": 2,
    "Gold": 3
}

# Load badge icon grid (2x3 image file)
@st.cache_data
def load_badge_icons(path):
    base_image = Image.open(path)
    icons = [base_image.crop((i % 3 * 384, i // 3 * 384, (i % 3 + 1) * 384, (i // 3 + 1) * 384)) for i in range(6)]
    resized = [icon.resize((40, 40)) for icon in icons]
    return resized

st.title("Pablómon Badge Profile Generator")
st.markdown("Select your current tier for each badge below. A radar chart will be generated based on your selections.")

uploaded_image = st.file_uploader("Upload your badge_icons.png (2x3 layout)", type=["png"])

if uploaded_image:
    badge_icons = load_badge_icons(uploaded_image)

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

        # Overlay badge icons at tips
        for i, angle in enumerate(angles[:-1]):
            x = np.cos(angle) * 3.3
            y = np.sin(angle) * 3.3
            icon = badge_icons[i]
            buf = io.BytesIO()
            icon.save(buf, format='PNG')
            st.image(buf.getvalue(), width=40, caption=labels[i], use_column_width=False)

        st.pyplot(fig)
else:
    st.warning("Please upload your badge_icons.png to begin.")
