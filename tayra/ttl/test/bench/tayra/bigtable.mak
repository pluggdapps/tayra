<%! 
  var = 'hello'
%>
<table>
  % for i in range(10) :
    <tr>
      %for j in range(1000) :
        <td> ${ var } </td>
	  %endfor
	</tr>
  %endfor
</table>
