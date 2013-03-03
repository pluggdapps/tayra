.. code-block:: ttl

    <!-- An inline comment spanning multiple
      lines -->
    @doctype xhtml+rdfa1.0 
    @body id="hello", cls="world", style='color: red;'
    @import tayra:test/stdttl/funcblock.ttl as f
    @import os, sys
    @inherit tayra:test/stdttl/base.ttl
    @implement tayra.interfaces:ITayraTestInterface as XYZTestInterface

    @@ a = 10 * 20 \
        * 30 +40 + [ x for x in range(1,10) ]
    
    ## TTL Comments

    <div .pluggdappsfooter #id { color : blue } edit name="hello world">

    @def func1() : 
      @@pass

    @interface ITayraTestInterface.render( self, args, kwargs ):
      <div> interface successfully invoked, okay

    @if a == 'pass' :
      @@pass
    @elif a == ':' :
      @@pass
    @else a == 1 :
      Google will join its biggest mobile rival, Apple, on the space trip as
      well.  Apple's iPhone 4 will join a crew running an app, called
      "SpaceLab for iOS."

    @for i in range(2) :
      Google will join its biggest mobile rival, Apple, on the space trip
      as well. Apple's iPhone 4 will join a crew running an app, called
      "SpaceLab for iOS."

    @@ i = 1
    @while i :
      <!--  comment --> 
      @@i -= 1

    <a .crumbname "${crumbsurl or ''}"> ${[ x for x in crumbsname]}

    :py:
    a = 'empty'
    def insideroot_butglobal():
      return '<div> insideroot_butglobal </div>'
    :py: 
    
    hello


