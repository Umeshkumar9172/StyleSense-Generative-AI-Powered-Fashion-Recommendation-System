import cv2
import numpy as np
from PIL import Image
import os

def load_face_cascade():
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    if not os.path.exists(cascade_path):
        raise FileNotFoundError(f"Haar cascade not found at {cascade_path}")
    return cv2.CascadeClassifier(cascade_path)

def detect_face(image_array):
    """
    Detects face in the image array (RGB) with improved detection sensitivity.
    Returns the face ROI (Region of Interest) or None if no face found.
    """
    print(f"  Image shape: {image_array.shape}")
    gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    
    # Apply image enhancement for better face detection
    # Histogram equalization
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray_enhanced = clahe.apply(gray)
    
    face_cascade = load_face_cascade()
    
    # Try multiple scale factors for better detection
    faces = []
    for scale_factor in [1.1, 1.15, 1.2, 1.3]:
        detected = face_cascade.detectMultiScale(gray_enhanced, scale_factor, 5, minSize=(50, 50))
        if len(detected) > 0:
            faces.extend(detected)
            print(f"  Faces detected at scale {scale_factor}: {len(detected)}")
    
    # Remove duplicates
    if len(faces) > 0:
        faces = np.array(faces)
        # Keep only unique faces (remove overlapping detections)
        unique_faces = []
        for face in faces:
            is_duplicate = False
            for unique_face in unique_faces:
                # Check if faces overlap
                x1, y1, w1, h1 = face
                x2, y2, w2, h2 = unique_face
                overlap = (abs(x1 - x2) < w1/2) and (abs(y1 - y2) < h1/2)
                if overlap:
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique_faces.append(face)
        faces = unique_faces
    
    print(f"  Total unique faces detected: {len(faces)}")
    
    if len(faces) == 0:
        return None
    
    # Return the largest face
    largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
    x, y, w, h = largest_face
    print(f"  Largest face dimensions: x={x}, y={y}, w={w}, h={h}")
    
    # Extract slightly smaller region to avoid background/hair
    margin = int(w * 0.15)
    face_roi = image_array[y+margin:y+h-margin, x+margin:x+w-margin]
    return face_roi

def classify_skin_tone(rgb_color):
    """
    Classifies skin tone based on the closest match to reference colors.
    rgb_color: tuple (R, G, B)
    """
    # Reference colors for skin tones (Approximate RGB)
    references = {
        "Fair": (255, 224, 189),
        "Medium": (234, 192, 134),
        "Olive": (198, 145, 95),
        "Deep": (100, 50, 40)
    }
    
    min_dist = float('inf')
    detected_tone = "Medium"
    
    r, g, b = rgb_color
    print(f"  Average RGB color: ({r}, {g}, {b})")
    
    for tone, ref_rgb in references.items():
        # Euclidean distance
        dist = np.sqrt((r - ref_rgb[0])**2 + (g - ref_rgb[1])**2 + (b - ref_rgb[2])**2)
        print(f"    - {tone}: distance = {dist:.2f}")
        if dist < min_dist:
            min_dist = dist
            detected_tone = tone
    
    print(f"  Best match: {detected_tone}")
    return detected_tone

def detect_face_shape(face_roi):
    """
    Detects face shape based on face dimensions.
    Returns one of: 'Round', 'Oval', 'Square', 'Heart', 'Oblong'
    """
    try:
        h, w = face_roi.shape[:2]
        aspect_ratio = w / h if h > 0 else 1
        
        print(f"  Face dimensions: width={w}, height={h}, ratio={aspect_ratio:.2f}")
        
        # Classify based on aspect ratio
        if aspect_ratio < 0.7:
            face_shape = "Oblong"
        elif aspect_ratio > 1.1:
            face_shape = "Heart"
        elif 0.85 < aspect_ratio < 1.05:
            face_shape = "Oval"
        elif aspect_ratio > 0.95:
            face_shape = "Round"
        else:
            face_shape = "Square"
        
        print(f"  Detected face shape: {face_shape}")
        return face_shape
    except Exception as e:
        print(f"  Could not detect face shape: {str(e)}")
        return "Oval"  # Default to Oval

def analyze_skin_tone(image_file):

    """
    Analyzes the uploaded image file to detect skin tone.
    Returns a dictionary with results.
    """
    try:
        print("Starting image analysis...")
        # Convert PIL Image to NumPy array
        image = Image.open(image_file).convert('RGB')
        print(f"  Image opened: format={image.format}, size={image.size}")
        
        image_array = np.array(image)
        
        face_roi = detect_face(image_array)
        
        if face_roi is None:
            print("  No face detected!")
            return {
                "success": False,
                "message": "No face detected in the image. Please upload a clear photo."
            }
        
        # Calculate average color of the face ROI
        print("  Calculating average skin color...")
        avg_color_per_row = np.average(face_roi, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        avg_rgb = tuple(avg_color.astype(int))
        
        skin_tone = classify_skin_tone(avg_rgb)
        face_shape = detect_face_shape(face_roi)
        
        print(f"Analysis complete! Skin tone: {skin_tone}, Face shape: {face_shape}\n")
        
        return {
            "success": True,
            "skin_tone": skin_tone,
            "face_shape": face_shape,
            "average_color": avg_rgb,
            "message": f"Detected skin tone: {skin_tone}, Face shape: {face_shape}"
        }
        
    except Exception as e:
        print(f"Error in analyze_skin_tone: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "message": f"Error processing image: {str(e)}"
        }
