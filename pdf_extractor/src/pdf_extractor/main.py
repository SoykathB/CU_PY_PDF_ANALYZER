#!/usr/bin/env python
# src/latest_ai_development/main.py
import sys
from pdf_extractor.src.pdf_extractor.crew import LatestAiDevelopmentCrew

def run(prompt,filepath=''):
  inputs = {
    'user_query': prompt,
    'filepath': filepath
  }
  workflow =  LatestAiDevelopmentCrew()
  data = workflow.kickoff(inputs=inputs)
  return data.raw