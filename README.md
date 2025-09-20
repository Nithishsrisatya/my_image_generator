# 🎨 AI Image Generator

A powerful web-based image generation application built with FastAPI + Gradio and Stable Diffusion. Generate stunning images from text descriptions with an intuitive interface, ready for deployment on Vercel.

## ✨ Features

- **Text-to-Image Generation**: Create images from natural language descriptions
- **Advanced Controls**: Adjust guidance scale, inference steps, and image dimensions
- **Negative Prompts**: Specify what you don't want in your images
- **Real-time Progress**: Visual progress tracking during generation
- **Image Gallery**: Automatically saves generated images with timestamps
- **GPU Support**: Optimized for both CPU and GPU processing
- **FastAPI Integration**: RESTful API endpoints for programmatic access
- **Production Ready**: Built for deployment on Vercel and other cloud platforms
- **Modern UI**: Clean, responsive interface built with Gradio

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- At least 8GB RAM (16GB recommended)
- NVIDIA GPU with CUDA support (optional, but recommended for faster generation)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd my_image_generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:7860` to access the web interface.

### API Endpoints

- **GET /** - Root endpoint with API information
- **GET /health** - Health check endpoint
- **GET /gradio** - Gradio web interface (mounted at root)

### Vercel Deployment

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy to Vercel**
   ```bash
   vercel --prod
   ```

3. **Set Environment Variables** (in Vercel dashboard):
   - Add any required environment variables for your deployment

### Alternative Deployment Options

#### Railway
```bash
pip install railway
railway login
railway deploy
```

#### Render
1. Connect your GitHub repository to Render
2. Select Python service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

#### Heroku
```bash
heroku create your-app-name
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-python
git push heroku main
```

## 📖 Usage

### Basic Image Generation

1. Enter a descriptive prompt in the text box (e.g., "A beautiful sunset over mountains")
2. Optionally add a negative prompt to exclude unwanted elements
3. Click "🎨 Generate Image" to start the generation process
4. Wait for the image to be generated and view the result

### Advanced Settings

- **Guidance Scale**: Controls how closely the model follows your prompt (1-20, default: 7.5)
- **Inference Steps**: Number of denoising steps (10-100, default: 20)
- **Image Dimensions**: Width and height in pixels (256-1024, default: 512x512)

### Example Prompts

Try these example prompts to get started:
- "A majestic eagle soaring over snow-capped mountains, photorealistic"
- "A cute robot in a futuristic city, cyberpunk style, neon lights"
- "A magical forest with glowing mushrooms and fireflies, fantasy art"
- "A cozy coffee shop interior with warm lighting, digital painting"

## 🛠️ Configuration

### Model Settings

The application uses Stable Diffusion v1.4 by default. You can modify the model in `app.py`:

```python
pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",  # Change this to use different models
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)
```

### Performance Optimization

For better performance:

1. **GPU Usage**: Ensure you have CUDA installed for GPU acceleration
2. **Memory Management**: Use the "Clear Model" button to free up GPU memory
3. **Batch Size**: Reduce image dimensions for faster generation

## 📁 Project Structure

```
my_image_generator/
│
├─ app.py              # Main application with Gradio interface
├─ requirements.txt    # Python dependencies
├─ README.md          # Project documentation
├─ .gitignore         # Git ignore rules
└─ generated_images/   # Output directory for generated images
```

## 🔧 Troubleshooting

### Common Issues

1. **Out of Memory Error**
   - Reduce image dimensions
   - Use CPU instead of GPU
   - Clear model from memory using the "Clear Model" button

2. **Slow Generation**
   - Ensure GPU is being used (check CUDA installation)
   - Reduce number of inference steps
   - Use smaller image dimensions

3. **Model Download Issues**
   - Check internet connection
   - Ensure sufficient disk space (~4GB for base model)
   - Try running with `--offline` flag if model is already downloaded

### Error Messages

- **"RuntimeError: CUDA out of memory"**: Reduce batch size or image dimensions
- **"ImportError: No module named 'diffusers'"**: Install requirements with `pip install -r requirements.txt`
- **"torch.cuda.is_available() returned False"**: CUDA not properly installed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Stability AI](https://stability.ai/) for Stable Diffusion
- [Gradio](https://gradio.app/) for the web interface framework
- [Hugging Face](https://huggingface.co/) for the Diffusers library

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Search existing issues on GitHub
3. Create a new issue with detailed information about your problem

---

**Happy generating! 🎨**
