import random
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier as Model
import pandas as pd


def algorithm(TrainCsv, Data):
    dataset = pd.read_csv(TrainCsv)
    dataset.fillna(0)
    data_x = dataset.iloc[:, :-1]
    data_y = dataset.iloc[:, -1]
    rendom_number = random.randrange(0, len(dataset))
    random_data = dataset.iloc[rendom_number, :-1]
    datas = random_data.values.tolist()
    sample_x = list(data_x.iloc[0])
    sample_y = data_y.iloc[0]

    string_columns = []
    for i in sample_x:
        if type(i) == str:
            string_columns.append(sample_x.index(i))
    yLabel = False
    if type(sample_y) == str:
        yLabelencoder = LabelEncoder()
        yLabel = True
        data_y = yLabelencoder.fit_transform(data_y)
    print(data_y)

    LabelEncoders = []

    for i in string_columns:
        newLabelEncoder = LabelEncoder()
        data_x.iloc[:, i] = newLabelEncoder.fit_transform(data_x.iloc[:, i])
        LabelEncoders.append(newLabelEncoder)
    model = Model()
    model.fit(data_x, data_y)
    l = 0
    a = LabelEncoders[0]
    for i in string_columns:
        z = LabelEncoders[l]
        datas[i] = z.transform([datas[i]])[0]
        l += 1

    predicted = model.predict([datas])
    if yLabel is True:
        predicted = yLabelencoder.inverse_transform([predicted])

    return predicted, random_data

print(algorithm('dataset.csv','asdf'))