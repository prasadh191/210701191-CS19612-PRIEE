from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from deep_translator import GoogleTranslator

app = Flask(__name__)
socketio = SocketIO(app)

# Supported languages and their codes
languages_supported = {
    'en': 'English',
    'hi': 'Hindi',
    'ta': 'Tamil',
    'bn': 'Bengali',
    # Add more languages as needed
}

# Sample legal information to be provided in multiple languages
legal_info = {
    'en': "I'm not sure I understand. Can you provide more information or clarify your question?",
    # Add more legal information as needed
}

@app.route('/')
def index():
    return render_template('index1.html', languages=languages_supported)

@socketio.on('send_message')
def handle_send_message(json):
    message = json['message']
    language = json['language']
    
    # Identify query type and generate response
    response = generate_response(message, language)
    
    emit('receive_message', {'message': response, 'language': language})

def generate_response(message, language):
    message_lower = message.lower()
    
    if 'student' in message_lower:
        response = """In India, there are several government schemes and initiatives aimed at providing support and assistance to marginalized communities, including students. These schemes are intended to promote equal opportunities in education and address the socio-economic challenges faced by these communities. Some of the key government schemes for marginalized communities students in India include:

1. **Scholarship Schemes**: Various scholarship schemes are available for students belonging to marginalized communities such as Scheduled Castes (SC), Scheduled Tribes (ST), Other Backward Classes (OBC), and economically weaker sections (EWS). These scholarships provide financial assistance for pursuing higher education.

2. **Pre-Matric and Post-Matric Scholarship Scheme**: These schemes are specifically designed to support students from marginalized communities at the pre-matric and post-matric levels.

3. **National Fellowship for SC Students**: This scheme provides financial assistance to SC students for pursuing M.Phil and Ph.D. courses.

4. **Free Education**: Under the Right to Education Act, 2009, children belonging to marginalized communities are entitled to free and compulsory education up to the age of 14 years.

5. **Mid-Day Meal Scheme**: This scheme provides nutritious meals to school children, with a special focus on students from marginalized communities.

6. **Reservation in Educational Institutions**: Reservation policies are in place to ensure that a certain percentage of seats in educational institutions are reserved for students belonging to SC, ST, OBC, and EWS categories.

These schemes are governed by various Acts such as the Constitution of India, the Right to Education Act, 2009, and specific guidelines issued by the Ministry of Social Justice and Empowerment, Ministry of Tribal Affairs, and Ministry of Human Resource Development. The implementation and monitoring of these schemes are done at both the central and state levels.

If any issues arise regarding the implementation of these schemes or if a student belonging to a marginalized community faces discrimination or denial of benefits, they can seek redressal through the appropriate authorities or legal forums as prescribed under the relevant laws and regulations applicable to their jurisdiction, which may include the respective State Government authorities or the National Commission for Scheduled Castes/Tribes, as well as the High Courts and the Supreme Court of India."""
    
    elif 'uneducated' in message_lower:
        response = """In India, there are various government schemes and programs aimed at providing support and opportunities for uneducated employees to acquire skills and education. These schemes are designed to empower individuals who have not had access to formal education and training, thereby enhancing their employability and socio-economic status. Some of the key government schemes for uneducated employees in India include:

1. **Skill India Mission:** Launched by the Government of India, Skill India Mission aims to provide skill training to individuals across various sectors and industries. It offers certification programs, apprenticeships, and training courses to enhance the employability of uneducated individuals.

2. **Pradhan Mantri Kaushal Vikas Yojana (PMKVY):** This scheme focuses on providing skill development training to youth, including uneducated individuals. It offers short-term training programs to help individuals acquire relevant skills and secure employment opportunities.

3. **National Literacy Mission:** The National Literacy Mission aims to eradicate illiteracy and provide basic education to adults, including uneducated employees. It offers adult literacy programs and bridge courses to enhance their reading, writing, and numeracy skills.

4. **Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA):** While not specific to skill development, MGNREGA guarantees 100 days of wage employment to unskilled workers in rural areas. It provides a source of livelihood to uneducated employees and promotes financial inclusion.

5. **Vocational Training Programs:** Various government-sponsored vocational training programs are available for uneducated individuals to acquire specialized skills in trades such as carpentry, plumbing, electrician, etc. These programs are offered through Industrial Training Institutes (ITIs) and other vocational training centers.

These schemes are governed by the Ministry of Skill Development and Entrepreneurship, Ministry of Human Resource Development, and other relevant ministries at the central and state levels. The implementation and monitoring of these schemes are carried out through various training centers, vocational institutions, and government agencies.

If uneducated employees are interested in availing the benefits of these schemes or seeking skill development opportunities, they can approach the nearest skill training center, employment exchange, or government office for guidance and enrollment. Additionally, for any grievances or assistance related to these schemes, individuals can reach out to the relevant authorities as per the jurisdiction, which may include the State Skill Development Mission, District Administration, or Ministry helpline numbers provided for each scheme."""
    elif 'domestic violence' in message_lower:
        response = """Domestic violence in India is primarily governed by the Protection of Women from Domestic Violence Act, 2005. This Act aims to provide a remedy for the protection of women from domestic violence and to ensure that the rights of women are not violated within a domestic relationship. The Act defines domestic violence to include physical, emotional, sexual, and economic abuse.

Under the Act, a victim of domestic violence or a person on behalf of the victim can file a complaint before the Magistrate seeking protection orders, residence orders, monetary relief, custody orders, etc. The Act defines a "domestic relationship" to include marriage, a domestic partnership, etc.

The jurisdiction for filing a complaint under the Protection of Women from Domestic Violence Act, 2005 lies with the Magistrate's Court within whose local jurisdiction the aggrieved person resides or carries on business or is employed. It is essential to consult with a lawyer who specializes in domestic violence cases to understand the legal process and to seek appropriate remedies under the Act."""
    else:
        response = legal_info['en']  # Default response if no specific query is matched

    return translate_text(response, language)

def translate_text(text, target_language):
    translator = GoogleTranslator(source='auto', target=target_language)
    translation = translator.translate(text)
    return translation

if __name__ == '__main__':
    socketio.run(app, debug=True)
    
