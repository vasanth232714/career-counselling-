from pymongo import MongoClient
import numpy as np
from scipy.spatial.distance import euclidean

# MongoDB Setup
client = MongoClient('mongodb://localhost:27017/')
db = client['career_guidance']
collection = db['user_responses']
domain_collection = db['domain_data']


questions = {
  
    "CS": [
        {
            "question": "I enjoy spending time on computers.",
            "explanation": "This question gauges your interest in using computers and engaging with technology regularly."
        },
        {
            "question": "I like solving puzzles and logical problems.",
            "explanation": "Solving puzzles helps in assessing your problem-solving skills and logical thinking."
        },
        {
            "question": "I often wonder how software and apps are created.",
            "explanation": "Curiosity about the creation of software indicates an interest in programming and development."
        },
        {
            "question": "I take interest in learning about new gadgets and technology.",
            "explanation": "This question explores your enthusiasm for staying updated with the latest tech advancements."
        },
        {
            "question": "I enjoy playing video games and often think about how they are made.",
            "explanation": "Interest in video games may indicate a passion for game development and design."
        },
        {
            "question": "I like mathematics, especially working with numbers and formulas.",
            "explanation": "Mathematical skills are foundational for many areas in computer science."
        },
        {
            "question": "I enjoy participating in coding competitions or clubs, if available.",
            "explanation": "Your engagement with coding competitions indicates a keen interest in programming."
        },
        {
            "question": "I am curious about how websites are designed and built.",
            "explanation": "Curiosity about web development shows interest in creating and maintaining websites."
        },
        {
            "question": "I enjoy working on science projects or experiments at school.",
            "explanation": "Interest in science projects indicates a penchant for practical and experimental learning."
        },
        {
            "question": "I find it interesting to look at and understand patterns in data.",
            "explanation": "Enjoyment of data analysis is essential for careers in big data and machine learning."
        },
        {
            "question": "I am excited about the possibility of creating my own software or apps in the future.",
            "explanation": "Aspiration to create software shows a strong interest in development and innovation."
        },
        {
            "question": "I pay attention to technological advancements and trends in news and media.",
            "explanation": "Keeping up with tech news indicates a proactive interest in technology."
        },
        {
            "question": "I like reading articles and books about technology.",
            "explanation": "Enjoyment of tech articles and books shows a sustained interest in the field."
        },
        {
            "question": "I am interested in how artificial intelligence works.",
            "explanation": "This question assesses your curiosity about AI and its applications."
        },
        {
            "question": "I enjoy discussing technology-related topics with others.",
            "explanation": "Sharing and discussing tech topics reflects a passion for the subject and community."
        },
        {
            "question": "I like thinking about solutions to everyday problems using technology.",
            "explanation": "Interest in tech solutions highlights your problem-solving mindset using technology."
        },
        {
            "question": "I enjoy activities such as making robots or working with simple electronics.",
            "explanation": "Engagement with robotics and electronics shows an interest in hands-on tech projects."
        },
        {
            "question": "I watch shows or videos that explain how technology works.",
            "explanation": "Watching educational tech content shows your effort to learn more about technology."
        },
        {
            "question": "I am interested in mobile app development and how different apps are made.",
            "explanation": "Interest in mobile apps suggests a keen interest in application development."
        },
        {
            "question": "I like working on personal technology projects or tinkering with gadgets at home.",
            "explanation": "Personal tech projects indicate a proactive engagement with technology."
        },
        {
            "question": "I find the idea of building and managing databases fascinating.",
            "explanation": "Interest in databases reflects a passion for data management and storage solutions."
        },
        {
            "question": "I am intrigued by cybersecurity and how to protect information.",
            "explanation": "This question gauges your interest in protecting digital information."
        },
        {
            "question": "I enjoy learning about different programming languages.",
            "explanation": "Interest in programming languages showcases a desire to explore various coding practices."
        },
        {
            "question": "I am interested in the internet of things (IoT) and how devices connect.",
            "explanation": "Curiosity about IoT reflects an interest in connected devices and smart technology."
        },
        {
            "question": "I think about the ethical implications of technology and its impact on society.",
            "explanation": "Concern for tech ethics shows awareness of its societal impact."
        },
        {
            "question": "I enjoy experimenting with different software and understanding their features.",
            "explanation": "Experiments with software indicate a hands-on approach to learning technology."
        },
        {
            "question": "I like understanding how games are programmed and created.",
            "explanation": "Interest in game programming shows curiosity about coding and development."
        },
        {
            "question": "Technology classes are some of my favorite subjects in school.",
            "explanation": "Enjoyment of tech classes reflects a strong interest in the field."
        },
        {
            "question": "I enjoy discussing and exploring the possibilities of future technologies.",
            "explanation": "This question gauges your aspiration and imagination regarding future tech."
        },
        {
            "question": "I like to understand how hardware components of computers work.",
            "explanation": "Interest in hardware reflects curiosity about the physical components of computers."
        },
        {
            "question": "I am excited by cloud computing and how data is stored and managed online.",
            "explanation": "Excitement about cloud computing shows an interest in modern data solutions."
        },
        {
            "question": "I enjoy learning about software development processes and methodologies.",
            "explanation": "Interest in development processes reflects a desire to understand how software is built."
        },
        {
            "question": "I find hacking and ethical hacking concepts fascinating.",
            "explanation": "Interest in hacking indicates curiosity about cybersecurity and ethical practices."
        },
        {
            "question": "I enjoy visualizing data using charts and graphs.",
            "explanation": "Enjoyment of data visualization shows interest in presenting data clearly and engagingly."
        },
        {
            "question": "I find blockchain technology and its applications interesting.",
            "explanation": "Interest in blockchain reflects curiosity about decentralized systems and cryptocurrencies."
        },
        {
            "question": "I like understanding how network systems and the internet work.",
            "explanation": "This question explores your interest in networking and internet infrastructure."
        },
        {
            "question": "I am interested in exploring career opportunities in the field of computer science.",
            "explanation": "Interest in a CS career shows you're considering it as a professional path."
        },
        {
            "question": "I enjoy collaborating with others on technology-related projects.",
            "explanation": "Enjoyment of collaboration indicates you value teamwork in tech projects."
        },
        {
            "question": "I like thinking about how technology can solve real-world problems.",
            "explanation": "Interest in tech solutions shows your innovative and problem-solving mindset."
        },
        {
            "question": "I often think about creating innovations using technology.",
            "explanation": "Curiosity about innovations highlights your creative approach to technology."
        }
  

        ],
 
   "Pure Science": [
    {
        "question": "I am fascinated by the molecular mechanisms that drive cell communication and signaling.",
        "explanation": "This reflects an interest in molecular biology and cellular processes."
    },
    {
        "question": "I enjoy studying how ecosystems respond to natural disasters and human activities.",
        "explanation": "Interest in ecological dynamics highlights a passion for environmental science."
    },
    {
        "question": "I like analyzing how genetic mutations impact biological functions.",
        "explanation": "Curiosity about genetic mutations indicates an interest in genomics."
    },
    {
        "question": "I am intrigued by the formation and classification of crystals and minerals.",
        "explanation": "This reflects a passion for crystallography and geology."
    },
    {
        "question": "I enjoy learning about the role of enzymes in biochemical pathways.",
        "explanation": "Interest in enzyme functions shows a passion for biochemistry."
    },
    {
        "question": "I find it fascinating to study the relationship between structure and function in proteins.",
        "explanation": "This indicates a focus on structural biology and biophysics."
    },
    {
        "question": "I am curious about the mechanisms of climate change and its global effects.",
        "explanation": "This reflects a passion for climatology and environmental science."
    },
    {
        "question": "I like exploring the effects of electromagnetic radiation on various materials.",
        "explanation": "Curiosity about radiation effects reflects an interest in material science and physics."
    },
    {
        "question": "I enjoy investigating the interactions between viruses and host cells.",
        "explanation": "Interest in virus-host interactions highlights a passion for virology."
    },
    {
        "question": "I am fascinated by the mathematical models used in predicting natural phenomena.",
        "explanation": "This shows an interest in mathematical physics and applied mathematics."
    },
    {
        "question": "I like studying the chemistry behind renewable energy sources.",
        "explanation": "Curiosity about renewable energy reflects an interest in green chemistry and sustainability."
    },
    {
        "question": "I find it intriguing how microbes play a role in biotechnology applications.",
        "explanation": "This highlights an interest in microbiology and industrial applications."
    },
    {
        "question": "I enjoy analyzing how different atmospheric conditions influence weather systems.",
        "explanation": "Interest in atmospheric conditions reflects a passion for meteorology."
    },
    {
        "question": "I am curious about how quantum mechanics explains the behavior of particles.",
        "explanation": "This reflects an interest in quantum physics and theoretical science."
    },
    {
        "question": "I like exploring how the periodic table explains elemental properties.",
        "explanation": "Curiosity about elemental properties highlights an interest in inorganic chemistry."
    },
    {
        "question": "I find it fascinating to study the geological layers of Earth.",
        "explanation": "This reflects an interest in stratigraphy and Earth science."
    },
    {
        "question": "I enjoy learning about the bioenergetics of cellular respiration.",
        "explanation": "This indicates a focus on cellular metabolism and biochemistry."
    },
    {
        "question": "I am intrigued by the principles of nuclear reactions and their applications.",
        "explanation": "This shows a passion for nuclear physics and engineering."
    },
    {
        "question": "I like studying the formation and movement of tectonic plates.",
        "explanation": "Curiosity about plate tectonics reflects an interest in geology."
    },
    {
        "question": "I am interested in how nanotechnology enhances material properties.",
        "explanation": "This reflects a passion for nanoscience and material innovation."
    },
    {
        "question": "I enjoy investigating the chemical composition of celestial bodies.",
        "explanation": "Interest in astrochemistry highlights a fascination for space science."
    },
    {
        "question": "I find it fascinating to study how plants use photosynthesis to store energy.",
        "explanation": "This reflects an interest in plant biology and biochemistry."
    },
    {
        "question": "I am curious about the mathematical constants that describe universal patterns.",
        "explanation": "This shows a passion for pure mathematics and its applications."
    },
    {
        "question": "I like exploring the chemical pathways involved in drug development.",
        "explanation": "Curiosity about pharmacology reflects an interest in medicinal chemistry."
    },
    {
        "question": "I enjoy studying how ecosystems evolve over geological timescales.",
        "explanation": "This highlights a passion for paleobiology and evolutionary science."
    },
    {
        "question": "I am fascinated by the role of thermodynamics in shaping physical systems.",
        "explanation": "This reflects an interest in energy systems and physics."
    },
    {
        "question": "I like investigating how physical laws apply to complex biological systems.",
        "explanation": "Curiosity about biophysics indicates an interest in interdisciplinary science."
    },
    {
        "question": "I find it intriguing to study the role of rare elements in modern technologies.",
        "explanation": "This reflects an interest in materials science and chemistry."
    },
    {
        "question": "I am curious about the mechanisms of evolutionary adaptation in species.",
        "explanation": "This indicates a passion for evolutionary biology."
    },
    {
        "question": "I enjoy learning about the chemical processes that govern Earth's atmosphere.",
        "explanation": "Interest in atmospheric chemistry highlights a focus on environmental science."
    },
    {
        "question": "I am fascinated by the study of extinct species and their ecosystems.",
        "explanation": "This reflects an interest in paleontology and Earth history."
    },
    {
        "question": "I like understanding the role of bioinformatics in modern biology.",
        "explanation": "Curiosity about computational biology indicates an interest in bioinformatics."
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

def get_questions_by_group(group):
    return questions.get(group, [])
def store_responses(name, group, responses, domain):
    """Stores user responses in the database."""
    user_data = {"name": name, "group": group, "domain": domain}
    for i, response in enumerate(responses, 1):
        user_data[f"q{i}"] = response
    collection.insert_one(user_data)
    print("Responses stored in the database.")

def predict_career(responses, domain_data):
    """
    Predicts the career domain based on user responses and calculates 
    distance to find the best match with an 80% or higher similarity threshold.
    """
    responses = np.array(responses)
    matched_domains = {"exact": [], "close": []}
    highest_match = {"domain": None, "distance": float("inf")}  # Track closest match below threshold

    for domain_info in domain_data:
        domain_responses = np.array([domain_info.get(f"q{i}", 0) for i in range(1, len(responses) + 1)])
        distance = euclidean(responses, domain_responses)
        similarity = (1 - distance / len(responses)) * 100  # Calculate similarity as a percentage

        print(f"Comparing with Domain: {domain_info['domain']}")
        print(f"Domain Responses: {domain_responses}")
        print(f"User Responses: {responses}")
        print(f"Distance: {distance}, Similarity: {similarity:.2f}%")

        if similarity >= 80:
            matched_domains["exact"].append((domain_info['domain'], similarity))
        else:
            if distance < highest_match["distance"]:
                highest_match = {"domain": domain_info["domain"], "distance": distance}

    # Sort exact matches by highest similarity
    matched_domains["exact"].sort(key=lambda x: x[1], reverse=True)

    return matched_domains

def handle_user_request(name, group, responses):
    """Handles the user input, predicts career, and returns results."""
    domain_data = get_domain_data().get(group, [])
    if not domain_data:
        return {"error": "Invalid group or no domain data available."}

    matched_domains, highest_match = predict_career(responses, domain_data)
    
    if matched_domains["exact"]:
        best_match = matched_domains["exact"][0][0]
        store_responses(name, group, responses, best_match)
        return {
            "message": f"We found a great match for you: {best_match}.",
            "suggestions": [domain for domain, _ in matched_domains["exact"]],
        }
    else:
        closest_domain = highest_match["domain"]
        store_responses(name, group, responses, closest_domain)
        return {
            "message": f"No exact match found. The closest domain is {closest_domain}. "
                       "You may also explore other groups for more options.",
            "closest": closest_domain,
        }
