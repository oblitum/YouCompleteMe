# -*- coding: utf-8 -*-

import re
import vim

CLANG_FILETYPES = set( [ 'c', 'cpp', 'objc', 'objcpp' ] )
vim.command( 'au InsertLeave * py clang_complete.firstParam()' )

def setup():
  if vim.eval( '&ft' ) in CLANG_FILETYPES:
    vim.command( 'noremap <silent> <buffer> <tab> :py clang_complete.updateParams()<cr>' )
    vim.command( 'snoremap <silent> <buffer> <tab> <c-\><c-n>:py clang_complete.updateParams()<cr>' )
    vim.command( 'syntax match placeHolder /⟪[^⟪]\\+⟫/' )
    vim.command( 'syntax match optionalPlaceHolder /⟦[^⟦]\\+⟧/' )

r = re.compile( u'⟪[^⟪]+⟫|⟦[^⟦]+⟧'.encode( 'utf8' ) )

def firstParam():
  if vim.eval( '&ft' ) in CLANG_FILETYPES:
    line = unicode( vim.current.line, 'utf8' ).encode( 'utf8' )
    result = r.search( line )
    if result is None:
      return

    ( start, end ) = result.span()
    selection = len( line[ start:end ].decode( 'utf8' ) )

    selectParams( start, selection )

def updateParams():
  line = unicode( vim.current.line, 'utf8' ).encode( 'utf8' )
  row, col = vim.current.window.cursor

  result = r.search( line, col )
  if result is None:
    result = r.search( line )
    if result is None:
      vim.command( 'call feedkeys("\<c-i>", "n")' )
      return

  ( start, end ) = result.span()
  selection = len( line[ start:end ].decode( 'utf8' ) )

  selectParams( start, selection )

def selectParams( start, selection  ):
  row, _ = vim.current.window.cursor
  vim.current.window.cursor = row, start
  isInclusive = vim.options[ 'selection' ] == 'inclusive'
  vim.command( 'call feedkeys("\<c-\>\<c-n>v%dl\<c-g>", "n")' %
               ( selection - isInclusive ) )
