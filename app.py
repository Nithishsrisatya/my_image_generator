import gradio as gr
from fastapi import FastAPI
import torch
from diffusers import StableDiffusionPipeline
import os
from datetime import datetime
import uuid
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="AI Image Generator",
    description="Generate stunning images from text descriptions using Stable Diffusion",
    version="1.0.0"
)

# Initialize the Stable Diffusion pipeline
def load_model():
    """Load the Stable Diffusion model"""
    try:
        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16
        )
        pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
        return pipe
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

# Global variable to store the model
model = None

def generate_image(prompt, negative_prompt="", guidance_scale=7.5, num_inference_steps=20, width=512, height=512):
    """Generate an image from text prompt"""
    global model

    if model is None:
        print("Loading model...")
        model = load_model()

    if model is None:
        return None, "Error: Could not load the model. Please check your installation."

    try:
        # Generate the image
        image = model(
            prompt=prompt,
            negative_prompt=negative_prompt,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            width=width,
            height=height
        ).images[0]

        # Create output directory if it doesn't exist
        output_dir = "generated_images"
        os.makedirs(output_dir, exist_ok=True)

        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{timestamp}_{unique_id}.png"
        filepath = os.path.join(output_dir, filename)

        # Save the image
        image.save(filepath)

        return image, f"✅ Image generated successfully! Saved as: {filename}"

    except Exception as e:
        return None, f"❌ Error generating image: {str(e)}"

def clear_model():
    """Clear the model from memory"""
    global model
    if model is not None:
        del model
        model = None
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    return "🗑️ Model cleared from memory"

# Create the Gradio interface
with gr.Blocks(title="AI Image Generator", theme=gr.themes.Soft()) as interface:
    gr.Markdown("# 🎨 AI Image Generator")
    gr.Markdown("Generate stunning images from text descriptions using Stable Diffusion v1.5")

    with gr.Row():
        with gr.Column(scale=2):
            prompt = gr.Textbox(
                label="Prompt",
                placeholder="Enter your image description here...",
                lines=3,
                info="Describe the image you want to generate"
            )

            negative_prompt = gr.Textbox(
                label="Negative Prompt (Optional)",
                placeholder="What you DON'T want in the image...",
                lines=2,
                info="Describe elements to avoid in the generation"
            )

        with gr.Column(scale=1):
            with gr.Accordion("Advanced Settings", open=False):
                guidance_scale = gr.Slider(
                    label="Guidance Scale",
                    minimum=1,
                    maximum=20,
                    value=7.5,
                    step=0.5,
                    info="How closely to follow the prompt (higher = more strict)"
                )

                num_inference_steps = gr.Slider(
                    label="Inference Steps",
                    minimum=10,
                    maximum=100,
                    value=20,
                    step=5,
                    info="Number of denoising steps (more = higher quality, slower)"
                )

                width = gr.Slider(
                    label="Width",
                    minimum=256,
                    maximum=1024,
                    value=512,
                    step=64,
                    info="Image width in pixels"
                )

                height = gr.Slider(
                    label="Height",
                    minimum=256,
                    maximum=1024,
                    value=512,
                    step=64,
                    info="Image height in pixels"
                )

    generate_btn = gr.Button(
        "🎨 Generate Image",
        variant="primary",
        size="lg"
    )

    clear_btn = gr.Button(
        "🗑️ Clear Model",
        variant="secondary"
    )

    with gr.Row():
        output_image = gr.Image(
            label="Generated Image",
            height=512
        )
        output_text = gr.Textbox(
            label="Status",
            interactive=False,
            lines=2
        )

    # Event handlers
    generate_btn.click(
        fn=generate_image,
        inputs=[prompt, negative_prompt, guidance_scale, num_inference_steps, width, height],
        outputs=[output_image, output_text]
    )

    clear_btn.click(
        fn=clear_model,
        inputs=[],
        outputs=[output_text]
    )

    # Example prompts
    gr.Examples(
        examples=[
            ["A beautiful sunset over mountains, digital art, highly detailed"],
            ["A cute robot in a futuristic city, cyberpunk style"],
            ["A magical forest with glowing mushrooms and fireflies"],
            ["A majestic eagle soaring over snow-capped peaks"],
            ["A cozy coffee shop interior with warm lighting"],
        ],
        inputs=prompt,
        label="Example Prompts"
    )

# Mount Gradio app to FastAPI
app = gr.mount_gradio_app(app, interface, path="/")

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "AI Image Generator API", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": model is not None}

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=7860,
        reload=True,
        log_level="info"
    )
