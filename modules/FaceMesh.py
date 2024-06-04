import cv2
import mediapipe as mp
import numpy as np

class FaceMeshKeyPoint:
    def __init__(self):
        mp_face_mesh = mp.solutions.face_mesh
        holistic = mp.solutions.holistic.Holistic()

        self.face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)
        self.vector_0 = np.zeros((468,2))
        
    def ExtractKeyPoint(self,img):
        try:
            rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_image)
            if len(results.multi_face_landmarks) != 1:
                return self.vector_0
            ListKeyPoint = [(landmark.x , landmark.y )
                            for face_landmarks in results.multi_face_landmarks
                            for landmark in face_landmarks.landmark]
           
            return np.array(ListKeyPoint)
        except:
            # print('Face not Found')
            return self.vector_0
        
    def Align(self, img):
        """
        Aligns the image based on the extracted key points.

        Args:
            img (numpy.ndarray): The input image.

        Returns:
            numpy.ndarray: The aligned image.

        """
        key_point = self.ExtractKeyPoint(img)
        if np.array_equal(key_point, self.vector_0):
            return img
        ih, iw, _ = img.shape 

        x_max = int((np.max(key_point[:, 0]) + 0.025) * iw)
        y_max = int(np.max(key_point[:, 1]) * ih)
        x_min = int((np.min(key_point[:, 0]) - 0.025) * iw)
        y_min = int((np.min(key_point[:, 1]) - 0.1) * ih)

        return img[y_min:y_max, x_min:x_max]

    
    def define_feature(self,img):
        kp1 = self.ExtractKeyPoint(img)
        img_Align = self.Align(img)
        kp2 = self.ExtractKeyPoint(img_Align)
        return np.concatenate((kp1, kp2), axis=0)
    
    
def Difference(marginFace, face):
    """
    Calculates the difference between two arrays using the Euclidean distance.

    Parameters:
    marginFace (numpy.ndarray): The first array.
    face (numpy.ndarray): The second array.

    Returns:
    numpy.ndarray: The difference between the two arrays.
    """
    return np.sqrt(np.sum((marginFace - face) ** 2, axis=1))


