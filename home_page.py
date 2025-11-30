import streamlit as st

# Navigation function
def navigate_to_page(page_name):
    st.session_state["current_page"] = page_name
    st.experimental_rerun()
st.set_page_config(page_title="Eye Disease Prediction", page_icon="👁")
def home_page():
    #add info about the eye disease detection system in the sidebar
    st.sidebar.markdown(
        """
        <h2 style='color: black ; text-align: center;'>Ocular Disease Recognition</h2>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.image('https://t3.ftcdn.net/jpg/08/54/43/30/360_F_854433023_EPD1MZclG0dFgGLaYERZv5xsnpoCVkxe.jpg')
    st.sidebar.markdown(
        """
        
        <p style='color: black; text-align: center;'>This web application is designed to detect eye diseases using deep learning algorithms.</p>
        """,
        unsafe_allow_html=True
    )
    #type of eye diseases
    st.sidebar.markdown(
        """
        <h3 style='color: black; text-align: center;'>Types of Eye Diseases</h3>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.markdown(
        """
        <ul>
            <li>Normal (N)</li>
            <li>Cataract (C)</li>
            <li>Glaucoma (G)</li>
            <li>Non Eye Disease (O)</li>
            <li> AMD (A)</li>
            <li> Myopia (M)</li>

        </ul>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
    """
    <style>
    /* Apply background image to the main content area */
    .main {
        background-image: url("https://www.shutterstock.com/image-photo/human-eye-technology-background-ai-600nw-2305962897.jpg");  
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style="text-align: center; padding: 1px; background-color: #b3a2a2 ; border-radius: 5px; border: 2px solid black;">
            <p style="color: black; font-size: 48px;"><b>Eye Disease Detection System</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )
    #add image
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://blinkphx.com/wp-content/uploads/2021/08/BlinkEyeCarePhoenix-MissingAssets-SupportingImages-EyeDiseaseDiagnosis-1.png" alt="Liver" width="300" height=400">
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4, col5,col6 = st.columns([1.5, 1, 1, 1, 1,1])
    with col2:
        if st.button("Login",type="primary"):
            navigate_to_page("login")
    with col5:
        if st.button("Sign Up",type="primary"):
            navigate_to_page("signup")
