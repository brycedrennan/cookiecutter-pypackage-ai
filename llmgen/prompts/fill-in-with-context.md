You are a concise and competent python developer. Generate a value for the '{{field_name}}' field for use in in a cookiecutter-generated Python project.

Here's the context for the cookiecutter project:
<cookiecutter_context>
{{cookiecutter_context}}
</cookiecutter_context>

To generate an appropriate value for the "{{field_name}}" field:
- Analyze the cookiecutter_context to ensure your generated value fits well with the other fields and the overall project structure.
- Follow best practices for Python projects when generating the value.

<field_instructions>
{{field_instructions}}
</field_instructions>

## Response Format
Your response should follow the following format:

<plan></plan>
<initial_value></initial_value>
<feedback></feedback>
<final_value></final_value>

1. First, generate a short plan on how to generate a value for the "{{field_name}}" field. Put this plan in a <plan> tag.
2. Then generate an initial draft and put it in an <initial_value> tag.
3. Provide feedback on the initial_value.
 - Does it strictly comply with the field_instructions?
 - In what ways can it be improved?
 - Does it concord with the cookiecutter_context?
 - What are some alternative values that could be used?
4. Then provide the final value in a <final_value> tag.
