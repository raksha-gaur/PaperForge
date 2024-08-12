from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
import re

FILE_PATH = r"C:\Users\raksh\Desktop\PaperForge\response.pdf"


def parse_questions(input_text):
    questions = []
    current_question = None

    for line in input_text.splitlines():
        line = line.strip()

        # Identify headings
        if re.match(r'^##', line):
            if current_question:
                questions.append(current_question)
            questions.append({'heading': line.strip('*#').strip()})
            current_question = None

        # Identify questions
        elif re.match(r'^\d+\.', line):
            if current_question:
                questions.append(current_question)
            current_question = {'question': line, 'options': ''}

        # Identify options
        elif re.match(r'^[abcdABCD]', line):
            if current_question:
                current_question['options'] += line + '<br/>'

    if current_question:
        questions.append(current_question)

    return questions


def create_pdf(title, questions, marks_per_mcq, marks_per_short_answer, marks_per_long_answer, total_marks):
    # Create a PDF document
    pdf = SimpleDocTemplate(FILE_PATH, pagesize=A4)

    # Create a list to hold the content
    content = []

    # Set up styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    question_style = ParagraphStyle(
        'QuestionStyle',
        fontSize=12,
        leading=15,
        spaceAfter=12,
        fontName='Times-Roman'
    )
    heading_style = ParagraphStyle(
        'HeadingStyle',
        fontSize=14,
        leading=16,
        spaceAfter=14,
        spaceBefore=14,
        alignment=1,
        fontName='Helvetica-Bold'
    )
    instruction_style = ParagraphStyle(
        'InstructionStyle',
        fontSize=12,
        leading=14,
        spaceAfter=12,
        fontName='Times-Roman'
    )

    # Add title
    content.append(Paragraph(f"Question Paper:{title}", title_style))
    content.append(Paragraph(f"Total Marks:{total_marks}", title_style))
    content.append(Spacer(1, 20))
    # Add instructions
    instructions = f"""
    <b>Instructions:</b><br/>
    - Multiple choice questions carry <b>{marks_per_mcq}</b> marks each.<br/>
    - Short answer questions carry <b>{marks_per_short_answer}</b> marks each.<br/>
    - Long answer questions carry <b>{marks_per_long_answer}</b> marks each.<br/>
    """
    content.append(Paragraph(instructions, instruction_style))
    content.append(Spacer(1, 20))

    # Add questions and headings
    for idx, question in enumerate(questions):
        if 'heading' in question:
            content.append(Paragraph(question['heading'], heading_style))
        else:
            question_text = question['question']
            content.append(KeepTogether([
                Paragraph(question_text, question_style),
                Paragraph(question['options'], question_style)
            ]))
            content.append(Spacer(1, 12))

    # Build the PDF
    pdf.build(content)
    with open(FILE_PATH, 'rb') as f:
        pdf_data = f.read()
    print(f"PDF generated successfully")
    return pdf_data
