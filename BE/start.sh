#!/bin/sh
streamlit run Main_text.py --server.port=8505 --server.address=0.0.0.0 &
uvicorn main:app --host 0.0.0.0 --port 8083 --reload