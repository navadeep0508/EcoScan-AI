from flask import Flask, render_template, Response, request, jsonify
from ultralytics import YOLO
import cv2
import os
import numpy as np
import base64

app = Flask(__name__)

# Load model
model = YOLO("best.pt")

# Global state for streaming and configuration
camera = None
stream_source = 0  # 0 for webcam, or file path string for video file
is_streaming = False
conf_threshold = 0.25

# Directory for video uploads
UPLOAD_FOLDER = os.path.join('static', 'temp_uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_camera():
    global camera, stream_source, is_streaming
    if not is_streaming:
        return None
    
    if camera is None:
        camera = cv2.VideoCapture(stream_source)
        # Optional webcam size optimization
        if stream_source == 0:
            camera.set(3, 1280)
            camera.set(4, 720)
    elif not camera.isOpened():
        camera.open(stream_source)
        
    return camera

def release_camera():
    global camera, is_streaming
    is_streaming = False
    if camera is not None:
        camera.release()
        camera = None

def generate_frames():
    global camera, is_streaming, conf_threshold, stream_source
    while is_streaming:
        cap = get_camera()
        if cap is None or not cap.isOpened():
            break
            
        success, frame = cap.read()
        if not success:
            # If it is a video file, loop it back to frame 0
            if isinstance(stream_source, str) and stream_source != '0':
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                success, frame = cap.read()
                if not success:
                    break
            else:
                break
                
        # Run YOLO prediction with dynamic confidence
        results = model(frame, conf=conf_threshold)
        
        # Plot detections
        annotated_frame = results[0].plot()
        
        # Convert frame to JPG
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        if not ret:
            continue
            
        frame_bytes = buffer.tobytes()
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame_bytes +
            b'\r\n'
        )
    
    # Ensure camera is released when stream completes
    release_camera()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/video')
def video():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/start_feed', methods=['POST'])
def start_feed():
    global is_streaming, stream_source, camera
    data = request.get_json() if request.is_json else {}
    source_type = data.get('source', 'webcam')
    
    # Release current camera session if active
    if camera is not None:
        camera.release()
        camera = None
        
    if source_type == 'webcam':
        stream_source = 0
    elif source_type == 'video':
        video_path = data.get('path')
        if video_path and os.path.exists(video_path):
            stream_source = video_path
        else:
            return jsonify({'success': False, 'error': 'Specified video file not found'}), 404
    else:
        return jsonify({'success': False, 'error': 'Invalid stream source type'}), 400
        
    is_streaming = True
    
    # Verify we can open the source
    cap = get_camera()
    if cap is None or not cap.isOpened():
        is_streaming = False
        if camera is not None:
            camera.release()
            camera = None
            
        # Check if we are running in the cloud (Render environment)
        is_cloud = 'RENDER' in os.environ or 'PORT' in os.environ
        if is_cloud and source_type == 'webcam':
            return jsonify({
                'success': False,
                'error': 'Webcam hardware is not available on cloud hosting servers (Render). Please use the "Uploader" or "Samples" tabs in the operations center to test the AI garbage detection!'
            }), 400
            
        return jsonify({'success': False, 'error': 'Failed to initialize the media source'}), 500
        
    return jsonify({
        'success': True,
        'source': 'webcam' if stream_source == 0 else 'video',
        'is_streaming': is_streaming
    })

@app.route('/stop_feed', methods=['POST'])
def stop_feed():
    release_camera()
    return jsonify({
        'success': True,
        'is_streaming': False
    })

@app.route('/set_confidence', methods=['POST'])
def set_confidence():
    global conf_threshold
    data = request.get_json() if request.is_json else {}
    conf = data.get('conf')
    if conf is not None:
        try:
            conf_threshold = float(conf)
            return jsonify({'success': True, 'confidence': conf_threshold})
        except ValueError:
            return jsonify({'success': False, 'error': 'Confidence must be a float'}), 400
    return jsonify({'success': False, 'error': 'Missing conf value'}), 400

@app.route('/detect_image', methods=['POST'])
def detect_image():
    global conf_threshold
    img = None
    
    # 1. Process uploaded custom file
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '':
            file_bytes = np.frombuffer(file.read(), np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            
    # 2. Process pre-loaded test file
    elif request.is_json:
        req_data = request.get_json()
        if req_data and 'filename' in req_data:
            filename = req_data['filename']
            # Remove any path traversal components
            filename = os.path.basename(filename)
            img_path = os.path.join('static', 'test_images', filename)
            if os.path.exists(img_path):
                img = cv2.imread(img_path)
            
    if img is None:
        return jsonify({'success': False, 'error': 'No valid image provided'}), 400
        
    # Get dynamic confidence from parameters or fallback to global configuration
    conf_val = conf_threshold
    if request.is_json:
        req_data = request.get_json()
        if req_data and 'conf' in req_data:
            try:
                conf_val = float(req_data['conf'])
            except ValueError:
                pass
            
    # Run YOLO prediction
    results = model(img, conf=conf_val)
    annotated_img = results[0].plot()
    
    # Process detections
    detections = []
    summary_counts = {}
    
    boxes = results[0].boxes
    for box in boxes:
        cls_id = int(box.cls[0].item())
        cls_name = model.names[cls_id]
        conf = float(box.conf[0].item())
        coords = box.xyxy[0].tolist()
        
        detections.append({
            'class': cls_name,
            'confidence': conf,
            'bbox': [int(c) for c in coords]
        })
        summary_counts[cls_name] = summary_counts.get(cls_name, 0) + 1
        
    # Encode output to base64 JPG
    ret, buffer = cv2.imencode('.jpg', annotated_img)
    if not ret:
        return jsonify({'success': False, 'error': 'Failed to encode output image'}), 500
        
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    
    return jsonify({
        'success': True,
        'image': f"data:image/jpeg;base64,{img_base64}",
        'detections': detections,
        'summary': summary_counts,
        'total_count': len(detections)
    })

@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'success': False, 'error': 'No video file provided'}), 400
        
    file = request.files['video']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
        
    # Save the file securely to temp folder
    filename = secure_filename_local(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    return jsonify({
        'success': True,
        'path': filepath,
        'filename': filename
    })

def secure_filename_local(filename):
    # Simple secure filename sanitizer
    return "".join(c for c in filename if c.isalnum() or c in ('.', '_', '-')).strip()

if __name__ == '__main__':
    # Dynamic port binding for Render deployment
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)