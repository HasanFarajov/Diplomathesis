import tkinter as tk
from tkinter import messagebox
from tkinter import *
#imported packages such as pandas, numpy
import pandas as pd
import numpy as np

# Models from Scikit-Learn
from sklearn import preprocessing

pd.options.display.float_format = '{:.2f}'.format
df = pd.read_csv('../Simulation/banking.csv')
df = df.drop(['step','nameOrig', 'nameDest'], axis=1)
le = preprocessing.LabelEncoder()
df.type = le.fit_transform(df.type)
target_variable = 'isFraud'
y = df.isFraud
X = df.drop(['isFraud','isFlaggedFraud'], axis=1)
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_scaled = sc.fit_transform(X)
from imblearn.under_sampling import RandomUnderSampler
undersample = RandomUnderSampler(sampling_strategy='majority')
X_over, y_over = undersample.fit_resample(X, y)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_over, y_over,test_size=0.5,random_state=1,shuffle=True)
##################################

# import the trained model
from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(n_estimators=200, random_state=42)
rfc.fit(X_train, y_train)

# define the mapping from transaction type strings to numbers
type_mapping = {
    'Cash out': 1,
    'Payment': 2,
    'Cash in': 3,
    'Transfer': 4,
    'Debit': 5
}

# define the Tkinter GUI
class FraudDetectorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("700x400")
        self.configure(background="cyan")
        self.title("Fraud Detector")
        self.iconbitmap('bank.ico')
        self.create_widgets()

    def create_widgets(self):
        # create labels and input fields
        self.title_label = tk.Label(self, text="PLEASE ENTER FEATURES FOR ANOMALY DETECTION", width=41, bg="cyan")
        self.title_label.place(x=200, y=15)
        self.type_label = tk.Label(self, text="Transaction Type:", width=16, bg="cyan")
        self.type_label.place(x=50, y=60)

        # create a drop-down menu for the transaction type
        self.type_var = tk.StringVar(self)
        self.type_var.set('Cash out')  # default value
        self.type_option_menu = tk.OptionMenu(self, self.type_var, *type_mapping.keys())
        self.type_option_menu.place(x=170, y=60)

        self.Amount = StringVar()
        self.OldBalOrg = StringVar()
        self.NewBalOrg = StringVar()
        self.OldBalDest = StringVar()
        self.NewBalDest = StringVar()

        self.amount_label = tk.Label(self, text="Amount:", width=16, bg="cyan")
        self.amount_label.place(x=310, y=60)
        self.amount_entry = tk.Entry(self, textvariable= self.Amount, width=20)
        self.amount_entry.place(x=435, y=60)

        self.old_bal_org_label = tk.Label(self, text="Old Balance Org:", width=16, bg="cyan")
        self.old_bal_org_label.place(x=50, y=100)
        self.old_bal_org_entry = tk.Entry(self, textvariable= self.OldBalOrg, width=20)
        self.old_bal_org_entry.place(x=170, y=100)

        self.new_bal_org_label = tk.Label(self, text="New Balance Org:", width=16, bg="cyan")
        self.new_bal_org_label.place(x=310, y=100)
        self.new_bal_org_entry = tk.Entry(self, textvariable= self.NewBalOrg, width=20)
        self.new_bal_org_entry.place(x=435, y=100)

        self.old_bal_dest_label = tk.Label(self, text="Old Balance Dest:", width=16, bg="cyan")
        self.old_bal_dest_label.place(x=50, y=140)
        self.old_bal_dest_entry = tk.Entry(self, textvariable= self.OldBalDest, width=20)
        self.old_bal_dest_entry.place(x=170, y=140)

        self.new_bal_dest_label = tk.Label(self, text="New Balance Dest:", width=16, bg="cyan")
        self.new_bal_dest_label.place(x=310, y=140)
        self.new_bal_dest_entry = tk.Entry(self, textvariable= self.NewBalDest, width=20)
        self.new_bal_dest_entry.place(x=435, y=140)

        # create a button to submit the input values
        reset = Button(self, text="Reset", width="12", height="1", activebackground="red", command=self.reset, bg="lightblue",
                       font=("Calibri 12 ")).place(x=230, y=180)
        self.submit_button = tk.Button(self, text="Submit", width="12", height="1", activebackground="red", command=self.detect_fraud,  bg="lightblue", font=("Calibri 12 "))
        self.submit_button.place(x=350, y=180)

    def reset(self):
        self.Amount.set("")
        self.OldBalOrg.set("")
        self.NewBalOrg.set("")
        self.OldBalDest.set("")
        self.NewBalDest.set("")

    def detect_fraud(self):
        if self.amount_entry.get() == "":
            user = "Amount Field is Empty!!"
            Label(self, text=user, fg="white", bg="red", font=("Calibri 10 bold")).place(x=270, y=230)
        elif self.old_bal_org_entry.get() == "":
            user = "Old Balance Origin Field is Empty!!"
            Label(self, text=user, fg="white", bg="red", font=("Calibri 10 bold")).place(x=270, y=230)
        elif self.old_bal_dest_entry.get() == "":
            user = "New Balance Origin Field is Empty!!"
            Label(self, text=user, fg="white", bg="red", font=("Calibri 10 bold")).place(x=270, y=230)
        elif self.old_bal_org_entry.get() == "":
            user = "Old Balance Destination Field is Empty!!"
            Label(self, text=user, fg="white", bg="red", font=("Calibri 10 bold")).place(x=270, y=230)
        elif self.new_bal_dest_entry.get() == "":
            user = "New Balance Destination Field is Empty!!"
            Label(self, text=user, fg="white", bg="red", font=("Calibri 10 bold")).place(x=270, y=230)
        else:
            # get the input values from the entry fields
            input_values = [
                type_mapping[self.type_var.get()],
                float(self.amount_entry.get()),
                float(self.old_bal_org_entry.get()),
                float(self.new_bal_org_entry.get()),
                float(self.old_bal_dest_entry.get()),
                float(self.new_bal_dest_entry.get())
            ]
            # convert the input values to a numpy array
            input_array = np.array(input_values).reshape(1, -1)

            # make a prediction using the trained model
            prediction = rfc.predict(input_array)

            # display a message box with the prediction
            if prediction[0] == 0:
                messagebox.showinfo("Fraud Detector", "Transaction is 99% not fraud.")
            else:
                messagebox.showwarning("Fraud Detector", "Transaction 99% is fraud!")
# create an instance of the GUI
app = FraudDetectorGUI()

# start the main event loop
app.mainloop()