import gradio as gr
import cv2
import os

def create_animation(images, fps):
    if not images:
        return None
    
    # தற்காலிக கோப்பு பெயர்
    output_video = "animation.mp4"
    
    # முதல் படத்தின் அளவை எடுத்தல்
    frame = cv2.imread(images[0])
    height, width, layers = frame.shape
    
    # Codec setup for Linux servers (Hugging Face runs on Linux)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_video, fourcc, int(fps), (width, height))

    for image_path in images:
        img = cv2.imread(image_path)
        if img is not None:
            img_resized = cv2.resize(img, (width, height)) 
            video.write(img_resized)

    video.release()
    return output_video

# Gradio Interface
interface = gr.Interface(
    fn=create_animation,
    inputs=[
        gr.File(file_count="multiple", label="படங்களை பதிவேற்றவும்"),
        gr.Slider(1, 60, value=10, label="FPS (வேகம்)")
    ],
    outputs=gr.Video(label="வெளியீடு"),
    title="Animation Maker",
    description="GitHub + Hugging Face மூலம் இயங்குகிறது."
)

if __name__ == "__main__":
    interface.launch()
