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
syn match   prologKeywords  contained "!!!\|@import\| as \|@body\|@inherit\|@implement\|@use\|@charset"
syn match   funcKeywords    contained "@function\|@interface"
syn match   controlKeywords contained "@if\|@elif\|@else\|@for\|@while"
syn match   prologDoctype   "^!!!.*;[ \t]*" contains=prologKeywords
syn region  prolog          start="^@[!ibuc]" end=";[ \t]*$" contains=prologKeywords,ttlString

" Textline
syn match   textLine        "^[^<:@!].*$" contains=pythonExprs
syn match   commentLine     "[ \t]*##.*$"

" Tagblock
syn region  ttlString       contained start=+"+ end=+"+ contains=ttlSpecialChar,javaScriptExpression,
                            \ pythonExprs
syn region  ttlString       contained start=+'+ end=+'+ contains=ttlSpecialChar,javaScriptExpression,
                            \ pythonExprs
syn match   ttlValue        contained "=[\t ]*[^'" \t>][^ \t>]*"hs=s+1 contains=javaScriptExpression,
                            \ pythonExprs
syn match   ttlTagN         contained "<[!%]\?\s*[-a-zA-Z0-9_#]"hs=s+1 contains=ttlTagName,ttlTagSpecifier
syn region  ttlStyle        contained start=+{+ keepend end=+}+ contains=pythonExprs,@htmlCss
syn region  ttlTag          contained start=+^[ ]*<[!%]\?[^/]+   end=+>+ contains=ttlTagN,ttlString,ttlStyle,
                            \ ttlValue,ttlTagError,ttlEvent,ttlCssDefinition,pythonExprs
syn region  ttlTagline      start=+^[ ]*<[!%]\?[^/]+  end=+[^\r\n]\{-}$+ contains=ttlTag,pythonExprs

" Function block
syn region  funcLine        start=+^[ ]*@function+  end=+:[ \t]*$+ contains=funcKeywords,@Python
syn region  ifaceLine       start=+^@interface+ end=+:[ ]*$+ contains=funcKeywords,@Python

" Control Block
syn region  ifLine          start=+^[ ]*@if+    end=+:[ \t]*$+ contains=controlKeywords,@Python
syn region  elifLine        start=+^[ ]*@elif+  end=+:[ \t]*$+ contains=controlKeywords,@Python
syn region  elseLine        start=+^[ ]*@else+  end=+:[ \t]*$+ contains=controlKeywords,@Python
syn region  forLine         start=+^[ ]*@for+   end=+:[ \t]*$+ contains=controlKeywords,@Python
syn region  whileLine       start=+^[ ]*@while+ end=+:[ \t]*$+ contains=controlKeywords,@Python

" Statement, Expression
syn region  pythonStatement start="^[ \t]*@@[^{]" end="$" contains=@Python
syn region  pythonExprs     contained start="\${" end="}" contains=@Python

" Embedded CSS
syn include @htmlCss            syntax/css.vim
unlet b:current_syntax
syn match htmlCssStyleComment   contained "\(<!--\|-->\)"
syn region cssStyle             start=+[ ]*<[!%]\?style+ keepend end=+^$+ contains=ttlTag,@htmlCss
syn region htmlCssDefinition    start='style="' keepend matchgroup=ttlString end='"' contains=css.*Attr,css.*Prop,
                                \ cssComment,cssLength,cssColor,cssURL,cssImportant,cssError,cssString,@htmlPreproc
TTLHiLink htmlStyleArg ttlString

"Embedded Javascript
syn include @htmlJavaScript     syntax/javascript.vim
unlet b:current_syntax
syn region  jsstyle             start=+[ ]*<[!%]\?script+ keepend end=+^$+ contains=ttlTag,@htmlJavaScript,pythonExprs
,
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
