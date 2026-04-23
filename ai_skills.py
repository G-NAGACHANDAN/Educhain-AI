"""
AI Skill Extraction Module
Uses NLP to extract skills from certificate data
"""

import nltk
from collections import Counter
import json
import os

class AISkillExtractor:
    """
    AI-powered skill extraction from course names and certificates
    
    Uses rule-based NLP and keyword matching to identify relevant skills
    from certificate data (course names, subjects, grades)
    """
    
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            try:
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
                nltk.download('averaged_perceptron_tagger', quiet=True)
            except:
                pass
        
        # Skill database: maps course keywords to relevant skills
        self.skill_database = {
            # Programming & CS
            'python': ['Python Programming', 'Data Analysis', 'Machine Learning', 'Web Development'],
            'java': ['Java Programming', 'Object-Oriented Programming', 'Software Development', 'Enterprise Applications'],
            'javascript': ['JavaScript', 'Web Development', 'Frontend Development', 'Node.js'],
            'c++': ['C++ Programming', 'Systems Programming', 'Problem Solving', 'Algorithms'],
            'data structures': ['Data Structures', 'Algorithms', 'Problem Solving', 'Computational Thinking'],
            'algorithms': ['Algorithms', 'Problem Solving', 'Optimization', 'Computational Complexity'],
            'machine learning': ['Machine Learning', 'Data Science', 'Python', 'Statistical Analysis', 'AI'],
            'artificial intelligence': ['AI', 'Machine Learning', 'Neural Networks', 'Deep Learning'],
            'database': ['Database Management', 'SQL', 'Data Modeling', 'Query Optimization'],
            'web development': ['Web Development', 'HTML/CSS', 'JavaScript', 'Responsive Design'],
            
            # Business & Management
            'marketing': ['Marketing Strategy', 'Digital Marketing', 'Brand Management', 'Market Research'],
            'management': ['Project Management', 'Leadership', 'Team Management', 'Strategic Planning'],
            'finance': ['Financial Analysis', 'Accounting', 'Investment Strategy', 'Risk Management'],
            'business': ['Business Strategy', 'Management', 'Communication', 'Critical Thinking'],
            
            # Engineering
            'electronics': ['Electronics', 'Circuit Design', 'Embedded Systems', 'Signal Processing'],
            'mechanical': ['Mechanical Engineering', 'CAD', 'Thermodynamics', 'Manufacturing'],
            'civil': ['Civil Engineering', 'Structural Design', 'Construction Management', 'AutoCAD'],
            
            # Science
            'physics': ['Physics', 'Analytical Thinking', 'Problem Solving', 'Mathematical Modeling'],
            'chemistry': ['Chemistry', 'Laboratory Skills', 'Analytical Chemistry', 'Research'],
            'biology': ['Biology', 'Life Sciences', 'Research', 'Laboratory Techniques'],
            
            # Soft Skills
            'communication': ['Communication', 'Presentation Skills', 'Writing', 'Public Speaking'],
            'leadership': ['Leadership', 'Team Building', 'Decision Making', 'Mentoring'],
            'project': ['Project Management', 'Planning', 'Organization', 'Time Management']
        }
        
        # Grade-based skill modifiers
        self.grade_skills = {
            'A+': ['Excellence', 'High Achiever', 'Mastery'],
            'A': ['Strong Performance', 'Proficiency'],
            'B': ['Good Understanding', 'Competence'],
        }
        
        # Certificate type skills
        self.cert_type_skills = {
            'Excellence': ['Academic Excellence', 'Outstanding Performance', 'Top Performer'],
            'Achievement': ['Goal Achievement', 'Dedication', 'Commitment'],
            'Completion': ['Course Completion', 'Continuous Learning'],
            'Participation': ['Active Participation', 'Engagement', 'Teamwork']
        }
        
        # Track all extracted skills
        self.all_skills = []
        self.load_skills()
    
    def extract_skills(self, course, grade='', certificate_type=''):
        """
        Extract skills from course name, grade, and certificate type
        
        AI Reasoning Flow:
        1. Tokenize and clean course name
        2. Match keywords against skill database
        3. Add grade-based skills if high performance
        4. Add certificate-type specific skills
        5. Return unique, relevant skills
        
        Args:
            course: Course name
            grade: Student's grade (optional)
            certificate_type: Type of certificate (optional)
        
        Returns:
            List of extracted skills
        """
        skills = []
        
        if not course:
            return skills
        
        # Convert to lowercase for matching
        course_lower = course.lower()
        
        # Extract skills from course keywords
        for keyword, skill_list in self.skill_database.items():
            if keyword in course_lower:
                skills.extend(skill_list)
        
        # Add grade-based skills
        if grade in self.grade_skills:
            skills.extend(self.grade_skills[grade])
        
        # Add certificate type skills
        if certificate_type in self.cert_type_skills:
            skills.extend(self.cert_type_skills[certificate_type])
        
        # If no specific match, add generic skills based on course
        if not skills:
            skills.append('Course Completion')
            if 'engineering' in course_lower:
                skills.extend(['Engineering', 'Technical Skills', 'Problem Solving'])
            elif 'science' in course_lower:
                skills.extend(['Scientific Thinking', 'Research', 'Analysis'])
            elif 'arts' in course_lower or 'humanities' in course_lower:
                skills.extend(['Creative Thinking', 'Communication', 'Critical Analysis'])
        
        # Remove duplicates and track
        skills = list(set(skills))
        self.all_skills.extend(skills)
        self.save_skills()
        
        return skills[:8]  # Return top 8 skills
    
    def get_all_skills(self):
        """Get most common skills across all certificates"""
        skill_counts = Counter(self.all_skills)
        return [skill for skill, count in skill_counts.most_common(50)]
    
    def save_skills(self):
        """Save skill tracking data"""
        os.makedirs('data', exist_ok=True)
        with open('data/skills.json', 'w') as f:
            json.dump({
                'all_skills': self.all_skills,
                'skill_counts': dict(Counter(self.all_skills))
            }, f, indent=2)
    
    def load_skills(self):
        """Load skill tracking data"""
        if os.path.exists('data/skills.json'):
            try:
                with open('data/skills.json', 'r') as f:
                    data = json.load(f)
                    self.all_skills = data.get('all_skills', [])
            except:
                self.all_skills = []

# AI UPGRADE NOTES:
# For more advanced AI skill extraction:
# 1. Use spaCy or transformers for NER (Named Entity Recognition)
# 2. Fine-tune BERT model on educational data
# 3. Use word embeddings to find semantic similarities
# 4. Implement skill taxonomy mapping
# 5. Add context-aware extraction (e.g., "Advanced Python" vs "Intro Python")
# Example with transformers:
# from transformers import pipeline
# classifier = pipeline("zero-shot-classification")
# result = classifier(course, candidate_labels=skill_list)
