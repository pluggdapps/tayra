" This file is subject to the terms and conditions defined in
" file 'LICENSE', which is part of this source code package.
"       Copyright (c) 2011 R Pratap Chakravarthy

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
syn include @Python syntax/python.vim
syn include @htmlCSS syntax/css.vim

" Top-level patterns,
"   string, htmlComment, ttlComment, prolog, pythonStmt, pythonExprs,
"   ttlTag, filterPyCode, ttlFunc, ttlInterface, ttlControl

" syn case ignore
syn keyword pythonTodo		contained FIXME NOTE NOTES TODO XXX
syn match   ttlBraces       contained "{}"
syn match   ttlEscape   	contained +\\['"\\\r\n>]+
syn match   token           contained "\S+"
syn match   attrEqual       contained +=+
syn region  string          contained start=+\z(['"]\)+ end="\z1" 
                            \ skip="\\\\\|\\\z1" keepend contains=ttlEscape

" Comments
syn match   commentText     contained ".+"
syn region  htmlComment     start=+<!--+  end=+-->+ keepend
                            \ contains=commentText,ttlTodo
syn match   ttlComment      +^[ \t]*##.*$+ contains=ttlTodo,pythonTodo

" Prolog
syn match   prologPrefix    contained "@"
syn keyword prologKeywords  contained doctype import as body inherit 
syn keyword prologKeywords  contained implement from import
syn region  prolog          start="^@[dibf]" end="[\r\n]" skip="\\\r\|\\\n"
    \ keepend contains=prologPrefix,prologKeywords,attrEqual,string,ttlEscape

" Statement
if main_syntax != 'python'
  unlet b:current_syntax
  syn match   stmtPrefix    contained "@@"
  syn region  pythonStmt    start="^[ \t]*@@" end="[\r\n]" skip="\\\r\|\\\n"
                            \ keepend contains=stmtPrefix,@Python,ttlEscape
endif

" Expression
syn match   pythonOps       contained "\${\|}"
syn keyword exprkeys        contained evalpy py
syn region  pythonExprs     start="[^\\]\${" end="}" 
                            \ skip="\\\r\|\\\n\|\\}"
                            \ keepend contains=pythonOps,ttlEscape,exprkeys,
                            \ @Python

" Tagline
syn keyword ttlTagName      contained address applet area a base basefont
syn keyword ttlTagName      contained big blockquote br caption center
syn keyword ttlTagName      contained cite code dd dfn dir div dl dt font
syn keyword ttlTagName      contained form hr html img
syn keyword ttlTagName      contained input isindex kbd li link map menu
syn keyword ttlTagName      contained meta ol option param pre p samp span
syn keyword ttlTagName      contained select small strike sub sup
syn keyword ttlTagName      contained table td textarea th tr tt ul var xmp
syn keyword ttlTagName      contained frame noframes frameset nobr blink
syn keyword ttlTagName      contained layer ilayer nolayer spacer
syn keyword ttlTagName      contained marquee head body
syn keyword ttlTagName      contained noscript
syn keyword ttlTagName      contained abbr acronym bdo button col label
syn keyword ttlTagName      contained colgroup del fieldset iframe ins legend
syn keyword ttlTagName      contained object optgroup q s tbody tfoot thead
syn keyword ttlTagName      contained script style

syn keyword ttlTagName      contained inpbutton inpchk inpcolor inpdate inpdt 
syn keyword ttlTagName      contained inpdtlocal inpemail inpfile inphidden
syn keyword ttlTagName      contained inpimg inpmonth inpnum inppass inpradio 
syn keyword ttlTagName      contained inprange inpreset inpsearch inpsub inptel
syn keyword ttlTagName      contained inptext intime inpurl inpweek

syn match   ttlStyle        contained "[^\\]{[^}]\+}" contains=@htmlCSS
syn match   ttlTagOp        contained "[<>]"
syn match   ttlID           contained "#[^ \t\r\n>]\+" 
syn match   ttlClass        contained "\.[^ \t\r\n>]\+" 
syn match   ttlName         contained "\:[^ \t\r\n>]\+" 
syn region  ttlTag          start="[ \t]*<[^!-]" end=">" keepend
                            \ contains=ttlTagOp,ttlTagName,ttlID,ttlClass,
                            \ ttlName,ttlStyle,string,ttlEscape,pythonExprs

" python filter block
syn match   filterSyn       contained ":\S\+:"
syn region  filterPyCode    start=":py:" end=":py:" keepend
                            \ contains=filterSyn,@Python

" Function block
syn keyword funcKeywords    contained @def
syn region  ttlFunc         start=+^[ \t]*@def+  end=+:[ \t]*$+ keepend
                            \ contains=funcKeywords,@Python

syn keyword ifacekeywords   contained @interface
syn region  ttlInterface    start=+^[ \t]*@interface+  end=+:[ \t]*$+ keepend
                            \ contains=ifacekeywords,@Python

" Control Block
syn keyword controlKeywords contained @if @elif @else @for @while
syn region  ttlControl      start=+^[ \t]*@\(if\|elif\|else\|for\|while\)+ 
                            \ end=+:[ \t]*$+ contains=controlKeywords,@Python


" Embedded style sheets
if main_syntax != 'java' || exists("java_css")
  syn keyword htmlArg           contained media
  syn include @htmlCss syntax/css.vim
  unlet b:current_syntax
  syn region cssStyle       start=+\z([ \t]*\)<style[^>]*>+ keepend
                            \ end=+\z1+ skip="\z1[ \t]\{2,}"
                            \ contains=ttlTag,@htmlCss
  " syn match ttlCssStyleCmt  contained "\(<!--\|-->\)"
  " syn region ttlCssDef      matchgroup=htmlArg start='style="' keepend
  "                           \ matchgroup=htmlString end='"'
  "                           \ contains=css.*Attr,css.*Prop,cssComment,
  "                           \ cssLength,cssColor,cssURL,cssImportant,
  "                           \ cssError,cssString
endif

" Embedded java-script
if main_syntax != 'java' || exists("java_javascript")
  syn include @htmlJavaScript syntax/javascript.vim
  unlet b:current_syntax
  syn region  javaScript    start=+^\z([ \t]*\)<script[^>]*>+ keepend 
                            \ end=+\z1+ skip="\z1[ \t]\{2,}"
                            \ contains=ttlTag,@htmlJavaScript
endif

TTLHiLink ttlEscape         Special
TTLHiLink ttlBraces         Special
TTLHiLink pythonOps         Special
TTLHiLink exprkeys          ModeMsg
TTLHiLink tokenSpecial      Comment
TTLHiLink string            String
TTLHiLink attr              Comment
TTLHiLink htmlComment       Comment
TTLHiLink commentText       Comment
TTLHiLink ttlComment        Comment
TTLHiLink prologPrefix      Special
TTLHiLink prologKeywords    Operator
TTLHiLink prolog            NonText
TTLHiLink stmtPrefix        Special
TTLHiLink ttlTag            Function
TTLHiLink ttlTagOp          ModeMsg
TTLHiLink ttlTagName        Statement
TTLHiLink ttlID             Type
TTLHiLink ttlClass          Type
TTLHiLink ttlName           Type
TTLHiLink filterSyn         Special
TTLHiLink funcKeywords      Function
TTLHiLink ifacekeywords     Function
TTLHiLink htmlArg           Type
TTLHiLink controlKeywords   Operator
TTLHiLink filterKeywords    Operator
TTLHiLink ttlCssStyleCmt    Comment
TTLHiLink ttlCssDef         Special

delcommand TTLHiLink

let b:current_syntax = "ttl"

if main_syntax == 'ttl'
  unlet main_syntax
endif

" vim: ts=4
