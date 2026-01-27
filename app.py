import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
            
        file = request.files['file']
        
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            try:
                if filepath.endswith('.csv'):
                    df = pd.read_csv(filepath)
                else:
                    df = pd.read_excel(filepath)

                numeric_cols = df.select_dtypes(include=[np.number]).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

                le = LabelEncoder()
                if 'Internet_Access' in df.columns:
                    df['Internet_Access'] = le.fit_transform(df['Internet_Access'].astype(str))
                if 'Result' in df.columns:
                    df['Result'] = le.fit_transform(df['Result'].astype(str))

                plt.figure(figsize=(10, 6))
                sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt=".2f")
                plt.tight_layout()
                heatmap_path = os.path.join('static', 'heatmap.png')
                plt.savefig(heatmap_path)
                plt.close()

                boxplot_path = None
                if 'Study_Hours' in df.columns and 'Result' in df.columns:
                    plt.figure(figsize=(8, 5))
                    sns.boxplot(x=df['Result'], y=df['Study_Hours'], palette="Set2")
                    plt.title('Study Hours vs Result')
                    plt.tight_layout()
                    boxplot_path = os.path.join('static', 'boxplot.png')
                    plt.savefig(boxplot_path)
                    plt.close()

                accuracy = "N/A"
                importance = {}
                
                if 'Result' in df.columns:
                    X = df.drop(['Result'], axis=1)
                    X = X.select_dtypes(include=[np.number])
                    y = df['Result']
                    
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                    
                    rf = RandomForestClassifier(n_estimators=100, random_state=42)
                    rf.fit(X_train, y_train)
                    preds = rf.predict(X_test)
                    
                    accuracy = round(accuracy_score(y_test, preds) * 100, 2)
                    
                    feats = pd.Series(rf.feature_importances_, index=X.columns)
                    importance = feats.sort_values(ascending=False).head(3).to_dict()

                return render_template('index.html', 
                                       processed=True, 
                                       heatmap='heatmap.png', 
                                       boxplot='boxplot.png' if boxplot_path else None,
                                       accuracy=accuracy,
                                       importance=importance)

            except Exception as e:
                return f"Error processing file: {e}"

    return render_template('index.html', processed=False)

if __name__ == '__main__':
    app.run(debug=True)