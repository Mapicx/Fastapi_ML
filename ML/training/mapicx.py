import pandas as pd
from ML.Database.database import engine
from sqlalchemy import text
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split
from mapicx import Mapicx, SGD
from sklearn.pipeline import make_pipeline
import numpy as np
from sklearn.metrics import accuracy_score


# Load data from database
df = None
with engine.connect() as conn:  # type: ignore
    result = conn.execute(text('SELECT * FROM "data"'))
    df = pd.DataFrame(result.fetchall(), columns=result.keys())

df.drop(columns=['Sample code number'], inplace=True)    
X = df.iloc[:, :-1].to_numpy()
y_raw = df.iloc[:, -1].to_numpy()

le = LabelEncoder()
y_int = np.array(le.fit_transform(y_raw))
y_int = np.reshape(y_int, (-1, 1))
ohe = OneHotEncoder(sparse_output=False)
Y = ohe.fit_transform(y_int)

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42, stratify=Y
)

# 2. Model factory
def create_model(n_features_ = X_train.shape[1], n_class = Y_train.shape[1]):
    m = Mapicx()
    m.add(n_features=n_features_, n_neurons=64, layer='Dense', activation='Relu')
    m.add(layer='Dropout', rate=0.4, n_features=0, n_neurons=0)
    m.add(n_features=64, n_neurons=64, layer='Dense', activation='Relu')
    m.add(layer='Dropout', rate=0.5, n_features=0, n_neurons=0)
    m.add(n_features=64, n_neurons=n_class, layer='Dense', activation='Softmax')
    opt = SGD(_learning_rate=1.0, _decay=1e-3, momentum=0.9)
    m.compile(optimizer=opt)
    return m

# 3. Build pipeline
pipeline = make_pipeline(
    StandardScaler(),
    create_model()
)

# 4. Train—note the mapicx__ prefix
pipeline.fit(
    X_train, Y_train,
    mapicx__epochs=100,
    mapicx__print_every=1
)

# 5. Evaluate
probs = pipeline.predict(X_test)
preds = np.argmax(probs, axis=1)
true  = np.argmax(Y_test, axis=1)
print("Test accuracy:", accuracy_score(true, preds))

import joblib

joblib.dump(pipeline, r"ML\Trained_model\mapicx_pipeline.pkl")
