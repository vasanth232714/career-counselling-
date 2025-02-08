from pymongo import MongoClient
import numpy as np
from scipy.spatial.distance import euclidean,cosine

# MongoDB Setup
client = MongoClient('mongodb://localhost:27017/')
db = client['career_guidance']
collection = db['user_responses']
domain_collection = db['domain_data']

def get_domain_data():
    # Example data, ideally this should come from MongoDB
    domain_data = {
        "CS": [
        {"domain": "Software Development", "q1": 4, "q2": 5, "q3": 4, "q4": 4, "q5": 5, "q6": 3, "q7": 4, "q8": 5, "q9": 4, "q10": 3,
         "q11": 4, "q12": 5, "q13": 4, "q14": 4, "q15": 5},
        {"domain": "AI and Machine Learning", "q1": 5, "q2": 5, "q3": 5, "q4": 4, "q5": 4, "q6": 4, "q7": 5, "q8": 5, "q9": 4, "q10": 5,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Cybersecurity", "q1": 4, "q2": 4, "q3": 5, "q4": 5, "q5": 4, "q6": 4, "q7": 5, "q8": 4, "q9": 5, "q10": 4,
         "q11": 4, "q12": 5, "q13": 4, "q14": 5, "q15": 4},
        {"domain": "Data Science", "q1": 5, "q2": 4, "q3": 5, "q4": 4, "q5": 5, "q6": 5, "q7": 4, "q8": 4, "q9": 5, "q10": 5,
         "q11": 4, "q12": 5, "q13": 4, "q14": 5, "q15": 4},
        {"domain": "Network Administration", "q1": 4, "q2": 4, "q3": 4, "q4": 5, "q5": 3, "q6": 4, "q7": 4, "q8": 4, "q9": 5, "q10": 4,
         "q11": 4, "q12": 4, "q13": 4, "q14": 5, "q15": 4},
        {"domain": "Database Management", "q1": 4, "q2": 5, "q3": 4, "q4": 3, "q5": 4, "q6": 4, "q7": 5, "q8": 4, "q9": 5, "q10": 4,
         "q11": 4, "q12": 4, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Human-Computer Interaction", "q1": 5, "q2": 5, "q3": 3, "q4": 4, "q5": 5, "q6": 5, "q7": 4, "q8": 5, "q9": 4, "q10": 5,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Software Engineering", "q1": 4, "q2": 5, "q3": 4, "q4": 4, "q5": 5, "q6": 4, "q7": 4, "q8": 5, "q9": 4, "q10": 4,
         "q11": 5, "q12": 4, "q13": 4, "q14": 5, "q15": 4},
        {"domain": "Cloud Computing", "q1": 5, "q2": 5, "q3": 5, "q4": 4, "q5": 4, "q6": 5, "q7": 4, "q8": 5, "q9": 5, "q10": 4,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Game Development", "q1": 4, "q2": 5, "q3": 5, "q4": 4, "q5": 5, "q6": 4, "q7": 4, "q8": 5, "q9": 4, "q10": 4,
         "q11": 5, "q12": 4, "q13": 4, "q14": 5, "q15": 4}
    ],
      "Pure Science": [
        {"domain": "Genetic Counseling", "q1": 4, "q2": 5, "q3": 3, "q4": 4, "q5": 5, "q6": 2, "q7": 3, "q8": 4, "q9": 4, "q10": 5,
         "q11": 5, "q12": 2, "q13": 4, "q14": 3, "q15": 4},
        {"domain": "Environmental Engineering", "q1": 4, "q2": 3, "q3": 5, "q4": 2, "q5": 4, "q6": 3, "q7": 3, "q8": 4, "q9": 5, "q10": 4,
         "q11": 4, "q12": 3, "q13": 5, "q14": 2, "q15": 4},
        {"domain": "Biochemistry", "q1": 5, "q2": 5, "q3": 4, "q4": 3, "q5": 5, "q6": 2, "q7": 3, "q8": 5, "q9": 4, "q10": 5,
         "q11": 5, "q12": 3, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Physics Research", "q1": 4, "q2": 3, "q3": 5, "q4": 2, "q5": 5, "q6": 4, "q7": 3, "q8": 5, "q9": 4, "q10": 5,
         "q11": 5, "q12": 2, "q13": 5, "q14": 3, "q15": 4},
        {"domain": "Astrophysics", "q1": 5, "q2": 4, "q3": 5, "q4": 4, "q5": 4, "q6": 4, "q7": 4, "q8": 5, "q9": 4, "q10": 5,
         "q11": 4, "q12": 3, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Materials Science", "q1": 5, "q2": 4, "q3": 5, "q4": 3, "q5": 5, "q6": 4, "q7": 3, "q8": 5, "q9": 4, "q10": 5,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Pharmacology", "q1": 4, "q2": 3, "q3": 5, "q4": 4, "q5": 5, "q6": 3, "q7": 4, "q8": 4, "q9": 5, "q10": 4,
         "q11": 4, "q12": 3, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Environmental Science", "q1": 5, "q2": 4, "q3": 5, "q4": 3, "q5": 5, "q6": 4, "q7": 3, "q8": 5, "q9": 4, "q10": 4,
         "q11": 5, "q12": 4, "q13": 5, "q14": 3, "q15": 5},
        {"domain": "Neuroscience", "q1": 5, "q2": 5, "q3": 4, "q4": 4, "q5": 5, "q6": 5, "q7": 4, "q8": 5, "q9": 4, "q10": 5,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Mathematical Biology", "q1": 4, "q2": 5, "q3": 4, "q4": 4, "q5": 5, "q6": 3, "q7": 4, "q8": 5, "q9": 3, "q10": 5,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 3},
    ],
        "Bio Maths": [
        {"domain": "Biostatistics", "q1": 5, "q2": 5, "q3": 4, "q4": 4, "q5": 5, "q6": 3, "q7": 4, "q8": 5, "q9": 4, "q10": 5,
         "q11": 4, "q12": 3, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Bioinformatics", "q1": 4, "q2": 4, "q3": 5, "q4": 5, "q5": 4, "q6": 3, "q7": 4, "q8": 5, "q9": 4, "q10": 4,
         "q11": 5, "q12": 4, "q13": 5, "q14": 3, "q15": 4},
        {"domain": "Computational Biology", "q1": 5, "q2": 5, "q3": 4, "q4": 4, "q5": 4, "q6": 4, "q7": 5, "q8": 5, "q9": 4, "q10": 5,
         "q11": 4, "q12": 3, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Ecological Modeling", "q1": 4, "q2": 4, "q3": 5, "q4": 5, "q5": 4, "q6": 3, "q7": 4, "q8": 5, "q9": 4, "q10": 4,
         "q11": 5, "q12": 3, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Epidemiological Modeling", "q1": 4, "q2": 5, "q3": 4, "q4": 4, "q5": 5, "q6": 3, "q7": 4, "q8": 5, "q9": 4, "q10": 5,
         "q11": 4, "q12": 3, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Statistical Genetics", "q1": 5, "q2": 4, "q3": 5, "q4": 5, "q5": 4, "q6": 4, "q7": 4, "q8": 5, "q9": 4, "q10": 5,
         "q11": 4, "q12": 3, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Genomics", "q1": 4, "q2": 5, "q3": 5, "q4": 4, "q5": 4, "q6": 4, "q7": 5, "q8": 5, "q9": 4, "q10": 4,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Neuroinformatics", "q1": 5, "q2": 4, "q3": 4, "q4": 5, "q5": 5, "q6": 4, "q7": 5, "q8": 4, "q9": 5, "q10": 5,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Systems Biology", "q1": 4, "q2": 5, "q3": 5, "q4": 4, "q5": 4, "q6": 4, "q7": 5, "q8": 4, "q9": 5, "q10": 4,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Mathematical Ecology", "q1": 5, "q2": 4, "q3": 4, "q4": 5, "q5": 4, "q6": 4, "q7": 5, "q8": 4, "q9": 5, "q10": 4,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 4},
    ],
        "Accounts": [
        {"domain": "Financial Planning", "q1": 5, "q2": 5, "q3": 4, "q4": 4, "q5": 5, "q6": 3, "q7": 4, "q8": 5, "q9": 4, "q10": 5,
         "q11": 5, "q12": 3, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Investment Banking", "q1": 4, "q2": 4, "q3": 5, "q4": 4, "q5": 4, "q6": 3, "q7": 4, "q8": 5, "q9": 4, "q10": 4,
         "q11": 5, "q12": 3, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Auditing", "q1": 4, "q2": 5, "q3": 4, "q4": 5, "q5": 4, "q6": 3, "q7": 4, "q8": 5, "q9": 4, "q10": 5,
         "q11": 4, "q12": 3, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Tax Accounting", "q1": 5, "q2": 4, "q3": 5, "q4": 4, "q5": 4, "q6": 4, "q7": 5, "q8": 4, "q9": 5, "q10": 4,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Payroll Management", "q1": 4, "q2": 4, "q3": 4, "q4": 5, "q5": 5, "q6": 4, "q7": 5, "q8": 4, "q9": 4, "q10": 5,
         "q11": 4, "q12": 3, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Forensic Accounting", "q1": 5, "q2": 5, "q3": 3, "q4": 4, "q5": 5, "q6": 4, "q7": 5, "q8": 4, "q9": 5, "q10": 5,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Cost Accounting", "q1": 4, "q2": 5, "q3": 4, "q4": 5, "q5": 4, "q6": 3, "q7": 5, "q8": 4, "q9": 5, "q10": 4,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Financial Reporting", "q1": 5, "q2": 4, "q3": 5, "q4": 4, "q5": 5, "q6": 3, "q7": 4, "q8": 5, "q9": 5, "q10": 4,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Treasury Management", "q1": 4, "q2": 4, "q3": 5, "q4": 5, "q5": 5, "q6": 3, "q7": 5, "q8": 4, "q9": 5, "q10": 5,
         "q11": 4, "q12": 4, "q13": 5, "q14": 5, "q15": 4},
        {"domain": "Mergers and Acquisitions", "q1": 5, "q2": 5, "q3": 4, "q4": 3, "q5": 5, "q6": 4, "q7": 5, "q8": 3, "q9": 5, "q10": 5,
         "q11": 5, "q12": 3, "q13": 5, "q14": 4, "q15": 4}
    ]
  }
    return domain_data

questions = {
    "CS": [
  {
    "question": "What do you enjoy most about coding?",
    "explanation": "This question helps understand your passion for programming, whether it's problem-solving, logic, creativity, or building functional systems."
  },
  {
    "question": "How comfortable are you with debugging complex code?",
    "explanation": "Debugging is essential for identifying and fixing issues in code. This question gauges your patience and skill in resolving errors in software."
  },
  {
    "question": "Do you prefer working on backend or frontend development?",
    "explanation": "Backend development involves server-side logic, databases, and APIs, while frontend development focuses on user interfaces. This question helps determine your area of interest."
  },
  {
    "question": "How do you feel about algorithms and data structures?",
    "explanation": "Algorithms and data structures are fundamental in solving complex problems efficiently. This assesses your comfort level with designing optimal solutions."
  },
  {
    "question": "What excites you about artificial intelligence and machine learning?",
    "explanation": "AI and ML involve creating systems that can learn and make decisions. This question explores your interest in automating tasks through intelligent algorithms."
  },
  {
    "question": "Are you interested in cloud computing and distributed systems?",
    "explanation": "Cloud computing refers to delivering services (like storage, processing) over the internet, while distributed systems involve multiple computers working together. This question gauges your interest in modern computing infrastructure."
  },
  {
    "question": "How familiar are you with database management systems (DBMS)?",
    "explanation": "DBMSs are systems that help store, retrieve, and manage data efficiently. This question explores your interest in managing large-scale data storage and retrieval."
  },
  {
    "question": "Do you enjoy working with large datasets?",
    "explanation": "Handling large datasets is crucial for data analysis and big data applications. This question helps understand your comfort with data-intensive tasks."
  },
  {
    "question": "How interested are you in mobile app development?",
    "explanation": "Mobile app development involves creating software specifically for mobile devices. This question determines if you're inclined toward designing user-friendly, functional apps."
  },
  {
    "question": "How do you feel about web development and building interactive sites?",
    "explanation": "Web development is about designing and building websites that engage users. This question assesses your interest in creating the online experiences we interact with every day."
  },
  {
    "question": "How comfortable are you with cybersecurity and ethical hacking?",
    "explanation": "Cybersecurity involves protecting systems from attacks, while ethical hacking is about finding vulnerabilities to strengthen defenses. This question assesses your interest in security fields."
  },
  {
    "question": "Do you enjoy working on software design and architecture?",
    "explanation": "Software architecture involves high-level design of complex systems. This question explores whether you like to plan, design, and structure systems at a larger scale."
  },
  {
    "question": "How comfortable are you with understanding low-level languages like C or assembly?",
    "explanation": "Low-level languages provide a close interface with hardware. This question gauges your interest in working closer to hardware and system-level programming."
  },
  {
    "question": "Are you drawn to developing innovative solutions with IoT?",
    "explanation": "The Internet of Things (IoT) involves connecting devices and sensors to collect and exchange data. This question explores your enthusiasm for smart, interconnected systems."
  },
  {
    "question": "How do you feel about working with blockchain technologies?",
    "explanation": "Blockchain is a decentralized ledger for secure and transparent transactions. This question assesses your interest in its applications like cryptocurrencies, smart contracts, etc."
  }
        ],
  "Pure Science": [
    {
      "question": "What area of science excites you the most?",
      "explanation": "Helps identify which branch of science (physics, chemistry, biology, etc.) you are most passionate about."
    },
    {
      "question": "How do you feel about conducting scientific experiments?",
      "explanation": "Explores your comfort level and interest in lab work and experimentation."
    },
    {
      "question": "Do you enjoy learning complex scientific theories?",
      "explanation": "Assesses your interest in theoretical aspects of science, like quantum mechanics or evolutionary biology."
    },
    {
      "question": "How comfortable are you with using scientific equipment?",
      "explanation": "Gauges your interest in hands-on work with tools like microscopes, spectrometers, etc."
    },
    {
      "question": "How do you feel about working in a lab environment?",
      "explanation": "Determines if you enjoy the structure and demands of a lab setting, which is central to many scientific careers."
    },
    {
      "question": "What motivates you to pursue scientific research?",
      "explanation": "Identifies your driving forces for research, such as discovery, innovation, or understanding the world."
    },
    {
      "question": "How interested are you in genetics and DNA analysis?",
      "explanation": "Assesses your fascination with biological inheritance, genetic disorders, and biotechnology."
    },
    {
      "question": "Do you enjoy studying the physical laws that govern the universe?",
      "explanation": "Determines your interest in fields like physics or cosmology, which focus on understanding fundamental forces."
    },
    {
      "question": "How do you feel about environmental science and conservation?",
      "explanation": "Explores your passion for sustainability, ecology, and addressing environmental challenges."
    },
    {
      "question": "What excites you about chemistry and chemical reactions?",
      "explanation": "Helps determine your enthusiasm for understanding the interactions between different substances."
    },
    {
      "question": "How comfortable are you with statistical analysis in scientific research?",
      "explanation": "Gauges your familiarity and interest in using statistics to validate experimental results."
    },
    {
      "question": "Do you enjoy studying microorganisms and their effects on humans?",
      "explanation": "Assesses your interest in microbiology and its applications in medicine, agriculture, and environmental science."
    },
    {
      "question": "How interested are you in understanding the structure and properties of materials?",
      "explanation": "Explores your interest in materials science and engineering, focusing on the properties of metals, polymers, ceramics, etc."
    },
    {
      "question": "What excites you about physics experiments and simulations?",
      "explanation": "Determines if you enjoy hands-on physics experiments or simulating physical processes using computational models."
    },
    {
      "question": "How do you feel about studying the Earth's physical processes?",
      "explanation": "Assesses your interest in geology, meteorology, or oceanography and understanding how natural systems work."
    }
  ],
  "Bio Maths": [
    {
      "question": "How do you feel about applying mathematical models to biological problems?",
      "explanation": "Explores your interest in using mathematics to solve complex biological systems."
    },
    {
      "question": "Do you enjoy working with statistics to analyze biological data?",
      "explanation": "Gauges your comfort with statistics, which are critical in analyzing trends and results in biological studies."
    },
    {
      "question": "How comfortable are you with bioinformatics and computational biology?",
      "explanation": "Assesses your interest in using algorithms, data models, and computational methods to analyze biological data."
    },
    {
      "question": "What excites you about solving mathematical problems related to ecology?",
      "explanation": "Explores your interest in applying mathematics to understand and predict ecological dynamics."
    },
    {
      "question": "How do you feel about studying population genetics and evolution through mathematical models?",
      "explanation": "Gauges your enthusiasm for using mathematics to study the genetic structure of populations and their evolutionary changes."
    },
    {
      "question": "Do you enjoy analyzing complex biological systems through simulation?",
      "explanation": "Evaluates your interest in using computer simulations to model and analyze biological processes."
    },
    {
      "question": "How comfortable are you with epidemiological modeling in disease research?",
      "explanation": "Assesses your interest in using mathematical models to study disease spread and control."
    },
    {
      "question": "What excites you about statistical genetics?",
      "explanation": "Explores your interest in using statistics to analyze genetic data, including linkage and association studies."
    },
    {
      "question": "Do you enjoy using quantitative techniques in neuroscience?",
      "explanation": "Gauges your interest in applying mathematical methods to study brain function and neural networks."
    },
    {
      "question": "How do you feel about analyzing biomolecular structures with mathematical tools?",
      "explanation": "Evaluates your enthusiasm for using mathematics to study the structure and function of molecules like proteins and DNA."
    },
    {
      "question": "What excites you about computational systems biology?",
      "explanation": "Assesses your interest in integrating mathematical models with experimental biology to study complex biological systems."
    },
    {
      "question": "How comfortable are you with biostatistics in clinical trials?",
      "explanation": "Gauges your interest in applying statistics to design, analyze, and interpret data from clinical trials."
    },
    {
      "question": "Do you enjoy studying mathematical epidemiology?",
      "explanation": "Evaluates your interest in using mathematical models to understand the dynamics of infectious diseases and public health interventions."
    },
    {
      "question": "What excites you about applying mathematical concepts to cancer research?",
      "explanation": "Assesses your passion for using mathematics to model tumor growth, treatment responses, and cancer progression."
    },
    {
      "question": "How do you feel about learning mathematical techniques in genomics?",
      "explanation": "Gauges your interest in applying mathematics to understand the structure and function of genomes."
    }
  ],
  "Accounts": [
    {
      "question": "How comfortable are you with understanding financial statements?",
      "explanation": "Gauges your familiarity with key financial documents like balance sheets, income statements, and cash flow statements."
    },
    {
      "question": "Do you enjoy analyzing and interpreting accounting data?",
      "explanation": "Assesses your interest in drawing insights from financial data to make informed decisions."
    },
    {
      "question": "How do you feel about preparing budgets and forecasts?",
      "explanation": "Explores your comfort with predicting financial performance and planning for future business activities."
    },
    {
      "question": "Are you interested in auditing and ensuring financial accuracy?",
      "explanation": "Determines if you have an interest in examining financial records to ensure they are accurate and compliant with regulations."
    },
    {
      "question": "What excites you about tax accounting and tax regulations?",
      "explanation": "Assesses your interest in understanding and applying tax laws to optimize financial outcomes for individuals or organizations."
    },
    {
      "question": "How comfortable are you with managing payroll and employee benefits?",
      "explanation": "Evaluates your interest in ensuring that employees are compensated correctly, including managing benefits, deductions, and compliance."
    },
    {
      "question": "Do you enjoy working with accounting software (e.g., QuickBooks, SAP)?",
      "explanation": "Gauges your familiarity and comfort level with the tools used for managing financial data and processes."
    },
    {
      "question": "How do you feel about financial risk management?",
      "explanation": "Assesses your interest in identifying and mitigating risks that could negatively impact financial performance."
    },
    {
      "question": "What excites you about forensic accounting?",
      "explanation": "Explores your interest in investigating financial discrepancies, fraud, and other irregularities."
    },
    {
      "question": "How comfortable are you with understanding cost accounting for manufacturing?",
      "explanation": "Evaluates your interest in tracking production costs and optimizing efficiency in manufacturing processes."
    },
    {
      "question": "Do you enjoy preparing financial reports for management or investors?",
      "explanation": "Assesses your interest in providing accurate and insightful reports that inform decision-making at the leadership level."
    },
    {
      "question": "What excites you about financial planning and analysis (FP&A)?",
      "explanation": "Gauges your interest in helping organizations plan their financial future through detailed analysis and forecasting."
    },
    {
      "question": "How comfortable are you with conducting internal audits?",
      "explanation": "Evaluates your interest in ensuring that internal controls are in place and that financial practices are efficient and compliant."
    },
    {
      "question": "Do you enjoy reconciling accounts and ensuring accurate records?",
      "explanation": "Assesses your attention to detail and interest in verifying that financial records are complete and correct."
    },
    {
      "question": "What excites you about working in international accounting?",
      "explanation": "Explores your interest in understanding and applying accounting principles across different countries and currencies."
    }
  ]
}
def get_domain_data():
    # Example data, ideally this should come from MongoDB
    domain_data = {
        "CS": [
        {"domain": "Software Development", "q1": 4, "q2": 5, "q3": 4, "q4": 4, "q5": 5, "q6": 3, "q7": 4, "q8": 5, "q9": 4, "q10": 3,
         "q11": 4, "q12": 5, "q13": 4, "q14": 4, "q15": 5},
        {"domain": "AI and Machine Learning", "q1": 5, "q2": 5, "q3": 5, "q4": 4, "q5": 4, "q6": 4, "q7": 5, "q8": 5, "q9": 4, "q10": 5,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Cybersecurity", "q1": 4, "q2": 4, "q3": 5, "q4": 5, "q5": 4, "q6": 4, "q7": 5, "q8": 4, "q9": 5, "q10": 4,
         "q11": 4, "q12": 5, "q13": 4, "q14": 5, "q15": 4},
        {"domain": "Data Science", "q1": 5, "q2": 4, "q3": 5, "q4": 4, "q5": 5, "q6": 5, "q7": 4, "q8": 4, "q9": 5, "q10": 5,
         "q11": 4, "q12": 5, "q13": 4, "q14": 5, "q15": 4},
        {"domain": "Network Administration", "q1": 4, "q2": 4, "q3": 4, "q4": 5, "q5": 3, "q6": 4, "q7": 4, "q8": 4, "q9": 5, "q10": 4,
         "q11": 4, "q12": 4, "q13": 4, "q14": 5, "q15": 4},
        {"domain": "Database Management", "q1": 4, "q2": 5, "q3": 4, "q4": 3, "q5": 4, "q6": 4, "q7": 5, "q8": 4, "q9": 5, "q10": 4,
         "q11": 4, "q12": 4, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Human-Computer Interaction", "q1": 5, "q2": 5, "q3": 3, "q4": 4, "q5": 5, "q6": 5, "q7": 4, "q8": 5, "q9": 4, "q10": 5,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Software Engineering", "q1": 4, "q2": 5, "q3": 4, "q4": 4, "q5": 5, "q6": 4, "q7": 4, "q8": 5, "q9": 4, "q10": 4,
         "q11": 5, "q12": 4, "q13": 4, "q14": 5, "q15": 4},
        {"domain": "Cloud Computing", "q1": 5, "q2": 5, "q3": 5, "q4": 4, "q5": 4, "q6": 5, "q7": 4, "q8": 5, "q9": 5, "q10": 4,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Game Development", "q1": 4, "q2": 5, "q3": 5, "q4": 4, "q5": 5, "q6": 4, "q7": 4, "q8": 5, "q9": 4, "q10": 4,
         "q11": 5, "q12": 4, "q13": 4, "q14": 5, "q15": 4}
    ],
      "Pure Science": [
        {"domain": "Genetic Counseling", "q1": 4, "q2": 5, "q3": 3, "q4": 4, "q5": 5, "q6": 2, "q7": 3, "q8": 4, "q9": 4, "q10": 5,
         "q11": 5, "q12": 2, "q13": 4, "q14": 3, "q15": 4},
        {"domain": "Environmental Engineering", "q1": 4, "q2": 3, "q3": 5, "q4": 2, "q5": 4, "q6": 3, "q7": 3, "q8": 4, "q9": 5, "q10": 4,
         "q11": 4, "q12": 3, "q13": 5, "q14": 2, "q15": 4},
        {"domain": "Biochemistry", "q1": 5, "q2": 5, "q3": 4, "q4": 3, "q5": 5, "q6": 2, "q7": 3, "q8": 5, "q9": 4, "q10": 5,
         "q11": 5, "q12": 3, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Physics Research", "q1": 4, "q2": 3, "q3": 5, "q4": 2, "q5": 5, "q6": 4, "q7": 3, "q8": 5, "q9": 4, "q10": 5,
         "q11": 5, "q12": 2, "q13": 5, "q14": 3, "q15": 4},
        {"domain": "Astrophysics", "q1": 5, "q2": 4, "q3": 5, "q4": 4, "q5": 4, "q6": 4, "q7": 4, "q8": 5, "q9": 4, "q10": 5,
         "q11": 4, "q12": 3, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Materials Science", "q1": 5, "q2": 4, "q3": 5, "q4": 3, "q5": 5, "q6": 4, "q7": 3, "q8": 5, "q9": 4, "q10": 5,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Pharmacology", "q1": 4, "q2": 3, "q3": 5, "q4": 4, "q5": 5, "q6": 3, "q7": 4, "q8": 4, "q9": 5, "q10": 4,
         "q11": 4, "q12": 3, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Environmental Science", "q1": 5, "q2": 4, "q3": 5, "q4": 3, "q5": 5, "q6": 4, "q7": 3, "q8": 5, "q9": 4, "q10": 4,
         "q11": 5, "q12": 4, "q13": 5, "q14": 3, "q15": 5},
        {"domain": "Neuroscience", "q1": 5, "q2": 5, "q3": 4, "q4": 4, "q5": 5, "q6": 5, "q7": 4, "q8": 5, "q9": 4, "q10": 5,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Mathematical Biology", "q1": 4, "q2": 5, "q3": 4, "q4": 4, "q5": 5, "q6": 3, "q7": 4, "q8": 5, "q9": 3, "q10": 5,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 3},
    ],
        "Bio Maths": [
        {"domain": "Biostatistics", "q1": 5, "q2": 5, "q3": 4, "q4": 4, "q5": 5, "q6": 3, "q7": 4, "q8": 5, "q9": 4, "q10": 5,
         "q11": 4, "q12": 3, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Bioinformatics", "q1": 4, "q2": 4, "q3": 5, "q4": 5, "q5": 4, "q6": 3, "q7": 4, "q8": 5, "q9": 4, "q10": 4,
         "q11": 5, "q12": 4, "q13": 5, "q14": 3, "q15": 4},
        {"domain": "Computational Biology", "q1": 5, "q2": 5, "q3": 4, "q4": 4, "q5": 4, "q6": 4, "q7": 5, "q8": 5, "q9": 4, "q10": 5,
         "q11": 4, "q12": 3, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Ecological Modeling", "q1": 4, "q2": 4, "q3": 5, "q4": 5, "q5": 4, "q6": 3, "q7": 4, "q8": 5, "q9": 4, "q10": 4,
         "q11": 5, "q12": 3, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Epidemiological Modeling", "q1": 4, "q2": 5, "q3": 4, "q4": 4, "q5": 5, "q6": 3, "q7": 4, "q8": 5, "q9": 4, "q10": 5,
         "q11": 4, "q12": 3, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Statistical Genetics", "q1": 5, "q2": 4, "q3": 5, "q4": 5, "q5": 4, "q6": 4, "q7": 4, "q8": 5, "q9": 4, "q10": 5,
         "q11": 4, "q12": 3, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Genomics", "q1": 4, "q2": 5, "q3": 5, "q4": 4, "q5": 4, "q6": 4, "q7": 5, "q8": 5, "q9": 4, "q10": 4,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Neuroinformatics", "q1": 5, "q2": 4, "q3": 4, "q4": 5, "q5": 5, "q6": 4, "q7": 5, "q8": 4, "q9": 5, "q10": 5,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Systems Biology", "q1": 4, "q2": 5, "q3": 5, "q4": 4, "q5": 4, "q6": 4, "q7": 5, "q8": 4, "q9": 5, "q10": 4,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Mathematical Ecology", "q1": 5, "q2": 4, "q3": 4, "q4": 5, "q5": 4, "q6": 4, "q7": 5, "q8": 4, "q9": 5, "q10": 4,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 4},
    ],
        "Accounts": [
        {"domain": "Financial Planning", "q1": 5, "q2": 5, "q3": 4, "q4": 4, "q5": 5, "q6": 3, "q7": 4, "q8": 5, "q9": 4, "q10": 5,
         "q11": 5, "q12": 3, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Investment Banking", "q1": 4, "q2": 4, "q3": 5, "q4": 4, "q5": 4, "q6": 3, "q7": 4, "q8": 5, "q9": 4, "q10": 4,
         "q11": 5, "q12": 3, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Auditing", "q1": 4, "q2": 5, "q3": 4, "q4": 5, "q5": 4, "q6": 3, "q7": 4, "q8": 5, "q9": 4, "q10": 5,
         "q11": 4, "q12": 3, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Tax Accounting", "q1": 5, "q2": 4, "q3": 5, "q4": 4, "q5": 4, "q6": 4, "q7": 5, "q8": 4, "q9": 5, "q10": 4,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Payroll Management", "q1": 4, "q2": 4, "q3": 4, "q4": 5, "q5": 5, "q6": 4, "q7": 5, "q8": 4, "q9": 4, "q10": 5,
         "q11": 4, "q12": 3, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Forensic Accounting", "q1": 5, "q2": 5, "q3": 3, "q4": 4, "q5": 5, "q6": 4, "q7": 5, "q8": 4, "q9": 5, "q10": 5,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Cost Accounting", "q1": 4, "q2": 5, "q3": 4, "q4": 5, "q5": 4, "q6": 3, "q7": 5, "q8": 4, "q9": 5, "q10": 4,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 4},
        {"domain": "Financial Reporting", "q1": 5, "q2": 4, "q3": 5, "q4": 4, "q5": 5, "q6": 3, "q7": 4, "q8": 5, "q9": 5, "q10": 4,
         "q11": 5, "q12": 4, "q13": 5, "q14": 4, "q15": 5},
        {"domain": "Treasury Management", "q1": 4, "q2": 4, "q3": 5, "q4": 5, "q5": 5, "q6": 3, "q7": 5, "q8": 4, "q9": 5, "q10": 5,
         "q11": 4, "q12": 4, "q13": 5, "q14": 5, "q15": 4},
        {"domain": "Mergers and Acquisitions", "q1": 5, "q2": 5, "q3": 4, "q4": 3, "q5": 5, "q6": 4, "q7": 5, "q8": 3, "q9": 5, "q10": 5,
         "q11": 5, "q12": 3, "q13": 5, "q14": 4, "q15": 4}
    ]
  }
    return domain_data

def ask_questions(group):
    if group not in questions:
        print("Invalid group selected.")
        return []

    responses = []
    print(f"Please answer the following questions for {group}:")
    
    for i, question in enumerate(questions[group]):
        print(f"{i + 1}. {question}")
        response = int(input("Enter your response (1-5): "))
        responses.append(response)
    
    return responses
# Store responses in MongoDB
def store_responses(name, group, responses, domain):
    user_data = {"name": name, "group": group, "domain": domain}
    for i, response in enumerate(responses, 1):
        user_data[f"q{i}"] = response
    collection.insert_one(user_data)
    print("Responses stored in the database.")

# Predict career domains based on user responses

def predict_career_with_similarity(responses, domain_data):
    responses = np.array(responses)  # User responses as a vector
    matched_domains = []

    for domain_info in domain_data:
        domain_vector = np.array([domain_info.get(f"q{i}", 0) for i in range(1, 16)])

        # Calculate Euclidean distance
        distance = euclidean(responses, domain_vector)

        # Calculate Cosine similarity (1 - cosine distance because higher similarity is better)
        similarity = 1 - cosine(responses, domain_vector)

        # Append domain, similarity, and distance for sorting and comparison
        matched_domains.append({
            "domain": domain_info['domain'],
            "distance": distance,
            "similarity": similarity
        })

    # Sort by highest similarity first, then lowest distance
    matched_domains.sort(key=lambda x: (-x["similarity"], x["distance"]))

    # Debugging: Print matches for clarity
    print("\nMatched Domains:")
    for match in matched_domains:
        print(f"Domain: {match['domain']}, Similarity: {match['similarity']:.2f}, Distance: {match['distance']:.2f}")

    return matched_domains
def get_questions_by_group(group):
    return questions.get(group, [])

if __name__ == "__main__":
    name = input("Enter your name: ")
    group = input("Enter your 12th group (CS/Pure Science/Bio Maths/Accounts): ")

    responses = ask_questions(group)

    if responses:
        # Fetch the appropriate domain data
        domain_data = get_domain_data().get(group, [])
        
        # Predict career domains with cosine similarity and Euclidean distance
        matched_domains = predict_career_with_similarity(responses, domain_data)

        # Display top 3 suggestions based on similarity
        print("\nTop Career Suggestions:")
        for i, match in enumerate(matched_domains[:3], 1):  # Top 3 matches
            print(f"{i}. Domain: {match['domain']}, Similarity: {match['similarity']:.2f}, Distance: {match['distance']:.2f}")

        # Store the best match in MongoDB
        if matched_domains:
            best_match = matched_domains[0]['domain']
            store_responses(name, group, responses, best_match)
