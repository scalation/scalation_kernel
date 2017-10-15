
from mako.template import Template

info_template = Template("""
<p><strong>Pretty Print Information</strong></p>
<table>
  <tr>
    <td>Name</td><td>${name}</td>
  </tr>
  <tr>
    <td>Type</td><td>${type}</td>
  </tr>
  <tr>
    <td>Value</td><td>${value}</td>
  </tr>
</table>
<p><i>In the future, we should be able to use the above information to better display the result in Jupyter.</i></p>
""")

vector_template = Template("""
<div style='overflow:auto;'>
<table>
  <tr>
    <td><strong>Index</strong></td>
% for elem in elems:
    <td>${loop.index}</td>
% endfor
  </tr>
  <tr>
    <td><strong>Value</strong></td>
% for elem in elems:
    <td>${elem}</td>
% endfor
  </tr>
</table>
</div>
""")

