import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Sandeep Pratap", "Pratyaya Prakash", "Govind Pandey", "Abhinav Kumar"]
usernames = ["sandeep007", "pratyaya057", "govind047", "abhinav008"]
passwords = ["XXX", "XXX", "XXX", "XXX"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)
