import cv2

def capture_from_camera(stream_url):
    cap = cv2.VideoCapture(stream_url)
    
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow("Camera Stream", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Example usage
stream_url = 'http://192.168.1.100:8080/video'  # Replace with your camera's stream URL
capture_from_camera(stream_url)
