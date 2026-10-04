import re
with open("practice5/receipt.txt", "r", encoding="utf-8") as file:
    text=file.read()
#followed by 0 or more b
result = re.findall(r'ab*', text)
print(result)
#a followed by three b
result = re.findall(r'ab{2,3}', text)
print(result)
#lowercase letters joined with _
result=re.findall(r'[a-z]+_[a-z]+', text)
print(result)
#one upprcase followed by lowercase
result=re.findall(r'[A-Z][a-z]+', text)
print(result)
#a followed by anything and endig in b
result=re.findall(r'a.*b', text)
print(result)
#replace spaces and commas and dots with :
result=re.sub(r'[ ,.]', ':', text)
print(result)
#snake case camel case
text2="hello_world_python"
result=re.sub(r'_([a-z])', lambda x: x.group(1).upper(), text2)
print(result)
#split a string at uppercase letters
text2="HelloWorldPython"
result=re.findall(r'[A-Z][a-z]*', text2)
print(result)
#insert spaces between words starting with capital letters
text2="HelloWorldPython"
result=re.sub(r'(A-Z)', r' \1', text2)
print(result)
#camel case snake case
text2="helloWorldPython"
result=re.sub(r'([A-Z])', r'_\1', text2).lower()
print(result)
