        # Function to create test dataset from classes_dict
        def create_test_dataset(classes_dict):
            test_dataset = []
            for class_name, data in classes_dict.items():
                patterns = data["pattern"]
                for pattern in patterns:
                    test_dataset.append((pattern, random.choice(data["response"])))
            return test_dataset

        # Function to evaluate the accuracy of the chatbot
        def evaluate_chatbot_accuracy(test_dataset):
            correct_responses = 0
            total_responses = len(test_dataset)

            for input_text, correct_response in test_dataset:
                # Pass input to the chatbot
                response = accuracy_predict(input_text)

                # Check if chatbot's response matches correct response
                if response.strip().lower() == correct_response.strip().lower():
                    correct_responses += 1

            # Calculate accuracy
            accuracy = (correct_responses / total_responses) * 100
            return accuracy

        # Create test dataset
        test_dataset = create_test_dataset(classes_dict)

        # Evaluate chatbot accuracy
        accuracy = evaluate_chatbot_accuracy(test_dataset)
        print("Accuracy:", accuracy)
        speak(accuracy)