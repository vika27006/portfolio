import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

df = pd.read_excel("AI_Impact_Student_Life_2026.xlsx")
df = df.drop("Student_ID", axis=1)

print("Первые 5 строк:")
print(df.head())
print(f"\nРазмер данных: {df.shape}")

quantitative_cols = ["Age", "Task_Frequency_Daily", "Time_Saved_Hours_Weekly",
                     "GPA_Baseline", "GPA_Post_AI", "Career_Confidence_Score"]

print("\nСтатистические характеристики количественных признаков:")
print(df[quantitative_cols].describe())

print("\nСредний итоговый балл по специальностям:")
print(df.groupby("Major")["GPA_Post_AI"].agg(["mean", "median", "std"]))

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.ravel()
for i, col in enumerate(quantitative_cols):
    axes[i].hist(df[col], bins=20, edgecolor='black', alpha=0.7)
    axes[i].set_title(f'Распределение: {col}')
    axes[i].set_xlabel(col)
    axes[i].set_ylabel('Students')
plt.tight_layout()
plt.show()

target = "GPA_Post_AI"
X = df.drop(target, axis=1)
y = df[target]

# Категориальные и числовые признаки
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

print(f"\nЦелевая переменная: {target}")

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numeric_cols),
    ('cat', OneHotEncoder(drop='first', sparse_output=False), categorical_cols)
])

X_processed = preprocessor.fit_transform(X)

# Разделение на train/test
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

print(f"\nОбучающая выборка: {X_train.shape}")
print(f"Тестовая выборка: {X_test.shape}")

def evaluate_model(model, X_train, X_test, y_train, y_test, name):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print(f"\n{name}")
    print(f"  MAE: {mean_absolute_error(y_test, y_pred):.4f}")
    print(f"  MSE: {mean_squared_error(y_test, y_pred):.4f}")
    print(f"  R²:  {r2_score(y_test, y_pred):.4f}")

    return y_pred

# Линейная регрессия
lr = LinearRegression()
y_pred_lr = evaluate_model(lr, X_train, X_test, y_train, y_test, "Линейная регрессия")

# Дерево решений
param_grid = {
    'max_depth': [5, 10, 15, 20, None],
    'min_samples_leaf': [1, 5, 10, 20]
}

dt = DecisionTreeRegressor(random_state=42)
grid_dt = GridSearchCV(dt, param_grid, cv=5, scoring='r2', n_jobs=-1)
grid_dt.fit(X_train, y_train)

print(f"Лучшие параметры: {grid_dt.best_params_}")
print(f"Лучшее R² на кросс-валидации: {grid_dt.best_score_:.4f}")

best_dt = grid_dt.best_estimator_
y_pred_dt = evaluate_model(best_dt, X_train, X_test, y_train, y_test, "Дерево решений")

# Градиентный бустинг
param_grid_gb = {
    'n_estimators': [50, 100, 150],
    'learning_rate': [0.05, 0.1, 0.15],
    'max_depth': [3, 4, 5]
}

gb = GradientBoostingRegressor(random_state=42)
grid_gb = GridSearchCV(gb, param_grid_gb, cv=3, scoring='r2', n_jobs=-1)
grid_gb.fit(X_train, y_train)

print(f"Лучшие параметры: {grid_gb.best_params_}")
print(f"Лучшее R² на кросс-валидации: {grid_gb.best_score_:.4f}")

best_gb = grid_gb.best_estimator_
y_pred_gb = evaluate_model(best_gb, X_train, X_test, y_train, y_test, "Градиентный бустинг")

# Срачнение моделей
results = pd.DataFrame({
    'Модель': ['Линейная регрессия', 'Дерево решений', 'Градиентный бустинг'],
    'R²': [
        r2_score(y_test, y_pred_lr),
        r2_score(y_test, y_pred_dt),
        r2_score(y_test, y_pred_gb)
    ]
}).sort_values('R²', ascending=False)

print(results)

# Визуализация
# График 1: Сравнение всех моделей
plt.figure(figsize=(12, 6))
plt.scatter(y_test, y_pred_lr, alpha=0.4, c='blue', label='Линейная регрессия', s=15)
plt.scatter(y_test, y_pred_dt, alpha=0.4, c='orange', label='Дерево решений', s=15)
plt.scatter(y_test, y_pred_gb, alpha=0.4, c='green', label='Градиентный бустинг', s=15)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', linewidth=2)
plt.xlabel('Реальный GPA')
plt.ylabel('Предсказанный GPA')
plt.title('Сравнение всех моделей')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# График 2: Реальные vs Предсказанные для лучшей модели
best_model_idx = results['R²'].idxmax()
best_model_name = results.loc[best_model_idx, 'Модель']
best_y_pred = [y_pred_lr, y_pred_dt, y_pred_gb][best_model_idx]

plt.figure(figsize=(10, 6))
plt.scatter(y_test, best_y_pred, alpha=0.5, c='blue', edgecolors='black')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', linewidth=2)
plt.xlabel('Реальный GPA')
plt.ylabel('Предсказанный GPA')
plt.title(f'Лучшая модель: {best_model_name}\nR² = {results.loc[best_model_idx, "R²"]:.4f}')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# График 3: Сравнение R²
plt.figure(figsize=(8, 5))
colors = ['green' if x == results['R²'].max() else 'gray' for x in results['R²']]
plt.bar(results['Модель'], results['R²'], color=colors, edgecolor='black')
plt.ylabel('R²')
plt.title('Сравнение качества моделей')
plt.ylim(0, 1)
for i, v in enumerate(results['R²']):
    plt.text(i, v + 0.02, f'{v:.4f}', ha='center')
plt.tight_layout()
plt.show()

