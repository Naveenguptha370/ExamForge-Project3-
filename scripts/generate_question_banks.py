import os

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    qb_dir = os.path.join(base_dir, 'backend', 'examinations', 'question_banks')
    os.makedirs(qb_dir, exist_ok=True)

    qb_domains = [
        ('ds_algo', 'Data Structures and Algorithms', 'CS201'),
        ('dbms', 'Database Management Systems and ACID Transactions', 'CS301'),
        ('os', 'Operating Systems and Kernel Architectures', 'CS302'),
        ('cn', 'Computer Networks and Protocol Engineering', 'CS303'),
        ('se', 'Software Engineering and Clean Architecture', 'CS304'),
        ('toc', 'Theory of Computation and Automata', 'CS305'),
        ('cd', 'Compiler Design and Code Generation', 'CS401'),
        ('ai', 'Artificial Intelligence and Knowledge Representation', 'AI201'),
        ('ml', 'Machine Learning and Statistical Learning Models', 'AI301'),
        ('dl', 'Deep Learning and Neural Network Architectures', 'AI401'),
        ('nlp', 'Natural Language Processing and Transformers', 'AI402'),
        ('cv', 'Computer Vision and Image Processing', 'AI403'),
        ('crypto', 'Cryptography and Network Security Protocols', 'CY301'),
        ('cyber_ops', 'Cyber Operations and Digital Forensics', 'CY302'),
        ('cloud', 'Cloud Infrastructure and Distributed Systems', 'IT301'),
        ('devops', 'DevOps and Site Reliability Engineering', 'IT302'),
        ('iot', 'Internet of Things and Sensor Networks', 'EC301'),
        ('embedded', 'Embedded Systems and Microcontrollers', 'EC302'),
        ('vlsi', 'VLSI Design and Semiconductor Physics', 'EC303'),
        ('dsp', 'Digital Signal Processing and Filters', 'EC304'),
        ('control', 'Control Systems and Feedback Dynamics', 'EE301'),
        ('power', 'Power Systems and Smart Grid Technology', 'EE302'),
        ('thermo', 'Thermodynamics and Heat Transfer Systems', 'ME301'),
        ('fluid', 'Fluid Mechanics and Aerodynamics', 'ME302'),
        ('robotics', 'Robotics Kinematics and Motion Planning', 'RO301'),
        ('materials', 'Materials Science and Metallurgy', 'MS301'),
        ('structures', 'Structural Analysis and Reinforced Concrete', 'CE301'),
        ('geotech', 'Geotechnical Engineering and Soil Mechanics', 'CE302'),
        ('biochem', 'Biochemical Engineering and Bioprocesses', 'BT301'),
        ('genetics', 'Molecular Genetics and Bioinformatics', 'BT302'),
    ]

    for qb_id, qb_title, qb_code in qb_domains:
        filepath = os.path.join(qb_dir, f'{qb_id}_question_bank.py')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f'"""\nInstitutional Question Bank and Cognitive Rubric: {qb_title} ({qb_code})\n')
            f.write('Standardized for ExamForge Automated Assessment Engine\n"""\n\n')
            f.write(f'COURSE_CODE = "{qb_code}"\n')
            f.write(f'COURSE_TITLE = "{qb_title}"\n')
            f.write('TOTAL_QUESTIONS = 500\n\n')
            f.write('QUESTIONS = [\n')
            for q_idx in range(1, 501):
                bloom = ['Remember', 'Understand', 'Apply', 'Analyze', 'Evaluate', 'Create'][(q_idx % 6)]
                diff = ['Easy', 'Medium', 'Hard'][(q_idx % 3)]
                marks = 2 if diff == 'Easy' else (5 if diff == 'Medium' else 10)
                f.write('    {\n')
                f.write(f'        "id": "{qb_code}-Q{q_idx:04d}",\n')
                f.write(f'        "question_text": "Explain in detail the fundamental principles and rigorous analytical formulation of {qb_title} scenario {q_idx}. Provide schematic diagrams, mathematical derivations, and edge cases.",\n')
                f.write(f'        "bloom_taxonomy": "{bloom}",\n')
                f.write(f'        "difficulty": "{diff}",\n')
                f.write(f'        "maximum_marks": {marks},\n')
                f.write(f'        "expected_time_minutes": {marks * 2},\n')
                f.write('        "rubrics": [\n')
                for r in range(1, 6):
                    f.write(f'            "Criterion {r}: Candidate demonstrates comprehensive accuracy in deriving component {r} with zero theoretical ambiguities.",\n')
                f.write('        ],\n')
                f.write(f'        "unit_mapping": {(q_idx % 5) + 1},\n')
                f.write(f'        "course_outcome": "CO{(q_idx % 5) + 1}",\n')
                f.write('    },\n')
            f.write(']\n\n')
            f.write('def get_questions_by_unit(unit_number: int):\n')
            f.write('    return [q for q in QUESTIONS if q["unit_mapping"] == unit_number]\n\n')
            f.write('def get_questions_by_difficulty(diff: str):\n')
            f.write('    return [q for q in QUESTIONS if q["difficulty"] == diff]\n')

    print(f'Generated {len(qb_domains)} question banks successfully.')

if __name__ == '__main__':
    main()
