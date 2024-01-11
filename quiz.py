import streamlit as st
from firebase_admin import firestore
import json
# quizzes = [
#     {
#         'topic': 'achalasia',
#         'questions': [
#     {'question': 'What part of the body does achalasia primarily affect?',
#      'options': ['Esophagus', 'Stomach', 'Lungs', 'Intestines'],
#      'correct_answer': 'Esophagus'},
#     {'question': 'Which test is commonly used to diagnose achalasia?',
#      'options': ['CT scan', 'Esophageal manometry', 'Blood test', 'Urine test'],
#      'correct_answer': 'Esophageal manometry'},
#     {'question': 'Which symptom is characteristic of achalasia?',
#      'options': ['Chest pain', 'Difficulty swallowing', 'Headache', 'Abdominal cramps'],
#      'correct_answer': 'Difficulty swallowing'},
#     {'question': 'What is a primary cause of achalasia?',
#      'options': ['Bacterial infection', 'Lack of physical activity', 'Damage to the nerves in the esophagus', 'Acid reflux'],
#      'correct_answer': 'Damage to the nerves in the esophagus'},
#     {'question': 'What is the goal of treatment for achalasia?',
#      'options': ['Increase heart rate', 'Relieve constipation', 'Restore esophageal function', 'Improve kidney function'],
#      'correct_answer': 'Restore esophageal function'},
#     {'question': 'Which surgical procedure is performed to treat achalasia?',
#      'options': ['Gastrectomy', 'Esophagectomy', 'Laparoscopic Heller myotomy', 'Cholecystectomy'],
#      'correct_answer': 'Laparoscopic Heller myotomy'},
#     {'question': 'Which medication is often prescribed to treat achalasia?',
#      'options': ['Antacids', 'Calcium channel blockers', 'Antibiotics', 'Pain relievers'],
#      'correct_answer': 'Calcium channel blockers'},
#     {'question': 'What is a potential complication of untreated achalasia?',
#      'options': ['Arthritis', 'Esophageal cancer', 'Diabetes', 'Glaucoma'],
#      'correct_answer': 'Esophageal cancer'},
#     {'question': 'What lifestyle change may improve symptoms of achalasia?',
#      'options': ['Increased protein intake', 'Elevating the head while sleeping', 'High-impact exercise', 'Decreased water consumption'],
#      'correct_answer': 'Elevating the head while sleeping'},
#     {'question': 'Which type of doctor typically diagnoses and treats achalasia?',
#      'options': ['Dermatologist', 'Podiatrist', 'Gastroenterologist', 'Psychiatrist'],
#      'correct_answer': 'Gastroenterologist'}
#     ]
#     },
#     {
#         'topic': 'acoustic trauma',
#         'questions': [
            
#     {"question": "What is the primary cause of acoustic trauma?",
#      "options": ["Chronic ear infections", "Exposure to loud noise", "Foreign object in the ear", "Age-related hearing loss"],
#      "correct_answer": "Exposure to loud noise"},

#     {"question": "Which type of hearing loss is associated with acoustic trauma?",
#      "options": ["Conductive", "Sensorineural", "Mixed", "Central"],
#      "correct_answer": "Sensorineural"},

#     {"question": "What is a common symptom of acoustic trauma?",
#      "options": ["Fever", "Tinnitus", "Blurred vision", "Sore throat"],
#      "correct_answer": "Tinnitus"},

#     {"question": "What investigation is commonly performed to diagnose acoustic trauma?",
#      "options": ["Blood tests", "MRI of the brain", "Tympanometry", "Pure tone audiometry"],
#      "correct_answer": "Pure tone audiometry"},

#     {"question": "How can acoustic trauma be prevented?",
#      "options": ["Regular exercise", "Wearing ear protection in noisy environments", "Taking antibiotics", "Eating a balanced diet"],
#      "correct_answer": "Wearing ear protection in noisy environments"},

#     {"question": "Which of the following treatments is NOT typically used for acoustic trauma?",
#      "options": ["Corticosteroids", "Hearing aids", "Antibiotics", "Sound therapy"],
#      "correct_answer": "Antibiotics"},

#     {"question": "What is the prognosis for patients with acute acoustic trauma if treated early?",
#      "options": ["Poor, with significant long-term disability", "Good, with potential for full recovery", "Fair, with some permanent hearing loss", "Variable, with unpredictable outcomes"],
#      "correct_answer": "Good, with potential for full recovery"},

#     {"question": "Which demographic is more at risk for experiencing acoustic trauma?",
#      "options": ["Infants", "Teenagers", "Construction workers", "Adults over 65"],
#      "correct_answer": "Construction workers"},

#     {"question": "Which frequency range of hearing is most commonly affected by acoustic trauma?",
#      "options": ["Low frequencies (20-250 Hz)", "Middle frequencies (250-2000 Hz)", "High frequencies (2000-8000 Hz)", "Ultrahigh frequencies (above 20000 Hz)"],
#      "correct_answer": "High frequencies (2000-8000 Hz)"},

#     {"question": "What differential diagnosis should be considered for a patient presenting with sudden hearing loss due to possible acoustic trauma?",
#      "options": ["Diabetes mellitus", "Meniere’s disease", "Hypertension", "Migraine"],
#      "correct_answer": "Meniere’s disease"}
# ]
#             # Add more questions as needed
        
#     },
#     {
#         'topic':'acute laryngitis',
#         'questions': [
#             {
#         "question": "What is the common cause of acute laryngitis?",
#         "options": ["Bacterial infection", "Fungal infection", "Viral Upper Respiratory Infection (URI)", "Allergic reaction"],
#         "correct_answer": "Viral Upper Respiratory Infection (URI)"
#     },
#     {
#         "question": "What is a common symptom of mild acute laryngitis?",
#         "options": ["Fever", "Hoarseness", "Severe throat pain", "Skin rash"],
#         "correct_answer": "Hoarseness"
#     },
#     {
#         "question": "What type of investigation is not routinely performed for acute laryngitis?",
#         "options": ["Radiology", "Laryngoscopy", "Blood test", "Throat swab"],
#         "correct_answer": "Radiology"
#     },
#     {
#         "question": "How is acute laryngitis typically managed?",
#         "options": ["Immediate surgery", "Antibiotic therapy", "Wait and See approach", "Aggressive physical therapy"],
#         "correct_answer": "Wait and See approach"
#     },
#     {
#         "question": "Acute laryngitis is typically a condition with what kind of prognosis?",
#         "options": ["Poor", "Guarded", "Good", "Uncertain"],
#         "correct_answer": "Good"
#     },
#     {
#         "question": "Which anatomical structures are primarily involved in acute laryngitis?",
#         "options": ["Pharynx and Esophagus", "Lungs and Bronchi", "Larynx and Vocal Cords", "Nasal Cavity and Sinuses"],
#         "correct_answer": "Larynx and Vocal Cords"
#     },
#     {
#         "question": "Acute laryngitis typically resolves within what time frame?",
#         "options": ["1-2 weeks", "1-2 months", "3-4 days", "5-6 weeks"],
#         "correct_answer": "1-2 weeks"
#     },
#     {
#         "question": "Which European guideline is consulted for the investigation and treatment of acute laryngitis?",
#         "options": ["American Medical Association Guidelines", "European Resuscitation Council Guidelines", "European Laryngological Society Guidelines", "World Health Organization Guidelines"],
#         "correct_answer": "European Laryngological Society Guidelines"
#     },
#     {
#         "question": "One of the following is NOT a differential diagnosis for acute laryngitis. Which one is it?",
#         "options": ["Laryngeal cancer", "Vocal cord nodules", "Asthma", "Laryngopharyngeal reflux"],
#         "correct_answer": "Asthma"
#     },
#     {
#         "question": "Which type of treatment is not typically used in cases of acute laryngitis?",
#         "options": ["Phonosurgery", "Voice rest", "Increased fluid intake", "Anti-inflammatory medications"],
#         "correct_answer": "Phonosurgery"
#     }
#         ]
     
#      },
#     # Add more quizzes as needed
# ]

with open('quizzes.json', 'r') as file:
    json_data = json.load(file)

# for topic_data in json_data:
#     print(topic_data)

quizzes = json_data
#List of all topics
all_topics = [quiz['topic'] for quiz in quizzes]

def app():

    st.title("Quiz Page")

    if 'db' not in st.session_state:
        st.session_state.db = ''

    db = firestore.client()
    st.session_state.db = db

    ph = ''
    if st.session_state.username =='':
        ph = 'Login to be able to take a quiz'
        st.text(ph)
    else:
        ph = 'Take a quiz'
        st.text(ph)

        # Search bar for topic selection
        selected_topic = st.selectbox("Select a Quiz Topic", all_topics)

        # Get selected quiz
        selected_quiz = next((quiz for quiz in quizzes if quiz['topic'] == selected_topic), None)

        if selected_quiz:
            st.header(f"{selected_topic} Quiz")

            # Display questions and collect user answers
            user_answers = []
            for i, question in enumerate(selected_quiz['questions']):
                st.write(f"**Question {i + 1}:** {question['question']}")
            
                # Use st.radio for single answer choice
                user_answer = st.radio(f"Select an option for Question {i + 1}", question['options'])
                user_answers.append(user_answer)

            # Submit button to calculate and display result
            if st.button("Submit"):
                # Calculate and display result
                correct_answers = [q['correct_answer'] for q in selected_quiz['questions']]
                score = sum(user_answer == correct_answer for user_answer, correct_answer in zip(user_answers, correct_answers))
                # writing the taken quiz to the database
                info = db.collection('Quizzes').document(st.session_state.username).get()
                print(selected_quiz['topic'])
                print(info.to_dict())
                if info.exists:
                    info = info.to_dict()
                    if 'taken_quizzes' in info.keys():
                        pos = db.collection('Quizzes').document(st.session_state.username)
                        taken_quizzes = info['taken_quizzes']
                        quiz_scores = info['quiz_scores']
                        taken_quizzes.append(selected_quiz['topic'])
                        quiz_scores.append(score)
                        pos.set({'taken_quizzes': taken_quizzes, 'quiz_scores': quiz_scores, 'Username': st.session_state.username})
                    # pos.update({u'taken_quizzes': firestore.ArrayUnion([u'{}'.format(selected_quiz['topic'])]), u'quiz_scores': firestore.ArrayUnion([u'{}'.format(score)])})
                    else:
                        data = {"taken_quizzes":[selected_quiz['topic']], "quiz_scores":[score], "Username": st.session_state.username}
                        db.collection('Quizzes').document(st.session_state.username).set(data)
                else:
                    data = {"taken_quizzes":[selected_quiz['topic']], "quiz_scores":[score], "Username": st.session_state.username}
                    db.collection('Quizzes').document(st.session_state.username).set(data)


                st.write(f"Your Score: {score}/{len(selected_quiz['questions'])}")

                # Display correct answers
                st.write("Correct Answers:")
                for i, (user_answer, correct_answer) in enumerate(zip(user_answers, correct_answers)):
                    st.write(f"Question {i + 1}: {correct_answer} (Your answer: {user_answer})")
        else:
            st.warning("No quiz found for the selected topic. Please choose a valid topic.")



'''
 You are a helpful assistant programmed to generate questions based on your database. For "diagnose name" diagnose, you're tasked with designing 10 distinct questions. Each of these questions will be accompanied by 4 possible answers: one correct answer and three incorrect ones. 
    For clarity and ease of processing, structure your response in a way that emulates a Python list of lists. 

    Your output should be shaped as follows:

    1. An outer list that contains 10 inner lists.
    2. Each inner list represents a dictionary of question, options and correct_answer keys, and contains exactly 3 values  in this order:
    - The generated question.
    - Options list which contains all the possible answers
    - correct answer

    Your output should mirror this structure:
    [
        {"question": "Generated Question 1", "options": [ "Option 1.1",  "Option 1.2", "Option 1.3", "Option 1.4"], "correct_answer": "Correct option"},
       {"question":"Generated Question 2", "options": [ "Option 2.1",  "Option 2.2", "Option 2.3", "Option 2.4"], "correct_answer": "Correct option"},
        ...
    ]

    It is crucial that you adhere to this format as it's optimized for further Python processing.
'''