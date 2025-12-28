import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO

# 1. Load the Custom Trained Model
# The 'best.pt' file contains the weights learned during the Colab training session.
model_path = 'best.pt'

try:
    print(f"🔄 Loading model from: {model_path}...")
    model = YOLO(model_path)
    print("✅ AI Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    print("👉 Make sure you downloaded 'best.pt' from Google Colab and placed it in this folder.")
    exit()

def analyze_insurance_claim(image_path):
    """
    Runs the Computer Vision model on a car image to detect damages.
    """
    print(f"\n🕵️ Analyzing Insurance Claim for image: {image_path}...")
    
    # 2. Run Inference (Prediction)
    # conf=0.25: Threshold. Only show detections with >25% confidence.
    results = model.predict(image_path, save=True, conf=0.25)
    
    # 3. Visualize Results
    for result in results:
        boxes = result.boxes
        damage_count = len(boxes)
        
        print(f"📊 Assessment Complete. Damages detected: {damage_count}")
        
        # --- VISUALIZATION LOGIC (CLEAN MODE) ---
        # labels=False: Hides the class names (removes corrupted text).
        # conf=False: Hides the confidence score for a cleaner look.
        # boxes=True: Keeps the bounding boxes to highlight damages.
        result_array = result.plot(labels=False, conf=False, boxes=True) 
        
        # Convert Color Space: OpenCV uses BGR, Matplotlib uses RGB
        result_rgb = cv2.cvtColor(result_array, cv2.COLOR_BGR2RGB)
        
        # Display the Final Image
        plt.figure(figsize=(12, 10))
        plt.imshow(result_rgb)
        plt.axis('off') # Hide X/Y axis numbers
        
        # Dynamic Title based on severity logic
        if damage_count == 0:
            status = "NO DAMAGE DETECTED"
            color = 'green'
        elif damage_count <= 2:
            status = "MINOR DAMAGE (Repairable)"
            color = 'orange'
        else:
            status = "CRITICAL DAMAGE (Potential Total Loss)"
            color = 'darkred'

        plt.title(f"AI Analysis: {damage_count} Areas Identified | Verdict: {status}", fontsize=14, color=color, fontweight='bold')
        
        plt.show()

if __name__ == '__main__':
    # ⚠️ ACTION REQUIRED: 
    # Ensure 'test_car.jpg' is in the folder before running.
    test_image = 'test_car.jpg'
    
    try:
        analyze_insurance_claim(test_image)
    except FileNotFoundError:
        print(f"❌ Error: File '{test_image}' not found. Please add a test image.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")