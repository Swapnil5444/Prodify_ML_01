import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QLinearGradient, QColor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Housing Price Prediction App')

        # Apply gradient background
        self.set_gradient_background()

        # Read the dataset
        dataset_path = r'E:\Prodigy_ML\Housing.csv'
        try:
            self.df = pd.read_csv(dataset_path)
        except FileNotFoundError:
            print(f"Dataset not found at {dataset_path}. Make sure the file path is correct.")
            sys.exit(1)

        # Create input widgets
        self.areaLabel = QLabel('Area in Square ft:')
        self.areaInput = QLineEdit(self)

        self.bedroomsLabel = QLabel('Number of Bedrooms:')
        self.bedroomsInput = QLineEdit(self)

        self.bathroomsLabel = QLabel('Number of Bathrooms:')
        self.bathroomsInput = QLineEdit(self)

        self.predictButton = QPushButton('Predict Price', self)
        self.predictButton.clicked.connect(self.predict_price)

        # Create a table widget
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(len(self.df))
        self.tableWidget.setColumnCount(len(self.df.columns))
        self.tableWidget.setHorizontalHeaderLabels(self.df.columns)

        # Create a layout
        layout = QVBoxLayout()
        layout.addWidget(self.areaLabel)
        layout.addWidget(self.areaInput)
        layout.addWidget(self.bedroomsLabel)
        layout.addWidget(self.bedroomsInput)
        layout.addWidget(self.bathroomsLabel)
        layout.addWidget(self.bathroomsInput)
        layout.addWidget(self.predictButton)
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        self.show()

    def set_gradient_background(self):
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(255, 0, 0))   # Red
        gradient.setColorAt(0.2, QColor(255, 165, 0))  # Orange
        gradient.setColorAt(0.4, QColor(255, 255, 0))  # Yellow
        gradient.setColorAt(0.6, QColor(0, 255, 0))    # Green
        gradient.setColorAt(0.8, QColor(0, 0, 255))    # Blue
        gradient.setColorAt(1.0, QColor(128, 0, 128))  # Purple

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setBrush(self.backgroundRole(), gradient)
        self.setPalette(palette)

    def predict_price(self):
        # Prepare the features (X) and target variable (y)
        features = self.df[['area', 'bedrooms', 'bathrooms']]
        target = self.df['price']

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

        # Create a linear regression model
        model = LinearRegression()

        # Train the model
        model.fit(X_train, y_train)

        # Make predictions
        area = float(self.areaInput.text())
        bedrooms = float(self.bedroomsInput.text())
        bathrooms = float(self.bathroomsInput.text())

        # Predict the price
        predicted_price = model.predict([[area, bedrooms, bathrooms]])

        # Display the predicted price
        self.tableWidget.clear()
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setHorizontalHeaderLabels(['Estimated Price: '])

        item = QTableWidgetItem(str(predicted_price[0]))
        self.tableWidget.setItem(0, 0, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = MyApp()
    sys.exit(app.exec_())