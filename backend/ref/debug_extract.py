import importlib.util
from pathlib import Path

path = Path(__file__).resolve().parent / 'mainOmr.py'
spec = importlib.util.spec_from_file_location('mainOmr', path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

image_path = Path(__file__).resolve().parent / 'MDD.jpg'
student_answers, *_ = mod.extract_answers(mod.load_image(str(image_path)))
print(student_answers)
print('score', sum(1 for i, a in enumerate(student_answers) if a == mod.FINAL_ANS[i]))
print('expected', mod.FINAL_ANS)
