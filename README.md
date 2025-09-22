multi-tool-medical-agent/
│
├── data/                       # Place downloaded Kaggle datasets here
│   ├── heart.csv
│   ├── cancer.csv
│   ├── diabetes.csv
│
├── scripts/                       # Helpers for dataset conversion
│   ├── convert_to_sqlite.py       # Convert one CSV → SQLite DB
│   ├── batch_convert.py           # Convert all 3 datasets
│
├── tools/                         # Agent tools
│   ├── db_tools.py  # HeartDiseaseDBTool, CancerDBTool, DiabetesDBTool
│   ├── web_search_tool.py      # MedicalWebSearchTool (SerpAPI / Bing)
│
├── .env.example                   # Template for API keys
├── requirements.txt               # Python dependencies
├── main_agent.py                  # Main entrypoint (agent assembly + CLI)
├── COLAB.md                       # Step-by-step Colab guide
├── README.md                      # Project instructions (copied from canvas)
│
└── (generated SQLite DBs after running conversion)
    ├── heart_disease.db
    ├── cancer.db
    ├── diabetes.db