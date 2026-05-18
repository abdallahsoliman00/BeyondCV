# An Implementation Using BeyondCV

Here in this folder, you will find the code needed to generate possibly one of the ugliest CV templates ever.
However, you will see how to programmatically make a CV template of your own using this library.


## How To Run
To try this library out, run the following command from the root directory:
```
python -m BuildImpl.main
```

This will generate a sample using this template from:\
[https://writing.colostate.edu/guides/documents/resume/functionalsample.pdf](https://writing.colostate.edu/guides/documents/resume/functionalsample.pdf)

If you want to try on another CV, just replace this:
```python
    profile = LLMProfileMaker(Path(__file__).parent / "sample_cv.pdf")
```
with this:
```python
    profile = LLMProfileMaker(r"path\to\other\cv")
```
