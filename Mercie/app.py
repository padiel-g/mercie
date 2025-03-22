import streamlit as st
import datetime

st.set_page_config(page_title="CampusCONNECT", page_icon="🏫")

# Custom CSS for dark blue background
st.markdown(
    """
    <style>
    body {
        color: white;
        background-color: darkblue;
    }
    .stApp {
        background-color: darkblue;
    }
    .stTextInput>div>div>input {
        background-color: #333;
        color: white;
    }
    .stTextArea>div>div>textarea {
        background-color: #333;
        color: white;
    }
    .stSelectbox>div>div>div>div {
        background-color: #333;
        color: white;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stSlider>div>div>div>div[data-baseweb="slider-thumb"] {
        background-color: #4CAF50;
    }
    .stSlider>div>div>div>div[data-baseweb="slider-track"] {
        background-color: #222;
    }
    .stSlider>div>div>div>div[data-baseweb="slider-track-fill"] {
        background-color: #4CAF50;
    }
    .stRadio>div>label {
        color: white;
    }
    .stCheckbox>label {
        color: white;
    }
    .stNumberInput>div>div>div>input {
        background-color: #333;
        color: white;
    }
    .stDateInput>div>div>input {
        background-color: #333;
        color: white;
    }
    .stTimeInput>div>div>input {
        background-color: #333;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("CampusCONNECT")

# Simulate user data (replace with database integration in a real app)
if "user_data" not in st.session_state:
    st.session_state.user_data = {
        "notifications": [],
        "lecture_feedback": {},
        "resource_uploads": [],
        "discussion_posts": [],
        "profile": {"name": "User", "bio": "", "photo": None, "interests":""},
        "schedule":[]
    }

# Sidebar for navigation
page = st.sidebar.radio("Navigation", ["Dashboard", "Notifications", "Lectures", "Resources", "Discussion", "Profile", "Emergency Alerts"])

if page == "Dashboard":
    st.header("Dashboard")
    st.subheader("Upcoming Lectures")
    if st.session_state.user_data["schedule"]:
        for lecture in st.session_state.user_data["schedule"]:
            st.write(f"- {lecture['title']} at {lecture['time']} in {lecture['venue']}")
    else:
        st.write("No upcoming lectures.")
    st.subheader("Recent Notifications")
    for notification in st.session_state.user_data["notifications"][-5:]:
        st.write(f"- {notification}")

elif page == "Notifications":
    st.header("Notifications")
    for notification in st.session_state.user_data["notifications"]:
        st.write(f"- {notification}")
    st.subheader("Custom Notification Settings")
    notification_type = st.radio("Notification Type", ["Email", "SMS", "In-App"])
    snooze_time = st.slider("Snooze Time (minutes)", 0, 60, 15)
    if st.button("Save Notification Settings"):
        st.success(f"Notification settings saved. Type: {notification_type}, Snooze: {snooze_time} minutes")

elif page == "Lectures":
    st.header("Lecture Feedback and Ratings")
    lecture_title = st.text_input("Lecture Title")
    feedback = st.text_area("Feedback")
    rating = st.slider("Rating (1-5)", 1, 5)
    if st.button("Submit Feedback"):
        st.session_state.user_data["lecture_feedback"][lecture_title] = {"feedback": feedback, "rating": rating}
        st.success("Feedback submitted!")
    st.subheader("Lecture Ratings")
    for title, data in st.session_state.user_data["lecture_feedback"].items():
        st.write(f"- {title}: Rating {data['rating']}")

elif page == "Resources":
    st.header("Resource Sharing")
    resource_type = st.selectbox("Resource Type", ["Tutorial", "Video", "Link", "Document"])
    resource_title = st.text_input("Resource Title")
    resource_content = st.text_area("Resource Content")
    if st.button("Upload Resource"):
        st.session_state.user_data["resource_uploads"].append({
            "type": resource_type,
            "title": resource_title,
            "content": resource_content
        })
        st.success("Resource uploaded!")
    st.subheader("Uploaded Resources")
    for resource in st.session_state.user_data["resource_uploads"]:
        st.write(f"- {resource['title']} ({resource['type']})")

elif page == "Discussion":
    st.header("Discussion Forums")
    question = st.text_input("Ask a Question")
    if st.button("Submit Question"):
        st.session_state.user_data["discussion_posts"].append({"question": question, "answers": []})
        st.success("Question submitted!")
    st.subheader("Questions and Answers")
    for post in st.session_state.user_data["discussion_posts"]:
        st.write(f"**Q:** {post['question']}")
        for answer in post["answers"]:
            st.write(f"  - **A:** {answer}")
        answer = st.text_area(f"Answer for '{post['question']}'")
        if st.button(f"Submit Answer for '{post['question']}'"):
            post["answers"].append(answer)
            st.success("Answer submitted!")

elif page == "Profile":
    st.header("Profile")
    name = st.text_input("Name", st.session_state.user_data["profile"]["name"])
    bio = st.text_area("Bio", st.session_state.user_data["profile"]["bio"])
    interests= st.text_area("Interests", st.session_state.user_data["profile"]["interests"])
    photo = st.file_uploader("Upload Photo", type=["png", "jpg", "jpeg"])

    if st.button("Save Profile"):
        st.session_state.user_data["profile"]["name"] = name
        st.session_state.user_data["profile"]["bio"] = bio
        st.session_state.user_data["profile"]["interests"] = interests
        if photo:
            st.session_state.user_data["profile"]["photo"] = photo.read()
        st.success("Profile updated!")
    st.subheader("Your Profile")
    if st.session_state.user_data["profile"]["photo"]:
        st.image(st.session_state.user_data["profile"]["photo"], caption="Profile Photo")
    st.write(f"Name: {st.session_state.user_data['profile']['name']}")
    st.write(f"Bio: {st.session_state.user_data['profile']['bio']}")
    st.write(f"Interests: {st.session_state.user_data['profile']['interests']}")

elif page == "Emergency Alerts":
    st.header("Emergency Alerts")
    alert_message = st.text_area("Emergency Message")
    if st.button("Send Emergency Alert"):
        st.session_state.user_data["notifications"].append(f"Emergency: {alert_message}")
        st.success("Emergency alert sent!")
    st.subheader("Schedule Manager")
    lecture_title = st.text_input("Lecture Title", key="lecture_title_schedule")
    lecture_time = st.time_input("Lecture Time")
    lecture_date = st.date_input("Lecture Date")
    lecture_venue = st.text_input("Lecture Venue")
    if st.button("Add Lecture"):
        st.session_state.user_data["schedule"].append({"title":lecture_title,"time": lecture_time, "date": lecture_date, "venue": lecture_venue})
        st.success