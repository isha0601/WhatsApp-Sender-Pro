
import streamlit as st
import pywhatkit as kit
from datetime import datetime

st.set_page_config(page_title="📲 WhatsApp Sender Pro", page_icon="💬")

st.title("💬 WhatsApp Sender Pro")

st.write("""
**Features**
- Send Text
- Send Images
- Schedule or Instant
""")

# Input fields
phone_number = st.text_input("Enter phone number (with country code)", "+91")
send_type = st.radio("What do you want to send?", ["Text Message", "Image"])

message = None
file_path = None

if send_type == "Text Message":
    message = st.text_area("Type your message")
else:
    file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    caption = st.text_input("Image Caption (optional)")

    if file is not None:
        # Save file temporarily
        file_path = f"temp_{file.name}"
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

when_to_send = st.radio("When to send?", ["Send Now", "Schedule"])

if when_to_send == "Schedule":
    hour = st.number_input("Hour (24h)", min_value=0, max_value=23, value=datetime.now().hour)
    minute = st.number_input("Minute", min_value=0, max_value=59, value=(datetime.now().minute + 2) % 60)

if st.button("🚀 Send"):
    if phone_number:
        try:
            if send_type == "Text Message" and message:
                if when_to_send == "Send Now":
                    st.info("Sending message in 20 seconds... keep browser open!")
                    kit.sendwhatmsg_instantly(phone_no=phone_number, message=message, wait_time=20, tab_close=True)
                else:
                    kit.sendwhatmsg(phone_no=phone_number, message=message, time_hour=hour, time_min=minute, wait_time=20, tab_close=True)
                st.success("✅ Message ready on WhatsApp Web!")
            elif send_type == "Image" and file_path:
                if when_to_send == "Send Now":
                    st.info("Sending image in 20 seconds...")
                    kit.sendwhats_image(receiver=phone_number, img_path=file_path, caption=caption, wait_time=20, tab_close=True)
                    st.success("✅ Image sent!")
                else:
                    st.warning("⚠️ Scheduling images not supported by pywhatkit directly. Please use instant send for images.")
            else:
                st.warning("Please provide all inputs.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter the phone number.")
