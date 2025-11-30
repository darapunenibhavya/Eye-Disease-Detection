import streamlit as st
from streamlit_option_menu import option_menu
from database import fetch_user,add_disease
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import torch
import numpy as np
from PIL import Image
from pathlib import Path
from model import ImprovedTinyVGGModel
from utils import *
device = 'cuda' if torch.cuda.is_available() else 'cpu'
MODEL_SAVE_PATH = "models/MultipleEyeDiseaseDetectModel.pth"
model_info = torch.load(MODEL_SAVE_PATH, map_location=torch.device('cpu'))
def generate_report(name, age, gender, disease, image_url,infor,precautions):
    html_content = f"""
    <html>
    <body style="text-align:center; background-image: url('https://img.freepik.com/free-vector/simple-blue-gradient-background-vector-business_53876-161578.jpg'); background-size: cover; background-repeat: no-repeat;">
        <h2>Patient Health Report</h2>
        <p><b>Name:</b> {name}</p>
        <p><b>Age:</b> {age}</p>
        <p><b>Gender:</b> {gender}</p>
        <p><b>Disease:</b> {disease}</p>
        <img src="{image_url}" width="300"/>
        <p><b>Information:</b> {infor}</p>
        <p><b>Precautions:</b> {precautions}</p>
    </body>
    </html>
    """
    return html_content.encode("utf-8")

# Instantiate Model
model = ImprovedTinyVGGModel(
    input_shape=3,
    hidden_units=48,
    output_shape=6).to(device)
data_path = Path("demo/test_images/")

def navigate_to_page(page_name):
    st.session_state["current_page"] = page_name
    st.experimental_rerun()

def user_home_page():
    user = fetch_user(st.session_state["current_user"])
    with st.sidebar:
        st.markdown(f"<h1 style='text-align: center;'>𝐖𝐄𝐋𝐂𝐎𝐌𝐄 👋 {user[1]}</h1>", unsafe_allow_html=True)
        st.image('https://static.vecteezy.com/system/resources/previews/026/773/363/non_2x/eye-with-ai-generated-free-png.png', use_column_width=True)
        select = option_menu(
            "",
            ["Patient Profile",'Predictions', 'Generate Report',"Logout"],
            icons=['person-square','eye-fill','file-earmark-fill','lock-fill'],
            menu_icon="cast",
            default_index=0,
            orientation="vertical",
            styles={
                "container": {"padding": "0", "background-color": "#d6d6d6"}, 
                "icon": {"color": "black", "font-size": "20px"},    
                "nav-link": {
                    "font-size": "16px",
                    "margin": "0px",
                    "color": "black",                                          
                },   
                "nav-link-selected": {
                    "background-color": "#10bec4",                            
                },
            },
        )

    if select == 'Patient Profile':
        st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url('https://scitechdaily.com/images/AI-Vision-Eye-Examination-Art-Concept.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        </style>
        """,
        unsafe_allow_html=True
        )

        # Extracting user data from session state after successful login
        if user:
            # Assuming 'user' is a tuple (id, name, email, password, regd_no, year_of_study, branch, student_type, student_image)
            name, age, gender,eye_power,eye_problem = user[1], user[3], user[4],user[5],user[6]
            if gender == 'Male👦🏻':
                image_link = "https://img.freepik.com/photos-premium/elevez-votre-marque-avatar-amical-qui-reflete-professionnalisme-ideal-pour-directeurs-ventes_1283595-18531.jpg?semt=ais_hybrid"
            else:
                image_link = "https://cdn-icons-png.flaticon.com/512/219/219969.png"

            # CSS Styling for vertical container
            profile_css = """
            <style>
                .profile-container {
                    background-color: #10bec4;
                    padding: 50px;
                    border-radius: 50px;
                    box-shadow: 10px 8px 12px rgba(0, 0, 0, 0.15);
                    max-width: 400px;
                    border: 2px solid black;
                    margin-left: 100%;
                    margin: auto;
                    font-family: Arial, sans-serif;
                    text-align: center;
                }
                .profile-header {
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 1px;
                    color: #333;
                }
                .profile-item {
                    font-size: 18px;
                    margin-bottom: 10px;
                    color: #555;
                }
                .profile-image img {
                    border-radius: 50%;
                    max-width: 250px;
                    max-height: 250px;
                    margin-bottom: 0px;
                }
            </style>
            """

            # HTML Structure for vertical alignment
            profile_html = f"""
            <div class="profile-container">
                <div class="profile-image">
                    <img src="{image_link}" alt="User Image">
                </div>
                <div class="profile-details">
                    <div class="profile-header">User Report</div>
                    <div class="profile-item"><strong>Name:</strong> {name}</div>
                    <div class="profile-item"><strong>Age:</strong> {age}</div>
                    <div class="profile-item"><strong>Gender:</strong> {gender}</div>
                    <div class="profile-item"><strong>Eye Power:</strong> {eye_power}</div>
                    <div class="profile-item"><strong>Eye Problem:</strong> {eye_problem}</div>
                </div>
            </div>
            """

            # Display styled content
            st.markdown(profile_css + profile_html, unsafe_allow_html=True)
    elif select == 'Predictions':
        st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url("https://www.unite.ai/wp-content/uploads/2024/07/Alex_Mc_Split-screen_image_on_one_side_a_human_eye_with_visib_31bfae24-931c-43e6-a918-b3af74cc2964_2.png");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-color: rgba(255, 255, 255, 0.6);
            background-blend-mode: overlay;
        }
        </style>
        """,
        unsafe_allow_html=True
        )
        def disease_info_box(disease_name):
            return f"""
                <div style="
                    background-color: rgba(255, 255, 255, 0.8);
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                    font-size: 40px;
                    font-weight: bold;
                    color: red;">
                    {disease_name}
                </div>
            """
        st.markdown("<h1 style='text-align: center;'>Eye Disease Prediction</h1>", unsafe_allow_html=True)
        uploaded_file=st.file_uploader("Upload Eye Fundus Image",type=['jpg','png','jpeg'])
        if uploaded_file is not None:
            # Save the uploaded image
            custom_image_path = data_path / uploaded_file.name
            with open(custom_image_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            # Load and preprocess the image
            custom_image_transformed = load_and_preprocess_image(custom_image_path)

            # Load the model
            model.load_state_dict(model_info)
            model.eval()

            # Predict the label for the image
            class_names = np.array(['AMD', 'Cataract', 'Glaucoma', 'Myopia', 'Non-eye', 'Normal'])
            predicted_label, image_pred_probs = predict_image(model,
                                                            custom_image_transformed,
                                                            class_names)

            add_disease(user[2],predicted_label[0])
            # Prediction result section
            col1, col2 = st.columns([1,2])
            # Display the uploaded image on the right column
            with col1:
                image = Image.open(custom_image_path)
                st.image(image, caption='Uploaded Image', use_column_width=True)
            with col2:
                st.markdown(
                    f'<h3 style="color: black;">Prediction Result</h3>', 
                    unsafe_allow_html=True
                )
                st.markdown(disease_info_box(predicted_label[0]), unsafe_allow_html=True)

            image_pred_probs = image_pred_probs.numpy().flatten()
            col_left, col_middle, col_right = st.columns([1, 10, 1])
            # Middle Column: Show Bar Chart of Probabilities
            with col_middle:
                df = pd.DataFrame({"Disease": class_names, "Probability": image_pred_probs * 100})
                #covert data to 1D array
                plt.figure(figsize=(6, 3))
                sns.barplot(data=df, x="Probability", y="Disease", palette="viridis")
                plt.xlabel("Probability (%)")
                plt.ylabel("Disease")
                plt.title("Eye Disease Prediction Probabilities")
                plt.grid(axis='x')
                plt.tight_layout()
                st.pyplot(plt)

    elif select == 'Generate Report':
        st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url("https://png.pngtree.com/thumb_back/fw800/background/20240715/pngtree-d-close-up-of-a-human-eye-with-blue-iris-generative-image_16011220.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-color: rgba(255, 255, 255, 0.6);
            background-blend-mode: overlay;
        }
        </style>
        """,
        unsafe_allow_html=True
        )
        col1,col2,col3=st.columns([5,10,5])
        col2.markdown(
            """
            <div style="text-align: center; padding: 1px; background-color: #f6fa87; border-radius: 70px; border: 2px solid black;">
                <p style="color: red; font-size: 35px;"><b>Report Generation</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )
        user=fetch_user(st.session_state["current_user"])
        try:
            name = user[1]
            age = user[3]
            gender = user[4]
            disease = user[8]
            url={'AMD':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_nb1F98stgF-YI0FhpiLbtAugxjKd7gl--w&s',
                'Cataract':'https://neoretina.com/blog/wp-content/uploads/2020/01/WhatsApp-Image-2020-01-04-at-5.37.43-PM.jpeg',
                'Glaucoma':'https://www.thindeyehospital.org/wp-content/uploads/2024/01/gloucoma.jpg',
                'Myopia':'https://cdn.britannica.com/51/180051-138-6BA69869/nearsightedness-farsightedness.jpg?w=800&h=450&c=crop',
                'Non-eye':'https://cdn.dribbble.com/userupload/2905340/file/original-10210d8c75d27373e95effe16950b396.png?resize=400x0',
                'Normal':'https://media.sciencephoto.com/image/p4200504/800wm/P4200504.jpg'}
            disease_info={
                'AMD':'Age-related macular degeneration (AMD) is an eye disease that may get worse over time. It’s the leading cause of severe, permanent vision loss in people over age 60. It happens when the small central portion of your retina, called the macula, wears down. AMD is a common condition among older adults.',
                'Cataract':'A cataract is a clouding of the lens in the eye that affects vision. Most cataracts are related to aging. Cataracts are very common in older people. By age 80, more than half of all Americans either have a cataract or have had cataract surgery.',
                'Glaucoma':'Glaucoma is a group of eye diseases that can cause vision loss and blindness by damaging a nerve in the back of your eye called the optic nerve. This nerve sends information from the light that enters your eye to your brain.',
                'Myopia':'Myopia, or nearsightedness, is a common refractive error of the eye that makes it difficult to focus on objects that are far away. The condition is caused by the shape of the eyeball being too long or the cornea being too curved.',
                'Non-eye':'Non-eye disease',
                'Normal':'Normal Eye'
            }
            precautions={
                'AMD':"Take medication: Use eye drops and other medications as prescribed by your healthcare provider.\nProtect your eyes: Wear sunglasses and a hat when you are outside, and wear eye protection when using power tools or playing sports.\nEat a healthy diet: Eat a diet rich in fruits and vegetables, especially dark leafy greens like spinach and kale.\nExercise regularly: Exercise can help you maintain a healthy weight and reduce your risk of developing AMD.\nQuit smoking: Smoking can increase your risk of developing AMD, so it is important to quit smoking if you are a smoker.\nGet regular eye exams: Regular eye exams can help your healthcare provider detect AMD early and start treatment before it gets worse.",
                'Cataract':"Wear sunglasses: Protect your eyes from the sun by wearing sunglasses that block UV rays.\nEat a healthy diet: Eat a diet rich in fruits and vegetables, especially dark leafy greens like spinach and kale.\nExercise regularly: Exercise can help you maintain a healthy weight and reduce your risk of developing cataracts.\nQuit smoking: Smoking can increase your risk of developing cataracts, so it is important to quit smoking if you are a smoker.\nGet regular eye exams: Regular eye exams can help your healthcare provider detect cataracts early and start treatment before they get worse.",
                'Glaucoma':"Take medication: Use eye drops and other medications as prescribed by your healthcare provider.\nProtect your eyes: Wear sunglasses and a hat when you are outside, and wear eye protection when using power tools or playing sports.\nEat a healthy diet: Eat a diet rich in fruits and vegetables, especially dark leafy greens like spinach and kale.\nExercise regularly: Exercise can help you maintain a healthy weight and reduce your risk of developing glaucoma.\nQuit smoking: Smoking can increase your risk of developing glaucoma, so it is important to quit smoking if you are a smoker.\nGet regular eye exams: Regular eye exams can help your healthcare provider detect glaucoma early and start treatment before it gets worse.",
                'Myopia':"Wear glasses or contact lenses: Corrective lenses can help you see clearly if you have myopia.\nProtect your eyes: Wear sunglasses that block UV rays and a hat when you are outside.\nTake breaks: If you spend a lot of time looking at a computer screen or reading, take breaks to rest your eyes.\nGet regular eye exams: Regular eye exams can help your healthcare provider detect myopia early and start treatment before it gets worse.",
                'Non-eye':'Non-eye disease',
                'Normal':'Maintain a healthy lifestyle: Eat a balanced diet, exercise regularly, and get enough sleep to keep your eyes healthy.\nProtect your eyes: Wear sunglasses that block UV rays and a hat when you are outside, and wear eye protection when using power tools or playing sports.\nGet regular eye exams: Regular eye exams can help your healthcare provider detect eye problems early and start treatment before they get worse.'
            }
            image_url = url[disease]
            info=disease_info[disease]
            # UI Styling
            st.markdown(
                """
                <style>
                    
                    .left {
                        flex: 1;
                        padding: 20px;
                    }
                    .right {
                        flex: 1;
                        text-align: center;
                    }
                    .center {
                        text-align: center;
                        margin-top: 20px;
                    }
                </style>
                """,
                unsafe_allow_html=True
            )

            # Display the container with user details and image
            st.markdown('<div class="container">', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown('<div class="left">', unsafe_allow_html=True)
                st.write(f"**Name:** {name}")
                st.write(f"**Age:** {age}")
                st.write(f"**Gender:** {gender}")
                st.write(f"**Disease:** {disease}")
                st.markdown('</div>', unsafe_allow_html=True)
                # Generate report file
                report_data = generate_report(name, age, gender, disease, image_url, disease_info[disease],precautions[disease])

                # Download button
                st.markdown('<div class="center">', unsafe_allow_html=True)
                st.download_button(label="📥 Download Report", data=report_data, file_name="Patient_Report.html", mime="text/html")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="right">', unsafe_allow_html=True)
                st.image(image_url, caption=disease, use_column_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
        except:
            st.error("No Disease Detected Yet")

    elif select == 'Logout':
        st.session_state["logged_in"] = False
        st.session_state["current_user"] = None
        navigate_to_page("home")
