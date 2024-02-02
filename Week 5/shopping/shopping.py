import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    # Set lists
    evidence = []
    labels = []

    # Data types used for the evidence list
    data_types = [int, float, int, float, int, float,
                  float, float, float, float, int, int, int, int, int, int, int]
    
    # Months used for the correct values in row["Month"]
    month_names = ["Jan", "Feb", "Mar", "Apr", "May",
                   "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    # Open file
    with open(filename, newline='') as file:
        # Set reader, skip to [1] in order to avoid the header
        reader = csv.DictReader(file)

        # Add evidence and labels to lists
        for row in reader:
            # Convert Month
            row["Month"] = month_names.index(row["Month"]) + 1
            # Convert Weekend col
            row["Weekend"] = 0 if "False" else 1
            # Convert VIsitorType
            row["VisitorType"] = 1 if "Returning_Visitor" else 0

            # Convert row to specific data types
            converted_row = [
                data_type(row[value]) for value, data_type in zip(reader.fieldnames, data_types)]
            evidence.append(converted_row)

            # Append to labels 0 if "FALSE", 1 if "TRUE"
            labels.append(0) if row["Revenue"] == "FALSE" else labels.append(1)

    # Return lists if length is equal
    if len(evidence) == len(labels):
        return((evidence, labels))
    
    # Throw error otherwise
    else:
        raise Exception("Something went wrong")



def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Implement KNeighborsClassifier
    model = KNeighborsClassifier(n_neighbors=1)

    # Fit the model
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    for label, prediction in zip(labels, predictions):
        if label == 1 and prediction == 1:
            true_positive += 1
        elif label == 0 and prediction == 0:
            true_negative += 1
        elif label == 0 and prediction == 1:
            false_positive += 1
        else:
            false_negative += 1

    # Calculate True Positive Rate (Sensitivity/Recall) and True Negative Rate (Specificity)
    sensitivity = true_positive / (true_positive + false_negative)
    specificity = true_negative / (true_negative + false_positive)

    return sensitivity, specificity




if __name__ == "__main__":
    main()
