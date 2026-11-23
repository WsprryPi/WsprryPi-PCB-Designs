import re,json

def parse(text):
 toks=re.findall(r'"(?:\\.|[^"\\])*"|[^\s()]+|[()]',text)
 stack=[]
 for t in toks:
  if t=='(':stack.append([])
  elif t==')':
   x=stack.pop()
   if not stack:return x
   stack[-1].append(x)
  else:stack[-1].append(t)

def children(n,key):return [x for x in n if isinstance(x,list) and x and x[0]==key]
def child(n,key):return next((x for x in children(n,key)),None)
def val(n,key):return child(n,key)[1]
def q(x):return json.dumps(str(x),ensure_ascii=False)
def uq(x):return json.loads(x) if x.startswith('"') else x

def dump(n,level=0):
 if not isinstance(n,list):return str(n)
 if not any(isinstance(x,list) for x in n):return '('+' '.join(map(str,n))+')'
 s='('
 for i,x in enumerate(n):
  if isinstance(x,list):s+='\n'+'\t'*(level+1)+dump(x,level+1)
  else:s+=(' ' if i else '')+str(x)
 return s+'\n'+'\t'*level+')'
