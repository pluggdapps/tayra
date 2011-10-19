" This file is subject to the terms and conditions defined in
" file 'LICENSE', which is part of this source code package.
"       Copyright (c) 2010 SKR Farms (P) LTD.

let b:did_ftplugin = 1

setlocal matchpairs+=<:>
setlocal matchpairs+=@::
setlocal matchpairs+=@:;
setlocal commentstring=<!--%s-->
setlocal comments=s:<!--,m:\ \ \ \ ,e:-->,f:#

if exists("g:ft_html_autocomment") && (g:ft_html_autocomment == 1)
    setlocal formatoptions-=t formatoptions+=croql
endif

" Undo the stuff we changed.
let b:undo_ftplugin = "setlocal commentstring< matchpairs< omnifunc< comments< formatoptions<" .
    \	" | unlet! b:match_ignorecase b:match_skip b:match_words b:browsefilter"
