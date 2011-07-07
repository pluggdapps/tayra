" Vim syntax file
" Language:	Tayra Style Sheets

" Quit when a (custom) syntax file was already loaded
"if exists("b:current_syntax")
"  finish
"endif

au BufRead,BufNewFile *.tss           set filetype=tayrastylesheet
setlocal shiftwidth=2
setlocal tabstop=2

" vim: ts=8 sw=2
