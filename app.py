import gradio as gr
from detector import ObjectDetector, MODELS

detector = ObjectDetector()

css = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

* { font-family: 'Space Grotesk', sans-serif !important; }

body, .gradio-container {
    background: transparent !important;
    min-height: 100vh;
}

#neural-bg {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 0;
    background: linear-gradient(135deg, #0a0a0f 0%, #0d1117 50%, #0a0f1a 100%);
}

.gradio-container {
    position: relative;
    z-index: 1;
    max-width: 1200px !important;
    margin: 0 auto !important;
}

#title { text-align: center; padding: 2rem 0 0.5rem; }

#title h1 {
    font-size: 3rem !important;
    font-weight: 700 !important;
    background: linear-gradient(90deg, #00d2ff, #3a7bd5, #00d2ff);
    background-size: 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s infinite linear;
    letter-spacing: -1px;
}

@keyframes shimmer {
    0% { background-position: 0% }
    100% { background-position: 200% }
}

#subtitle { text-align: center; margin-bottom: 2rem !important; }
#subtitle p { color: #4a5568 !important; }

.tab-nav { background: #0d1117 !important; border-bottom: 1px solid #1a2332 !important; }
.tab-nav button { color: #4a5568 !important; font-weight: 500 !important; padding: 0.75rem 1.5rem !important; border-radius: 0 !important; transition: all 0.2s !important; }
.tab-nav button.selected { color: #00d2ff !important; border-bottom: 2px solid #00d2ff !important; background: transparent !important; }

.controls-row {
    background: rgba(13,17,23,0.85) !important;
    border: 1px solid #1a2332 !important;
    border-radius: 12px !important;
    padding: 1.25rem !important;
    margin-bottom: 1.5rem !important;
    backdrop-filter: blur(10px) !important;
}

label { color: #8892a4 !important; font-size: 0.8rem !important; font-weight: 500 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; }
select, .wrap { background: #161b22 !important; border: 1px solid #1a2332 !important; border-radius: 8px !important; color: #e6edf3 !important; }
input[type=range] { accent-color: #00d2ff !important; }

.block {
    background: rgba(13,17,23,0.85) !important;
    border: 1px solid #1a2332 !important;
    border-radius: 12px !important;
    backdrop-filter: blur(10px) !important;
}

button.primary {
    background: linear-gradient(90deg, #00d2ff, #3a7bd5) !important;
    border: none !important;
    border-radius: 8px !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 0.75rem 2rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s !important;
}
button.primary:hover { opacity: 0.85 !important; }

textarea, input[type=text] { background: #161b22 !important; border: 1px solid #1a2332 !important; color: #e6edf3 !important; border-radius: 8px !important; }
.image-container, canvas { border-radius: 10px !important; border: 1px solid #1a2332 !important; }
footer { display: none !important; }
"""

html_bg = """
<canvas id="neural-bg"></canvas>
<script>
const canvas = document.getElementById('neural-bg');
const ctx = canvas.getContext('2d');

function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resize();
window.addEventListener('resize', resize);

const PARTICLE_COUNT = 80;
const CONNECTION_DISTANCE = 150;
const particles = [];

for (let i = 0; i < PARTICLE_COUNT; i++) {
    particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4,
        r: Math.random() * 2.5 + 1,
        pulse: Math.random() * Math.PI * 2,
    });
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.pulse += 0.02;

        if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
        if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

        for (let j = i + 1; j < particles.length; j++) {
            const q = particles[j];
            const dx = p.x - q.x;
            const dy = p.y - q.y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < CONNECTION_DISTANCE) {
                const alpha = (1 - dist / CONNECTION_DISTANCE) * 0.9;
                ctx.beginPath();
                ctx.strokeStyle = `rgba(0, 210, 255, ${alpha})`;
                ctx.lineWidth = 0.8;
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(q.x, q.y);
                ctx.stroke();
            }
        }

        const glow = Math.sin(p.pulse) * 0.3 + 0.7;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(0, 210, 255, 1)`;
        ctx.fill();

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r * 2.5, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(0, 210, 255, 0.3)`;
        ctx.fill();
    }

    requestAnimationFrame(draw);
}
draw();
</script>
"""

def run_image(image, confidence, model_label):
    if image is None:
        return None, "No image uploaded", ""
    detector.load_model(model_label)
    return detector.detect_image(image, confidence)

def run_video(video, confidence, model_label):
    if video is None:
        return None
    detector.load_model(model_label)
    return detector.detect_video(video, confidence)

def run_webcam(image, confidence, model_label):
    if image is None:
        return None, "No feed", ""
    detector.load_model(model_label)
    return detector.detect_image(image, confidence)

with gr.Blocks(css=css, title="VisionAI — Object Detection") as app:

    gr.HTML(html_bg)
    gr.Markdown("# ⬡ VisionAI Detection", elem_id="title")
    gr.Markdown("Real-time object detection powered by YOLOv8", elem_id="subtitle")

    with gr.Row(elem_classes="controls-row"):
        model_selector = gr.Dropdown(
            choices=list(MODELS.keys()),
            value="YOLOv8 Nano (fastest)",
            label="🤖 Model",
        )
        confidence = gr.Slider(
            minimum=0.1,
            maximum=0.9,
            value=0.25,
            step=0.05,
            label="⚡ Confidence Threshold",
        )

    with gr.Tabs():
        with gr.Tab("🖼️  Image"):
            with gr.Row():
                with gr.Column():
                    img_input = gr.Image(type="pil", label="Upload Image")
                    img_btn = gr.Button("Detect Objects →", variant="primary")
                with gr.Column():
                    img_output = gr.Image(label="Detection Result")
                    img_count = gr.Textbox(label="Count")
                    img_summary = gr.Textbox(label="Detections", lines=8)
            img_btn.click(
                fn=run_image,
                inputs=[img_input, confidence, model_selector],
                outputs=[img_output, img_summary, img_count],
            )

        with gr.Tab("🎥  Video"):
            with gr.Row():
                with gr.Column():
                    vid_input = gr.Video(label="Upload Video")
                    vid_btn = gr.Button("Process Video →", variant="primary")
                with gr.Column():
                    vid_output = gr.Video(label="Annotated Output")
            vid_btn.click(
                fn=run_video,
                inputs=[vid_input, confidence, model_selector],
                outputs=[vid_output],
            )

        with gr.Tab("📷  Webcam"):
            gr.Markdown("#### Allow camera access when prompted by your browser.")
            with gr.Row():
                with gr.Column():
                    webcam_input = gr.Image(
                        sources=["webcam"],
                        streaming=True,
                        type="pil",
                        label="Live Camera Feed",
                    )
                with gr.Column():
                    webcam_output = gr.Image(label="Detection Output")
                    webcam_count = gr.Textbox(label="Count")
                    webcam_summary = gr.Textbox(label="Detections", lines=8)
            webcam_input.stream(
                fn=run_webcam,
                inputs=[webcam_input, confidence, model_selector],
                outputs=[webcam_output, webcam_count, webcam_summary],
            )

if __name__ == "__main__":
    app.launch()