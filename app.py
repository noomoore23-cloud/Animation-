import gradio as gr
import cv2
import os
import shutil

# தற்காலிக கோப்புறையை சுத்தம் செய்ய
def clear_temp_folder():
    if os.path.exists("temp_output"):
        shutil.rmtree("temp_output")
    os.makedirs("temp_output")

def create_animation(images, fps, output_format):
    if not images:
        return None
    
    clear_temp_folder()
    
    # முதல் படத்தின் அளவை எடுத்தல்
    frame = cv2.imread(images[0])
    height, width, layers = frame.shape
    
    # வெளியீட்டு கோப்பு பெயர்
    extension = ".mp4" if output_format == "MP4" else ".avi"
    output_path = f"temp_output/animation{extension}"
    
    # Codec தேர்வு
    if output_format == "MP4":
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    else:
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')

    video = cv2.VideoWriter(output_path, fourcc, int(fps), (width, height))

    for image_path in images:
        img = cv2.imread(image_path)
        if img is not None:
            # எல்லா படங்களையும் முதல் படத்தின் அளவுக்கு மாற்றுதல் (Resize)
            img_resized = cv2.resize(img, (width, height)) 
            video.write(img_resized)

    video.release()
    return output_path

# Gradio முகப்பு
with gr.Interface(
    fn=create_animation,
    inputs=[
        gr.File(file_count="multiple", label="Upload Images (வரிசையாக தேர்வு செய்யவும்)"),
        gr.Slider(1, 60, value=12, label="FPS (வேகம்)"),
        gr.Radio(["MP4", "AVI"], value="MP4", label="Video Format")
    ],
    outputs=gr.Video(label="Output Animation"),
    title="Mobile Animation Maker",
    description="உங்கள் படங்களை வீடியோவாக மாற்றும் எளிய கருவி. Termux-ல் இயங்கக்கூடியது."
) as app:
    pass

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", share=True)
