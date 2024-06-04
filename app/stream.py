# streaming camera
import cv2
from utils.detect import load_model, get_label
from db.controller_db import update_db
def streaming_camera(option):
    """
    Stream the camera to the screen.
    """
    labels = {0: 'Abnormal', 1: 'Normal'}
    cap = cv2.VideoCapture(option)
    anchor = None
    FM,session = load_model()
    
    
    while True:
        ret, frame = cap.read()
        if anchor is None:
            anchor = frame
        if not ret:
            break
        label = get_label(FM, session, anchor, frame)
        update_db(str(label))
        if option == 0:
            cv2.putText(frame, f'{labels[label]}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        
    cap.release()
    cv2.destroyAllWindows()