# TODO
- Add documentation to the codebase. (Could use Shpinx)
- Show the different information extracted by the LLM, or even better, make the LLM extract information from the document depending on the CVTemplate created.
- Remove tables with unresolved placeholders.
- Add support for addding header images to the document.
- Add a `SectionTitle` type to Template.py
    - Both `Section` and `RepetingSection` should accept a `title: SectionTitle` variable in their `__init__` function. This title should then be added to the section 
