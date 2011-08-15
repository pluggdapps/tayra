Pure sandboxing in python is not entirely possible. Nevertheless pypy 
is providing the sandboxing feature, which can be used if required. Some ideas
for sandboxing,
* try __builtins__ = {}
* Avoid passing any objects via which a module object is accessible.
* Parse the python code found in control blocks, function params,
  and exression substitution and kick out the compromising parts.

Template authors are responsible for the code that they are writing, along
with the plugins that they are going to use. The way in which the security
can be breached beyond the control of the application developer is when 
anonymous code gets evaluated in the templates context.

Tayra does not use eval anywhere during the compilation process and the
expression text in expression substitution ${ ... } is directly placed as
python code.

So as long as the developers do not use eval() anywhere in their template
text, I guess things should be fairly safe.

May be I am wrong and I would love to stand corrected.
