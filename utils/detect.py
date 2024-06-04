from modules.onnx import load_session, infer
from modules.FaceMesh import FaceMeshKeyPoint, Difference
from scipy.special import softmax


def load_model():
    FM = FaceMeshKeyPoint()
    session = load_session('models/model.onnx')
    return FM, session

def get_label(FM, session, anchor, frame):
    """
    Calculates the label for a given anchor and frame.

    Args:
        FM: The feature matching object.
        session: The inference session.
        anchor: The anchor frame.
        frame: The frame to compare with the anchor.

    Returns:
        The label indicating whether the frame matches the anchor or not.
        Returns 1 if the frame matches the anchor, otherwise returns 0.
    """
    frame = FM.define_feature(frame)
    anchor = FM.define_feature(anchor)
    diff = Difference(anchor, frame).astype('float32')
    out = infer(session, diff.reshape(1, -1))
    
    results = softmax(out)
    if results[0][1] >= 0.5:
        return 1
    else:
        return 0
