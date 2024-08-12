from backend.llm_response import get_llm_response
from backend.output import create_pdf, parse_questions
from backend.prompt_templates import create_prompt_template
from backend.vectorstore import create_vectorstore, extract_text_from_pdf


def generate_question_paper(pdf_file, title, num_mcqs, marks_per_mcq, num_short_answers, marks_per_short_answer,
                            num_long_answers, marks_per_long_answer, start_page, end_page):
    text = extract_text_from_pdf(pdf_file, start_page, end_page)
    vectorstore = create_vectorstore(text)
    prompt = create_prompt_template(num_mcqs, num_short_answers, num_long_answers)
    questions = get_llm_response(vectorstore, prompt)
    parsed_questions = parse_questions(questions)
    total_marks = (num_mcqs * marks_per_mcq) + (num_short_answers * marks_per_short_answer) + (num_long_answers *
                                                                                               marks_per_long_answer)
    question_paper_pdf = create_pdf(title, parsed_questions, marks_per_mcq, marks_per_short_answer,
                                    marks_per_long_answer, total_marks)
    return question_paper_pdf
