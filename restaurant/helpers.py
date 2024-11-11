from scull_suite.settings import BASE_DIR
import onnxruntime as onnx

class MLClassifier:
    __session = onnx.InferenceSession(f'{BASE_DIR}/restaurant/nlp_classifier.onnx', providers = ['CPUExecutionProvider'])
    __input_name = __session.get_inputs()[0].name
    __label_name = __session.get_outputs()[0].name
    __prob_name = __session.get_outputs()[1].name

    @classmethod
    def classify_text(cls, text: str):
        '''
            Given a text, classify on categories.

            Parameters
            ----------

            text : str
                Text that you need to classify.

            Returns
            -------

            list
                A list that contains classification result and the probabilities
                for each category.

                list[0] A list with classification result.

                list[1] A dictionary with the probability distribution of each category. 
                Dictionary key is the category number and dictionary value is the probability.
        '''
        
        return cls.__session.run([cls.__label_name, cls.__prob_name], {cls.__input_name: [text]})
    
    def get_highest_prob(prob_distribution: dict):
        '''
            Get the highest probability on probability distribution output.

            Parameters
            ----------
            prob_distribution : dict
                A dictionary with the probabilities of each output category.
                keys are categories, values are the probabilities of each category.

            Returns
            -------
            float
                The highest probability on the probability distribution.
        '''
        highest_probability = 0

        for probability in prob_distribution.values():
            if probability > highest_probability:
                highest_probability = probability

        return highest_probability
       

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
    
    
