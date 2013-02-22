" Vim filetype plugin file
" Language: ttl
" Maintainer: Pratap Chakravarthy <prataprc at gmail dot com>
" Last Changed:
" URL: pypi.python.org/pypi/tayra

" Only use this filetype plugin when no other was loaded.
if exists("b:did_ftplugin")
  finish
endif

" Use HTML and Django template ftplugins.
runtime! ftplugin/html.vim
runtime! ftplugin/django.vim
