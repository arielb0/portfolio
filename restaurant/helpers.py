from scull_suite.settings import BASE_DIR
import onnxruntime as onnx

'''
    TODO: Create a class with this function and instantiate on models.
'''
def make_inference(text: str):
    '''
        Given a a input text predicts if review is positive or negative,
        using a Open Neural Network Exchange (ONNX) format
    '''
    
    session = onnx.InferenceSession(f'{BASE_DIR}/restaurant/en_review_classificator.onnx', providers=['CPUExecutionProvider'])
    input_name = session.get_inputs()[0].name
    label_name = session.get_outputs()[0].name
    
    prediction = session.run([label_name], {input_name: [text]})

    return prediction[0]
    
    
