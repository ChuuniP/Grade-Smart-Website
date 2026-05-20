import mainOmr
result = mainOmr.main('MDD.jpg')
print(result['score'], result['correct'], result['wrong'], result['blank'])
