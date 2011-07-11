" Vim syntax file
" Language:	Tayra Template Language

" For version 5.x: Clear all syntax items
" For version 6.x: Quit when a syntax file was already loaded
if !exists("main_syntax")
  if version < 600
    syntax clear
  elseif exists("b:current_syntax")
    finish
  endif
  let main_syntax = 'ttl'
endif

" don't use standard HiLink, it will not work with included syntax files
if version < 508
  command! -nargs=+ TTLHiLink hi link <args>
else
  command! -nargs=+ TTLHiLink hi def link <args>
endif

syntax spell toplevel
syn case ignore

" Comments (the real ones or the old netscape ones)
if exists("html_wrong_comments")
  syn region htmlComment                start=+<!--+    end=+--\s*>+
else
  syn region htmlComment                start=+<!+      end=+>+   contains=htmlCommentPart,htmlCommentError
  syn match  htmlCommentError contained "[^><!]"
  syn region htmlCommentPart  contained start=+--+      end=+--\s*+  contains=@htmlPreProc
endif
syn region htmlComment                  start=+<!DOCTYPE+ keepend end=+>+

" Literals
syn match   ttlSpecialChar  contained "&#\=[0-9A-Za-z]\{1,8};"
syn match   ttlTagError     contained "[^>]<"ms=s+1
syn match   ttlTagName      contained "[-a-zA-Z0-9]\+"
syn match   ttlTagSpecifier contained "[#\.][-A-Za-z0-9_]\+"

" Python syntax
syn include @Python         syntax/python.vim

" Blocks
"syn region  blockTTL        start="^\z([ \t]*\)" end="^\z1" contains=prolog

" Prolog
syn match   prologKeywords  contained "!!!\|@import\| as \|@body\|@inherit\|@implement\|@use"
syn match   funcKeywords    contained "@function\|@interface"
syn match   controlKeywords contained "@if\|@elif\|@else\|@for\|@while"
syn match   prologDoctype   "^!!!.*;[ \t]*" contains=prologKeywords
syn region  prolog          start="^@[!ibu]" end=";[ \t]*$" contains=prologKeywords

" Textline
syn match   textLine        "^[^<:@!].*$" contains=pythonExprs
syn match   textSuffix      ">.*$"ms=s+1 contains=pythonExprs
syn match   commentLine     "[ \t]*##.*$"

" Tagblock
syn region  ttlString       contained start=+"+ end=+"+ contains=ttlSpecialChar,javaScriptExpression,
                            \ pythonExprs,@ttlPreproc
syn region  ttlString       contained start=+'+ end=+'+ contains=ttlSpecialChar,javaScriptExpression,
                            \ pythonExprs,@ttlPreproc
syn match   ttlValue        contained "=[\t ]*[^'" \t>][^ \t>]*"hs=s+1 contains=javaScriptExpression,
                            \ pythonExprs,@ttlPreproc
syn match   ttlTagN         contained "<\s*[-a-zA-Z0-9_#]"hs=s+1 contains=ttlTagName,ttlTagSpecifier
syn region  ttlTag          start=+^[ \t]*<[^/]+   end=+>.*$+ contains=ttlTagN,ttlString,ttlValue,ttlTagError,
                            \ ttlEvent,ttlCssDefinition,pythonExprs,textSuffix,@ttlPreproc

" Function block
syn region  funcLine        start=+^[ \t]*@function+  end=+:[ \t]*$+ contains=funcKeywords,@Python
syn region  ifaceLine       start=+^@interface+ end=+:[ \t]*$+ contains=funcKeywords,@Python

" Control Block
syn region  ifLine          start=+^[ \t]*@if+    end=+:[ \t]*$+ contains=controlKeywords,@Python
syn region  elifLine        start=+^[ \t]*@elif+  end=+:[ \t]*$+ contains=controlKeywords,@Python
syn region  elseLine        start=+^[ \t]*@else+  end=+:[ \t]*$+ contains=controlKeywords,@Python
syn region  forLine         start=+^[ \t]*@for+   end=+:[ \t]*$+ contains=controlKeywords,@Python
syn region  whileLine       start=+^[ \t]*@while+ end=+:[ \t]*$+ contains=controlKeywords,@Python

" Statement, Expression
syn region  pythonStatement start="^[ \t]*@@[^{]" end="$" contains=@Python
syn region  pythonExprs     contained start="\${" end="}" contains=@Python

" Embedded CSS
"syn include @htmlCss            syntax/css.vim
"unlet b:current_syntax
"syn match htmlCssStyleComment   contained "\(<!--\|-->\)"
"syn region cssStyle             start=+[ \t]*<style+ keepend end=+[ \t]*[<@$:]+me=e-1 contains=ttlTag,@htmlCss
"syn region htmlCssDefinition matchgroup=htmlArg start='style="' keepend matchgroup=htmlString end='"' contains=css.*Attr,css.*Prop,cssComment,cssLength,cssColor,cssURL,cssImportant,cssError,cssString,@htmlPreproc
"TTLHiLink htmlStyleArg htmlString
"
" Embedded Javascript
"syn include @htmlJavaScript     syntax/javascript.vim
"unlet b:current_syntax
"syn region  javaScript          start=+[ \t]*<script+ keepend end=+[ \t]*[<@$:]+me=s-1 contains=ttlTag,@htmlJavaScript,
"                               \ htmlCssStyleComment

TTLHiLink ttlSpecialChar    Special
TTLHiLink comment           Comment
TTLHiLink prologKeywords    Operator
TTLHiLink funcKeywords      Function
TTLHiLink controlKeywords   Operator
TTLHiLink prolog            NonText
TTLHiLink prologDoctype     NonText
TTLHiLink ttlString         String
TTLHiLink ttlValue          String
TTLHiLink ttlTagName        ModeMsg
TTLHiLink ttlTag            Function
TTLHiLink pythonExprs       Special
TTLHiLink htmlComment       Comment
TTLHiLink commentLine       Comment

delcommand TTLHiLink

let b:current_syntax = "ttl"

if main_syntax == 'ttl'
  unlet main_syntax
endif

" vim: ts=4
