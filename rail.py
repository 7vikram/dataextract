import streamlit as st

col1, col2 = st.columns([0.15, 0.85])  # Left for image, right for title
with col1:
    st.image("SBT_Logo.png", width=300)  # Adjust width as needed

with col2:
    st.markdown(
        """
        <style>
        /* Tooltip styling for title */
        .title-tooltip {
            position: relative;
            display: inline-block;
            cursor: pointer;
        }

        /* Tooltip text */
        .title-tooltip:hover::after {
            content: attr(data-tooltip);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background-color: rgba(0, 0, 0, 0.7); /* Dark background for the tooltip */
            color: white;
            padding: 5px;
            border-radius: 5px;
            font-size: 12px;
            white-space: nowrap;
            z-index: 1;  /* Ensure tooltip is above */
            opacity: 1;
            transition: opacity 0.3s;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Add the title with a tooltip
    st.markdown(
        """
        <style>
        .title-tooltip {
            position: relative;
            top: 10px;   /* Moves the text down */
            color: #8B008B;
            left: 280px; /* Moves the text to the right */
            text-align: left;  /* Aligns the text to the right */
        }
        </style>
        <div class="title-tooltip" data-tooltip="Explore various pathways for climate action">
            <span style="font-size: 50px; font-weight: bold;">Pathway Explorer</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("## Under-construction")
