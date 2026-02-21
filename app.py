import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from datetime import date
import pandas as pd

from src.data_input import SubjectInput, StudentProfile, validate_profile
from src.pdf_reader import load_and_chunk_pdf, create_vector_store
from src.topic_analyzer import extract_topics, rank_topics
from src.scheduler import generate_schedule
from src.summary_generator import generate_summary, save_summary
from src.config import UPLOADS_PATH, OUTPUTS_PATH
