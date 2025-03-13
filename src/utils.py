from src.exception import CustomException
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
import sys
import os
import dill


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models, params):
    try:
        report = {}
        for model_name, model in models.items():
            param_grid = params[model_name]

            gs = GridSearchCV(model, param_grid, cv=3)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            # model.fit(X_train, y_train)

            train_preds = model.predict(X_train)
            test_preds = model.predict(X_test)

            train_scores = r2_score(y_train, train_preds)
            test_scores = r2_score(y_test, test_preds)

            report[model_name] = test_scores

        return report

    except Exception as e:
        raise CustomException(e, sys)
