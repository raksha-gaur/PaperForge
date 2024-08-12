from langchain.prompts import PromptTemplate

USER_INPUT = "Generate questions based on the provided context and configuration, ensuring that each type is " \
             "represented under the appropriate headings [##Multiple Choice Questions, ##Short Answers, ##Long" \
             " Answers]. You do not need to provide answers. Please ensure that you generate the exact number of" \
             " questions specified for each type, and avoid repeating your response."


def create_prompt_template(num_mcqs, num_short_answers, num_long_answers):
    prefix = f"""[INST] You have to create questions in this following configuration:
    - Number of Multiple Choice Questions: {num_mcqs}
    - Number of Short Answer Questions: {num_short_answers}
    - Number of Long Answer Questions: {num_long_answers}
    [/INST]"""

    suffix = """
    [INST] Question: {template_userInput} [/INST]
    Answer:
    """

    new_prompt_template = PromptTemplate(
        input_variables=["context", "template_userInput"],
        template=prefix + "\n\n" + suffix
    )

    formatted_prompt = new_prompt_template.format(
        template_userInput=USER_INPUT
    )

    return formatted_prompt
